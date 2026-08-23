from app.models.ticket_state import TicketState

def estimation_node(state: TicketState) -> TicketState:
    print("\n Scrum Master Agent: Estimating effort...")
    
    for ticket in state.intent_data:
        tech = ticket.get("techstack", "").lower()
        desc_len = len(ticket.get("description", ""))
        
        # Simple heuristic logic (You can replace this with another LLM call if you want)
        points = 1
        
        if "backend" in tech or "api" in tech:
            points = 3
        if "frontend" in tech and "page" in ticket.get("title", "").lower():
            points = 5
        if "devops" in tech:
            points = 8
        if desc_len > 200: # If description is huge, it's complex
            points += 2
            
        # Snap to Fibonacci
        allowed = [1, 2, 3, 5, 8, 13]
        points = min(allowed, key=lambda x: abs(x - points))
        
        ticket["story_points"] = points
        ticket["priority"] = "High" if points >= 8 else "Medium"
        
        print(f" Rated '{ticket['title']}' as {points} SP")

    return state