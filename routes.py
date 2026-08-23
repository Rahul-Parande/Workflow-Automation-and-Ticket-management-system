from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.core.builder import get_planning_graph, get_refinement_graph, get_execution_graph

router = APIRouter(tags=["AI Ticket Agents"])

# --- 1. SCHEMAS (What Node.js sends to Python) ---

class SprintPlanRequest(BaseModel):
    goal: str
    board_id: str
    board_users: List[Dict[str, Any]]  # Node.js passes the users here!
    active_sprint_id: Optional[str] = None

class RefineTicketRequest(BaseModel):
    instruction: str
    ticket: Dict[str, Any]

class ExecuteTicketsRequest(BaseModel):
    approved_tickets: List[Dict[str, Any]]
    auth_token: str # Passed from Node so Python can call Node back

# --- 2. ENDPOINTS ---

@router.post("/plan")
async def generate_sprint_plan(request: SprintPlanRequest):
    try:
        workflow = get_planning_graph()
        initial_state = {
            "user_input": request.goal,
            "board_id": request.board_id,
            "board_users": request.board_users,
            "active_sprint_id": request.active_sprint_id,
            "intent_data": []
        }
        
        result = workflow.invoke(initial_state)
        return {"draft_tickets": result.get("intent_data", [])}
        
    except Exception as e:
        # 🟢 FIX: Print the actual error to the console!
        print(f"🔥 CRASH IN PLAN ROUTE: {e}") 
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/refine")
async def refine_single_ticket(request: RefineTicketRequest):
    """
    PHASE 2: User clicks "Refine" on a single ticket in the UI.
    """
    try:
        workflow = get_refinement_graph()
        
        initial_state = {
            "user_input": request.instruction,
            # We pass the single ticket as a list of 1 item
            "intent_data": [request.ticket] 
        }
        
        result = workflow.invoke(initial_state)
        
        # Return the single updated ticket
        updated_ticket = result.get("intent_data", [])[0] if result.get("intent_data") else request.ticket
        return {"updated_ticket": updated_ticket}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute")
async def execute_approved_plan(request: ExecuteTicketsRequest):
    """
    PHASE 3: User approves the list. Python sends them to the Node database.
    """
    try:
        workflow = get_execution_graph()
        
        initial_state = {
            "intent_data": request.approved_tickets,
            "auth_token": request.auth_token
        }
        
        result = workflow.invoke(initial_state)
        return {"status": "success", "results": result.get("intent_data", [])}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))