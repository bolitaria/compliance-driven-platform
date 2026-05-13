from memory_governor import MemoryGovernor

def test_remember_filters_pii():
    token = MemoryGovernor.remember("user123", {"preference": "dark", "email": "a@b.com"})
    context = MemoryGovernor.recall(token)
    assert "preference" in context
    assert "email" not in context  # PII should be stripped

def test_forget_erases_data():
    token = MemoryGovernor.remember("user456", {"lang": "es"})
    assert MemoryGovernor.forget(token) is True
    assert MemoryGovernor.recall(token) is None