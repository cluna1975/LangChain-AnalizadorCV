from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def construir_prompt_con_historial() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente útil que mantiene el contexto de la conversación."),
        MessagesPlaceholder(variable_name="historial"),
        ("human", "Usuario: {pregunta_actual}"),
    ])


if __name__ == "__main__":
    chat_prompt = construir_prompt_con_historial()

    historial_conversacion = [
        HumanMessage(content="Usuario: ¿Cuál es la capital de Francia?"),
        AIMessage(content="IA: La capital de Francia es París."),
        HumanMessage(content="Usuario: ¿Y cuántos habitantes tiene?"),
        AIMessage(content="IA: París tiene aproximadamente 2.2 millones de habitantes en la ciudad propiamente dicha."),
    ]

    mensajes = chat_prompt.format_messages(
        historial=historial_conversacion,
        pregunta_actual="¿Puedes decirme algo interesante de su arquitectura?",
    )

    print("Prompt con historial renderizado:")
    for mensaje in mensajes:
        print(mensaje.content)