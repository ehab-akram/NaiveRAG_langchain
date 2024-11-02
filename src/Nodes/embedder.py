from langchain_huggingface import HuggingFaceEmbeddings


def HuggingFace_Embedding(model_name, normalize_embeddings, batch_size):
    encode_kwargs = {
        'normalize_embeddings': normalize_embeddings,
        'batch_size': batch_size,
    }
    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs=encode_kwargs
    )
    return hf
