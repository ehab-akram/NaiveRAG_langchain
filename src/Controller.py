import logging

from src.Nodes.Chunker import Markdown_chunking
from src.Nodes.Convertor_MD import ConvertorToMD
from src.Nodes.Loader import load_documents
from src.Nodes.Model_llm import llama_llm
from src.Nodes.Store import chroma_store
from src.Nodes.embedder import HuggingFace_Embedding
from pathlib import Path

logger = logging.getLogger(__name__)


def conversion_controller(config):
    enable_conversion = config.get("ConvertorToMD", {}).get("enable_convertor", True)
    input_dir = config.get("Directions", {}).get("input_dir", "Unknown")
    output_dir = config.get("Directions", {}).get("Converted_dir", "Unknown")
    input_dir = Path(input_dir).resolve()
    output_dir = Path(output_dir).resolve()
    if enable_conversion:
        logger.info("Document conversion is enabled.")
        convertor = ConvertorToMD(input_dir=input_dir, output_dir=output_dir)
        convertor.document_checker()
    else:
        logger.info("Document conversion is disabled.")


def loading_controller(config):
    logger.info("Start Loading Directory")
    directory_path = Path(config.get("Directions", {}).get("Converted_dir", "unknown")).resolve()
    docs = load_documents(directory_path)
    return docs


def Chunking_controller(config, docs):
    logger.info("Start Chunking  Documents")
    strip_headers = config.get("Chunking", {}).get("strip_headers", True)
    return_each_line = config.get("Chunking", {}).get("return_each_line", False)
    text = ''.join(doc.page_content for doc in docs)
    chunks = Markdown_chunking(strip_headers, return_each_line, text)

    logger.info(f"Successfully Chunking {len(chunks)}  Documents")
    return chunks


def embedding_controller(config):
    model_name = config.get("embedding", {}).get("model_name")
    normalize_embeddings = config.get("embedding", {}).get("normalize_embeddings")
    batch_size = config.get("embedding", {}).get("batch_size")
    logger.info(f"loading embedding Model {model_name}")
    embed = HuggingFace_Embedding(model_name, normalize_embeddings, batch_size)
    return embed


def Store_controller(config, chunks, embedd):
    persist_directory = str(Path(config.get("Directions", {}).get("persist_directory")).resolve())
    collection_name = config.get("Directions", {}).get("collection_name")
    logger.info("Creating Vector_Store ...")
    db = chroma_store(chunks, embedd, persist_directory, collection_name)

    return db


def llm_controller(config):
    model_name = config.get("model", {}).get("model_name")
    temperature = config.get("model", {}).get("temperature")
    num_predict = config.get("model", {}).get("num_predict")
    llm = llama_llm(model_name, temperature, num_predict)
    return llm

