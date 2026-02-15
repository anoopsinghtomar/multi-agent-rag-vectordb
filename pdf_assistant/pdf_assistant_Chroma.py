import typer
import os
from typing import Optional, List
from phi.assistant import Assistant
from phi.storage.assistant.local import SQLiteAssistantStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# ---------------------------
# Knowledge base (Chroma)
# ---------------------------
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=Chroma(
        collection="recipes",
        persist_directory="./chroma_db"
    )
)

# ---------------------------
# Storage (SQLite)
# ---------------------------
storage = SQLiteAssistantStorage(
    table_name="pdf_assistant",
    db_url=os.getenv("DATABASE_URL")
)

def pdf_assistant(new: bool = False, user: str = "user"):
    run_id: Optional[str] = None

    if not new:
        existing_run_ids: List[str] = storage.get_all_run_ids(user=user)
        if len(existing_run_ids) > 0:
            run_id = existing_run_ids[0]

    assistant = Assistant(
        run_id=run_id,
        user_id=user,
        knowledge_bases=[knowledge_base],
        storage=storage,
        show_tool_calls=True,
        search_knowledge_bases=True,
        read_chat_history=True
    )

    if run_id is None:
        run_id = assistant.run_id
        print(f"New assistant created with run_id: {run_id}")
    else:
        print(f"Using existing assistant with run_id: {run_id}")

    assistant.cli_app(markdown=True)

if __name__ == "__main__":
    typer.run(pdf_assistant)
