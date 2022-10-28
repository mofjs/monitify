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
                            "key": {"type": "string"},
                            "chatId": {"type": "string"}
                        },
                        "required": ["type", "url", "key", "chatId"]
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
        "sources": {
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
                            "hostname": {"type": "string", "format": "hostname"},
                            "port": {"type": "number"},
                            "username": {"type": "string"},
                            "password": {"type": "string"},
                        },
                        "required": ["type", "name", "hostname", "username", "password"]
                    },
                    {
                        "type": "object",
                        "properties": {
                            "type": {"const": "owncloud"},
                            "name": {"type": "string"},
                            "url": {"type": "string", "format": "uri"},
                            "username": {"type": "string"},
                            "password": {"type": "string"},
                            "directory": {"type": "string"}
                        },
                        "required": ["type", "name", "url", "username", "password"]
                    }
                ]
            }
        }
    }
}


def parse_config(path: Path) -> object:
    try:
        if path.suffix == ".yml":
            return yaml.safe_load(path.read_text())
        if path.suffix == ".json":
            return json.load(path.read_text())
    finally:
        return None


def validate_config(config: Any) -> bool:
    try:
        jsonschema.validate(config, config_schema)
        return True
    except jsonschema.ValidationError as e:
        print(e)
        return False
