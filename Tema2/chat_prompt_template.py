from langchain_core.prompts import ChatPromptTemplate


def construir_prompt_traduccion() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", "Eres un traductor del español al inglés muy preciso."),
        ("human", "{texto}"),
    ])


if __name__ == "__main__":
    chat_prompt = construir_prompt_traduccion()
    mensajes = chat_prompt.format_messages(texto="Hola mundo, ¿cómo estás?")

    print("Prompt renderizado:")
    for mensaje in mensajes:
        print(f"[{mensaje.type}] {mensaje.content}")