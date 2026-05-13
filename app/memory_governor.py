import hashlib
import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

audit_logger = logging.getLogger("audit")
_memory_store: Dict[str, dict] = {}

def pseudonymize(identifier: str) -> str:
    salt = os.getenv("PSEUDO_SALT", "default-salt")
    return hashlib.sha256((identifier + salt).encode()).hexdigest()

class MemoryGovernor:
    @staticmethod
    def remember(user_id: str, context: dict, consent_level: str = "basic") -> str:
        forbidden_fields = {"email", "phone", "name", "dni", "address", "ssn"}
        safe_context = {k: v for k, v in context.items() if k not in forbidden_fields}
        token = pseudonymize(user_id)
        entry = {
            "context": safe_context,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=90)).isoformat(),
            "consent_level": consent_level
        }
        _memory_store[token] = entry
        audit_logger.info(f"Memory stored for token {token[:8]}... | purpose: {consent_level}")
        return token

    @staticmethod
    def recall(token: str) -> Optional[dict]:
        entry = _memory_store.get(token)
        if entry and datetime.fromisoformat(entry["expires_at"]) > datetime.now(timezone.utc):
            return entry["context"]
        return None

    @staticmethod
    def forget(token: str) -> bool:
        if token in _memory_store:
            del _memory_store[token]
            audit_logger.info(f"Memory deleted for token {token[:8]}...")
            return True
        return False