# Proposed JSON Communication Structure

**Date:** November 1, 2025
**Version:** 1.0.0

---

## Overview

This document defines the standardized JSON communication structure for all agents in the modular framework, based on Anthropic's best practices and JSON-RPC 2.0 patterns.

---

## Design Principles

1. **Standardization**: All agents produce consistent output format
2. **Extensibility**: Schema supports agent-specific extensions
3. **Versioning**: Schema version tracking for evolution
4. **Validation**: JSON Schema Draft 7 for type safety
5. **Interoperability**: Agents can consume each other's outputs

---

## Base Agent Output Schema

### Schema File
`agents/schemas/agent-output-schema.json`

### Schema Definition

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

---

## Security Agent Output Example

### Complete Security Audit Output

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
          "reason": "No imports or references found in codebase",
          "confidence": "high",
          "last_modified": "2025-09-15T08:22:00Z",
          "file_size": 1024,
          "references_found": 0,
          "suggested_action": "Rename with underscore prefix to verify"
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

---

## Inter-Agent Message Schema

### Schema File
`agents/schemas/inter-agent-message-schema.json`

### Purpose
Enables agents to send requests, responses, and notifications to each other.

### Schema Definition

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
      "description": "Unique message identifier (UUID)"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO-8601 timestamp"
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

### Message Types

#### Request
Agent A requests information or action from Agent B.

```json
{
  "message_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-11-01T10:30:00Z",
  "from_agent": "Security Monitoring Agent",
  "to_agent": "Performance Monitoring Agent",
  "message_type": "request",
  "payload": {
    "action": "audit",
    "url": "https://example.com",
    "focus_areas": ["security_headers", "ssl_config"]
  }
}
```

#### Response
Agent B responds to Agent A's request.

```json
{
  "message_id": "660f9511-f30c-52e5-b827-557766551111",
  "timestamp": "2025-11-01T10:35:00Z",
  "from_agent": "Performance Monitoring Agent",
  "to_agent": "Security Monitoring Agent",
  "message_type": "response",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "payload": {
    "security_headers": {
      "HSTS": true,
      "CSP": false,
      "X-Frame-Options": true
    },
    "ssl_grade": "A+"
  }
}
```

#### Notification
Agent broadcasts information without expecting a response.

```json
{
  "message_id": "770g0622-g41d-63f6-c938-668877662222",
  "timestamp": "2025-11-01T10:40:00Z",
  "from_agent": "Security Monitoring Agent",
  "to_agent": "Content Coordinator Agent",
  "message_type": "notification",
  "payload": {
    "event": "critical_issues_found",
    "count": 2,
    "categories": ["xss", "csrf"]
  }
}
```

#### Error
Agent reports an error condition.

```json
{
  "message_id": "880h1733-h52e-74g7-d049-779988773333",
  "timestamp": "2025-11-01T10:45:00Z",
  "from_agent": "Security Monitoring Agent",
  "to_agent": "Performance Monitoring Agent",
  "message_type": "error",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "payload": {
    "error_code": "TIMEOUT",
    "error_message": "Request timed out after 30 seconds",
    "details": {}
  }
}
```

---

## Security-Specific Schema Extensions

### Schema File
`agents/schemas/security-findings-schema.json`

### Purpose
Extends base schema with security-specific data structures.

### Security Issue Object

```json
{
  "id": "string (unique identifier)",
  "category": "string (xss, csrf, cors, etc.)",
  "severity": "critical | high | medium | low | info",
  "file_path": "string (relative file path)",
  "line_number": "integer",
  "code_snippet": "string (code at issue location)",
  "description": "string (human-readable description)",
  "recommendation": "string (remediation steps)",
  "cwe_id": "string (CWE identifier, optional)",
  "mobile_specific": "boolean",
  "auto_fixable": "boolean (optional)"
}
```

### Standards Violation Object

```json
{
  "framework": "string (TypeScript/React, Python 3, etc.)",
  "rule": "string (rule description)",
  "file_path": "string",
  "line_number": "integer",
  "code_snippet": "string",
  "expected": "string (what should be)",
  "actual": "string (what is found)",
  "auto_fixable": "boolean"
}
```

### Unused File Object

```json
{
  "file_path": "string",
  "reason": "string (why considered unused)",
  "confidence": "high | medium | low",
  "last_modified": "string (ISO-8601 date)",
  "file_size": "integer (bytes)",
  "references_found": "integer",
  "suggested_action": "string"
}
```

---

## Usage Examples

### Creating Standardized Output

```python
from lib.agent_communication import create_agent_output

output = create_agent_output(
    agent_name="Security Monitoring Agent",
    agent_version="2.0.0",
    category="security",
    results={
        "data": {
            "security_issues": [...],
            "standards_violations": [...],
            "unused_files": [...]
        },
        "artifacts": [...],
        "metrics": {...}
    },
    execution_time_ms=45000,
    workflow_name="full_security_audit"
)
```

### Validating Output

```python
from lib.schema_validator import validate_output

is_valid, errors = validate_output(
    output=agent_output,
    schema_name="agent-output-schema.json"
)

if not is_valid:
    print(f"Validation errors: {errors}")
```

### Sending Inter-Agent Message

```python
from lib.agent_communication import AgentMessenger

messenger = AgentMessenger("Security Monitoring Agent")

message_id = messenger.send_message(
    to_agent="Performance Monitoring Agent",
    message_type="request",
    payload={
        "action": "check_security_headers",
        "url": "https://example.com"
    }
)
```

### Receiving Messages

```python
messenger = AgentMessenger("Security Monitoring Agent")
messages = messenger.receive_messages(mark_read=True)

for message in messages:
    if message["message_type"] == "request":
        # Handle request
        response_payload = handle_request(message["payload"])

        # Send response
        messenger.send_response(message, response_payload)
```

---

## Schema Versioning

### Version Format
Semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes to schema structure
- **MINOR**: Backward-compatible additions
- **PATCH**: Bug fixes and clarifications

### Version Evolution

**1.0.0** (Current)
- Initial standardized schema
- Core fields defined
- Security agent support

**1.1.0** (Future - Backward Compatible)
- Add optional fields
- Add new agent categories
- Enhance artifact metadata

**2.0.0** (Future - Breaking Change)
- Restructure results format
- Change required fields
- Modify validation rules

### Compatibility

Agents MUST:
- Include `schema_version` field
- Validate against specified schema version
- Handle unknown fields gracefully
- Support at least N-1 schema versions

---

## Benefits of Standardized Communication

### For Agents
- Clear contract for outputs
- Type safety through validation
- Easy to consume other agents' outputs
- Consistent error handling

### For Orchestration
- Predictable data formats
- Easy to chain agents
- Automated workflow composition
- Central monitoring and logging

### For Developers
- Clear documentation
- IDE autocomplete support
- Easier testing
- Reduced integration bugs

### For Users
- Consistent experience
- Comparable metrics across agents
- Unified reporting
- Easier debugging

---

## References

- **JSON Schema Draft 7**: https://json-schema.org/draft-07/schema
- **JSON-RPC 2.0**: https://www.jsonrpc.org/specification
- **Anthropic MCP**: Model Context Protocol documentation
- **ISO 8601**: Date and time format standard
