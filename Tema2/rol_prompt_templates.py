from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate


def construir_prompt_rol() -> ChatPromptTemplate:
    plantilla_sistema = SystemMessagePromptTemplate.from_template(
        "Eres un {rol} especializado en {especialidad}. Responde de manera {tono}"
    )

    plantilla_humano = HumanMessagePromptTemplate.from_template(
        "Mi pregunta sobre {tema} es: {pregunta}"
    )

    return ChatPromptTemplate.from_messages([
        plantilla_sistema,
        plantilla_humano,
    ])


if __name__ == "__main__":
    chat_prompt = construir_prompt_rol()
    mensajes = chat_prompt.format_messages(
        rol="nutricionista",
        especialidad="dietas veganas",
        tono="profesional pero accesible",
        tema="proteínas vegetales",
        pregunta="¿Cuáles son las mejores fuentes de proteína vegana para un atleta profesional?",
    )

    print("Prompt con rol renderizado:")
    for mensaje in mensajes:
        print(mensaje.content)