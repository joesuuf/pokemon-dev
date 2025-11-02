#!/usr/bin/env python3
"""
JSON Schema Validator for Agent Outputs
========================================

Validates agent outputs against standardized JSON schemas.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple, List
from jsonschema import validate, ValidationError, Draft7Validator


class SchemaValidator:
    """Validates agent outputs against JSON schemas."""

    def __init__(self, schemas_dir: Path = None):
        """
        Initialize validator with schemas directory.

        Args:
            schemas_dir: Path to directory containing JSON schemas
        """
        if schemas_dir is None:
            schemas_dir = Path(__file__).parent.parent / "schemas"

        self.schemas_dir = Path(schemas_dir)
        self.schemas_cache: Dict[str, Dict] = {}

    def load_schema(self, schema_name: str) -> Dict[str, Any]:
        """
        Load a JSON schema from file.

        Args:
            schema_name: Name of schema file (e.g., 'agent-output-schema.json')

        Returns:
            Loaded schema dictionary
        """
        if schema_name in self.schemas_cache:
            return self.schemas_cache[schema_name]

        schema_path = self.schemas_dir / schema_name
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema not found: {schema_path}")

        with open(schema_path) as f:
            schema = json.load(f)

        self.schemas_cache[schema_name] = schema
        return schema

    def validate_output(self, output: Dict[str, Any],
                       schema_name: str = "agent-output-schema.json") -> Tuple[bool, List[str]]:
        """
        Validate agent output against schema.

        Args:
            output: Agent output dictionary to validate
            schema_name: Schema file name

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        try:
            schema = self.load_schema(schema_name)
            validate(instance=output, schema=schema)
            return True, []
        except ValidationError as e:
            errors = []
            # Collect all validation errors
            for error in e.absolute_path:
                errors.append(self._format_error(e))
            # If no nested errors, just format the main error
            if not errors:
                errors = [self._format_error(e)]
            return False, errors if errors else [self._format_error(e)]
        except Exception as e:
            return False, [f"Validation error: {str(e)}"]

    def _format_error(self, error: ValidationError) -> str:
        """Format validation error message."""
        path = ".".join(str(p) for p in error.path)
        return f"Validation error at '{path}': {error.message}"

    def validate_and_raise(self, output: Dict[str, Any],
                          schema_name: str = "agent-output-schema.json"):
        """
        Validate and raise exception if invalid.

        Args:
            output: Agent output to validate
            schema_name: Schema file name

        Raises:
            ValidationError: If output is invalid
        """
        is_valid, errors = self.validate_output(output, schema_name)
        if not is_valid:
            raise ValidationError("\n".join(errors))


# Global validator instance
_validator = None

def get_validator() -> SchemaValidator:
    """Get global validator instance."""
    global _validator
    if _validator is None:
        _validator = SchemaValidator()
    return _validator


def validate_output(output: Dict[str, Any],
                   schema_name: str = "agent-output-schema.json") -> Tuple[bool, List[str]]:
    """Convenience function to validate output."""
    return get_validator().validate_output(output, schema_name)
