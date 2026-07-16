from langchain_core.prompts import PromptTemplate


def construir_prompt_marketing(producto: str) -> str:
    template = "Eres un experto en marketing. Sugiere un eslogan creativo para un producto {producto}"
    prompt = PromptTemplate(template=template, input_variables=["producto"])
    return prompt.format(producto=producto)


if __name__ == "__main__":
    prompt_lleno = construir_prompt_marketing("café orgánico")
    print("Prompt generado:")
    print(prompt_lleno)