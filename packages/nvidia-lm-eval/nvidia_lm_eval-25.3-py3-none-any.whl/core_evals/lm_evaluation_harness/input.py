import logging
import os
import pathlib
import yaml
from typing import Optional

from .utils import MisconfigurationError, deep_update, dotlist_to_dict, is_package_installed
from .api_dataclasses import Evaluation

def load_run_config(yaml_file: str) -> dict:
    """Load the run configuration from the YAML file.

    NOTE: The YAML config allows to override all the run configuration parameters.
    """
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)
    return config


def parse_cli_args(args) -> dict:
    """Parse CLI arguments into the run configuration format.

    NOTE: The CLI args allow to override a subset of the run configuration parameters.
    """
    config = {
        "config": {
            "type": args.eval_type,
            "output_dir": args.output_dir,
        },
        "target": {
            "api_endpoint": {
                "api_key": args.api_key_name,
                "model_id": args.model_id,
                "type": args.model_type,
                "url": args.model_url,
            }
        }
    }
    overrides = parse_override_params(args.overrides)
    # "--overrides takes precedence over other CLI args (e.g. --model_id)"
    config = deep_update(
        config, overrides, skip_nones=True
    )
    return config


def parse_override_params(override_params_str: Optional[str] = None) -> dict:
    if not override_params_str:
        return {}
    override_params = override_params_str.split(",")
    return dotlist_to_dict(override_params)


def validate_cli_args(run_config_cli_overrides: dict) -> None:
    required_keys = [
        (("config", "type"), "--eval_type"),
        (("config", "output_dir"), "--output_dir"),
        (("target", "api_endpoint", "model_id"), "--model_id"),
        (("target", "api_endpoint", "type"), "--model_type"),
        (("target", "api_endpoint", "url"), "--model_url"),
    ]

    for (keys, arg) in required_keys:
        d = run_config_cli_overrides
        for key in keys:
            if key not in d or d[key] is None:
                raise MisconfigurationError(f"Missing required argument: {arg} (run config key: {'.'.join(keys)})")
            d = d[key]


def get_framework_evaluations(
    filepath: str, run_config_cli_overrides: Optional[dict] = None
) -> tuple[str, str, list[Evaluation]]:
    framework = {}
    with open(filepath, "r") as f:
        framework = yaml.safe_load(f)

        framework_name = framework["framework"]["name"]
        pkg_name = framework["framework"]["pkg_name"]
        run_config_framework_defaults = framework["defaults"]

    evaluations = dict()
    for evaluation_dict in framework["evaluations"]:
        # Apply run config evaluation defaults onto the framework defaults
        run_config = deep_update(
            run_config_framework_defaults, evaluation_dict["defaults"], skip_nones=True)

        # Apply run config CLI overrides onto the framework+evaluation defaults
        # TODO(pj): This is a hack and we should only override the config of the evaluation
        #           that was picked in the CLI. Move it somehow one level up where we
        #           already have the evaluation picked.
        run_config = deep_update(
            run_config, run_config_cli_overrides or {}, skip_nones=True)

        evaluation = Evaluation(
            framework_name=framework_name,
            pkg_name=pkg_name,
            **run_config,
        )

        evaluations[evaluation_dict["defaults"]["config"]["type"]] = evaluation
    return framework_name, pkg_name, evaluations


def get_available_evaluations(run_config_cli_overrides: Optional[dict] = None) -> tuple[dict[str, dict[str, Evaluation]], dict[str, Evaluation]]:
    def_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'framework.yml')
    if not os.path.exists(def_file):
        raise ValueError(f"Framework Definition File does not exists at {def_file}")

    framework_eval_mapping = {}  # framework name -> set of tasks   | used in 'framework.task' invocation
    eval_name_mapping = {}       # task name      -> set of tasks   | used in 'task' invocation

    logging.debug(f"Loading task definitions from file: {def_file}")
    framework_name, pkg_name, framework_evaluations = get_framework_evaluations(def_file, run_config_cli_overrides)
    if not is_package_installed(pkg_name):
        logging.warning(f"Framework {framework_name} is not installed. Skipping. Evaluations from this framework will not be available to run.")
    else:
        framework_eval_mapping[framework_name] = framework_evaluations
        eval_name_mapping.update(framework_evaluations)

    return framework_eval_mapping, eval_name_mapping


def validate_evaluation(run_config_cli_overrides: dict) -> Evaluation:
    # NOTE: evaluation type can be either 'framework.evaluation' or 'evaluation'
    # TODO(pj): Does it still make sense, when we have one framework per docker?
    eval_type_components = run_config_cli_overrides["config"]["type"].split(".")
    if len(eval_type_components) == 2:
        framework_name, evaluation_name = eval_type_components
    elif len(eval_type_components) == 1:
        framework_name, evaluation_name = None, eval_type_components[0]
    else:
        raise MisconfigurationError("eval_type must follow 'framework_name.evaluation_name'. No additional dots are allowed.")

    framework_evalss_mapping, all_evals_mapping = get_available_evaluations(run_config_cli_overrides)

    if framework_name:
        try:
            evals_mapping = framework_evalss_mapping[framework_name]
        except KeyError:
            raise MisconfigurationError(f"Unknown framework {framework_name}. Frameworks available: {', '.join(framework_evalss_mapping.keys())}")
    else:
        evals_mapping = all_evals_mapping

    try:
        evaluation = evals_mapping[evaluation_name]
    except KeyError:
        raise MisconfigurationError(f"Unknown evaluation {evaluation_name}. Evaluations available: {', '.join(evals_mapping.keys())}")

    logging.info(f"Invoked config:\n{str(evaluation)}")

    try:
        os.makedirs(evaluation.config.output_dir, exist_ok=True)
    except OSError as error:
        print(f"An error occurred while creating output directory: {error}")

    with open(os.path.join(evaluation.config.output_dir, "run_config.yml"), "w") as f:
        yaml.dump(evaluation.model_dump(), f)

    return evaluation
