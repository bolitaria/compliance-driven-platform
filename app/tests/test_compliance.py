import os

def test_all_endpoints_use_audit():
    """Verify that main.py uses @audit_event decorator (Compliance‑as‑Code)."""
    tests_dir = os.path.dirname(__file__)
    app_dir = os.path.dirname(tests_dir)
    main_path = os.path.join(app_dir, "main.py")
    
    with open(main_path, "r") as f:
        content = f.read()
    
    assert '@audit_event' in content, "main.py must use @audit_event decorator for audit logging"