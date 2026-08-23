import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.ticket_state import TicketState
from dotenv import load_dotenv

load_dotenv()
# Load API Key securely
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0.2)

ARCHITECT_PROMPT = """
You are a Senior Software Architect. 
Your goal is to decompose the user's request into actionable technical tickets.

User Request: {input}

RULES:
1. Break goals into atomic tasks (Frontend, Backend, DevOps, DB).
2. Write a clear Title and a DETAILED Description (Goals, Tech Constraints, Validation).
3. Assign a 'techstack' from: ["Frontend", "Backend", "Devops", "Data", "Design"].
4. Do NOT assign users. Do NOT estimate points.

Output strictly valid JSON list of objects:
[{{ "title": "...", "description": "...", "techstack": "...", "intent": "create_ticket" }}]
"""

def architect_node(state: TicketState) -> TicketState:
    print("\n Architect Agent: Designing the solution...")
    
    response = llm.invoke(ARCHITECT_PROMPT.format(input=state.user_input))
    content = response.content.strip().replace("```json", "").replace("```", "")
    
    try:
        tickets = json.loads(content)
        # We initialize the tickets with basic data
        state.intent_data = tickets
        print(f"✅ Generated {len(tickets)} draft tickets.")
        return {"intent_data": tickets}
    except Exception as e:
        print(f"Architect Error: {e}")
        state.intent_data = []
        return {"intent_data": []}