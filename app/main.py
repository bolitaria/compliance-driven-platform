import logging
import random
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from audit_logger import audit_event
from items_storage import item_store
from memory_governor import MemoryGovernor

# Configure logging so audit events appear in container logs
logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")

app = FastAPI()

# ---------- Demo endpoints ----------
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/items")
async def get_items():
    """Returns all demo infrastructure items."""
    items = item_store.get_all()
    return {"items": [item.dict() for item in items]}


# ---------- Traceable Reasoning ----------
class LoanRequest(BaseModel):
    income: float
    debt: float
    employment_years: int

class DecisionResponse(BaseModel):
    approved: bool
    reasoning: list[str]

@app.post("/api/loan-decision")
@audit_event(action="loan_decision", resource="loan", principal="api_user")
async def decide_loan(request: Request, loan: LoanRequest):
    reasoning_steps = []
    policy_id = "FRB_RegB_v2"
    dti = loan.debt / loan.income if loan.income > 0 else float('inf')

    reasoning_steps.append(f"Income: {loan.income}, Debt: {loan.debt}, DTI: {dti:.2f}")

    approved = True
    if dti > 0.4:
        approved = False
        reasoning_steps.append(f"Applied policy {policy_id}: DTI > 0.4 → reject")
    if loan.employment_years < 2:
        approved = False
        reasoning_steps.append(f"Applied policy {policy_id}: Employment years < 2 → reject")

    logging.getLogger("audit").info(f"Reasoning chain: {reasoning_steps}")
    return {"approved": approved, "reasoning": reasoning_steps}


# ---------- Governed Memory ----------
class RememberRequest(BaseModel):
    user_id: str
    context: dict

@app.post("/api/remember")
async def remember_endpoint(payload: RememberRequest):
    token = MemoryGovernor.remember(payload.user_id, payload.context)
    return {"token": token}

@app.get("/api/recall/{token}")
async def recall_endpoint(token: str):
    context = MemoryGovernor.recall(token)
    if context is None:
        raise HTTPException(status_code=404, detail="Memory not found or expired")
    return context

@app.delete("/api/forget/{token}")
async def forget_endpoint(token: str):
    if MemoryGovernor.forget(token):
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Token not found")


# ---------- Serve React static files (must be last) ----------
app.mount("/", StaticFiles(directory="static", html=True), name="static")