from pathlib import Path
from langchain.prompts import ChatPromptTemplate
import uvicorn
from fastapi import FastAPI
import requests
import logging
from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from pydantic import BaseModel
from src.Controller import conversion_controller, loading_controller, Chunking_controller, embedding_controller, \
    Store_controller, llm_controller
from utils.utils import setup_logging, load_settings

Config_file_path = str(Path("..\\..\\config\\settings.json").resolve())
config = load_settings(file_path=Config_file_path)
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Naive RAG Server",
    version="0.1",
    description="Simple APi server used for calling Naive RAG"
)


class QueryRequest(BaseModel):
    query: str


db_instance = None


@app.post("/Init_model")
def Init_model():
    global db_instance
    conversion_controller(config)

    # Load the Document
    docs = loading_controller(config)

    # chunking the Document
    Chunks = Chunking_controller(config, docs)

    # embedding the Document
    embed = embedding_controller(config)

    db_instance = Store_controller(config, Chunks, embed)
    return {"Chroma": "Vector Store Created Successfully"}


@app.post("/query")
def generate_answer(query_request: QueryRequest):
    global db_instance

    try:
        if db_instance is None:
            logger.info("Load Vector Store")
            persist_directory = str(Path(config.get("Directions", {}).get("persist_directory")).resolve())
            db_instance = Chroma(persist_directory=persist_directory, embedding_function=embedding_controller(config))

        docs_chroma = db_instance.similarity_search_with_score(query_request.query, 2)
        context_text = "\n\n".join([doc.page_content for doc, _score in docs_chroma])

        # Initialize LLM and create prompt
        llm = llm_controller(config)
        system_message = config.get("prompt", {}).get("system_message_llm", "Answer the following Question")
        human_message = config.get("prompt", {}).get("human_message_llm", "Answer the following Question")

        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", human_message),
        ])

        chain = chat_prompt | llm

        # LLM invocation
        response = chain.invoke({
            "query": query_request.query,
            "context": context_text
        })

        return {"response": response.content}
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        return {"error": f"Error generating answer: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000)
