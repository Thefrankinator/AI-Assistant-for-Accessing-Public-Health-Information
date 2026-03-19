import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))



from langchain_community.vectorstores import FAISS # type: ignore
from langchain_core.tools import create_retriever_tool # type: ignore
from langchain.agents import create_agent # type: ignore
from dotenv import load_dotenv # type: ignore
from embeddings.embedding_generator import get_embedding_model
from langchain.agents.middleware import before_model, after_model ,  AgentState # type: ignore
from langchain.messages import AIMessage , HumanMessage , ToolMessage # type: ignore
from langgraph.runtime import Runtime # type: ignore
from typing import Any
import re
from datetime import datetime
from pathlib import Path
import json

load_dotenv()

vector_store = FAISS.load_local("data/faiss_vector_store", embeddings = get_embedding_model(), allow_dangerous_deserialization=True)

LOG_FILE = Path("data/logs/rag_queries.json")

MAX_CHARACTERS = 500

HEALTH_KEYWORDS = [
    # Medical
    "vaccin", "vaccination", "maladie", "symptôme", "traitement",
    "médicament", "dose", "virus", "infection", "épidémie",
    "diagnostic", "médecin", "hôpital", "santé", "patient",
    # Insurance / legal
    "amo", "ramed", "cnops", "anam", "assurance", "cotisation",
    "couverture", "remboursement", "régime", "affilié",
    # Moroccan health system
    "msps", "ministère", "pni", "programme", "maroc",
    # Diseases in your corpus
    "hépatite", "méningite", "rougeole", "poliomyélite",
    "tétanos", "tuberculose", "paludisme",
]



INJECTION_PATTERNS = [

    r"ignore (les|tes|vos|mes) instructions",
    r"ignore (le|ton|votre) (système|contexte|prompt)",
    r"oublie (tout|tes règles|le contexte|tes instructions)",
    r"ne (tiens|tenez) pas compte (de|des)",
    r"fais (comme si|semblant)",
    
    r"tu es maintenant",
    r"tu n'es plus",
    r"nouveau (rôle|personnage|assistant|système)",
    r"joue (le rôle|un rôle)",
    r"comporte(-toi)? comme",
    r"agis comme",
    r"prétends (être|que tu es)",


    r"(montre|affiche|répète|dis-moi) (ton|le|tes) (prompt|instructions|système|contexte|règles)",
    r"qu('|e )(est|était) (ton|votre) (prompt|instruction|système)",
    r"quel est ton (prompt|système|contexte)",


    r"jailbreak",
    r"DAN\b",                    
    r"mode (sans restriction|illimité|développeur|dev)",
    r"désactive (les|tes) (filtres|restrictions|règles)",

    r"prompt injection",
    r"(injecte|injection) (de|du) prompt",
    r"ignore (ce qui précède|ce qui suit)",
    r"fin (du|de) (contexte|prompt|système)",

    r"(donne|envoie|partage)-moi (ton|le|les) (contexte|documents|données|index|base)",
    r"quels (sont|étaient) (tes|les) documents",
    r"(liste|montre) (tous|toutes) (les|tes) (documents|sources|données)",
]


def create_faiss_retriever_tool(vector_store: FAISS):
    
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    return create_retriever_tool(
        retriever=retriever,
        name = "AAFAPHI_Retriever",
        description = "Useful for retrieving relevant chunks of information from the vector store based on a user query. Input should be a string query, output will be a list of relevant documents.")
    

def get_user_message(state: AgentState) -> str | None:
 
    if not state.get("messages"):
        return None

    # Find the last HumanMessage specifically
    for message in reversed(state["messages"]):
        if isinstance(message, HumanMessage):
            return message.content

    return None   # no human message found


@before_model(can_jump_to=["end"])
def guard_injection(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """
    Detect and block prompt injection attempts.
    """

    user_question = get_user_message(state)
    if user_question is None:
        return None

    text = user_question.lower()

    # Check every pattern
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text):
            return {
                "messages": [AIMessage(
                    "Cette requête n'est pas autorisée. "
                    "Je suis MedAssist, conçu uniquement pour répondre "
                    "aux questions de santé publique au Maroc. "
                    "Comment puis-je vous aider ?"
                )],
                "jump_to": "end"
            }

    return None   


@before_model(can_jump_to=["end"])
def guard_message_length(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """
    Block user messages that are too long.
    Prevents token waste and prompt flooding.
    """

    # Safely get user message
    user_question = get_user_message(state)
    if user_question is None:
        return None

    message_length = len(user_question)

    if message_length > MAX_CHARACTERS:
        return {
            "messages": [AIMessage(
                f"Votre message est trop long ({message_length} caractères). "
                f"Veuillez le limiter à {MAX_CHARACTERS} caractères maximum. "
                f"Essayez de reformuler votre question de manière plus concise."
            )],
            "jump_to": "end"
        }

    return None  



@after_model
def detect_fallback(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """
    Detect when the LLM couldn't find an answer and
    enrich the response with a helpful suggestion.
    """
    if not state.get("messages"):
        return None

    answer = state["messages"][-1].content.lower()


    if answer == "Je ne trouve pas cette information dans les documents disponibles." :

        current_answer = state["messages"][-1].content
        suggestion = (
            "\n\n💡 Suggestion: Pour plus d'informations, consultez :\n"
            "  • Le site du Ministère de la Santé : www.sante.gov.ma\n"
            "  • L'ANAM : www.anam.ma\n"
            "  • Votre médecin traitant."
        )

        return {
            "messages": list(state["messages"][:-1]) + [
                AIMessage(content=current_answer + suggestion)
            ]
        }

    return None




@after_model
def log_interaction(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """
    Log every question-answer pair to a JSON file.
    """
    
    if not state.get("messages"):
        return None

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Get last human question
    question = get_user_message(state)
    answer = state["messages"][-1].content
    

    list_metadata = []
    
    result = vector_store.similarity_search(question,k=3)
    list_metadata.append([doc.metadata for doc in result])
    
    entry = {
        "timestamp":   datetime.now().isoformat(),
        "question":    question,
        "answer":      answer,
        "answered":    len(answer.strip()) > 30,
        "answer_length": len(answer),
        "metadata": list_metadata  
    }

    # Load and append
    logs = []
    if LOG_FILE.exists():
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=4)

    return None



def invoke_agent(question : str) :
    agent = create_agent(
        model = 'gpt-4.1-mini',
        tools = [create_faiss_retriever_tool(vector_store)],
        middleware = [guard_message_length , guard_injection,detect_fallback,log_interaction],
        system_prompt = """Tu es un assistant spécialisé dans la santé publique au Maroc.
    Ton role est d'aider les utilisateurs à accéder à des informations fiables et pertinentes sur la santé publique au Maroc.
    Tu peux répondre à des questions sur les maladies, les vaccins, les symptômes, les traitements, les centres de santé,
    les campagnes de sensibilisation, et plus encore. Utilise les outils à ta disposition pour rechercher dans 
    ta base de données et fournir des réponses précises et utiles.
    Si la réponse n'est pas dans le contexte, réponds:
    "Je ne trouve pas cette information dans les documents disponibles."""
    )



    return  agent.invoke(
        {
            "messages": [HumanMessage(content=question)]
        }
    )

if __name__ == "__main__":
    question =  " C'est quoi l'AMO pour les etudiants ? "
    result  = invoke_agent(question)
    #print(result['messages'][-1].content)


    