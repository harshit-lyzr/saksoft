from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()
# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()


class Conversation(BaseModel):
    agent_id: str
    question: str
    agent_answer: str
    admin_answer: Optional[str] = None


# Endpoint to retrieve conversations by agent_id
@app.get("/conversations/{agent_id}")
async def get_conversations(agent_id: str):
    conversations = supabase.table('saksoft').select('*').eq('agent_id', agent_id).execute()
    if conversations.data:
        return conversations.data
    raise HTTPException(status_code=404, detail="Conversations not found for the agent_id")


# Endpoint to add conversation
@app.post("/conversations/", status_code=201)
async def add_conversation(conversation: Conversation):
    data = {
        "agent_id": conversation.agent_id,
        "question": conversation.question,
        "agent_answer": conversation.agent_answer,
        "admin_answer": conversation.admin_answer
    }

    response = supabase.table('saksoft').insert(data).execute()

    if response:
        return {"message": "Conversation added successfully"}

    raise HTTPException(status_code=400, detail="Failed to add conversation")

# Endpoint to update conversation by ID
@app.put("/conversations/{id}", status_code=200)
async def update_conversation(id: int, conversation: Conversation):
    # Update the conversation with the provided ID
    response = supabase.table('saksoft').update({
        "agent_id": conversation.agent_id,
        "question": conversation.question,
        "agent_answer": conversation.agent_answer,
        "admin_answer": conversation.admin_answer
    }).eq('id', id).execute()

    if response.data:
        return response.data
    raise HTTPException(status_code=404, detail="Conversation not found or failed to update")

# Endpoint to delete conversation by ID
@app.delete("/conversations/{id}", status_code=200)
async def delete_conversation(id: int):
    # Delete the conversation with the provided ID
    response = supabase.table('saksoft').delete().eq('id', id).execute()

    if response.data:
        return {"message": "Conversation deleted successfully"}
    raise HTTPException(status_code=404, detail="Conversation not found or failed to delete")
