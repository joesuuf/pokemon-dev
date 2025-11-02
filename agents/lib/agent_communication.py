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
from typing import Dict, Any, Optional, List
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

    def receive_messages(self, mark_read: bool = True) -> List[Dict[str, Any]]:
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
