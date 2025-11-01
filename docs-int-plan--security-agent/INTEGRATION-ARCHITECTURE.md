# Integration Architecture

**Date:** November 1, 2025
**Version:** 1.0.0

---

## Overview

This document defines the architecture for integrating the security agent into the modular framework, including directory structure, component responsibilities, and design patterns.

---

## New Directory Structure

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

---

## Component Responsibilities

### 1. Schemas (`agents/schemas/`)

**Purpose**: Define standard output formats for all agents

**Files**:
- `agent-output-schema.json` - Base schema for all agents
- `security-findings-schema.json` - Security-specific extensions
- `inter-agent-message-schema.json` - Agent-to-agent messages

**Responsibilities**:
- Define data structures
- Enable validation and type safety
- Support versioning and evolution
- Provide documentation through JSON Schema

**Design Principles**:
- Use JSON Schema Draft 7
- Semantic versioning for schemas
- Required vs optional fields clearly defined
- Comprehensive descriptions

---

### 2. Library (`agents/lib/`)

**Purpose**: Shared utilities for all agents

#### `__init__.py`
Package initialization and exports.

```python
"""
Agents Library
==============

Shared utilities for modular agents.
"""

from .agent_communication import AgentMessenger, create_agent_output
from .schema_validator import SchemaValidator, validate_output

__all__ = [
    'AgentMessenger',
    'create_agent_output',
    'SchemaValidator',
    'validate_output'
]

__version__ = '1.0.0'
```

#### `agent_communication.py`
**Responsibilities**:
- Inter-agent message passing
- Message queue management
- Request/response correlation
- Helper functions for standardized outputs

**Key Classes**:
- `AgentMessenger`: Handle message sending/receiving
- Helper functions: `create_agent_output()`

**Design Patterns**:
- File-based message queue (simple, reliable)
- Inbox/outbox pattern
- Automatic message validation

#### `schema_validator.py`
**Responsibilities**:
- Validate outputs against JSON schemas
- Load and cache schemas
- Format validation errors
- Version compatibility checking

**Key Classes**:
- `SchemaValidator`: Main validation class
- Helper functions: `validate_output()`, `get_validator()`

**Design Patterns**:
- Singleton pattern for global validator
- Schema caching for performance
- Clear error messages

---

### 3. Skills (`agents/skills/security/`)

**Purpose**: Modular, reusable security functions

#### Skill Pattern

Every skill follows this pattern:

```python
#!/usr/bin/env python3
"""
Skill Name
==========

Description of what this skill does.
"""

from typing import Dict, Any

def skill_function(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute the skill.

    Args:
        context: Input context with required data

    Returns:
        Result dictionary
    """
    # Skill implementation
    pass

# Skill registration for framework
SKILLS = [{
    'name': 'skill_name',
    'description': 'What the skill does',
    'category': 'security',
    'function': skill_function,
    'required_tools': ['read', 'grep'],
    'config': {...},
    'enabled': True
}]
```

#### Security Skills

**1. mobile_xss_scanner.py**
- Detects XSS vulnerabilities
- Patterns: dangerouslySetInnerHTML, eval, innerHTML, etc.
- Returns list of XSS issues with severity

**2. csrf_validator.py**
- Validates CSRF protection in forms
- Checks for CSRF tokens
- Verifies token implementation

**3. cors_checker.py**
- Analyzes CORS configurations
- Identifies wildcard policies
- Validates origin restrictions

**4. csp_analyzer.py**
- Checks Content Security Policy
- Validates CSP headers
- Identifies unsafe directives

**5. typescript_standards_checker.py**
- TypeScript/React standards validation
- Component naming conventions
- Type safety checks

**6. python_standards_checker.py**
- Python 3 standards validation
- PEP 8 compliance
- Type hints and docstrings

**7. dead_code_detector.py**
- Identifies unused files
- Reference counting
- Confidence scoring

**Design Principles**:
- Single responsibility per skill
- Testable in isolation
- Clear input/output contracts
- Comprehensive error handling

---

### 4. Workflows (`agents/workflows/security/`)

**Purpose**: Compose skills into complete audits

#### Workflow Pattern

```yaml
name: workflow_name
description: What this workflow does
skills:
  - skill_1
  - skill_2
  - skill_3
config:
  timeout: 300
  generate_report: true
  report_formats: ["json", "html"]
```

#### Security Workflows

**1. full_security_audit.yaml**
- Complete security and standards audit
- All skills executed sequentially
- Comprehensive reporting

**2. mobile_attack_scan.yaml**
- Mobile-specific vulnerability scanning
- XSS, CSRF, CORS checks only
- Quick execution for CI/CD

**3. standards_check.yaml**
- Framework standards validation only
- TypeScript + Python standards
- Markdown report output

**4. dead_code_cleanup.yaml**
- Unused code identification
- High-confidence files only
- Cleanup recommendations

**Design Principles**:
- Workflow = skill composition
- Configurable execution
- Different audit types for different needs
- Clear execution order

---

### 5. Agent Implementation (`agents/python/security_monitoring_agent.py`)

**Purpose**: Security monitoring agent implementation

**Class Structure**:
```python
class SecurityMonitoringAgent(ModularAgent):
    """Security monitoring with mobile attack detection."""

    def _register_core_skills(self):
        """Register built-in skills."""
        pass

    def run(self, **kwargs) -> Dict[str, Any]:
        """Run audit and return standardized JSON."""
        pass

    def _to_standard_output(self, result, workflow, duration, context):
        """Convert to standard format."""
        pass

    # Helper methods...
```

**Responsibilities**:
- Extend ModularAgent base class
- Register core skills
- Execute workflows
- Convert outputs to standard JSON format
- Validate against schemas
- Generate reports
- Handle errors gracefully

**Integration Points**:
- Loads skills from `skills/security/`
- Loads workflows from `workflows/security/`
- Uses schemas from `schemas/`
- Uses library utilities from `lib/`

---

### 6. Agent Specification (`agents/md/security_monitoring_agent.md`)

**Purpose**: Agent specification following Anthropic subagent pattern

**Structure**:
```markdown
---
name: Security Monitoring Agent
description: ...
version: 2.0.0
model: claude-sonnet-4
tools: [bash, read, write, grep, glob]
skills_dir: ./skills/security
workflows_dir: ./workflows/security
enabled_skills: [...]
enabled_workflows: [...]
output_schema: schemas/agent-output-schema.json
---

# System Prompt

Natural language instructions for the agent...
```

**Responsibilities**:
- Define agent configuration (YAML frontmatter)
- Provide natural language system prompt
- Specify tool requirements
- Document capabilities
- Define integration points
- Set success metrics

**Design Principles**:
- Human-readable
- Version controlled
- Self-documenting
- Anthropic-compatible

---

## Data Flow Architecture

### Skill Execution Flow

```
┌─────────────────┐
│ Agent.run()     │
└────────┬────────┘
         │
         v
┌─────────────────────┐
│ Load Workflow       │
│ (YAML)              │
└──────────┬──────────┘
           │
           v
┌───────────────────────┐
│ For each skill in     │
│ workflow:             │
│                       │
│  1. Load skill        │
│  2. Execute function  │
│  3. Collect results   │
│  4. Merge into context│
└──────────┬────────────┘
           │
           v
┌──────────────────────┐
│ Aggregate Results    │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│ Convert to Standard  │
│ JSON Output          │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│ Validate Against     │
│ Schema               │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│ Generate Reports     │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│ Return Output        │
└────────────────────────┘
```

### Inter-Agent Communication Flow

```
┌─────────────────┐
│ Agent A         │
│                 │
│  send_message() │
└────────┬────────┘
         │
         v
┌─────────────────────┐
│ Write to:           │
│ - Agent A outbox    │
│ - Agent B inbox     │
└──────────┬──────────┘
           │
           v
┌──────────────────────┐
│ Agent B              │
│                      │
│  receive_messages()  │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│ Process Message      │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│ Agent B              │
│                      │
│  send_response()     │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│ Write to:            │
│ - Agent B outbox     │
│ - Agent A inbox      │
└──────────────────────┘
```

---

## Design Patterns

### 1. Strategy Pattern (Skills)
- Each skill is a strategy
- Skills are interchangeable
- Workflow selects strategies to execute

### 2. Template Method Pattern (ModularAgent)
- Base class defines skeleton
- Subclasses implement specific steps
- Consistent execution flow

### 3. Builder Pattern (Output Creation)
- `create_agent_output()` helper
- Incremental output construction
- Final validation before return

### 4. Observer Pattern (Message Passing)
- Agents observe inbox for messages
- React to messages asynchronously
- Loose coupling between agents

### 5. Factory Pattern (Skill Loading)
- Skills registered via SKILLS list
- Framework dynamically loads skills
- Easy to add new skills

---

## Technology Stack

### Python
- **Version**: 3.8+
- **Type Hints**: Used throughout
- **Async**: Not required (file-based messaging)

### JSON Schema
- **Version**: Draft 7
- **Library**: `jsonschema`
- **Validation**: Runtime validation

### YAML
- **Library**: `PyYAML`
- **Usage**: Workflow definitions, frontmatter

### File System
- **Message Queue**: File-based
- **Reports**: Generated files
- **Schemas**: JSON files

---

## Scalability Considerations

### Performance
- **Skill Parallelization**: Future enhancement
- **Caching**: Schema caching implemented
- **Lazy Loading**: Skills loaded on-demand

### Extensibility
- **New Skills**: Drop-in Python files
- **New Workflows**: Drop-in YAML files
- **New Agents**: Extend ModularAgent
- **Schema Evolution**: Versioned schemas

### Reliability
- **Error Isolation**: Skill failures don't stop workflow
- **Validation**: JSON schema enforcement
- **Logging**: Comprehensive error logging
- **Rollback**: Keep old agent during transition

---

## Security Considerations

### Code Security
- **Input Validation**: All context validated
- **Path Traversal**: Prevented in file operations
- **Code Injection**: No eval or exec used
- **Dependency Security**: Minimal dependencies

### Data Security
- **Sensitive Data**: Not logged or stored
- **Message Privacy**: File permissions enforced
- **Report Security**: Configurable output directories

### Access Control
- **File Permissions**: Inbox/outbox restricted
- **Schema Validation**: Prevents malformed data
- **Tool Restrictions**: Agents declare required tools

---

## Testing Strategy

### Unit Tests
- Each skill tested independently
- Schema validation tests
- Communication library tests

### Integration Tests
- Workflow execution tests
- Agent-to-agent communication tests
- End-to-end audit tests

### Validation Tests
- Schema compliance tests
- Output format tests
- Error handling tests

---

## Migration Path

### Phase 1: New System
- Build new modular structure
- Parallel to old system
- No disruption to existing users

### Phase 2: Gradual Migration
- Update documentation
- Provide migration tools
- Support both systems

### Phase 3: Deprecation
- Deprecate old system
- Add warnings
- Final migration window

### Phase 4: Removal
- Archive old system
- Full cutover
- Clean up

---

## Future Enhancements

### Short Term
- Parallel skill execution
- Skill dependency resolution
- Enhanced error recovery
- Performance profiling

### Medium Term
- Web UI for report viewing
- Real-time monitoring dashboard
- Skill marketplace
- Plugin system

### Long Term
- Machine learning for pattern detection
- Auto-fix capabilities
- Predictive analysis
- Cloud-native deployment

---

## References

- **Anthropic Best Practices**: Building Effective Agents
- **JSON Schema**: http://json-schema.org/
- **YAML Specification**: https://yaml.org/
- **Python Type Hints**: PEP 484, 585
