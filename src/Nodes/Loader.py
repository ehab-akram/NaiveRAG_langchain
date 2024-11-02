import logging

from langchain_community.document_loaders import DirectoryLoader, TextLoader

logger = logging.getLogger(__name__)


def load_documents(path):
    # loading the Files
    text_loader_kwargs = {"autodetect_encoding": True}
    loader = DirectoryLoader(path=path, glob="**/*.txt", show_progress=True,
                             loader_cls=TextLoader, silent_errors=True, loader_kwargs=text_loader_kwargs,
                             use_multithreading=True)
    docs = loader.load()

    logger.info(f"Successfully Loading  {len(docs)} Documents")
    return docs
