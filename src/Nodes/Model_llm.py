from langchain_ollama.chat_models import ChatOllama


def llama_llm(model_name, temperature, num_predict):
    model = ChatOllama(
        model=model_name,
        temperature=temperature,
        num_predict=num_predict
    )

    return model
