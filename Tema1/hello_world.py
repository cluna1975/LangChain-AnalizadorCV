import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

script_dir = Path(__file__).resolve().parent
local_dotenv = script_dir / '.env'
root_dotenv = script_dir.parent / '.env'

load_dotenv(dotenv_path=local_dotenv, override=False)
if not os.getenv('OLLAMA_MODEL'):
    load_dotenv(dotenv_path=root_dotenv, override=False)

modelo = os.getenv('OLLAMA_MODEL', 'qwen2.5-coder:1.5b-base')
pregunta = 'Escribe una función en Python que verifique si una palabra es un palíndromo'

print(f'🧠 Pregunta: {pregunta}')
print(f'⚡ Consultando a Ollama ({modelo})...')

try:
    llm = ChatOllama(model=modelo, temperature=0.7)
    respuesta = llm.invoke(pregunta)
    print('\n💬 Respuesta:')
    print(respuesta.content)
except Exception as error:
    mensaje = str(error).lower()
    if '10061' in mensaje or 'connecterror' in mensaje or 'connection refused' in mensaje:
        print('\n⚠️ Ollama no está disponible en localhost.')
        print('Inicia el servidor con: ollama serve')
        print('Y asegúrate de que el modelo exista con: ollama pull ' + modelo)
    else:
        print(f'\n⚠️ Error al consultar Ollama: {error}')
