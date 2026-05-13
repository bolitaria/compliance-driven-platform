import json
import logging
import pytest
from audit_logger import audit_event

@pytest.mark.asyncio
async def test_audit_decorator_logs_success(caplog):
    caplog.set_level(logging.INFO, logger="audit")
    
    @audit_event(action="test_action", resource="test_res")
    async def dummy_func():
        return "ok"
    
    result = await dummy_func()
    assert result == "ok"
    
    records = [r for r in caplog.records if r.name == "audit"]
    assert len(records) == 1
    event = json.loads(records[0].message)
    assert event["action"] == "test_action"
    assert event["status"] == "success"
    assert "traceId" in event