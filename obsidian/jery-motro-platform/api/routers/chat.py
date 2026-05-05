from fastapi import APIRouter
from schemas.chat import ChatRequest, ChatResponse
from services.rag_service import RAGService

router = APIRouter(prefix="/api/chat", tags=["JeryMotro AI (RAG)"])

@router.post("/", response_model=ChatResponse)
def ask_jerymotro_ai(request: ChatRequest):
    """
    Interroge JeryMotro AI avec une question en langage naturel.
    Retourne la réponse du LLM (Groq) basée sur le contexte (ChromaDB).
    """
    result = RAGService.generate_response(request.message)
    return result
