import sys

if sys.version_info[1] >= 8:
    from typing import Final, Optional
else:
    from typing_extensions import Final, Optional
from typing import Tuple, Dict, Union
import argparse
import pathlib
import logging
import yaml
import itertools
import packaging.version
import warnings

# This is a weird hack to avoid Intel MKL issues on the cluster when this is called as a subprocess of a process that has itself initialized PyTorch.
# Since numpy gets imported later anyway for dataset stuff, this shouldn't affect performance.
import numpy as np  # noqa: F401

import torch

from e3nn.util.jit import script

from nequip.model import model_from_config
from nequip.data import dataset_from_config
from nequip.utils import Config
from nequip.utils.versions import check_code_version, get_current_code_versions
from nequip.scripts.train import default_config
from nequip.utils.misc import dtype_to_name
from nequip.utils._global_options import _set_global_options

CONFIG_KEY: Final[str] = "config"
NEQUIP_VERSION_KEY: Final[str] = "nequip_version"
TORCH_VERSION_KEY: Final[str] = "torch_version"
E3NN_VERSION_KEY: Final[str] = "e3nn_version"
CODE_COMMITS_KEY: Final[str] = "code_commits"
R_MAX_KEY: Final[str] = "r_max"
N_SPECIES_KEY: Final[str] = "n_species"
TYPE_NAMES_KEY: Final[str] = "type_names"
JIT_BAILOUT_KEY: Final[str] = "_jit_bailout_depth"
JIT_FUSION_STRATEGY: Final[str] = "_jit_fusion_strategy"
TF32_KEY: Final[str] = "allow_tf32"
DEFAULT_DTYPE_KEY: Final[str] = "default_dtype"
MODEL_DTYPE_KEY: Final[str] = "model_dtype"

_ALL_METADATA_KEYS = [
    CONFIG_KEY,
    NEQUIP_VERSION_KEY,
    TORCH_VERSION_KEY,
    E3NN_VERSION_KEY,
    R_MAX_KEY,
    N_SPECIES_KEY,
    TYPE_NAMES_KEY,
    JIT_BAILOUT_KEY,
    JIT_FUSION_STRATEGY,
    TF32_KEY,
    DEFAULT_DTYPE_KEY,
    MODEL_DTYPE_KEY,
]


def _register_metadata_key(key: str) -> None:
    _ALL_METADATA_KEYS.append(key)


_current_metadata: Optional[dict] = None


def _set_deploy_metadata(key: str, value) -> None:
    # TODO: not thread safe but who cares?
    global _current_metadata
    if _current_metadata is None:
        pass  # not deploying right now
    elif key not in _ALL_METADATA_KEYS:
        raise KeyError(f"{key} is not a registered model deployment metadata key")
    elif key in _current_metadata:
        raise RuntimeError(f"{key} already set in the deployment metadata")
    else:
        _current_metadata[key] = value


def _compile_for_deploy(model):
    model.eval()

    if not isinstance(model, torch.jit.ScriptModule):
        model = script(model)

    return model


def load_deployed_model(
    model_path: Union[pathlib.Path, str],
    device: Union[str, torch.device] = "cpu",
    freeze: bool = True,
    set_global_options: Union[str, bool] = "warn",
) -> Tuple[torch.jit.ScriptModule, Dict[str, str]]:
    r"""Load a deployed model.

    Args:
        model_path: the path to the deployed model's ``.pth`` file.

    Returns:
        model, metadata dictionary
    """
    metadata = {k: "" for k in _ALL_METADATA_KEYS}
    try:
        model = torch.jit.load(model_path, map_location=device, _extra_files=metadata)
    except RuntimeError as e:
        raise ValueError(
            f"{model_path} does not seem to be a deployed NequIP model file. Did you forget to deploy it using `nequip-deploy`? \n\n(Underlying error: {e})"
        )
    # Confirm nequip made it
    if len(metadata[NEQUIP_VERSION_KEY]) == 0:
        if len(metadata[JIT_BAILOUT_KEY]) != 0:
            # In versions <0.6.0, there may have been a bug leading to empty "*_version"
            # metadata keys.  We can be pretty confident this is a NequIP model from
            # those versions, though, if it stored "_jit_bailout_depth"
            # https://github.com/mir-group/nequip/commit/2f43aa84542df733bbe38cb9d6cca176b0e98054
            # Likely addresses https://github.com/mir-group/nequip/issues/431
            warnings.warn(
                f"{model_path} appears to be from a older (0.5.* or earlier) version of `nequip` "
                "that pre-dates a variety of breaking changes. Please carefully check the "
                "correctness of your results for unexpected behaviour, and consider re-deploying "
                "your model using this current `nequip` installation."
            )
        else:
            raise ValueError(
                f"{model_path} does not seem to be a deployed NequIP model file"
            )
    # Confirm its TorchScript
    assert isinstance(model, torch.jit.ScriptModule)
    # Make sure we're in eval mode
    model.eval()
    # Freeze on load:
    if freeze and hasattr(model, "training"):
        # hasattr is how torch checks whether model is unfrozen
        # only freeze if already unfrozen
        model = torch.jit.freeze(model)
    # Everything we store right now is ASCII, so decode for printing
    metadata = {k: v.decode("ascii") for k, v in metadata.items()}
    # Update metadata for backward compatibility
    if metadata[DEFAULT_DTYPE_KEY] == "":
        # Default and model go together
        assert metadata[MODEL_DTYPE_KEY] == ""
        # If there isn't a dtype, it should be older than 0.6.0---but
        # this may not be reflected in the version fields (see above check)
        # So we only check if it is available:
        if len(metadata[NEQUIP_VERSION_KEY]) > 0:
            assert packaging.version.parse(
                metadata[NEQUIP_VERSION_KEY]
            ) < packaging.version.parse("0.6.0")

        # The old pre-0.6.0 defaults:
        metadata[DEFAULT_DTYPE_KEY] = "float32"
        metadata[MODEL_DTYPE_KEY] = "float32"
        warnings.warn(
            "Models deployed before v0.6.0 don't contain information about their default_dtype or model_dtype; assuming the old default of float32 for both, but this might not be right if you had explicitly set default_dtype=float64."
        )

    # Set up global settings:
    assert set_global_options in (True, False, "warn")
    if set_global_options:
        global_config_dict = {}
        global_config_dict["allow_tf32"] = bool(int(metadata[TF32_KEY]))
        global_config_dict["default_dtype"] = str(metadata[DEFAULT_DTYPE_KEY])
        # JIT strategy
        strategy = metadata.get(JIT_FUSION_STRATEGY, "")
        if strategy != "":
            strategy = [e.split(",") for e in strategy.split(";")]
            strategy = [(e[0], int(e[1])) for e in strategy]
        else:
            strategy = default_config[JIT_FUSION_STRATEGY]
        global_config_dict["_jit_fusion_strategy"] = strategy
        # JIT bailout
        # _set_global_options will check torch version
        jit_bailout: int = metadata.get(JIT_BAILOUT_KEY, "")
        if jit_bailout == "":
            jit_bailout = default_config[JIT_BAILOUT_KEY]
        jit_bailout = int(jit_bailout)
        global_config_dict["_jit_bailout_depth"] = jit_bailout
        # call to actually set the global options
        _set_global_options(
            global_config_dict,
            warn_on_override=set_global_options == "warn",
        )
    return model, metadata


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Deploy and view information about previously deployed NequIP models."
    )
    # backward compat for 3.6
    if sys.version_info[1] > 6:
        required = {"required": True}
    else:
        required = {}
    parser.add_argument("--verbose", help="log level", default="INFO", type=str)
    subparsers = parser.add_subparsers(dest="command", title="commands", **required)
    info_parser = subparsers.add_parser(
        "info", help="Get information from a deployed model file"
    )
    info_parser.add_argument(
        "model_path",
        help="Path to a deployed model file.",
        type=pathlib.Path,
    )
    info_parser.add_argument(
        "--print-config",
        help="Print the full config of the model.",
        action="store_true",
    )

    build_parser = subparsers.add_parser("build", help="Build a deployment model")
    build_parser.add_argument(
        "--model",
        help="Path to a YAML file defining a model to deploy. Unless you know why you need to, do not use this option.",
        type=pathlib.Path,
    )
    build_parser.add_argument(
        "--train-dir",
        help="Path to a working directory from a training session to deploy.",
        type=pathlib.Path,
    )
    build_parser.add_argument(
        "--checkpoint",
        help="Which model checkpoint from --train-dir to deploy. Defaults to `best_model.pth`. If --train-dir is provided, this is a relative path;  if --model is provided instead, this is an absolute path.",
        type=str,
        default=None,
    )
    build_parser.add_argument(
        "--override",
        help="Override top-level configuration keys from the `--train-dir`/`--model`'s config YAML file.  This should be a valid YAML string. Unless you know why you need to, do not use this option.",
        type=str,
        default=None,
    )
    build_parser.add_argument(
        "--using-dataset",
        help="Allow model builders to use a dataset during deployment. By default uses the training dataset, but can point to a YAML file for another dataset.",
        type=pathlib.Path,
        const=True,
        nargs="?",
    )
    build_parser.add_argument(
        "out_file",
        help="Output file for deployed model.",
        type=pathlib.Path,
    )

    args = parser.parse_args(args=args)

    logging.basicConfig(level=getattr(logging, args.verbose.upper()))

    if args.command == "info":
        model, metadata = load_deployed_model(
            args.model_path, set_global_options=False, freeze=False
        )
        config = metadata.pop(CONFIG_KEY)
        if args.print_config:
            print(config)
        else:
            metadata_str = "\n".join("  %s: %s" % e for e in metadata.items())
            logging.info(f"Loaded TorchScript model with metadata:\n{metadata_str}\n")
            logging.info(
                f"Model has {sum(p.numel() for p in model.parameters())} weights"
            )
            logging.info(
                f"Model has {sum(p.numel() for p in model.parameters() if p.requires_grad)} trainable weights"
            )
            logging.info(
                f"Model weights and buffers take {sum(p.numel() * p.element_size() for p in itertools.chain(model.parameters(), model.buffers())) / (1024 * 1024):.2f} MB"
            )
            logging.debug(f"Model had config:\n{config}")

    elif args.command == "build":
        state_dict = None
        if args.model and args.train_dir:
            raise ValueError("--model and --train-dir cannot both be specified.")
        checkpoint_file = args.checkpoint
        if args.train_dir is not None:
            if checkpoint_file is None:
                checkpoint_file = "best_model.pth"
            logging.info(f"Loading {checkpoint_file} from training session...")
            checkpoint_file = str(args.train_dir / "best_model.pth")
            config = Config.from_file(str(args.train_dir / "config.yaml"))
        elif args.model is not None:
            logging.info("Building model from config...")
            config = Config.from_file(str(args.model), defaults=default_config)
        else:
            raise ValueError("one of --train-dir or --model must be given")

        # Set override options before _set_global_options so that things like allow_tf32 are correctly handled
        if args.override is not None:
            override_options = yaml.load(args.override, Loader=yaml.Loader)
            assert isinstance(
                override_options, dict
            ), "--override's YAML string must define a dictionary of top-level options"
            overridden_keys = set(config.keys()).intersection(override_options.keys())
            set_keys = set(override_options.keys()) - set(overridden_keys)
            logging.info(
                f"--override:  overrode keys {list(overridden_keys)} and set new keys {list(set_keys)}"
            )
            config.update(override_options)
            del override_options, overridden_keys, set_keys

        _set_global_options(config)
        check_code_version(config)

        # -- load model --
        # figure out first if a dataset is involved
        dataset = None
        if args.using_dataset:
            dataset_config = config
            if args.using_dataset is not True:
                dataset_config = Config.from_file(str(args.using_dataset))
            dataset = dataset_from_config(dataset_config)
            if args.using_dataset is True:
                # we're using the one from training config
                # downselect to training set
                dataset = dataset.index_select(config.train_idcs)
        # build the actual model]
        # reset the global metadata dict so that model builders can fill it:
        global _current_metadata
        _current_metadata = {}
        model = model_from_config(config, dataset=dataset, deploy=True)
        if checkpoint_file is not None:
            state_dict = torch.load(
                str(args.train_dir / "best_model.pth"), map_location="cpu"
            )
            model.load_state_dict(state_dict, strict=True)

        # -- compile --
        model = _compile_for_deploy(model)
        logging.info("Compiled & optimized model.")

        # Deploy
        metadata: dict = {}
        code_versions, code_commits = get_current_code_versions(config)
        for code, version in code_versions.items():
            metadata[code + "_version"] = version
        if len(code_commits) > 0:
            metadata[CODE_COMMITS_KEY] = ";".join(
                f"{k}={v}" for k, v in code_commits.items()
            )

        metadata[R_MAX_KEY] = str(float(config["r_max"]))
        n_species = str(config["num_types"])
        type_names = config["type_names"]
        metadata[N_SPECIES_KEY] = str(n_species)
        metadata[TYPE_NAMES_KEY] = " ".join(type_names)

        metadata[JIT_BAILOUT_KEY] = str(config[JIT_BAILOUT_KEY])
        if (
            packaging.version.parse(torch.__version__)
            >= packaging.version.parse("1.11")
            and JIT_FUSION_STRATEGY in config
        ):
            metadata[JIT_FUSION_STRATEGY] = ";".join(
                "%s,%i" % e for e in config[JIT_FUSION_STRATEGY]
            )
        metadata[TF32_KEY] = str(int(config["allow_tf32"]))
        metadata[DEFAULT_DTYPE_KEY] = dtype_to_name(config["default_dtype"])
        metadata[MODEL_DTYPE_KEY] = dtype_to_name(config["model_dtype"])
        metadata[CONFIG_KEY] = yaml.dump(Config.as_dict(config))

        for k, v in _current_metadata.items():
            if k in metadata:
                raise RuntimeError(f"Custom deploy key {k} was already set")
            metadata[k] = v
        _current_metadata = None

        metadata = {k: v.encode("ascii") for k, v in metadata.items()}

        torch.jit.save(model, args.out_file, _extra_files=metadata)
    else:
        raise ValueError

    return


if __name__ == "__main__":
    main()
