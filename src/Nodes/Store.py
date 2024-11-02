from langchain_community.vectorstores import Chroma


def chroma_store(chunks, embed, persist_directory, collection_name):
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embed,
        collection_name=collection_name,
        persist_directory=persist_directory,

    )

    return db
