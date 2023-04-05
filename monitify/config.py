import json
import yaml
import jsonschema
from pathlib import Path
from typing import Any

config_schema = {
    "type": "object",
    "properties": {
        "notifications": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {
                "oneOf": [
                    {
                        "type": "object",
                        "properties": {
                            "type": {"const": "wa"},
                            "url": {"type": "string", "format": "uri"},
                            "api_key": {"type": "string"},
                            "chat_id": {"type": "string"}
                        },
                        "required": ["type", "url", "api_key", "chat_id"]
                    },
                    {
                        "type": "object",
                        "properties": {
                            "type": {"const": "teams"},
                            "url": {"type": "string", "format": "uri"}
                        },
                        "required": ["type", "url"]
                    }
                ]
            }
        },
        "tasks": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {
                "oneOf": [
                    {
                        "type": "object",
                        "properties": {
                            "type": {"const": "email"},
                            "name": {"type": "string"},
                            "host": {"type": "string", "format": "hostname"},
                            "port": {"type": "number"},
                            "user": {"type": "string"},
                            "password": {"type": "string"},
                            "delay": {"type": "number"},
                        },
                        "required": ["type", "name", "host", "user", "password"],
                        "additionalProperties": False
                    },
                    {
                        "type": "object",
                        "properties": {
                            "type": {"const": "owncloud"},
                            "name": {"type": "string"},
                            "url": {"type": "string", "format": "uri"},
                            "user_id": {"type": "string"},
                            "password": {"type": "string"},
                            "path": {"type": "string"},
                            "delay": {"type": "number"},
                        },
                        "required": ["type", "name", "url", "user_id", "password"],
                        "additionalProperties": False
                    },
                    {
                        "type": "object",
                        "properties": {
                            "type": {"const": "exchange"},
                            "name": {"type": "string"},
                            "server": {"type": "string", "format": "hostname"},
                            "username": {"type": "string"},
                            "password": {"type": "string"},
                            "email": {"type": "string"},
                            "timeout": {"type": "number"},
                        },
                        "required": ["type", "name", "server", "username", "password", "email"],
                        "additionalProperties": False
                    }
                ]
            }
        }
    }
}


def parse_config(path: Path) -> object:
    if path.suffix == ".yml":
        return yaml.safe_load(path.read_text())
    if path.suffix == ".json":
        return json.load(path.read_text())
    raise Exception("Unsupported config file format.")


def validate_config(config: Any) -> bool:
    try:
        jsonschema.validate(config, config_schema)
        return True
    except jsonschema.ValidationError:
        return False
