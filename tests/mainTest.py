import logging
from utils.utils import load_settings, setup_logging
from langchain_core.prompts import ChatPromptTemplate
from src.Controller import conversion_controller, loading_controller, Chunking_controller, embedding_controller, \
    Store_controller, llm_controller
from pathlib import Path

logger = logging.getLogger(__name__)
config = load_settings(file_path=r"D:\@Ehab_Training\@RAG\Code\NaiveRAG\config\settings.json")
setup_logging()

# Convert Documents
conversion_controller(config)

# Load the Document
docs = loading_controller(config)

# chunking the Document
Chunks = Chunking_controller(config, docs)

# embedding the Document
embed = embedding_controller(config)

# create Chroma
db = Store_controller(config, Chunks, embed)

query = 'خطوات اتباع القوانين'
docs_chroma = db.similarity_search_with_score(query , 2)
context_text = "\n\n".join([doc.page_content for doc, _score in docs_chroma])


llm = llm_controller(config)
PROMPT_TEMPLATE = config.get("prompt", {}).get("llm_prompt", "Answer the following Question")

prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
prompt = prompt_template.format(context=context_text, question=query)


response = llm.predict(prompt)








