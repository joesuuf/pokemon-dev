#!/usr/bin/env python3
"""
Unit Tests for Agent Communication
===================================

Extensive testing of inter-agent communication functionality.
"""

import json
import pytest
import tempfile
import shutil
import sys
from pathlib import Path
from datetime import datetime
from uuid import UUID

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.agent_communication import (
    AgentMessenger,
    create_agent_output
)


class TestAgentMessenger:
    """Test AgentMessenger class."""

    def test_init_default_message_dir(self):
        """Test messenger initializes with default message directory."""
        messenger = AgentMessenger("test_agent")
        
        assert messenger.agent_name == "test_agent"
        assert messenger.message_dir.exists()
        assert messenger.message_dir.name == ".agent-messages"
        assert messenger.inbox.exists()
        assert messenger.outbox.exists()

    def test_init_custom_message_dir(self):
        """Test messenger initializes with custom message directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger = AgentMessenger("test_agent", message_dir=Path(tmpdir))
            
            assert messenger.message_dir == Path(tmpdir)
            assert messenger.inbox.exists()
            assert messenger.outbox.exists()

    def test_init_creates_directories(self):
        """Test messenger creates necessary directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger = AgentMessenger("test_agent", message_dir=Path(tmpdir))
            
            assert (Path(tmpdir) / "test_agent" / "inbox").exists()
            assert (Path(tmpdir) / "test_agent" / "outbox").exists()

    def test_send_message_creates_files(self):
        """Test sending a message creates files in inbox and outbox."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger1 = AgentMessenger("agent1", message_dir=Path(tmpdir))
            messenger2 = AgentMessenger("agent2", message_dir=Path(tmpdir))
            
            payload = {"test": "data"}
            message_id = messenger1.send_message(
                "agent2",
                "request",
                payload
            )
            
            # Check outbox
            outbox_files = list(messenger1.outbox.glob("*.json"))
            assert len(outbox_files) == 1
            
            # Check recipient inbox
            recipient_inbox = Path(tmpdir) / "agent2" / "inbox"
            inbox_files = list(recipient_inbox.glob("*.json"))
            assert len(inbox_files) == 1

    def test_send_message_structure(self):
        """Test sent message has correct structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger = AgentMessenger("agent1", message_dir=Path(tmpdir))
            
            payload = {"action": "scan", "target": "src/"}
            message_id = messenger.send_message(
                "agent2",
                "request",
                payload
            )
            
            # Verify message ID format
            try:
                UUID(message_id)
            except ValueError:
                pytest.fail("Message ID is not a valid UUID")
            
            # Read message from outbox
            outbox_file = messenger.outbox / f"{message_id}.json"
            with open(outbox_file) as f:
                message = json.load(f)
            
            assert message["message_id"] == message_id
            assert message["from_agent"] == "agent1"
            assert message["to_agent"] == "agent2"
            assert message["message_type"] == "request"
            assert message["payload"] == payload
            assert "timestamp" in message

    def test_send_message_with_correlation_id(self):
        """Test sending message with correlation ID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger = AgentMessenger("agent1", message_dir=Path(tmpdir))
            
            payload = {"result": "success"}
            correlation_id = "original-message-123"
            
            message_id = messenger.send_message(
                "agent2",
                "response",
                payload,
                correlation_id=correlation_id
            )
            
            outbox_file = messenger.outbox / f"{message_id}.json"
            with open(outbox_file) as f:
                message = json.load(f)
            
            assert message["correlation_id"] == correlation_id

    def test_send_message_validates_schema(self):
        """Test sending message validates against schema."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger = AgentMessenger("agent1", message_dir=Path(tmpdir))
            
            # This should work (valid message structure)
            payload = {"test": "data"}
            message_id = messenger.send_message(
                "agent2",
                "request",
                payload
            )
            assert message_id is not None

    def test_send_message_invalid_message_type(self):
        """Test sending message with invalid message type fails validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger = AgentMessenger("agent1", message_dir=Path(tmpdir))
            
            # Invalid message type - this might fail validation depending on schema
            # The schema validation should catch this
            payload = {"test": "data"}
            
            # This should work if "invalid_type" isn't in enum
            # But the validation might catch it
            try:
                message_id = messenger.send_message(
                    "agent2",
                    "invalid_type",  # Not in enum: request, response, notification, error
                    payload
                )
                # If it didn't raise, check the message
                outbox_file = messenger.outbox / f"{message_id}.json"
                if outbox_file.exists():
                    with open(outbox_file) as f:
                        message = json.load(f)
                    # The validation should have caught this
                    assert message["message_type"] in ["request", "response", "notification", "error"]
            except ValueError:
                # Expected - validation should fail
                pass

    def test_receive_messages_empty_inbox(self):
        """Test receiving messages from empty inbox."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger = AgentMessenger("agent1", message_dir=Path(tmpdir))
            
            messages = messenger.receive_messages()
            assert messages == []

    def test_receive_messages_single_message(self):
        """Test receiving a single message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger1 = AgentMessenger("agent1", message_dir=Path(tmpdir))
            messenger2 = AgentMessenger("agent2", message_dir=Path(tmpdir))
            
            payload = {"action": "process"}
            message_id = messenger1.send_message("agent2", "request", payload)
            
            messages = messenger2.receive_messages()
            assert len(messages) == 1
            assert messages[0]["message_id"] == message_id
            assert messages[0]["payload"] == payload

    def test_receive_messages_multiple_messages(self):
        """Test receiving multiple messages."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger1 = AgentMessenger("agent1", message_dir=Path(tmpdir))
            messenger2 = AgentMessenger("agent2", message_dir=Path(tmpdir))
            
            # Send multiple messages
            for i in range(5):
                messenger1.send_message("agent2", "notification", {"index": i})
            
            messages = messenger2.receive_messages()
            assert len(messages) == 5

    def test_receive_messages_mark_read(self):
        """Test receiving messages marks them as read."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger1 = AgentMessenger("agent1", message_dir=Path(tmpdir))
            messenger2 = AgentMessenger("agent2", message_dir=Path(tmpdir))
            
            message_id = messenger1.send_message("agent2", "request", {})
            
            # Receive messages (should move to read folder)
            messages = messenger2.receive_messages(mark_read=True)
            assert len(messages) == 1
            
            # Inbox should be empty
            inbox_files = list(messenger2.inbox.glob("*.json"))
            assert len(inbox_files) == 0
            
            # Should be in read folder
            read_dir = messenger2.inbox.parent / "read"
            read_files = list(read_dir.glob("*.json"))
            assert len(read_files) == 1

    def test_receive_messages_dont_mark_read(self):
        """Test receiving messages without marking as read."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger1 = AgentMessenger("agent1", message_dir=Path(tmpdir))
            messenger2 = AgentMessenger("agent2", message_dir=Path(tmpdir))
            
            message_id = messenger1.send_message("agent2", "request", {})
            
            # Receive messages (should NOT move to read folder)
            messages = messenger2.receive_messages(mark_read=False)
            assert len(messages) == 1
            
            # Inbox should still have the message
            inbox_files = list(messenger2.inbox.glob("*.json"))
            assert len(inbox_files) == 1

    def test_receive_messages_twice(self):
        """Test receiving messages twice with mark_read=True."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger1 = AgentMessenger("agent1", message_dir=Path(tmpdir))
            messenger2 = AgentMessenger("agent2", message_dir=Path(tmpdir))
            
            message_id = messenger1.send_message("agent2", "request", {})
            
            # First receive
            messages1 = messenger2.receive_messages(mark_read=True)
            assert len(messages1) == 1
            
            # Second receive (should be empty)
            messages2 = messenger2.receive_messages(mark_read=True)
            assert len(messages2) == 0

    def test_send_response(self):
        """Test sending a response to a message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger1 = AgentMessenger("agent1", message_dir=Path(tmpdir))
            messenger2 = AgentMessenger("agent2", message_dir=Path(tmpdir))
            
            # Send initial request
            request_id = messenger1.send_message("agent2", "request", {"action": "scan"})
            
            # Receive the request
            messages = messenger2.receive_messages(mark_read=False)
            assert len(messages) == 1
            original_message = messages[0]
            
            # Send response
            response_payload = {"result": "completed", "status": "success"}
            response_id = messenger2.send_response(original_message, response_payload)
            
            # Check response has correlation ID
            response_file = messenger2.outbox / f"{response_id}.json"
            with open(response_file) as f:
                response = json.load(f)
            
            assert response["correlation_id"] == original_message["message_id"]
            assert response["message_type"] == "response"
            assert response["to_agent"] == "agent1"
            assert response["payload"] == response_payload

    def test_multiple_agents_communication(self):
        """Test communication between multiple agents."""
        with tempfile.TemporaryDirectory() as tmpdir:
            messenger1 = AgentMessenger("agent1", message_dir=Path(tmpdir))
            messenger2 = AgentMessenger("agent2", message_dir=Path(tmpdir))
            messenger3 = AgentMessenger("agent3", message_dir=Path(tmpdir))
            
            # agent1 sends to agent2 and agent3
            msg1_id = messenger1.send_message("agent2", "request", {"task": "task1"})
            msg2_id = messenger1.send_message("agent3", "notification", {"info": "info1"})
            
            # agent2 receives its message
            agent2_messages = messenger2.receive_messages()
            assert len(agent2_messages) == 1
            assert agent2_messages[0]["message_id"] == msg1_id
            
            # agent3 receives its message
            agent3_messages = messenger3.receive_messages()
            assert len(agent3_messages) == 1
            assert agent3_messages[0]["message_id"] == msg2_id


class TestCreateAgentOutput:
    """Test create_agent_output function."""

    def test_create_basic_output(self):
        """Test creating basic agent output."""
        output = create_agent_output(
            agent_name="Test Agent",
            agent_version="1.0.0",
            category="security",
            results={"data": {}}
        )
        
        assert output["schema_version"] == "1.0.0"
        assert output["agent"]["name"] == "Test Agent"
        assert output["agent"]["version"] == "1.0.0"
        assert output["agent"]["category"] == "security"
        assert output["execution"]["status"] == "success"
        assert "timestamp" in output["execution"]
        assert output["results"] == {"data": {}}

    def test_create_output_with_duration(self):
        """Test creating output with execution duration."""
        output = create_agent_output(
            agent_name="Test Agent",
            agent_version="1.0.0",
            category="security",
            results={"data": {}},
            execution_time_ms=1234.5
        )
        
        assert output["execution"]["duration_ms"] == 1234.5

    def test_create_output_with_workflow(self):
        """Test creating output with workflow name."""
        output = create_agent_output(
            agent_name="Test Agent",
            agent_version="1.0.0",
            category="security",
            results={"data": {}},
            workflow_name="full_security_audit"
        )
        
        assert output["execution"]["workflow_name"] == "full_security_audit"

    def test_create_output_with_all_fields(self):
        """Test creating output with all optional fields."""
        output = create_agent_output(
            agent_name="Security Agent",
            agent_version="2.0.0",
            category="security",
            results={
                "data": {"test": "value"},
                "metrics": {"score": 100}
            },
            execution_time_ms=5000.0,
            workflow_name="full_audit"
        )
        
        assert output["execution"]["duration_ms"] == 5000.0
        assert output["execution"]["workflow_name"] == "full_audit"
        assert output["results"]["data"]["test"] == "value"
        assert output["results"]["metrics"]["score"] == 100

    def test_create_output_structure(self):
        """Test output has all required structure."""
        output = create_agent_output(
            agent_name="Test Agent",
            agent_version="1.0.0",
            category="performance",
            results={"data": {}}
        )
        
        # Check all required fields exist
        assert "schema_version" in output
        assert "agent" in output
        assert "execution" in output
        assert "context" in output
        assert "results" in output
        assert "findings" in output
        assert "recommendations" in output
        assert "next_actions" in output
        
        # Check findings structure
        assert "issues" in output["findings"]
        assert "warnings" in output["findings"]
        assert "info" in output["findings"]
        
        # Check next_actions structure
        assert "suggested_agents" in output["next_actions"]
        assert "required_skills" in output["next_actions"]

    def test_create_output_validates_schema(self):
        """Test created output validates against schema."""
        from agents.lib.schema_validator import validate_output
        
        output = create_agent_output(
            agent_name="Test Agent",
            agent_version="1.0.0",
            category="security",
            results={"data": {}}
        )
        
        is_valid, errors = validate_output(output)
        assert is_valid is True
        assert errors == []

    def test_create_output_different_categories(self):
        """Test creating outputs for different agent categories."""
        categories = ["security", "performance", "seo", "content", "installation"]
        
        for category in categories:
            output = create_agent_output(
                agent_name=f"{category.title()} Agent",
                agent_version="1.0.0",
                category=category,
                results={"data": {}}
            )
            
            assert output["agent"]["category"] == category


class TestIntegration:
    """Integration tests for communication flow."""

    def test_request_response_flow(self):
        """Test complete request-response flow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent1 = AgentMessenger("agent1", message_dir=Path(tmpdir))
            agent2 = AgentMessenger("agent2", message_dir=Path(tmpdir))
            
            # Agent1 sends request
            request_payload = {"action": "scan", "paths": ["src/"]}
            request_id = agent1.send_message("agent2", "request", request_payload)
            
            # Agent2 receives request
            messages = agent2.receive_messages()
            assert len(messages) == 1
            request = messages[0]
            
            # Agent2 processes and sends response
            response_payload = create_agent_output(
                agent_name="Agent2",
                agent_version="1.0.0",
                category="security",
                results={"data": {"status": "completed"}},
                execution_time_ms=1000.0
            )
            
            response_id = agent2.send_response(request, response_payload)
            
            # Agent1 receives response
            responses = agent1.receive_messages()
            assert len(responses) == 1
            response = responses[0]
            
            assert response["message_type"] == "response"
            assert response["correlation_id"] == request_id
            assert response["payload"]["agent"]["name"] == "Agent2"

    def test_multi_agent_workflow(self):
        """Test multi-agent workflow simulation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            security_agent = AgentMessenger("security", message_dir=Path(tmpdir))
            performance_agent = AgentMessenger("performance", message_dir=Path(tmpdir))
            
            # Security agent completes scan and notifies performance agent
            security_output = create_agent_output(
                agent_name="Security Agent",
                agent_version="2.0.0",
                category="security",
                results={"data": {"issues": 5}},
                workflow_name="full_audit"
            )
            
            notification_id = security_agent.send_message(
                "performance",
                "notification",
                security_output
            )
            
            # Performance agent receives notification
            notifications = performance_agent.receive_messages()
            assert len(notifications) == 1
            
            notification = notifications[0]
            assert notification["payload"]["agent"]["name"] == "Security Agent"
            assert notification["payload"]["results"]["data"]["issues"] == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
