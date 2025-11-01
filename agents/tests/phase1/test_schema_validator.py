#!/usr/bin/env python3
"""
Unit Tests for Schema Validator
================================

Extensive testing of schema validation functionality.
"""

import json
import pytest
import tempfile
import sys
from pathlib import Path
from jsonschema import ValidationError

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.schema_validator import SchemaValidator, get_validator, validate_output


class TestSchemaValidator:
    """Test SchemaValidator class."""

    def test_init_default_schemas_dir(self):
        """Test validator initializes with default schemas directory."""
        validator = SchemaValidator()
        assert validator.schemas_dir.exists()
        assert validator.schemas_dir.name == "schemas"
        assert validator.schemas_cache == {}

    def test_init_custom_schemas_dir(self):
        """Test validator initializes with custom schemas directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = SchemaValidator(schemas_dir=Path(tmpdir))
            assert validator.schemas_dir == Path(tmpdir)
            assert validator.schemas_cache == {}

    def test_load_schema(self):
        """Test loading a schema file."""
        validator = SchemaValidator()
        schema = validator.load_schema("agent-output-schema.json")
        
        assert schema is not None
        assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
        assert schema["title"] == "Agent Output Schema"
        assert "required" in schema
        assert "properties" in schema

    def test_load_schema_caching(self):
        """Test schema is cached after first load."""
        validator = SchemaValidator()
        
        schema1 = validator.load_schema("agent-output-schema.json")
        assert len(validator.schemas_cache) == 1
        
        schema2 = validator.load_schema("agent-output-schema.json")
        assert schema1 is schema2  # Same object (cached)
        assert len(validator.schemas_cache) == 1

    def test_load_schema_not_found(self):
        """Test loading non-existent schema raises FileNotFoundError."""
        validator = SchemaValidator()
        
        with pytest.raises(FileNotFoundError):
            validator.load_schema("non-existent-schema.json")

    def test_load_all_schemas(self):
        """Test loading all available schemas."""
        validator = SchemaValidator()
        
        schemas = [
            "agent-output-schema.json",
            "security-findings-schema.json",
            "inter-agent-message-schema.json"
        ]
        
        for schema_name in schemas:
            schema = validator.load_schema(schema_name)
            assert schema is not None
            assert "$schema" in schema

    def test_validate_valid_output(self):
        """Test validating a valid agent output."""
        validator = SchemaValidator()
        
        valid_output = {
            "schema_version": "1.0.0",
            "agent": {
                "name": "Test Agent",
                "version": "1.0.0",
                "category": "security"
            },
            "execution": {
                "timestamp": "2025-11-01T10:30:00Z",
                "status": "success"
            },
            "results": {
                "data": {}
            }
        }
        
        is_valid, errors = validator.validate_output(valid_output)
        assert is_valid is True
        assert errors == []

    def test_validate_invalid_output_missing_required(self):
        """Test validating output missing required fields."""
        validator = SchemaValidator()
        
        invalid_output = {
            "schema_version": "1.0.0",
            # Missing "agent", "execution", "results"
        }
        
        is_valid, errors = validator.validate_output(invalid_output)
        assert is_valid is False
        assert len(errors) > 0
        assert "required" in errors[0].lower() or "missing" in errors[0].lower()

    def test_validate_invalid_output_wrong_type(self):
        """Test validating output with wrong data types."""
        validator = SchemaValidator()
        
        invalid_output = {
            "schema_version": 123,  # Should be string
            "agent": {
                "name": "Test Agent",
                "version": "1.0.0",
                "category": "security"
            },
            "execution": {
                "timestamp": "2025-11-01T10:30:00Z",
                "status": "success"
            },
            "results": {
                "data": {}
            }
        }
        
        is_valid, errors = validator.validate_output(invalid_output)
        assert is_valid is False
        assert len(errors) > 0

    def test_validate_invalid_output_wrong_enum(self):
        """Test validating output with invalid enum value."""
        validator = SchemaValidator()
        
        invalid_output = {
            "schema_version": "1.0.0",
            "agent": {
                "name": "Test Agent",
                "version": "1.0.0",
                "category": "invalid_category"  # Invalid enum
            },
            "execution": {
                "timestamp": "2025-11-01T10:30:00Z",
                "status": "success"
            },
            "results": {
                "data": {}
            }
        }
        
        is_valid, errors = validator.validate_output(invalid_output)
        assert is_valid is False
        assert len(errors) > 0

    def test_validate_invalid_output_wrong_pattern(self):
        """Test validating output with invalid pattern."""
        validator = SchemaValidator()
        
        invalid_output = {
            "schema_version": "invalid-version",  # Should match \d+\.\d+\.\d+
            "agent": {
                "name": "Test Agent",
                "version": "1.0.0",
                "category": "security"
            },
            "execution": {
                "timestamp": "2025-11-01T10:30:00Z",
                "status": "success"
            },
            "results": {
                "data": {}
            }
        }
        
        is_valid, errors = validator.validate_output(invalid_output)
        assert is_valid is False
        assert len(errors) > 0

    def test_validate_complete_output(self):
        """Test validating complete output with all optional fields."""
        validator = SchemaValidator()
        
        complete_output = {
            "schema_version": "1.0.0",
            "agent": {
                "name": "Security Monitoring Agent",
                "version": "2.0.0",
                "category": "security"
            },
            "execution": {
                "timestamp": "2025-11-01T10:30:00Z",
                "duration_ms": 45000,
                "status": "success",
                "workflow_name": "full_security_audit"
            },
            "context": {
                "input": {
                    "scan_paths": ["src/**/*.tsx"],
                    "security_checks": ["xss", "csrf"]
                },
                "metadata": {
                    "files_scanned": 142
                }
            },
            "results": {
                "data": {
                    "security_issues": [],
                    "standards_violations": [],
                    "unused_files": []
                },
                "artifacts": [
                    {
                        "type": "report",
                        "format": "json",
                        "path": "security-reports/report.json"
                    }
                ],
                "metrics": {
                    "critical_count": 0,
                    "security_score": 100
                }
            },
            "findings": {
                "issues": [],
                "warnings": [],
                "info": []
            },
            "recommendations": [],
            "next_actions": {
                "suggested_agents": [],
                "required_skills": []
            }
        }
        
        is_valid, errors = validator.validate_output(complete_output)
        assert is_valid is True
        assert errors == []

    def test_validate_and_raise_valid(self):
        """Test validate_and_raise with valid output (no exception)."""
        validator = SchemaValidator()
        
        valid_output = {
            "schema_version": "1.0.0",
            "agent": {
                "name": "Test Agent",
                "version": "1.0.0",
                "category": "security"
            },
            "execution": {
                "timestamp": "2025-11-01T10:30:00Z",
                "status": "success"
            },
            "results": {
                "data": {}
            }
        }
        
        # Should not raise
        validator.validate_and_raise(valid_output)

    def test_validate_and_raise_invalid(self):
        """Test validate_and_raise with invalid output (raises exception)."""
        validator = SchemaValidator()
        
        invalid_output = {
            "schema_version": "1.0.0",
            # Missing required fields
        }
        
        with pytest.raises(ValidationError):
            validator.validate_and_raise(invalid_output)

    def test_format_error(self):
        """Test error formatting."""
        validator = SchemaValidator()
        
        # Create a mock validation error
        schema = validator.load_schema("agent-output-schema.json")
        
        invalid_data = {"schema_version": 123}
        
        with pytest.raises(ValidationError) as exc_info:
            from jsonschema import validate
            validate(instance=invalid_data, schema=schema)
        
        error = exc_info.value
        formatted = validator._format_error(error)
        
        assert "Validation error" in formatted or "error" in formatted.lower()

    def test_validate_custom_schema(self):
        """Test validating against a custom schema."""
        validator = SchemaValidator()
        
        # Test with inter-agent message schema
        message = {
            "message_id": "test-id-123",
            "timestamp": "2025-11-01T10:30:00Z",
            "from_agent": "agent1",
            "to_agent": "agent2",
            "message_type": "request",
            "payload": {}
        }
        
        is_valid, errors = validator.validate_output(
            message, 
            "inter-agent-message-schema.json"
        )
        assert is_valid is True
        assert errors == []


class TestGlobalValidator:
    """Test global validator functions."""

    def test_get_validator_singleton(self):
        """Test get_validator returns singleton instance."""
        validator1 = get_validator()
        validator2 = get_validator()
        
        assert validator1 is validator2

    def test_validate_output_convenience(self):
        """Test convenience validate_output function."""
        valid_output = {
            "schema_version": "1.0.0",
            "agent": {
                "name": "Test Agent",
                "version": "1.0.0",
                "category": "security"
            },
            "execution": {
                "timestamp": "2025-11-01T10:30:00Z",
                "status": "success"
            },
            "results": {
                "data": {}
            }
        }
        
        is_valid, errors = validate_output(valid_output)
        assert is_valid is True
        assert errors == []

    def test_validate_output_with_custom_schema(self):
        """Test convenience function with custom schema."""
        message = {
            "message_id": "test-id-123",
            "timestamp": "2025-11-01T10:30:00Z",
            "from_agent": "agent1",
            "to_agent": "agent2",
            "message_type": "notification",
            "payload": {}
        }
        
        is_valid, errors = validate_output(
            message,
            "inter-agent-message-schema.json"
        )
        assert is_valid is True
        assert errors == []


class TestSchemaEdgeCases:
    """Test edge cases and error conditions."""

    def test_validate_empty_dict(self):
        """Test validating empty dictionary."""
        validator = SchemaValidator()
        
        is_valid, errors = validator.validate_output({})
        assert is_valid is False
        assert len(errors) > 0

    def test_validate_none(self):
        """Test validating None (should handle gracefully)."""
        validator = SchemaValidator()
        
        is_valid, errors = validator.validate_output(None)
        assert is_valid is False
        assert len(errors) > 0

    def test_validate_list(self):
        """Test validating list instead of object."""
        validator = SchemaValidator()
        
        is_valid, errors = validator.validate_output([])
        assert is_valid is False
        assert len(errors) > 0

    def test_validate_string(self):
        """Test validating string instead of object."""
        validator = SchemaValidator()
        
        is_valid, errors = validator.validate_output("invalid")
        assert is_valid is False
        assert len(errors) > 0

    def test_validate_nested_structure(self):
        """Test validating deeply nested structure."""
        validator = SchemaValidator()
        
        nested_output = {
            "schema_version": "1.0.0",
            "agent": {
                "name": "Test Agent",
                "version": "1.0.0",
                "category": "security"
            },
            "execution": {
                "timestamp": "2025-11-01T10:30:00Z",
                "status": "success"
            },
            "results": {
                "data": {
                    "nested": {
                        "deep": {
                            "very_deep": {
                                "value": "test"
                            }
                        }
                    }
                }
            }
        }
        
        is_valid, errors = validator.validate_output(nested_output)
        assert is_valid is True
        assert errors == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
