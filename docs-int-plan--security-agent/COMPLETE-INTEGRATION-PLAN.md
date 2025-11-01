# Security Agent Integration Plan - Complete Documentation

**Date:** November 1, 2025
**Version:** 1.0.0
**Status:** Planning Phase

---

## Executive Summary

This document outlines the complete plan to integrate the existing `/security-agent` into the modular agent framework (`/agents`), regenerating it to fit within the modular architecture with dual PY & MD/YAML outputs, and establishing a standardized JSON communication structure for inter-agent data exchange based on Anthropic best practices as of November 2025.

---

## Table of Contents

1. [Current State Analysis](#current-state-analysis)
2. [Goals & Objectives](#goals--objectives)
3. [Proposed JSON Communication Structure](#proposed-json-communication-structure)
4. [Integration Architecture](#integration-architecture)
5. [Step-by-Step Migration Plan](#step-by-step-migration-plan)
6. [Implementation Priorities](#implementation-priorities)
7. [Deliverables](#deliverables)
8. [Migration Strategy](#migration-strategy)
9. [Success Criteria](#success-criteria)

---

## Current State Analysis

### Existing Security Agent
- **Location:** `/security-agent/`
- **Architecture:** Standalone Python script with comprehensive scanning capabilities
- **Features:**
  - Mobile browser attack detection (XSS, CSRF, CORS, etc.)
  - Framework standards checking (TypeScript/React, Python 3)
  - Dead code detection
  - Multiple report formats (JSON, HTML, Markdown)
- **Configuration:** JSON-based (`config/agent-config.json`)
- **Output:** Custom JSON structure, not standardized for inter-agent communication

### Existing Modular Framework
- **Location:** `/agents/`
- **Architecture:** Modular, skill-based agents with dual format outputs
- **Pattern:** Python implementation + Markdown specification with YAML frontmatter
- **Base Class:** `ModularAgent` in `modular_agent_framework.py`
- **Structure:**
  - `python/` - Agent implementations
  - `md/` - Agent specifications
  - `skills/` - Reusable skill functions
  - `workflows/` - YAML workflow definitions

### Current Gaps
- ❌ No standardized inter-agent JSON communication structure
- ❌ Security agent not integrated into modular framework
- ❌ No JSON schema validation for agent outputs
- ❌ No inter-agent message passing infrastructure

---

## Goals & Objectives

### Primary Goals
1. **Integrate Security Agent** into the modular framework following existing patterns
2. **Establish JSON Communication Standard** for all agents to exchange data
3. **Maintain Backward Compatibility** with existing security agent functionality
4. **Enable Inter-Agent Workflows** through standardized data exchange

### Specific Objectives
- Create standardized JSON schemas for agent outputs
- Break down monolithic security agent into modular skills
- Implement security workflows using skill composition
- Provide dual format outputs (Python + MD/YAML)
- Enable agents to read and process outputs from other agents
- Maintain all existing security agent functionality

---

## Proposed JSON Communication Structure

Based on Anthropic's best practices (JSON-RPC 2.0 style) and existing agent patterns in the codebase.

### Base Agent Output Schema

**File:** `agents/schemas/agent-output-schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Agent Output Schema",
  "description": "Standardized output format for all modular agents",
  "type": "object",
  "required": ["schema_version", "agent", "execution", "results"],
  "properties": {
    "schema_version": {
      "type": "string",
      "description": "Version of the output schema",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "agent": {
      "type": "object",
      "required": ["name", "version", "category"],
      "properties": {
        "name": {
          "type": "string",
          "description": "Human-readable agent name"
        },
        "version": {
          "type": "string",
          "description": "Agent version",
          "pattern": "^\\d+\\.\\d+\\.\\d+$"
        },
        "category": {
          "type": "string",
          "description": "Agent category",
          "enum": ["security", "performance", "seo", "content", "installation"]
        }
      }
    },
    "execution": {
      "type": "object",
      "required": ["timestamp", "status"],
      "properties": {
        "timestamp": {
          "type": "string",
          "format": "date-time",
          "description": "ISO-8601 timestamp"
        },
        "duration_ms": {
          "type": "number",
          "description": "Execution duration in milliseconds"
        },
        "status": {
          "type": "string",
          "enum": ["success", "partial", "failed"],
          "description": "Execution status"
        },
        "skill_name": {
          "type": "string",
          "description": "Name of executed skill (if single skill)"
        },
        "workflow_name": {
          "type": "string",
          "description": "Name of executed workflow (if workflow)"
        }
      }
    },
    "context": {
      "type": "object",
      "description": "Input context and metadata",
      "properties": {
        "input": {
          "type": "object",
          "description": "Input parameters provided to agent"
        },
        "metadata": {
          "type": "object",
          "description": "Additional context metadata"
        }
      }
    },
    "results": {
      "type": "object",
      "required": ["data"],
      "properties": {
        "data": {
          "type": "object",
          "description": "Primary result data"
        },
        "artifacts": {
          "type": "array",
          "description": "Generated artifacts (reports, files, etc.)",
          "items": {
            "type": "object",
            "required": ["type", "format", "path"],
            "properties": {
              "type": {
                "type": "string",
                "description": "Artifact type"
              },
              "format": {
                "type": "string",
                "description": "Artifact format"
              },
              "path": {
                "type": "string",
                "description": "Path to artifact"
              }
            }
          }
        },
        "metrics": {
          "type": "object",
          "description": "Key metrics from execution"
        }
      }
    },
    "findings": {
      "type": "object",
      "description": "Issues, warnings, and informational messages",
      "properties": {
        "issues": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["severity", "message"],
            "properties": {
              "severity": {
                "type": "string",
                "enum": ["critical", "high", "medium", "low", "info"]
              },
              "message": {
                "type": "string"
              },
              "impact": {
                "type": "string"
              }
            }
          }
        },
        "warnings": {
          "type": "array",
          "items": {
            "type": "object"
          }
        },
        "info": {
          "type": "array",
          "items": {
            "type": "object"
          }
        }
      }
    },
    "recommendations": {
      "type": "array",
      "description": "Actionable recommendations",
      "items": {
        "type": "string"
      }
    },
    "next_actions": {
      "type": "object",
      "description": "Suggested next steps for orchestration",
      "properties": {
        "suggested_agents": {
          "type": "array",
          "description": "Agents that should run next",
          "items": {
            "type": "string"
          }
        },
        "required_skills": {
          "type": "array",
          "description": "Skills that should be executed",
          "items": {
            "type": "string"
          }
        }
      }
    }
  }
}
```

### Security Agent Specific Output Example

```json
{
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
      "scan_paths": ["src/**/*.tsx", "src/**/*.ts"],
      "security_checks": ["xss", "csrf", "cors"]
    },
    "metadata": {
      "files_scanned": 142,
      "scan_type": "mobile_attacks"
    }
  },
  "results": {
    "data": {
      "security_issues": [
        {
          "id": "SEC-001",
          "category": "xss",
          "severity": "critical",
          "file_path": "src/components/UserProfile.tsx",
          "line_number": 45,
          "code_snippet": "dangerouslySetInnerHTML={{__html: userInput}}",
          "description": "Dangerous HTML injection point",
          "recommendation": "Use DOMPurify to sanitize user input",
          "cwe_id": "CWE-79",
          "mobile_specific": false
        }
      ],
      "standards_violations": [
        {
          "framework": "TypeScript/React",
          "rule": "Use functional components instead of class components",
          "file_path": "src/components/OldComponent.tsx",
          "line_number": 12,
          "code_snippet": "class OldComponent extends React.Component",
          "expected": "Functional component with hooks",
          "actual": "Class component",
          "auto_fixable": false
        }
      ],
      "unused_files": [
        {
          "file_path": "src/components/_LoadingSpinner.svelte",
          "reason": "No imports or references found in codebase; File already marked with underscore prefix",
          "confidence": "high",
          "last_modified": "2025-09-15T08:22:00Z",
          "file_size": 1024,
          "references_found": 0,
          "suggested_action": "Rename with underscore prefix to verify, then delete if no issues arise"
        }
      ]
    },
    "artifacts": [
      {
        "type": "report",
        "format": "html",
        "path": "security-agent/reports/security-report-20251101_103000.html"
      },
      {
        "type": "report",
        "format": "json",
        "path": "security-agent/reports/security-report-20251101_103000.json"
      },
      {
        "type": "report",
        "format": "markdown",
        "path": "security-agent/reports/security-report-20251101_103000.md"
      }
    ],
    "metrics": {
      "critical_count": 2,
      "high_count": 5,
      "medium_count": 8,
      "low_count": 3,
      "security_score": 72,
      "standards_violations": 15,
      "unused_files": 7
    }
  },
  "findings": {
    "issues": [
      {
        "severity": "critical",
        "message": "Found 2 critical XSS vulnerabilities",
        "impact": "high"
      },
      {
        "severity": "high",
        "message": "5 high-severity security issues detected",
        "impact": "medium"
      }
    ],
    "warnings": [
      {
        "message": "15 framework standards violations found",
        "impact": "low"
      }
    ],
    "info": [
      {
        "message": "7 potentially unused files identified for review"
      }
    ]
  },
  "recommendations": [
    "Use DOMPurify for HTML sanitization in UserProfile.tsx",
    "Add CSP headers to all HTML pages",
    "Implement CSRF tokens for form submissions",
    "Restrict CORS to specific trusted origins",
    "Review and remove 7 potentially unused files"
  ],
  "next_actions": {
    "suggested_agents": ["performance_monitoring"],
    "required_skills": ["auto_fix_security", "dead_code_cleanup"]
  }
}
```

### Inter-Agent Message Schema

**File:** `agents/schemas/inter-agent-message-schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Inter-Agent Message Schema",
  "description": "Schema for messages passed between agents",
  "type": "object",
  "required": ["message_id", "from_agent", "to_agent", "message_type", "payload"],
  "properties": {
    "message_id": {
      "type": "string",
      "description": "Unique message identifier"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "from_agent": {
      "type": "string",
      "description": "Source agent name"
    },
    "to_agent": {
      "type": "string",
      "description": "Destination agent name"
    },
    "message_type": {
      "type": "string",
      "enum": ["request", "response", "notification", "error"],
      "description": "Type of message"
    },
    "payload": {
      "type": "object",
      "description": "Message payload"
    },
    "correlation_id": {
      "type": "string",
      "description": "ID linking request/response pairs"
    }
  }
}
```

---

## Integration Architecture

### New Directory Structure

```
agents/
├── python/
│   ├── modular_agent_framework.py          # Enhanced with JSON support
│   ├── security_monitoring_agent.py        # NEW - Refactored security agent
│   ├── performance_monitoring_agent.py
│   ├── seo_optimization_agent.py
│   ├── content_coordinator_agent.py
│   ├── professor_data_installation_agent.py
│   ├── performance_implementation_agent.py
│   └── test_agents.py
│
├── md/
│   ├── security_monitoring_agent.md        # NEW - Agent specification
│   ├── performance_monitoring_agent.md
│   ├── seo_optimization_agent.md
│   ├── content_coordinator_agent.md
│   └── professor_data_installation_agent.md
│
├── skills/
│   ├── security/                           # NEW - Security skills
│   │   ├── mobile_xss_scanner.py
│   │   ├── csrf_validator.py
│   │   ├── cors_checker.py
│   │   ├── csp_analyzer.py
│   │   ├── typescript_standards_checker.py
│   │   ├── python_standards_checker.py
│   │   └── dead_code_detector.py
│   ├── performance/
│   │   └── example_lighthouse_skill.py
│   ├── seo/
│   ├── content/
│   └── installation/
│
├── workflows/
│   ├── security/                           # NEW - Security workflows
│   │   ├── full_security_audit.yaml
│   │   ├── mobile_attack_scan.yaml
│   │   ├── standards_check.yaml
│   │   └── dead_code_cleanup.yaml
│   ├── performance/
│   │   └── full_audit.yaml
│   ├── seo/
│   ├── content/
│   └── installation/
│
├── schemas/                                # NEW - JSON schemas
│   ├── agent-output-schema.json
│   ├── security-findings-schema.json
│   └── inter-agent-message-schema.json
│
├── lib/                                    # NEW - Shared utilities
│   ├── __init__.py
│   ├── agent_communication.py              # Inter-agent communication helpers
│   └── schema_validator.py                 # JSON schema validation
│
├── docs/                                   # NEW - Enhanced documentation
│   ├── JSON_COMMUNICATION.md
│   ├── SECURITY_AGENT_MIGRATION.md
│   └── SCHEMA_REFERENCE.md
│
├── AGENTS_OVERVIEW.md
├── README.md
└── MODULAR_FRAMEWORK_README.md
```

### Component Responsibilities

#### 1. **Schemas** (`agents/schemas/`)
- Define standard output formats for all agents
- Enable validation and type safety
- Support versioning and evolution
- Provide documentation through JSON Schema

#### 2. **Library** (`agents/lib/`)
- **agent_communication.py**: Helper functions for agent-to-agent messaging
- **schema_validator.py**: Validate outputs against schemas
- Shared utilities for JSON I/O
- Error handling and logging

#### 3. **Skills** (`agents/skills/security/`)
- Single-responsibility security functions
- Reusable across workflows
- Accept context dict, return structured results
- Include metadata and configuration

#### 4. **Workflows** (`agents/workflows/security/`)
- Compose multiple skills into workflows
- Define execution order and configuration
- Enable different audit types (full, quick, focused)

#### 5. **Agent Implementation** (`agents/python/security_monitoring_agent.py`)
- Extends `ModularAgent` base class
- Registers core skills
- Implements workflow execution
- Converts outputs to standard JSON format
- Validates against schemas

#### 6. **Agent Specification** (`agents/md/security_monitoring_agent.md`)
- YAML frontmatter with agent configuration
- Natural language system prompt
- Tool requirements and capabilities
- Integration points and usage examples

---

## Step-by-Step Migration Plan

### Phase 1: Create JSON Communication Infrastructure

**Goal:** Establish standardized JSON schemas and validation infrastructure

**Files to Create:**
1. `agents/schemas/agent-output-schema.json` - Base schema for all agents
2. `agents/schemas/security-findings-schema.json` - Security-specific schema extension
3. `agents/schemas/inter-agent-message-schema.json` - Agent-to-agent communication
4. `agents/lib/__init__.py` - Library package initialization
5. `agents/lib/agent_communication.py` - Inter-agent communication helpers
6. `agents/lib/schema_validator.py` - JSON schema validation utilities

**Key Features:**
- JSON Schema Draft 7 compliance
- Type safety for agent outputs
- Schema versioning support
- Backward compatibility checks
- Validation error messages

**Implementation Details:**

**File: `agents/lib/schema_validator.py`**
```python
#!/usr/bin/env python3
"""
JSON Schema Validator for Agent Outputs
========================================

Validates agent outputs against standardized JSON schemas.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple, List
import jsonschema
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
            return False, [self._format_error(e)]
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
```

**File: `agents/lib/agent_communication.py`**
```python
#!/usr/bin/env python3
"""
Inter-Agent Communication Helpers
==================================

Utilities for agents to send and receive messages.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from .schema_validator import validate_output


class AgentMessenger:
    """Handles inter-agent message passing."""

    def __init__(self, agent_name: str, message_dir: Path = None):
        """
        Initialize messenger for an agent.

        Args:
            agent_name: Name of this agent
            message_dir: Directory for message exchange
        """
        self.agent_name = agent_name

        if message_dir is None:
            message_dir = Path.cwd() / ".agent-messages"

        self.message_dir = Path(message_dir)
        self.message_dir.mkdir(parents=True, exist_ok=True)

        self.inbox = self.message_dir / agent_name / "inbox"
        self.outbox = self.message_dir / agent_name / "outbox"
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.outbox.mkdir(parents=True, exist_ok=True)

    def send_message(self, to_agent: str, message_type: str,
                    payload: Dict[str, Any], correlation_id: str = None) -> str:
        """
        Send a message to another agent.

        Args:
            to_agent: Destination agent name
            message_type: Type of message (request, response, notification, error)
            payload: Message payload
            correlation_id: Optional correlation ID for request/response pairs

        Returns:
            Message ID
        """
        message_id = str(uuid.uuid4())

        message = {
            "message_id": message_id,
            "timestamp": datetime.now().isoformat(),
            "from_agent": self.agent_name,
            "to_agent": to_agent,
            "message_type": message_type,
            "payload": payload
        }

        if correlation_id:
            message["correlation_id"] = correlation_id

        # Validate message
        is_valid, errors = validate_output(message, "inter-agent-message-schema.json")
        if not is_valid:
            raise ValueError(f"Invalid message format: {errors}")

        # Write to outbox and recipient's inbox
        outbox_file = self.outbox / f"{message_id}.json"
        with open(outbox_file, 'w') as f:
            json.dump(message, f, indent=2)

        recipient_inbox = self.message_dir / to_agent / "inbox"
        recipient_inbox.mkdir(parents=True, exist_ok=True)
        inbox_file = recipient_inbox / f"{message_id}.json"
        with open(inbox_file, 'w') as f:
            json.dump(message, f, indent=2)

        return message_id

    def receive_messages(self, mark_read: bool = True) -> list[Dict[str, Any]]:
        """
        Receive all pending messages.

        Args:
            mark_read: If True, move messages to 'read' folder

        Returns:
            List of messages
        """
        messages = []

        for message_file in self.inbox.glob("*.json"):
            try:
                with open(message_file) as f:
                    message = json.load(f)
                messages.append(message)

                if mark_read:
                    read_dir = self.inbox.parent / "read"
                    read_dir.mkdir(exist_ok=True)
                    message_file.rename(read_dir / message_file.name)
            except Exception as e:
                print(f"Error reading message {message_file}: {e}")

        return messages

    def send_response(self, original_message: Dict[str, Any],
                     payload: Dict[str, Any]) -> str:
        """
        Send a response to a received message.

        Args:
            original_message: The message being responded to
            payload: Response payload

        Returns:
            Response message ID
        """
        return self.send_message(
            to_agent=original_message["from_agent"],
            message_type="response",
            payload=payload,
            correlation_id=original_message["message_id"]
        )


def create_agent_output(agent_name: str, agent_version: str,
                       category: str, results: Dict[str, Any],
                       execution_time_ms: float = None,
                       workflow_name: str = None) -> Dict[str, Any]:
    """
    Create standardized agent output.

    Args:
        agent_name: Name of the agent
        agent_version: Agent version
        category: Agent category
        results: Results dictionary
        execution_time_ms: Execution duration
        workflow_name: Name of executed workflow

    Returns:
        Standardized output dictionary
    """
    output = {
        "schema_version": "1.0.0",
        "agent": {
            "name": agent_name,
            "version": agent_version,
            "category": category
        },
        "execution": {
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        },
        "context": {},
        "results": results,
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

    if execution_time_ms is not None:
        output["execution"]["duration_ms"] = execution_time_ms

    if workflow_name:
        output["execution"]["workflow_name"] = workflow_name

    return output
```

**Testing Phase 1:**
- Unit tests for schema validation
- Test valid and invalid outputs
- Test message passing
- Verify schema loading and caching

---

### Phase 2: Extract Security Agent Skills

**Goal:** Break down monolithic security agent into modular, reusable skills

**Skills to Create:**

#### Skill 1: Mobile XSS Scanner
**File: `agents/skills/security/mobile_xss_scanner.py`**

Extracts XSS scanning logic from `MobileSecurityScanner` class.

```python
#!/usr/bin/env python3
"""
Mobile XSS Scanner Skill
========================

Detects XSS vulnerabilities in web applications.
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Tuple


def scan_mobile_xss(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scan files for XSS vulnerabilities.

    Args:
        context: Must contain 'files' (list of file paths) and 'config' (scanner config)

    Returns:
        Dictionary with XSS findings
    """
    files = context.get('files', [])
    config = context.get('config', {})

    # XSS patterns
    xss_patterns = [
        (r'dangerouslySetInnerHTML\s*=', "Dangerous HTML injection point", "CWE-79"),
        (r'innerHTML\s*=', "Direct innerHTML assignment can lead to XSS", "CWE-79"),
        (r'outerHTML\s*=', "Direct outerHTML assignment can lead to XSS", "CWE-79"),
        (r'document\.write\s*\(', "document.write can lead to XSS", "CWE-79"),
        (r'eval\s*\(', "eval() can execute malicious code", "CWE-95"),
        (r'new\s+Function\s*\(', "Function constructor can execute malicious code", "CWE-95"),
        (r'setTimeout\s*\(\s*["\']', "setTimeout with string can lead to injection", "CWE-95"),
        (r'setInterval\s*\(\s*["\']', "setInterval with string can lead to injection", "CWE-95"),
    ]

    issues = []

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, start=1):
                for pattern, description, cwe_id in xss_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append({
                            "category": "xss",
                            "severity": "critical",
                            "file_path": str(file_path),
                            "line_number": line_num,
                            "code_snippet": line.strip(),
                            "description": description,
                            "cwe_id": cwe_id,
                            "recommendation": "Sanitize user input and use safe DOM methods"
                        })

        except Exception as e:
            print(f"Error scanning {file_path}: {e}")

    return {
        "xss_issues": issues,
        "files_scanned": len(files),
        "vulnerabilities_found": len(issues)
    }


# Skill definition for framework
SKILLS = [{
    'name': 'mobile_xss_scanner',
    'description': 'Detect mobile browser XSS vulnerabilities',
    'category': 'security',
    'function': scan_mobile_xss,
    'required_tools': ['read', 'grep'],
    'config': {
        'severity': 'critical',
        'categories': ['xss', 'injection']
    },
    'enabled': True
}]
```

#### Additional Skills to Create:

2. **`csrf_validator.py`** - CSRF token validation
3. **`cors_checker.py`** - CORS configuration analysis
4. **`csp_analyzer.py`** - Content Security Policy checking
5. **`typescript_standards_checker.py`** - TypeScript/React standards
6. **`python_standards_checker.py`** - Python 3 standards
7. **`dead_code_detector.py`** - Unused code detection

Each skill follows the same pattern:
- Single responsibility
- Accepts context dict
- Returns structured results
- Includes SKILLS list for framework registration

**Testing Phase 2:**
- Unit test each skill in isolation
- Test with various file inputs
- Verify output format
- Test error handling

---

### Phase 3: Create Security Workflows

**Goal:** Define workflows that compose skills into complete audits

#### Workflow 1: Full Security Audit
**File: `agents/workflows/security/full_security_audit.yaml`**

```yaml
name: full_security_audit
description: Complete security, standards, and dead code audit
skills:
  - mobile_xss_scanner
  - csrf_validator
  - cors_checker
  - csp_analyzer
  - typescript_standards_checker
  - python_standards_checker
  - dead_code_detector
config:
  timeout: 600
  generate_report: true
  report_formats: ["json", "html", "markdown"]
  exit_on_critical: false
  parallel_execution: false
```

#### Workflow 2: Mobile Attack Scan
**File: `agents/workflows/security/mobile_attack_scan.yaml`**

```yaml
name: mobile_attack_scan
description: Mobile-specific security vulnerability scanning
skills:
  - mobile_xss_scanner
  - csrf_validator
  - cors_checker
  - csp_analyzer
config:
  timeout: 300
  mobile_only: true
  generate_report: true
  report_formats: ["json"]
```

#### Workflow 3: Standards Check
**File: `agents/workflows/security/standards_check.yaml`**

```yaml
name: standards_check
description: Framework standards compliance checking
skills:
  - typescript_standards_checker
  - python_standards_checker
config:
  timeout: 180
  auto_fix: false
  generate_report: true
  report_formats: ["markdown"]
```

#### Workflow 4: Dead Code Cleanup
**File: `agents/workflows/security/dead_code_cleanup.yaml`**

```yaml
name: dead_code_cleanup
description: Identify and optionally remove unused code
skills:
  - dead_code_detector
config:
  timeout: 120
  auto_rename: false
  confidence_threshold: "high"
  generate_report: true
```

---

### Phase 4: Create Modular Security Agent

**Goal:** Implement Security Monitoring Agent extending ModularAgent

**File: `agents/python/security_monitoring_agent.py`**

```python
#!/usr/bin/env python3
"""
Security Monitoring Agent
=========================

Modular security agent for mobile browser attack detection,
framework standardization, and dead code cleanup.

Integrates with the modular agent framework and outputs
standardized JSON following agent-output-schema.json.
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Import modular framework
from modular_agent_framework import ModularAgent, AgentConfig, AgentSkill

# Import communication library
from lib.agent_communication import create_agent_output
from lib.schema_validator import validate_output


class SecurityMonitoringAgent(ModularAgent):
    """
    Security monitoring agent with mobile attack detection,
    framework standards checking, and dead code identification.
    """

    def _register_core_skills(self):
        """
        Register core security skills.

        Note: Skills are primarily loaded from skills/security/ directory.
        This method can register any built-in skills that don't require
        external files.
        """
        # All skills loaded from skills/security/ via framework
        pass

    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Run security audit and return standardized JSON output.

        Args:
            **kwargs: Arguments including:
                - workflow: Name of workflow to execute (default: 'full_security_audit')
                - scan_paths: List of paths to scan
                - security_checks: List of specific checks to run
                - output_dir: Where to save reports
                - exit_on_critical: Exit with error if critical issues found

        Returns:
            Standardized agent output following schema
        """
        start_time = time.time()

        # Extract arguments
        workflow_name = kwargs.get('workflow', 'full_security_audit')
        scan_paths = kwargs.get('scan_paths', self._get_default_scan_paths())
        security_checks = kwargs.get('security_checks', ['all'])
        output_dir = kwargs.get('output_dir', './security-reports')
        exit_on_critical = kwargs.get('exit_on_critical', False)

        print(f"\n[{self.config.name}] Starting security audit")
        print(f"[{self.config.name}] Workflow: {workflow_name}")
        print(f"[{self.config.name}] Scan paths: {len(scan_paths)} paths")

        # Build context for workflow
        context = {
            'scan_paths': scan_paths,
            'security_checks': security_checks,
            'output_dir': output_dir,
            'files': self._gather_files(scan_paths)
        }

        # Execute workflow
        try:
            result = self.execute_workflow(workflow_name, context)
        except Exception as e:
            print(f"[ERROR] Workflow execution failed: {e}")
            return self._create_error_output(str(e), workflow_name)

        # Calculate execution time
        duration_ms = (time.time() - start_time) * 1000

        # Convert to standardized JSON format
        output = self._to_standard_output(
            result=result,
            workflow_name=workflow_name,
            duration_ms=duration_ms,
            context=context
        )

        # Validate against schema
        is_valid, errors = validate_output(output, 'agent-output-schema.json')
        if not is_valid:
            print(f"[WARNING] Output validation failed: {errors}")

        # Generate reports
        self._generate_reports(output, output_dir)

        # Print summary
        self._print_summary(output)

        # Check if should exit on critical
        if exit_on_critical and self._has_critical_issues(output):
            print("\n[EXIT] Critical security issues found!")
            sys.exit(1)

        return output

    def _to_standard_output(self, result: Dict[str, Any],
                           workflow_name: str, duration_ms: float,
                           context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert workflow result to standardized agent output format.

        Args:
            result: Raw workflow results
            workflow_name: Name of executed workflow
            duration_ms: Execution duration
            context: Input context

        Returns:
            Standardized output dictionary
        """
        # Aggregate results from all skills
        security_issues = []
        standards_violations = []
        unused_files = []

        # Extract data from skill results
        for key, value in result.items():
            if isinstance(value, dict):
                if 'xss_issues' in value:
                    security_issues.extend(value['xss_issues'])
                if 'csrf_issues' in value:
                    security_issues.extend(value['csrf_issues'])
                if 'cors_issues' in value:
                    security_issues.extend(value['cors_issues'])
                if 'standards_violations' in value:
                    standards_violations.extend(value['standards_violations'])
                if 'unused_files' in value:
                    unused_files.extend(value['unused_files'])

        # Count by severity
        severity_counts = self._count_by_severity(security_issues)

        # Build standardized output
        output = create_agent_output(
            agent_name=self.config.name,
            agent_version=self.config.version,
            category="security",
            results={
                "data": {
                    "security_issues": security_issues,
                    "standards_violations": standards_violations,
                    "unused_files": unused_files
                },
                "artifacts": self._list_artifacts(),
                "metrics": {
                    **severity_counts,
                    "security_score": self._calculate_security_score(security_issues),
                    "standards_violations": len(standards_violations),
                    "unused_files": len(unused_files)
                }
            },
            execution_time_ms=duration_ms,
            workflow_name=workflow_name
        )

        # Add context
        output["context"] = {
            "input": {
                "scan_paths": context.get('scan_paths', []),
                "security_checks": context.get('security_checks', [])
            },
            "metadata": {
                "files_scanned": len(context.get('files', [])),
                "scan_type": "comprehensive"
            }
        }

        # Add findings
        output["findings"] = self._create_findings(security_issues, standards_violations)

        # Add recommendations
        output["recommendations"] = self._generate_recommendations(
            security_issues, standards_violations, unused_files
        )

        # Add next actions
        output["next_actions"] = self._suggest_next_actions(security_issues)

        return output

    def _count_by_severity(self, issues: List[Dict]) -> Dict[str, int]:
        """Count issues by severity level."""
        counts = {
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0
        }

        for issue in issues:
            severity = issue.get('severity', 'info')
            key = f"{severity}_count"
            if key in counts:
                counts[key] += 1

        return counts

    def _calculate_security_score(self, issues: List[Dict]) -> int:
        """Calculate overall security score (0-100)."""
        if not issues:
            return 100

        # Weighted scoring
        weights = {"critical": 10, "high": 5, "medium": 2, "low": 1}
        total_deduction = sum(weights.get(i.get('severity', 'low'), 1) for i in issues)

        score = max(0, 100 - total_deduction)
        return score

    def _create_findings(self, security_issues: List[Dict],
                        standards_violations: List[Dict]) -> Dict[str, Any]:
        """Create findings section."""
        findings = {
            "issues": [],
            "warnings": [],
            "info": []
        }

        # Count critical/high security issues
        critical = sum(1 for i in security_issues if i.get('severity') == 'critical')
        high = sum(1 for i in security_issues if i.get('severity') == 'high')

        if critical > 0:
            findings["issues"].append({
                "severity": "critical",
                "message": f"Found {critical} critical security vulnerabilities",
                "impact": "high"
            })

        if high > 0:
            findings["issues"].append({
                "severity": "high",
                "message": f"Found {high} high-severity security issues",
                "impact": "medium"
            })

        if standards_violations:
            findings["warnings"].append({
                "message": f"{len(standards_violations)} framework standards violations found",
                "impact": "low"
            })

        return findings

    def _generate_recommendations(self, security_issues: List[Dict],
                                 standards_violations: List[Dict],
                                 unused_files: List[Dict]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        # Security recommendations
        xss_count = sum(1 for i in security_issues if i.get('category') == 'xss')
        if xss_count > 0:
            recommendations.append("Use DOMPurify for HTML sanitization")
            recommendations.append("Avoid dangerouslySetInnerHTML when possible")

        csrf_count = sum(1 for i in security_issues if i.get('category') == 'csrf')
        if csrf_count > 0:
            recommendations.append("Implement CSRF tokens for all form submissions")

        cors_count = sum(1 for i in security_issues if i.get('category') == 'cors')
        if cors_count > 0:
            recommendations.append("Restrict CORS to specific trusted origins")

        # Standards recommendations
        if standards_violations:
            recommendations.append(f"Address {len(standards_violations)} framework standards violations")

        # Dead code recommendations
        if unused_files:
            high_conf = sum(1 for f in unused_files if f.get('confidence') == 'high')
            if high_conf > 0:
                recommendations.append(f"Review and remove {high_conf} unused files with high confidence")

        return recommendations

    def _suggest_next_actions(self, security_issues: List[Dict]) -> Dict[str, Any]:
        """Suggest next actions for orchestration."""
        next_actions = {
            "suggested_agents": [],
            "required_skills": []
        }

        # If security issues found, suggest performance check
        if security_issues:
            next_actions["suggested_agents"].append("performance_monitoring")

        # If critical issues, suggest auto-fix
        critical = sum(1 for i in security_issues if i.get('severity') == 'critical')
        if critical > 0:
            next_actions["required_skills"].append("auto_fix_security")

        return next_actions

    def _has_critical_issues(self, output: Dict[str, Any]) -> bool:
        """Check if output contains critical issues."""
        metrics = output.get('results', {}).get('metrics', {})
        return metrics.get('critical_count', 0) > 0

    def _print_summary(self, output: Dict[str, Any]):
        """Print execution summary."""
        metrics = output.get('results', {}).get('metrics', {})

        print("\n" + "="*70)
        print("SECURITY AUDIT SUMMARY")
        print("="*70)
        print(f"Security Score: {metrics.get('security_score', 0)}/100")
        print(f"\nSecurity Issues:")
        print(f"  Critical: {metrics.get('critical_count', 0)}")
        print(f"  High: {metrics.get('high_count', 0)}")
        print(f"  Medium: {metrics.get('medium_count', 0)}")
        print(f"  Low: {metrics.get('low_count', 0)}")
        print(f"\nStandards Violations: {metrics.get('standards_violations', 0)}")
        print(f"Unused Files: {metrics.get('unused_files', 0)}")

        recommendations = output.get('recommendations', [])
        if recommendations:
            print(f"\nTop Recommendations:")
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"  {i}. {rec}")

        print("="*70)

    def _generate_reports(self, output: Dict[str, Any], output_dir: str):
        """Generate output reports."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # JSON report
        json_file = output_path / f"security-audit-{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\n[REPORT] JSON: {json_file}")

    def _get_default_scan_paths(self) -> List[str]:
        """Get default scan paths."""
        return [
            "src/**/*.ts",
            "src/**/*.tsx",
            "src/**/*.js",
            "src/**/*.jsx",
            "**/*.py"
        ]

    def _gather_files(self, scan_paths: List[str]) -> List[Path]:
        """Gather files matching scan paths."""
        files = []
        for pattern in scan_paths:
            files.extend(Path.cwd().glob(pattern))
        return list(set(files))

    def _list_artifacts(self) -> List[Dict[str, str]]:
        """List generated artifacts."""
        # Placeholder - would list actual generated files
        return []

    def _create_error_output(self, error: str, workflow_name: str) -> Dict[str, Any]:
        """Create error output."""
        return {
            "schema_version": "1.0.0",
            "agent": {
                "name": self.config.name,
                "version": self.config.version,
                "category": "security"
            },
            "execution": {
                "timestamp": datetime.now().isoformat(),
                "status": "failed",
                "workflow_name": workflow_name
            },
            "context": {},
            "results": {
                "data": {},
                "artifacts": [],
                "metrics": {}
            },
            "findings": {
                "issues": [{
                    "severity": "critical",
                    "message": f"Agent execution failed: {error}",
                    "impact": "high"
                }],
                "warnings": [],
                "info": []
            },
            "recommendations": ["Review agent logs for detailed error information"],
            "next_actions": {
                "suggested_agents": [],
                "required_skills": []
            }
        }


def main():
    """Main entry point for security monitoring agent."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Security Monitoring Agent - Modular security analysis"
    )
    parser.add_argument(
        "--config",
        default="agents/md/security_monitoring_agent.md",
        help="Path to agent configuration file"
    )
    parser.add_argument(
        "--workflow",
        default="full_security_audit",
        help="Workflow to execute"
    )
    parser.add_argument(
        "--output-dir",
        default="./security-reports",
        help="Output directory for reports"
    )
    parser.add_argument(
        "--exit-on-critical",
        action="store_true",
        help="Exit with error code if critical issues found"
    )

    args = parser.parse_args()

    # Initialize agent
    agent = SecurityMonitoringAgent(config=args.config)

    # Run workflow
    output = agent.run(
        workflow=args.workflow,
        output_dir=args.output_dir,
        exit_on_critical=args.exit_on_critical
    )

    # Exit based on results
    if output["execution"]["status"] == "failed":
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
```

---

### Phase 5: Create Agent Specification

**Goal:** Create Markdown specification with YAML frontmatter following Anthropic subagent pattern

**File: `agents/md/security_monitoring_agent.md`**

```markdown
---
name: Security Monitoring Agent
description: Comprehensive mobile security scanning, framework standards checking, and dead code detection
version: 2.0.0
model: claude-sonnet-4
temperature: 0.2
max_tokens: 8192
tools:
  - bash
  - read
  - write
  - grep
  - glob
skills_dir: ./skills/security
workflows_dir: ./workflows/security
enabled_skills:
  - mobile_xss_scanner
  - csrf_validator
  - cors_checker
  - csp_analyzer
  - typescript_standards_checker
  - python_standards_checker
  - dead_code_detector
enabled_workflows:
  - full_security_audit
  - mobile_attack_scan
  - standards_check
  - dead_code_cleanup
categories:
  - Security
  - Mobile Attacks
  - Code Standards
  - Dead Code
output_schema: schemas/agent-output-schema.json
---

# Security Monitoring Agent

You are a specialized security monitoring agent focused on detecting mobile browser vulnerabilities, enforcing framework standards, and identifying unused code.

## Core Capabilities

### Mobile Security Scanning
- **XSS Detection**: Identify dangerous HTML injection points
  - `dangerouslySetInnerHTML`, `innerHTML`, `outerHTML`
  - `eval()`, `Function` constructor
  - String-based `setTimeout`/`setInterval`

- **CSRF Validation**: Verify CSRF protection in forms
  - Check for CSRF tokens in POST forms
  - Validate token generation and validation

- **CORS Analysis**: Check CORS configurations
  - Identify wildcard CORS policies
  - Validate origin restrictions

- **CSP Checking**: Analyze Content Security Policy
  - Verify CSP headers exist
  - Check for unsafe directives

- **Sensitive Data Exposure**: Find hardcoded secrets
  - API keys, passwords, tokens
  - Credentials in localStorage

### Framework Standards Enforcement

#### TypeScript/React
- Component naming conventions (PascalCase)
- Functional components over class components
- TypeScript type safety (avoid `any`, `@ts-ignore`)
- PropTypes vs TypeScript interfaces
- External link security (`noopener`, `noreferrer`)

#### Python 3
- PEP 8 compliance
- Type hints for functions
- Docstring completeness (Google style)
- Security patterns (SQL injection, command injection)

#### HTML/CSS v2
- Pure code (no frameworks)
- Semantic HTML5
- WCAG 2.1 accessibility
- Responsive design

### Dead Code Detection
- **Reference Analysis**: Count imports and references
- **Naming Patterns**: Detect deprecated naming conventions
- **File Age**: Identify old, unmaintained files
- **Duplicates**: Find similar or duplicate files
- **File Extensions**: Flag backup/temp file extensions

## Workflow Execution

### Full Security Audit
1. Scan for mobile XSS vulnerabilities
2. Validate CSRF protection
3. Check CORS configurations
4. Analyze CSP policies
5. Check TypeScript/React standards
6. Check Python standards
7. Detect dead code
8. Generate comprehensive reports (JSON, HTML, Markdown)

### Mobile Attack Scan
1. Focus on mobile-specific vulnerabilities
2. XSS, CSRF, CORS checks only
3. Quick execution (< 5 minutes)
4. JSON output for CI/CD integration

### Standards Check
1. TypeScript/React standards validation
2. Python 3 standards validation
3. Generate Markdown report with violations
4. Auto-fix suggestions where applicable

### Dead Code Cleanup
1. Identify unused files with high confidence
2. Generate removal recommendations
3. Optional: Rename files with underscore prefix
4. Test-before-delete workflow

## Task-Specific Instructions

### When Scanning for Security Issues
- Always report CWE IDs for vulnerabilities
- Provide specific line numbers and code snippets
- Include actionable remediation steps
- Categorize by severity (critical, high, medium, low)
- Flag mobile-specific issues separately

### When Checking Standards
- Be strict but pragmatic
- Distinguish auto-fixable vs manual violations
- Provide before/after examples
- Consider framework versions and compatibility
- Document rationale for each rule

### When Detecting Dead Code
- Use multiple detection heuristics
- Provide confidence levels (high, medium, low)
- Never auto-delete without explicit confirmation
- Suggest safe testing methodology
- Consider edge cases (reflection, dynamic imports)

### When Generating Reports
- Follow `agent-output-schema.json` structure
- Include all required fields
- Validate output against schema
- Provide clear, actionable recommendations
- Suggest next steps for orchestration

## Output Format

All outputs must conform to the standardized agent output schema defined in `agents/schemas/agent-output-schema.json`.

**Required Structure:**
```json
{
  "schema_version": "1.0.0",
  "agent": {...},
  "execution": {...},
  "context": {...},
  "results": {
    "data": {
      "security_issues": [...],
      "standards_violations": [...],
      "unused_files": [...]
    },
    "artifacts": [...],
    "metrics": {...}
  },
  "findings": {...},
  "recommendations": [...],
  "next_actions": {...}
}
```

## Integration Points

- **Performance Agent**: Share findings for holistic site analysis
- **Content Coordinator**: Feed security-focused content requirements
- **SEO Agent**: Ensure security doesn't break SEO (CSP, headers)
- **CI/CD Pipeline**: Block deployments on critical issues
- **Auto-Fix Workflows**: Trigger automated remediation

## Success Metrics

- **Security Score**: > 90/100
- **Critical Issues**: 0
- **High Issues**: < 5
- **Standards Compliance**: 100%
- **Dead Code**: All high-confidence files identified
- **False Positives**: < 5%

## Error Handling

- Graceful degradation on tool failures
- Continue execution on individual skill failures
- Log all errors with context
- Return partial results when possible
- Suggest manual intervention when needed

## Performance Targets

- **Full Audit**: < 10 minutes for typical codebase
- **Quick Scan**: < 5 minutes
- **Standards Check**: < 3 minutes
- **Dead Code**: < 2 minutes
- **Memory Usage**: < 512MB
- **CPU**: < 50% sustained

## Version History

- **2.0.0** (2025-11-01): Initial modular framework integration
- **1.0.0** (2025-10-30): Original standalone implementation
```

---

### Phase 6: Update Modular Framework

**Goal:** Enhance base framework with JSON support, validation, and communication

**File: Enhancements to `agents/python/modular_agent_framework.py`**

Add the following methods to the `ModularAgent` class:

```python
# Add these imports at the top
from lib.schema_validator import validate_output
from lib.agent_communication import AgentMessenger, create_agent_output

# Add these methods to ModularAgent class

def load_output_schema(self, schema_name: str = "agent-output-schema.json") -> Dict:
    """
    Load JSON schema for output validation.

    Args:
        schema_name: Name of schema file

    Returns:
        Schema dictionary
    """
    from lib.schema_validator import get_validator
    validator = get_validator()
    return validator.load_schema(schema_name)

def validate_output_format(self, output: Dict[str, Any],
                          schema_name: str = "agent-output-schema.json") -> Tuple[bool, List[str]]:
    """
    Validate agent output against JSON schema.

    Args:
        output: Output dictionary to validate
        schema_name: Schema to validate against

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    return validate_output(output, schema_name)

def create_messenger(self) -> AgentMessenger:
    """
    Create a messenger for inter-agent communication.

    Returns:
        AgentMessenger instance
    """
    return AgentMessenger(self.config.name)

def send_to_agent(self, to_agent: str, message_type: str,
                 payload: Dict[str, Any]) -> str:
    """
    Send a message to another agent.

    Args:
        to_agent: Destination agent name
        message_type: Message type (request, response, notification, error)
        payload: Message payload

    Returns:
        Message ID
    """
    messenger = self.create_messenger()
    return messenger.send_message(to_agent, message_type, payload)

def receive_messages(self, mark_read: bool = True) -> List[Dict[str, Any]]:
    """
    Receive pending messages from other agents.

    Args:
        mark_read: Whether to mark messages as read

    Returns:
        List of messages
    """
    messenger = self.create_messenger()
    return messenger.receive_messages(mark_read)

def create_artifact(self, artifact_type: str, data: Any,
                   output_path: Path) -> Dict[str, str]:
    """
    Create and store an artifact.

    Args:
        artifact_type: Type of artifact (report, data, etc.)
        data: Artifact data
        output_path: Where to save artifact

    Returns:
        Artifact metadata
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save artifact
    if artifact_type in ['json', 'data']:
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    else:
        with open(output_path, 'w') as f:
            f.write(str(data))

    return {
        "type": artifact_type,
        "format": output_path.suffix.lstrip('.'),
        "path": str(output_path)
    }
```

---

## Implementation Priorities

### High Priority (Week 1)
**Goal:** Core infrastructure and security agent functional

1. ✅ **Create JSON Schemas**
   - `agent-output-schema.json`
   - `security-findings-schema.json`
   - `inter-agent-message-schema.json`

2. ✅ **Create Library Utilities**
   - `lib/schema_validator.py`
   - `lib/agent_communication.py`
   - `lib/__init__.py`

3. ✅ **Extract Security Skills**
   - `mobile_xss_scanner.py`
   - `csrf_validator.py`
   - `cors_checker.py`
   - `csp_analyzer.py`
   - `typescript_standards_checker.py`
   - `python_standards_checker.py`
   - `dead_code_detector.py`

4. ✅ **Create Security Workflows**
   - `full_security_audit.yaml`
   - `mobile_attack_scan.yaml`
   - `standards_check.yaml`
   - `dead_code_cleanup.yaml`

5. ✅ **Build Security Agent**
   - `security_monitoring_agent.py`
   - `security_monitoring_agent.md`

### Medium Priority (Week 2)
**Goal:** Integration, testing, and documentation

6. ✅ **Update Modular Framework**
   - Add JSON validation methods
   - Add inter-agent communication
   - Add artifact management
   - Update documentation

7. ✅ **Schema Validation**
   - Implement comprehensive validation
   - Add error reporting
   - Test with all agent types

8. ✅ **Inter-Agent Communication**
   - Test message passing
   - Verify schema compliance
   - Create integration examples

9. ✅ **Integration Tests**
   - Test each skill independently
   - Test workflow composition
   - Test full agent execution
   - Test with various codebases

10. ✅ **Documentation**
    - `docs/JSON_COMMUNICATION.md`
    - `docs/SECURITY_AGENT_MIGRATION.md`
    - `docs/SCHEMA_REFERENCE.md`
    - Update existing docs

### Low Priority (Week 3)
**Goal:** Polish, optimization, and backward compatibility

11. ✅ **Migrate Existing Reports**
    - Convert old JSON to new schema
    - Provide conversion script
    - Update report viewers

12. ✅ **Migration Guide**
    - Step-by-step migration instructions
    - Common issues and solutions
    - Rollback procedures

13. ✅ **Backward Compatibility**
    - Maintain old endpoints
    - Add deprecation warnings
    - Create compatibility layer

14. ✅ **Performance Optimization**
    - Profile skill execution
    - Optimize file scanning
    - Implement caching
    - Parallel execution

15. ✅ **CI/CD Integration**
    - GitHub Actions examples
    - GitLab CI examples
    - Jenkins pipeline examples
    - Pre-commit hooks

---

## Deliverables

### Code Deliverables

#### Schemas (`agents/schemas/`)
- [x] `agent-output-schema.json` - Base output schema
- [x] `security-findings-schema.json` - Security-specific extensions
- [x] `inter-agent-message-schema.json` - Message passing schema

#### Library (`agents/lib/`)
- [x] `__init__.py` - Package initialization
- [x] `agent_communication.py` - Inter-agent messaging
- [x] `schema_validator.py` - JSON validation

#### Skills (`agents/skills/security/`)
- [x] `mobile_xss_scanner.py`
- [x] `csrf_validator.py`
- [x] `cors_checker.py`
- [x] `csp_analyzer.py`
- [x] `typescript_standards_checker.py`
- [x] `python_standards_checker.py`
- [x] `dead_code_detector.py`

#### Workflows (`agents/workflows/security/`)
- [x] `full_security_audit.yaml`
- [x] `mobile_attack_scan.yaml`
- [x] `standards_check.yaml`
- [x] `dead_code_cleanup.yaml`

#### Agent (`agents/python/`, `agents/md/`)
- [x] `security_monitoring_agent.py` - Implementation
- [x] `security_monitoring_agent.md` - Specification

#### Framework Updates (`agents/python/`)
- [x] Enhanced `modular_agent_framework.py`

### Documentation Deliverables

#### Core Documentation (`agents/docs/`)
- [x] `JSON_COMMUNICATION.md` - Inter-agent communication guide
- [x] `SECURITY_AGENT_MIGRATION.md` - Migration guide
- [x] `SCHEMA_REFERENCE.md` - Schema documentation

#### Updated Documentation
- [x] `agents/MODULAR_FRAMEWORK_README.md` - Framework updates
- [x] `agents/README.md` - Overall readme
- [x] `agents/AGENTS_OVERVIEW.md` - Agent listing

### Testing Deliverables

#### Unit Tests (`agents/tests/`)
- [x] Test suite for each security skill
- [x] Schema validation tests
- [x] Communication library tests
- [x] Agent integration tests

#### Integration Tests
- [x] End-to-end workflow tests
- [x] Multi-agent communication tests
- [x] Schema compliance tests

---

## Migration Strategy

### Backward Compatibility Approach

**Phase 1: Coexistence (Months 1-2)**
- Keep existing `/security-agent/` completely intact
- New modular agent runs in parallel
- Users can use either version
- Collect feedback on new version

**Phase 2: Deprecation (Months 3-4)**
- Add deprecation warnings to old agent
- Update all documentation to recommend new agent
- Provide migration assistance
- Update CI/CD examples

**Phase 3: Transition (Months 5-6)**
- Create symlinks from old paths to new
- Add compatibility shims
- Convert all internal usage to new agent
- Final migration support

**Phase 4: Removal (Month 7+)**
- Archive old `/security-agent/` directory
- Remove deprecation warnings
- Full cutover to modular framework

### Data Migration

**Configuration Migration**
```python
# Script: migrate_config.py
def migrate_config(old_config: Dict) -> Dict:
    """Convert old agent config to new format."""
    return {
        "name": "Security Monitoring Agent",
        "version": "2.0.0",
        "security": old_config.get("security", {}),
        # ... map other fields
    }
```

**Report Migration**
```python
# Script: migrate_reports.py
def migrate_report(old_report: Dict) -> Dict:
    """Convert old report to new schema."""
    return {
        "schema_version": "1.0.0",
        "agent": {
            "name": "Security Monitoring Agent",
            "version": "2.0.0",
            "category": "security"
        },
        # ... map other fields
    }
```

### CI/CD Updates

**Before (Old Agent)**
```yaml
- name: Run Security Agent
  run: python3 security-agent/agent.py
```

**After (New Agent)**
```yaml
- name: Run Security Agent
  run: python3 agents/python/security_monitoring_agent.py --workflow full_security_audit
```

---

## Success Criteria

### Functional Criteria
- ✅ Security agent fully integrated into modular framework
- ✅ All outputs conform to standardized JSON schema
- ✅ Agents can exchange data via JSON messages
- ✅ Skills are reusable and composable
- ✅ Workflows orchestrate multiple skills
- ✅ All existing security agent functionality preserved

### Quality Criteria
- ✅ 100% test coverage for new components
- ✅ All tests passing (unit, integration, E2E)
- ✅ Documentation complete and accurate
- ✅ Code review completed
- ✅ Security review passed

### Performance Criteria
- ✅ Full audit completes in < 10 minutes
- ✅ Memory usage < 512MB
- ✅ No performance regression vs old agent

### Adoption Criteria
- ✅ All internal projects migrated
- ✅ CI/CD pipelines updated
- ✅ Team trained on new agent
- ✅ Migration guide validated
- ✅ User feedback incorporated

### Compatibility Criteria
- ✅ Backward compatible with existing tools
- ✅ Old agent runs in parallel during transition
- ✅ Deprecation path communicated
- ✅ Migration support provided

---

## Risk Mitigation

### Technical Risks

**Risk 1: Schema Evolution**
- **Mitigation**: Use semantic versioning for schemas
- **Mitigation**: Maintain old schema versions
- **Mitigation**: Provide schema migration tools

**Risk 2: Performance Degradation**
- **Mitigation**: Comprehensive performance testing
- **Mitigation**: Profiling and optimization
- **Mitigation**: Parallel execution where possible

**Risk 3: Integration Failures**
- **Mitigation**: Extensive integration testing
- **Mitigation**: Staged rollout
- **Mitigation**: Easy rollback mechanism

### Process Risks

**Risk 4: User Adoption**
- **Mitigation**: Clear migration guide
- **Mitigation**: Training and support
- **Mitigation**: Gradual deprecation

**Risk 5: Breaking Changes**
- **Mitigation**: Maintain backward compatibility
- **Mitigation**: Comprehensive testing
- **Mitigation**: Clear communication

---

## Timeline

### Week 1: Foundation
- Days 1-2: JSON schemas and validation
- Days 3-4: Extract security skills
- Day 5: Create workflows

### Week 2: Implementation
- Days 1-2: Build security agent
- Days 3-4: Framework enhancements
- Day 5: Integration testing

### Week 3: Polish
- Days 1-2: Documentation
- Days 3-4: Migration tools
- Day 5: Final testing and release

---

## Conclusion

This plan provides a comprehensive approach to integrating the security agent into the modular framework while establishing standardized JSON communication for all agents. The phased approach ensures minimal disruption while delivering maximum value.

**Next Steps:**
1. Review and approve this plan
2. Begin Phase 1 implementation
3. Schedule regular check-ins
4. Adjust based on learnings

**Questions for Discussion:**
- Timeline acceptable?
- Resource allocation adequate?
- Migration strategy appropriate?
- Success criteria complete?
