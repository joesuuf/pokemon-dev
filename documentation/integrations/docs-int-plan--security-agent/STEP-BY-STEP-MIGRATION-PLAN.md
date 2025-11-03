# Step-by-Step Migration Plan

**Date:** November 1, 2025
**Version:** 1.0.0

---

## Overview

This document provides a detailed, phased approach to migrating the security agent into the modular framework. Each phase includes specific tasks, deliverables, and success criteria.

---

## Phase 1: Create JSON Communication Infrastructure

**Duration**: 2-3 days
**Priority**: High
**Goal**: Establish standardized JSON schemas and validation infrastructure

### Tasks

#### Task 1.1: Create JSON Schemas

**Files to Create**:
1. `agents/schemas/agent-output-schema.json`
2. `agents/schemas/security-findings-schema.json`
3. `agents/schemas/inter-agent-message-schema.json`

**Implementation**:
- Use JSON Schema Draft 7
- Include comprehensive descriptions
- Define required vs optional fields
- Add examples in descriptions

**Testing**:
```bash
# Validate schemas are valid JSON Schema
python -c "import json; json.load(open('agents/schemas/agent-output-schema.json'))"
```

#### Task 1.2: Create Schema Validator

**File**: `agents/lib/schema_validator.py`

**Key Features**:
- Load and cache schemas
- Validate dictionaries against schemas
- Format error messages
- Version checking

**Implementation Checklist**:
- [ ] `SchemaValidator` class
- [ ] `load_schema()` method
- [ ] `validate_output()` method
- [ ] `_format_error()` helper
- [ ] Global `get_validator()` function

**Testing**:
```python
# Test valid output
from lib.schema_validator import validate_output

valid_output = {
    "schema_version": "1.0.0",
    "agent": {...},
    "execution": {...},
    "results": {...}
}

is_valid, errors = validate_output(valid_output)
assert is_valid == True

# Test invalid output
invalid_output = {"invalid": "data"}
is_valid, errors = validate_output(invalid_output)
assert is_valid == False
assert len(errors) > 0
```

#### Task 1.3: Create Communication Library

**File**: `agents/lib/agent_communication.py`

**Key Features**:
- `AgentMessenger` class for message passing
- File-based inbox/outbox
- Message validation
- Request/response correlation
- Helper function `create_agent_output()`

**Implementation Checklist**:
- [ ] `AgentMessenger.__init__()`
- [ ] `send_message()` method
- [ ] `receive_messages()` method
- [ ] `send_response()` method
- [ ] `create_agent_output()` helper function

**Testing**:
```python
# Test message sending
from lib.agent_communication import AgentMessenger

messenger_a = AgentMessenger("Agent A")
messenger_b = AgentMessenger("Agent B")

# Send message
msg_id = messenger_a.send_message(
    to_agent="Agent B",
    message_type="request",
    payload={"test": "data"}
)

# Receive message
messages = messenger_b.receive_messages()
assert len(messages) == 1
assert messages[0]["from_agent"] == "Agent A"
```

#### Task 1.4: Create Library Package

**File**: `agents/lib/__init__.py`

**Content**:
```python
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

### Success Criteria

- [ ] All schema files created and valid
- [ ] Schema validator working with test cases
- [ ] Communication library functional
- [ ] Unit tests passing (>90% coverage)
- [ ] Documentation complete

### Deliverables

1. `agents/schemas/` - All schema files
2. `agents/lib/schema_validator.py`
3. `agents/lib/agent_communication.py`
4. `agents/lib/__init__.py`
5. Unit tests for library
6. Documentation

---

## Phase 2: Extract Security Agent Skills

**Duration**: 3-4 days
**Priority**: High
**Goal**: Break down monolithic security agent into modular, reusable skills

### Tasks

#### Task 2.1: Mobile XSS Scanner Skill

**File**: `agents/skills/security/mobile_xss_scanner.py`

**Extract From**: `security-agent/agent.py` - `MobileSecurityScanner` class

**Key Code to Extract**:
- XSS_PATTERNS list
- Pattern matching logic
- Issue creation logic

**Implementation**:
```python
def scan_mobile_xss(context: Dict[str, Any]) -> Dict[str, Any]:
    files = context.get('files', [])
    # ... scanning logic ...
    return {
        "xss_issues": issues,
        "files_scanned": len(files),
        "vulnerabilities_found": len(issues)
    }

SKILLS = [{
    'name': 'mobile_xss_scanner',
    'description': 'Detect mobile browser XSS vulnerabilities',
    'category': 'security',
    'function': scan_mobile_xss,
    'required_tools': ['read', 'grep'],
    'config': {...},
    'enabled': True
}]
```

**Testing**:
```python
# Test with sample file
context = {
    'files': [Path('test_file.tsx')],
    'config': {}
}

result = scan_mobile_xss(context)
assert 'xss_issues' in result
assert isinstance(result['xss_issues'], list)
```

#### Task 2.2: CSRF Validator Skill

**File**: `agents/skills/security/csrf_validator.py`

**Extract From**: `security-agent/agent.py` - `MobileSecurityScanner._check_csrf_protection()`

**Implementation Similar to Task 2.1**

#### Task 2.3: CORS Checker Skill

**File**: `agents/skills/security/cors_checker.py`

**Extract From**: Pattern matching and header checking logic

#### Task 2.4: CSP Analyzer Skill

**File**: `agents/skills/security/csp_analyzer.py`

**Extract From**: `_check_csp()` method

#### Task 2.5: TypeScript Standards Checker

**File**: `agents/skills/security/typescript_standards_checker.py`

**Extract From**: `TypeScriptReactStandardsChecker` class

**Key Methods to Extract**:
- `_check_component_naming()`
- `_check_class_components()`
- `_check_proptypes()`
- `_check_typescript_types()`
- `_check_react_security()`

#### Task 2.6: Python Standards Checker

**File**: `agents/skills/security/python_standards_checker.py`

**Extract From**: `PythonStandardsChecker` class

#### Task 2.7: Dead Code Detector

**File**: `agents/skills/security/dead_code_detector.py`

**Extract From**: `DeadCodeDetector` class

**Key Methods to Extract**:
- `detect_unused_files()`
- `_build_reference_map()`
- `_analyze_file()`
- `_find_similar_files()`

### Skill Development Template

For each skill:

1. **Extract logic** from original `security-agent/agent.py`
2. **Create function** that accepts `context: Dict[str, Any]`
3. **Return structured results** as dictionary
4. **Add SKILLS registration** list
5. **Write unit tests**
6. **Document in docstring**

### Success Criteria

- [ ] All 7 skills created
- [ ] Each skill works independently
- [ ] Unit tests for each skill (>85% coverage)
- [ ] Skills produce consistent output format
- [ ] Documentation complete

### Deliverables

1. 7 skill files in `agents/skills/security/`
2. Unit tests for each skill
3. Test fixtures and sample data
4. Documentation for each skill

---

## Phase 3: Create Security Workflows

**Duration**: 1-2 days
**Priority**: High
**Goal**: Define workflows that compose skills into complete audits

### Tasks

#### Task 3.1: Full Security Audit Workflow

**File**: `agents/workflows/security/full_security_audit.yaml`

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

#### Task 3.2: Mobile Attack Scan Workflow

**File**: `agents/workflows/security/mobile_attack_scan.yaml`

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

#### Task 3.3: Standards Check Workflow

**File**: `agents/workflows/security/standards_check.yaml`

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

#### Task 3.4: Dead Code Cleanup Workflow

**File**: `agents/workflows/security/dead_code_cleanup.yaml`

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

### Success Criteria

- [ ] All 4 workflows created
- [ ] YAML syntax valid
- [ ] Skills referenced exist
- [ ] Configurations logical
- [ ] Documentation complete

### Deliverables

1. 4 workflow YAML files
2. Workflow documentation
3. Usage examples

---

## Phase 4: Create Modular Security Agent

**Duration**: 3-4 days
**Priority**: High
**Goal**: Implement Security Monitoring Agent extending ModularAgent

### Tasks

#### Task 4.1: Create Agent Implementation

**File**: `agents/python/security_monitoring_agent.py`

**Key Components**:

1. **Class Definition**
```python
class SecurityMonitoringAgent(ModularAgent):
    """Security monitoring with mobile attack detection."""
```

2. **Core Methods**:
- `_register_core_skills()` - Register built-in skills
- `run(**kwargs)` - Main entry point
- `_to_standard_output()` - Convert to JSON schema
- Helper methods for metrics, findings, recommendations

3. **Main Function**:
```python
def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(...)
    args = parser.parse_args()
    agent = SecurityMonitoringAgent(args.config)
    output = agent.run(...)
    sys.exit(...)
```

**Implementation Checklist**:
- [ ] Class extends ModularAgent
- [ ] `_register_core_skills()` implemented
- [ ] `run()` method implemented
- [ ] `_to_standard_output()` converts to schema
- [ ] Validation against schema
- [ ] Report generation
- [ ] Error handling
- [ ] Summary printing
- [ ] CLI argument parsing

#### Task 4.2: Implement Output Conversion

**Key Logic**:
```python
def _to_standard_output(self, result, workflow, duration, context):
    # Aggregate results from skills
    security_issues = []
    standards_violations = []
    unused_files = []

    # Extract from skill results
    for key, value in result.items():
        # ... aggregation logic ...

    # Build standardized output
    output = create_agent_output(
        agent_name=self.config.name,
        agent_version=self.config.version,
        category="security",
        results={...},
        execution_time_ms=duration,
        workflow_name=workflow
    )

    # Add findings, recommendations, next_actions
    # ...

    return output
```

#### Task 4.3: Implement Helper Methods

**Methods to Implement**:
- `_count_by_severity()` - Count issues by severity
- `_calculate_security_score()` - Calculate 0-100 score
- `_create_findings()` - Create findings section
- `_generate_recommendations()` - Generate actionable items
- `_suggest_next_actions()` - Suggest orchestration steps
- `_has_critical_issues()` - Check for critical issues
- `_print_summary()` - Print execution summary
- `_generate_reports()` - Generate output files

### Success Criteria

- [ ] Agent class created and functional
- [ ] All methods implemented
- [ ] Output validates against schema
- [ ] CLI works correctly
- [ ] Integration tests passing
- [ ] Documentation complete

### Deliverables

1. `agents/python/security_monitoring_agent.py`
2. Integration tests
3. CLI documentation
4. Usage examples

---

## Phase 5: Create Agent Specification

**Duration**: 1 day
**Priority**: High
**Goal**: Create Markdown specification with YAML frontmatter

### Tasks

#### Task 5.1: Create MD File

**File**: `agents/md/security_monitoring_agent.md`

**Structure**:
```markdown
---
name: Security Monitoring Agent
description: Comprehensive mobile security scanning...
version: 2.0.0
model: claude-sonnet-4
temperature: 0.2
max_tokens: 8192
tools: [bash, read, write, grep, glob]
skills_dir: ./skills/security
workflows_dir: ./workflows/security
enabled_skills: [...]
enabled_workflows: [...]
categories: [Security, Mobile Attacks, Code Standards]
output_schema: schemas/agent-output-schema.json
---

# Security Monitoring Agent

Natural language system prompt...
```

#### Task 5.2: Write System Prompt

**Sections to Include**:
1. **Core Capabilities**
   - Mobile Security Scanning
   - Framework Standards
   - Dead Code Detection

2. **Workflow Execution**
   - Full Audit
   - Mobile Attack Scan
   - Standards Check
   - Dead Code Cleanup

3. **Task-Specific Instructions**
   - When scanning for security issues
   - When checking standards
   - When detecting dead code
   - When generating reports

4. **Output Format**
   - Schema compliance
   - Required structure

5. **Integration Points**
   - Other agents
   - CI/CD pipelines

6. **Success Metrics**
   - Security score targets
   - Compliance goals

### Success Criteria

- [ ] MD file created with valid YAML frontmatter
- [ ] System prompt comprehensive
- [ ] All capabilities documented
- [ ] Examples provided
- [ ] Integration points clear

### Deliverables

1. `agents/md/security_monitoring_agent.md`
2. Examples and usage guide

---

## Phase 6: Update Modular Framework

**Duration**: 2 days
**Priority**: Medium
**Goal**: Enhance base framework with JSON support and communication

### Tasks

#### Task 6.1: Add JSON Schema Support

**File**: `agents/python/modular_agent_framework.py`

**Methods to Add**:
```python
def load_output_schema(self, schema_name: str) -> Dict:
    """Load JSON schema for output validation."""
    pass

def validate_output_format(self, output: Dict, schema_name: str) -> Tuple[bool, List[str]]:
    """Validate agent output against schema."""
    pass
```

#### Task 6.2: Add Inter-Agent Communication

**Methods to Add**:
```python
def create_messenger(self) -> AgentMessenger:
    """Create messenger for inter-agent communication."""
    pass

def send_to_agent(self, to_agent: str, message_type: str, payload: Dict) -> str:
    """Send message to another agent."""
    pass

def receive_messages(self, mark_read: bool = True) -> List[Dict]:
    """Receive pending messages."""
    pass
```

#### Task 6.3: Add Artifact Management

**Methods to Add**:
```python
def create_artifact(self, artifact_type: str, data: Any, output_path: Path) -> Dict:
    """Create and store an artifact."""
    pass
```

#### Task 6.4: Update Documentation

**Files to Update**:
- `agents/MODULAR_FRAMEWORK_README.md`
- Add examples of new methods
- Update architecture diagrams

### Success Criteria

- [ ] All methods added to ModularAgent
- [ ] Backward compatible
- [ ] Tests updated
- [ ] Documentation updated

### Deliverables

1. Updated `modular_agent_framework.py`
2. Updated documentation
3. Migration guide for existing agents

---

## Validation & Testing

After completing all phases:

### Integration Testing

```bash
# Test complete workflow
cd agents/python
python security_monitoring_agent.py \
  --workflow full_security_audit \
  --output-dir ../../test-reports

# Verify output
python -c "
import json
with open('../../test-reports/security-audit-*.json') as f:
    output = json.load(f)
    assert 'schema_version' in output
    assert output['agent']['name'] == 'Security Monitoring Agent'
    print('✅ Output validation passed')
"
```

### Schema Validation Testing

```python
from lib.schema_validator import validate_output

# Load agent output
with open('test-reports/security-audit-*.json') as f:
    output = json.load(f)

# Validate
is_valid, errors = validate_output(output, 'agent-output-schema.json')

if not is_valid:
    print(f"❌ Validation failed: {errors}")
else:
    print("✅ Schema validation passed")
```

### Inter-Agent Communication Testing

```python
# Test message passing
from lib.agent_communication import AgentMessenger

security_agent = AgentMessenger("Security Monitoring Agent")
performance_agent = AgentMessenger("Performance Monitoring Agent")

# Send request
msg_id = security_agent.send_message(
    to_agent="Performance Monitoring Agent",
    message_type="request",
    payload={"action": "check_headers", "url": "https://example.com"}
)

# Receive and respond
messages = performance_agent.receive_messages()
assert len(messages) == 1

response_id = performance_agent.send_response(
    original_message=messages[0],
    payload={"headers": {...}}
)

# Verify response received
responses = security_agent.receive_messages()
assert len(responses) == 1
assert responses[0]["correlation_id"] == msg_id

print("✅ Inter-agent communication working")
```

---

## Rollback Plan

If issues arise:

### Step 1: Stop Using New Agent
```bash
# Revert to old agent
python security-agent/agent.py
```

### Step 2: Identify Issue
- Check logs
- Review error messages
- Identify failing component

### Step 3: Fix or Rollback
- Fix specific issue if possible
- Otherwise, continue using old agent
- Plan remediation

### Step 4: Communicate
- Notify team
- Update documentation
- Plan next steps

---

## Post-Migration Tasks

After successful migration:

1. **Update CI/CD Pipelines**
2. **Migrate Existing Reports**
3. **Train Team**
4. **Update Documentation**
5. **Deprecate Old Agent**
6. **Monitor Performance**
7. **Gather Feedback**
8. **Plan Improvements**

---

## Success Metrics

Track these metrics post-migration:

- **Adoption Rate**: % of projects using new agent
- **Performance**: Execution time comparison
- **Reliability**: Success rate of audits
- **User Satisfaction**: Feedback scores
- **Issues Found**: Number and severity
- **False Positives**: Rate of false alarms

---

## Timeline Summary

| Phase | Duration | Priority | Dependencies |
|-------|----------|----------|--------------|
| Phase 1: Infrastructure | 2-3 days | High | None |
| Phase 2: Extract Skills | 3-4 days | High | Phase 1 |
| Phase 3: Create Workflows | 1-2 days | High | Phase 2 |
| Phase 4: Build Agent | 3-4 days | High | Phase 1-3 |
| Phase 5: Agent Spec | 1 day | High | Phase 4 |
| Phase 6: Framework Updates | 2 days | Medium | Phase 1 |

**Total Estimated Duration**: 12-17 days (2.5-3.5 weeks)

---

## Next Steps

1. ✅ Review and approve this migration plan
2. ⏳ Begin Phase 1 implementation
3. ⏳ Set up daily progress check-ins
4. ⏳ Adjust timeline based on learnings
5. ⏳ Document any deviations or issues
