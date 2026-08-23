from app.models.ticket_state import TicketState
from app.utils.ticket_id import generate_ticket_id
from app.services.assigner import assign_tickets as logic_assignment

def staffing_node(state: TicketState) -> dict:
    print("\n⏱️ Staffing Agent: Estimating points & Assigning users...")
    
    # --- 1. ESTIMATION PHASE ---
    for ticket in state.intent_data:
        tech = ticket.get("techstack", "").lower()
        desc_len = len(ticket.get("description", ""))
        
        # Base logic for story points
        points = 1
        if "backend" in tech or "api" in tech or "data" in tech:
            points = 3
        if "frontend" in tech:
            points = 2
        if "devops" in tech or "architect" in tech:
            points = 5
            
        # Bump up points for long/complex descriptions
        if desc_len > 200: 
            points += 2
            
        # Snap to Fibonacci (1, 2, 3, 5, 8)
        allowed = [1, 2, 3, 5, 8]
        points = min(allowed, key=lambda x: abs(x - points))
        
        # Inject the calculated points into the ticket!
        ticket["story_points"] = points
        ticket["priority"] = "High" if points >= 5 else "Medium"
        
        print(f"   🔹 Estimated '{ticket.get('title')}' at {points} SP")

    # --- 2. ASSIGNMENT PHASE ---
    # Now it goes to your logic with the points included
    updated_state = logic_assignment(state)
    
    return {"intent_data": updated_state.intent_data}