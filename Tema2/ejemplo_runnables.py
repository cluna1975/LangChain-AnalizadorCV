from langchain_core.runnables import RunnableLambda


def numero_a_texto(x):
    return f"Numero {x}"


def duplicar_texto(texto):
    return [texto] * 2


if __name__ == "__main__":
    paso1 = RunnableLambda(numero_a_texto)
    paso2 = RunnableLambda(duplicar_texto)
    cadena = paso1 | paso2

    resultado = cadena.invoke(43)
    print("Resultado del runnable:")
    print(resultado)