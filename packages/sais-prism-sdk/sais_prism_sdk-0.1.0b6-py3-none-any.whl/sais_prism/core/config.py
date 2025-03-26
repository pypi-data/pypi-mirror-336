from pydantic import BaseModel, Extra, validator
from typing import Dict, Any, List, Optional, Union
import os
import yaml
from types import SimpleNamespace
import argparse
import json
import sys


class FoundationConfig(BaseModel):
    experiment_name: str = "default_experiment"


class UnifiedDataAccessConfig(BaseModel):
    enabled: bool = False
    cached: bool = True
    token: Optional[str] = None
    data_access: Dict[str, List[str]] = {}


class MLFlowConfig(BaseModel):
    class ModelRepoConfig(BaseModel):
        model_uri: str = ""
        registered: bool = True
        name: str = "default_model"
        tag: Dict[str, str] = {}
        version: str = "0.1.0"
    class SecurityConfig(BaseModel):
        enabled: bool = False
        username: str = ""
        password: str = ""

    enabled: bool = True
    auto_log: bool = True
    system_tracing: bool = True
    model_repo: ModelRepoConfig = ModelRepoConfig()
    security: SecurityConfig = SecurityConfig()
    metrics: Union[Dict[str, List[str]], List[str]] = {}

    @validator("metrics", pre=True)
    def transform_metrics(cls, v):
        if isinstance(v, list):
            return {"metrics": v}
        return v

    artifacts: Union[Dict[str, List[str]], List[str]] = []
    parameters: Dict[str, Any] = {}


class DynamicConfig(BaseModel):
    class Config:
        extra = Extra.allow


class SAISConfig(DynamicConfig):
    foundation: FoundationConfig = FoundationConfig()
    unified_data_access: UnifiedDataAccessConfig = UnifiedDataAccessConfig()
    ml: MLFlowConfig = MLFlowConfig()


class ConfigManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _convert_namespace_to_dict(self, ns):
        """
        Recursively convert a SimpleNamespace to a dictionary while preserving/converting data types.
        """
        if not isinstance(ns, SimpleNamespace):
            if isinstance(ns, str):
                try:
                    return float(ns)
                except ValueError:
                    return ns
            return ns
        return {key: self._convert_namespace_to_dict(value) for key, value in ns.__dict__.items()}

    def _convert_to_namespace(self, model):
        if isinstance(model, BaseModel):
            namespace = SimpleNamespace()
            for name, value in vars(model).items():
                setattr(namespace, name, self._convert_to_namespace(value))
            return namespace
        elif isinstance(model, dict):
            return SimpleNamespace(**{
                k: self._convert_to_namespace(v) for k, v in model.items()
            })
        elif isinstance(model, list):
            return [self._convert_to_namespace(item) for item in model]
        return model

    def _load_config(self):
        self.config_path = os.path.join(os.getcwd(), "sais_foundation.yaml")
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                "sais_foundation.yaml not found in project root")

        with open(self.config_path) as f:
            self.raw_config = yaml.safe_load(f)

        self.config = self._convert_to_namespace(SAISConfig(**self.raw_config))
    
    def update_config(self, key_path: str, value: Any, update_yaml=False):
        """
        Update a config value using dot-notation path
        Example: update_config("ml.parameters.device", "cuda")
        
        Args:
            key_path: Dot-notation path to the config value
            value: New value to set
            update_yaml: If True, also update the YAML file on disk
        """
        parts = key_path.split('.')
        current = self.config
        
        # Navigate to the nested attribute
        for i, part in enumerate(parts[:-1]):
            if not hasattr(current, part):
                # Create missing namespaces
                setattr(current, part, SimpleNamespace())
            current = getattr(current, part)
        
        # Set the value at the final level
        try:
            # Try to convert string value to appropriate type (int, float, bool, list, dict)
            if isinstance(value, str):
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                elif value.isdigit():
                    value = int(value)
                elif value.replace('.', '', 1).isdigit() and value.count('.') <= 1:
                    value = float(value)
                elif value.startswith('[') and value.endswith(']'):
                    try:
                        value = json.loads(value)
                    except:
                        pass  # Keep as string if JSON parsing fails
                elif value.startswith('{') and value.endswith('}'):
                    try:
                        value = json.loads(value)
                    except:
                        pass  # Keep as string if JSON parsing fails
        except:
            # If conversion fails, keep the original value
            pass
        
        setattr(current, parts[-1], value)
        
        # Update the YAML file if requested
        if update_yaml:
            self._update_yaml_file(key_path, value)
    
    def _update_yaml_file(self, key_path: str, value: Any):
        """
        Update the YAML file with the new configuration value
        """
        parts = key_path.split('.')
        current = self.raw_config
        
        # Navigate to the nested level in the raw config dict
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Set the value at the final level
        current[parts[-1]] = value
        
        # Write the updated config back to the YAML file
        with open(self.config_path, 'w') as f:
            yaml.dump(self.raw_config, f, default_flow_style=False, sort_keys=False)

    def get(self, key: str, default=None) -> Any:
        return getattr(self.config, key, default)


class DynamicConfigAccessor:
    def __getattr__(self, name: str) -> Any:
        return ConfigManager().get(name)


config = DynamicConfigAccessor()


def parse_cli_args(description="Override configuration values", update_yaml=True):
    """
    Parse command line arguments to override YAML configuration.
    
    Arguments can be specified in two formats:
    1. Multiple parameters with individual --config flags:
       --config key1.key2.key3=value1 --config key4.key5=value2
    
    2. Multiple parameters with a single --config flag:
       --config key1.key2.key3=value1 key4.key5=value2
    
    Example:
    python script.py --config ml.parameters.device=cuda ml.parameters.num_train_epochs=5
    
    Args:
        description: Description for the argument parser
        update_yaml: If True, also update the YAML file on disk with the new values
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--config', action='append', nargs='+', default=[], 
                       help='Override config values in format key1.key2.key3=value1 [key2=value2 ...]')
    
    # Parse only the known args, ignore the rest
    args, _ = parser.parse_known_args()
    
    config_manager = ConfigManager()
    
    # Process config overrides
    for config_args in args.config:
        # Each config_args is a list of one or more key=value pairs
        for config_str in config_args:
            if '=' not in config_str:
                print(f"Warning: Invalid config format '{config_str}'. Must be in format key=value", file=sys.stderr)
                continue
                
            key_path, value = config_str.split('=', 1)
            config_manager.update_config(key_path, value, update_yaml=update_yaml)
            print(f"Config override: {key_path} = {value}")
