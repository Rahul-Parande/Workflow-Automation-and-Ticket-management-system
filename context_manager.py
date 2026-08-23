from app.models.ticket_state import TicketState
from app.tools.context_tools import fetch_project_context

def context_node(state: TicketState) -> TicketState:
    print("\n Context Agent: Gathering project data...")
    
    if not state.board_id or not state.auth_token:
        print(" Missing board_id or token. Skipping context.")
        return state

    data = fetch_project_context(state.board_id, state.auth_token)
    
    state.board_users = data["users"]
    state.active_sprint_id = data["active_sprint_id"]
    state.next_sprint_id = data["next_sprint_id"]
    
    print(f" Found {len(state.board_users)} users and Sprint {state.active_sprint_id}")
    return state