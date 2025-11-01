#!/usr/bin/env python3
"""
Modular Agent Framework
=======================

Base framework for creating modular, skill-based agents following Anthropic's best practices.

This framework allows agents to:
- Load skills on-demand
- Compose workflows from multiple skills
- Be configured via YAML/MD files
- Maintain standalone operation
- Be ultra-specific to tasks through skill composition

Based on Anthropic's agent best practices:
- https://www.anthropic.com/research/building-effective-agents
- https://docs.claude.com/en/docs/claude-code/agent-skills
- https://docs.claude.com/en/docs/claude-code/sub-agents
"""

import json
import os
import sys
import yaml
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Union


@dataclass
class AgentSkill:
    """
    Represents a modular skill that can be loaded into an agent.

    Following Anthropic's Skills documentation pattern.
    """
    name: str
    description: str
    category: str
    function: Callable
    required_tools: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True


@dataclass
class AgentWorkflow:
    """
    Represents a workflow composed of multiple skills.

    Workflows define how skills work together to accomplish complex tasks.
    """
    name: str
    description: str
    skills: List[str]  # Skill names in execution order
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentConfig:
    """
    Agent configuration following Anthropic's subagent pattern.

    Can be loaded from YAML frontmatter in MD files.
    """
    name: str
    description: str
    version: str
    tools: List[str]
    model: str = "claude-sonnet-4"
    temperature: float = 0.7
    max_tokens: int = 4096
    skills_dir: str = "./skills"
    workflows_dir: str = "./workflows"
    enabled_skills: List[str] = field(default_factory=list)
    enabled_workflows: List[str] = field(default_factory=list)


class ModularAgent(ABC):
    """
    Base class for all modular agents.

    Provides:
    - Skill loading and management
    - Workflow composition
    - Configuration from YAML/MD files
    - Standalone operation
    - Tool integration
    """

    def __init__(self, config: Union[AgentConfig, str, Path]):
        """
        Initialize agent with configuration.

        Args:
            config: AgentConfig object, path to YAML file, or path to MD file with YAML frontmatter
        """
        if isinstance(config, (str, Path)):
            self.config = self._load_config(Path(config))
        else:
            self.config = config

        self.skills: Dict[str, AgentSkill] = {}
        self.workflows: Dict[str, AgentWorkflow] = {}
        self.tools: Dict[str, Callable] = {}

        # Initialize
        self._register_core_skills()
        self._load_skills()
        self._load_workflows()

        print(f"[{self.config.name}] Initialized")
        print(f"[{self.config.name}] Skills loaded: {len(self.skills)}")
        print(f"[{self.config.name}] Workflows loaded: {len(self.workflows)}")

    def _load_config(self, config_path: Path) -> AgentConfig:
        """
        Load configuration from YAML or MD file.

        Supports both:
        - Pure YAML files (.yaml, .yml)
        - MD files with YAML frontmatter (following Anthropic pattern)
        """
        print(f"[CONFIG] Loading from {config_path}")

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        content = config_path.read_text()

        # Check if MD file with frontmatter
        if config_path.suffix == '.md':
            # Parse YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    # System prompt is in parts[2]
                    frontmatter['system_prompt'] = parts[2].strip()
                else:
                    raise ValueError("Invalid MD file format - missing frontmatter")
            else:
                raise ValueError("MD file must start with YAML frontmatter (---)")
        else:
            # Pure YAML file
            frontmatter = yaml.safe_load(content)

        # Create AgentConfig from loaded data
        return AgentConfig(
            name=frontmatter['name'],
            description=frontmatter['description'],
            version=frontmatter.get('version', '1.0.0'),
            tools=frontmatter.get('tools', []),
            model=frontmatter.get('model', 'claude-sonnet-4'),
            temperature=frontmatter.get('temperature', 0.7),
            max_tokens=frontmatter.get('max_tokens', 4096),
            skills_dir=frontmatter.get('skills_dir', './skills'),
            workflows_dir=frontmatter.get('workflows_dir', './workflows'),
            enabled_skills=frontmatter.get('enabled_skills', []),
            enabled_workflows=frontmatter.get('enabled_workflows', [])
        )

    @abstractmethod
    def _register_core_skills(self):
        """
        Register core skills specific to this agent type.

        Each agent subclass must implement this to define its core capabilities.
        """
        pass

    def register_skill(self, skill: AgentSkill):
        """Register a skill with the agent."""
        if skill.enabled:
            self.skills[skill.name] = skill
            print(f"[SKILL] Registered: {skill.name} ({skill.category})")

    def register_workflow(self, workflow: AgentWorkflow):
        """Register a workflow with the agent."""
        # Validate that all required skills exist
        missing_skills = [s for s in workflow.skills if s not in self.skills]
        if missing_skills:
            print(f"[WARNING] Workflow '{workflow.name}' requires missing skills: {missing_skills}")
            return

        self.workflows[workflow.name] = workflow
        print(f"[WORKFLOW] Registered: {workflow.name}")

    def _load_skills(self):
        """
        Load additional skills from skills directory.

        Skills are Python files that define skill functions.
        """
        skills_dir = Path(self.config.skills_dir)
        if not skills_dir.exists():
            print(f"[SKILLS] Directory not found: {skills_dir}")
            return

        # Load skill definitions from Python files
        for skill_file in skills_dir.glob("*.py"):
            if skill_file.name.startswith('_'):
                continue

            try:
                # Import skill module
                spec = __import__(skill_file.stem)

                # Look for skill definitions
                if hasattr(spec, 'SKILLS'):
                    for skill_def in spec.SKILLS:
                        skill = AgentSkill(**skill_def)
                        if not self.config.enabled_skills or skill.name in self.config.enabled_skills:
                            self.register_skill(skill)

            except Exception as e:
                print(f"[ERROR] Failed to load skill from {skill_file}: {e}")

    def _load_workflows(self):
        """
        Load workflows from workflows directory.

        Workflows are YAML files defining skill composition.
        """
        workflows_dir = Path(self.config.workflows_dir)
        if not workflows_dir.exists():
            print(f"[WORKFLOWS] Directory not found: {workflows_dir}")
            return

        for workflow_file in workflows_dir.glob("*.yaml"):
            try:
                with open(workflow_file) as f:
                    workflow_def = yaml.safe_load(f)

                workflow = AgentWorkflow(**workflow_def)
                if not self.config.enabled_workflows or workflow.name in self.config.enabled_workflows:
                    self.register_workflow(workflow)

            except Exception as e:
                print(f"[ERROR] Failed to load workflow from {workflow_file}: {e}")

    def execute_skill(self, skill_name: str, **kwargs) -> Any:
        """
        Execute a specific skill.

        Args:
            skill_name: Name of the skill to execute
            **kwargs: Arguments to pass to the skill function

        Returns:
            Result from skill execution
        """
        if skill_name not in self.skills:
            raise ValueError(f"Skill not found: {skill_name}")

        skill = self.skills[skill_name]
        print(f"[EXECUTE] Running skill: {skill_name}")

        try:
            result = skill.function(**kwargs)
            print(f"[EXECUTE] Skill '{skill_name}' completed successfully")
            return result
        except Exception as e:
            print(f"[ERROR] Skill '{skill_name}' failed: {e}")
            raise

    def execute_workflow(self, workflow_name: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a workflow (sequence of skills).

        Args:
            workflow_name: Name of the workflow to execute
            context: Shared context passed between skills

        Returns:
            Final context after all skills execute
        """
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow not found: {workflow_name}")

        workflow = self.workflows[workflow_name]
        print(f"[WORKFLOW] Executing: {workflow_name}")
        print(f"[WORKFLOW] Steps: {', '.join(workflow.skills)}")

        context = context or {}
        context['workflow_config'] = workflow.config

        for skill_name in workflow.skills:
            print(f"[WORKFLOW] Step: {skill_name}")
            result = self.execute_skill(skill_name, context=context)

            # Merge result into context
            if isinstance(result, dict):
                context.update(result)
            else:
                context[skill_name] = result

        print(f"[WORKFLOW] Completed: {workflow_name}")
        return context

    def list_skills(self) -> List[str]:
        """List all available skills."""
        return list(self.skills.keys())

    def list_workflows(self) -> List[str]:
        """List all available workflows."""
        return list(self.workflows.keys())

    def get_skill_info(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific skill."""
        if skill_name not in self.skills:
            return None

        skill = self.skills[skill_name]
        return {
            'name': skill.name,
            'description': skill.description,
            'category': skill.category,
            'required_tools': skill.required_tools,
            'enabled': skill.enabled
        }

    def export_config(self, output_path: Path, format: str = 'yaml'):
        """
        Export agent configuration.

        Args:
            output_path: Where to save the config
            format: 'yaml' or 'md' (MD with YAML frontmatter)
        """
        config_dict = asdict(self.config)

        if format == 'md':
            # Create MD file with YAML frontmatter (Anthropic subagent pattern)
            frontmatter = yaml.dump(config_dict, default_flow_style=False)
            system_prompt = config_dict.get('system_prompt', f"You are {self.config.name}, {self.config.description}")

            content = f"---\n{frontmatter}---\n\n{system_prompt}\n"
            output_path.write_text(content)

        else:
            # Pure YAML
            with open(output_path, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False)

        print(f"[EXPORT] Config exported to {output_path}")

    @abstractmethod
    def run(self, **kwargs) -> Any:
        """
        Main entry point for agent execution.

        Each agent subclass implements its specific execution logic.
        """
        pass


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

class ExamplePerformanceAgent(ModularAgent):
    """
    Example implementation showing how to create a modular agent.
    """

    def _register_core_skills(self):
        """Register core performance monitoring skills."""

        # Skill 1: Lighthouse Audit
        def lighthouse_audit(context: Dict[str, Any]) -> Dict[str, Any]:
            """Run Lighthouse audit."""
            url = context.get('url')
            # ... lighthouse logic ...
            return {'lighthouse_score': 95}

        self.register_skill(AgentSkill(
            name='lighthouse_audit',
            description='Run Google Lighthouse audit',
            category='performance',
            function=lighthouse_audit,
            required_tools=['lighthouse'],
            config={'timeout': 120}
        ))

        # Skill 2: Security Headers Check
        def check_security_headers(context: Dict[str, Any]) -> Dict[str, Any]:
            """Check security headers."""
            url = context.get('url')
            # ... security check logic ...
            return {'security_score': 85}

        self.register_skill(AgentSkill(
            name='check_security_headers',
            description='Validate security headers',
            category='security',
            function=check_security_headers,
            required_tools=['requests']
        ))

    def run(self, url: str, workflow: str = None) -> Dict[str, Any]:
        """Run performance audit."""
        context = {'url': url}

        if workflow and workflow in self.workflows:
            return self.execute_workflow(workflow, context)
        else:
            # Run all skills sequentially
            results = {}
            for skill_name in self.skills:
                result = self.execute_skill(skill_name, context=context)
                results.update(result)
            return results


def main():
    """Example usage of modular agent framework."""

    # Example 1: Create from code
    config = AgentConfig(
        name="Performance Monitor",
        description="Modular performance monitoring agent",
        version="1.0.0",
        tools=["lighthouse", "requests"],
        enabled_skills=["lighthouse_audit", "check_security_headers"]
    )

    agent = ExamplePerformanceAgent(config)

    # List capabilities
    print(f"\nAvailable skills: {agent.list_skills()}")
    print(f"Available workflows: {agent.list_workflows()}")

    # Run agent
    results = agent.run(url="https://example.com")
    print(f"\nResults: {results}")


if __name__ == "__main__":
    main()
