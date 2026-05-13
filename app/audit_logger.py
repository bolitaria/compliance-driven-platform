# Compliance‑as‑Code

import logging
import json
import uuid
from datetime import datetime, timezone
from functools import wraps

# Immutable structured audit logging - mandatory for all significant actions
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)

def audit_event(action: str, resource: str, principal: str = "system"):
    """
    Decorator that guarantees an audit event is emitted for the decorated function.
    The event includes traceId, timestamp, action, principal, resource, and result.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            trace_id = str(uuid.uuid4())
            start = datetime.now(timezone.utc)
            try:
                result = await func(*args, **kwargs)
                status = "success"
                return result
            except Exception as e:
                status = "failure"
                raise e
            finally:
                duration_ms = (datetime.now(timezone.utc) - start).total_seconds() * 1000
                event = {
                    "traceId": trace_id,
                    "action": action,
                    "principal": principal,
                    "resource": resource,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "duration_ms": duration_ms,
                    "status": status
                }
                audit_logger.info(json.dumps(event))
        return wrapper
    return decorator