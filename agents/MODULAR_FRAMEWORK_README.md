# Modular Agent Framework - Complete Guide

## Overview

This framework implements Anthropic's best practices for building modular, skill-based agents with ultra-specific task capabilities through composable skills and workflows.

Based on:
- [Building Effective AI Agents](https://www.anthropic.com/research/building-effective-agents)
- [Agent Skills Documentation](https://docs.claude.com/en/docs/claude-code/agent-skills)
- [Sub agents Documentation](https://docs.claude.com/en/docs/claude-code/sub-agents)

## Key Concepts

### 1. **Agents** (MD Files with YAML Frontmatter)
Agents are defined using Anthropic's subagent pattern:
```markdown
---
name: Agent Name
description: What the agent does
version: 1.0.0
model: claude-sonnet-4
tools: [bash, read, write]
skills_dir: ./skills/category
workflows_dir: ./workflows/category
enabled_skills: [skill1, skill2]
enabled_workflows: [workflow1]
---

System prompt goes here...
```

### 2. **Skills** (Modular Functions)
Skills are reusable, pluggable functions:
```python
def my_skill(context: dict) -> dict:
    """Do something specific."""
    return {'result': 'success'}

SKILLS = [{
    'name': 'my_skill',
    'description': 'Description',
    'category': 'performance',
    'function': my_skill,
    'required_tools': ['bash'],
    'enabled': True
}]
```

### 3. **Workflows** (Skill Composition)
Workflows chain skills together:
```yaml
name: my_workflow
description: Multi-step workflow
skills:
  - skill1
  - skill2
  - skill3
config:
  timeout: 300
```

## Directory Structure

```
agents/
├── python/
│   ├── modular_agent_framework.py    # Base framework
│   ├── test_agents.py                 # Unit tests
│   ├── performance_monitoring_agent.py
│   ├── seo_optimization_agent.py
│   ├── content_coordinator_agent.py
│   └── professor_data_installation_agent.py
├── md/
│   ├── performance_monitoring_agent.md  # Anthropic format
│   ├── seo_optimization_agent.md
│   ├── content_coordinator_agent.md
│   └── professor_data_installation_agent.md
├── skills/
│   ├── performance/
│   │   └── example_lighthouse_skill.py
│   ├── seo/
│   ├── content/
│   └── installation/
└── workflows/
    ├── performance/
    │   └── full_audit.yaml
    ├── seo/
    ├── content/
    └── installation/
```

## Usage Examples

### Creating an Agent from MD File

```python
from modular_agent_framework import ModularAgent

# Load agent from MD file (Anthropic subagent format)
agent = PerformanceAgent("agents/md/performance_monitoring_agent.md")

# List capabilities
print(agent.list_skills())      # ['lighthouse_audit', 'security_check', ...]
print(agent.list_workflows())    # ['full_audit', 'quick_scan', ...]

# Execute specific skill
result = agent.execute_skill('lighthouse_audit', url='https://example.com')

# Execute workflow
result = agent.execute_workflow('full_audit', context={'url': 'https://example.com'})
```

### Creating Custom Skills

```python
# skills/custom/my_skill.py

def analyze_custom_metric(context: dict) -> dict:
    """Analyze a custom performance metric."""
    url = context['url']
    # Your analysis logic
    return {'custom_score': 95}

SKILLS = [{
    'name': 'analyze_custom_metric',
    'description': 'Custom metric analysis',
    'category': 'custom',
    'function': analyze_custom_metric,
    'required_tools': ['bash', 'read'],
    'config': {'threshold': 90},
    'enabled': True
}]
```

### Creating Custom Workflows

```yaml
# workflows/custom/my_workflow.yaml

name: custom_optimization
description: Custom optimization workflow
skills:
  - lighthouse_audit
  - analyze_custom_metric
  - generate_report
config:
  timeout: 600
  parallel: false
```

### Running Agent Self-Tests

```bash
# Test all agents
python agents/python/test_agents.py

# Test specific agent
python agents/python/test_agents.py --agent performance

# Test specific skill (if implemented)
python agents/python/test_agents.py --skill lighthouse_audit

# Verbose output
python agents/python/test_agents.py --verbose
```

## Making Agents Ultra-Specific to Tasks

### Approach 1: Enable Only Needed Skills

```yaml
# MD file frontmatter
enabled_skills:
  - lighthouse_audit     # Only this skill
  - security_check      # And this one
# All other skills disabled
```

### Approach 2: Create Task-Specific Workflows

```yaml
# workflows/performance/quick_mobile_audit.yaml
name: quick_mobile_audit
description: Fast mobile performance check
skills:
  - lighthouse_audit
config:
  device: mobile
  timeout: 60
  metrics: [lcp, cls, fid]  # Only these metrics
```

### Approach 3: Skill Configuration

```python
SKILLS = [{
    'name': 'lighthouse_audit',
    'config': {
        'device': 'mobile',        # Ultra-specific: mobile only
        'categories': ['performance'],  # Only performance, skip others
        'throttling': '3G',        # Specific network
        'metrics': ['lcp', 'fid']  # Only these metrics
    }
}]
```

### Approach 4: Dynamic Skill Loading

```python
# Load skills based on task
if task == 'mobile_performance':
    agent.config.enabled_skills = ['lighthouse_mobile', 'mobile_vitals']
elif task == 'security_audit':
    agent.config.enabled_skills = ['security_headers', 'ssl_check', 'cors_validation']

agent._load_skills()  # Reload with new config
```

## Agent Debugging

### Self-Debugging

Each agent has unit tests that can run:
```python
# Agent debugs itself
python test_agents.py --agent performance

# Check specific skill
agent.get_skill_info('lighthouse_audit')
# Returns: {name, description, category, tools, enabled}
```

### Cross-Agent Debugging

```python
# Debugging Agent checks Performance Agent
debugging_agent = DebuggingAgent()
issues = debugging_agent.diagnose(performance_agent)

# Issues found:
# - Skill 'lighthouse_audit' requires tool 'lighthouse' (not installed)
# - Workflow 'full_audit' references unknown skill 'missing_skill'
```

## Format Comparison

| Format | Use Case | Advantages |
|--------|----------|------------|
| **Python .py** | Standalone execution, complex logic | Full Python capabilities, easy debugging |
| **Markdown .md** | Anthropic subagents, Claude Code | Natural language prompts, version control friendly |
| **YAML .yaml** | Configuration, workflows | Human-readable, easy to edit |

## Best Practices

### 1. Keep Skills Atomic
```python
# ✅ Good: Single responsibility
def check_security_headers(context):
    """Only checks security headers."""
    pass

# ❌ Bad: Multiple responsibilities
def check_everything(context):
    """Checks headers, SSL, CORS, cookies..."""
    pass
```

### 2. Use Context for Data Flow
```python
# Skills receive context and return results
def skill1(context):
    return {'data': 'from skill1'}

def skill2(context):
    data = context.get('data')  # From skill1
    return {'final': f"processed {data}"}
```

### 3. Version Skills
```python
SKILLS = [{
    'name': 'lighthouse_audit_v2',  # Versioned
    'version': '2.0.0',
    'deprecated': False
}]
```

### 4. Document Required Tools
```python
SKILLS = [{
    'required_tools': ['lighthouse', 'bash'],  # Explicit dependencies
    'install_command': 'npm install -g lighthouse'
}]
```

## Integration with Anthropic Patterns

### Subagent Pattern
```markdown
---
name: Performance Subagent
description: Focused subagent for performance tasks
parent_agent: Main Agent
---

You are a specialized subagent focused only on performance monitoring.
Your parent agent delegates performance tasks to you.
```

### Skill Pattern
Following Claude Code Skills documentation:
- Skills are task-specific markdown files
- Can include scripts and documents
- Extend agent capabilities modularly

### Tool Use Pattern
```yaml
tools:
  - bash: For running commands
  - read: For reading files
  - write: For writing reports
  - web_fetch: For accessing URLs
```

## Troubleshooting

### Skill Not Loading

```python
# Check skills directory exists
agent.config.skills_dir  # Should point to existing directory

# Check skill file format
# File must define SKILLS list
# SKILLS = [{'name': ..., 'function': ...}]

# Check enabled_skills
agent.config.enabled_skills  # Should include skill name
```

### Workflow Fails

```python
# Check all skills exist
workflow.skills  # ['skill1', 'skill2']
agent.list_skills()  # Should include all workflow skills

# Check context
context = {'required_key': 'value'}
agent.execute_workflow('my_workflow', context)
```

### Test Failures

```bash
# Run with verbose
python test_agents.py --verbose

# Check specific test
python test_agents.py TestPerformanceMonitoringAgent.test_lighthouse_audit_skill
```

## Future Enhancements

- [ ] Hot-reload skills without restarting agent
- [ ] Skill marketplace/registry
- [ ] Visual workflow builder
- [ ] A/B testing for skills
- [ ] Skill performance profiling
- [ ] Auto-generated documentation from skills
- [ ] Skill dependency resolution
- [ ] Workflow DAG visualization

---

**Framework Version:** 1.0.0
**Last Updated:** October 31, 2025
**Status:** Production Ready ✅
