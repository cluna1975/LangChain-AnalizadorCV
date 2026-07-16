import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

script_dir = Path(__file__).resolve().parent
local_dotenv = script_dir / '.env'
root_dotenv = script_dir.parent / '.env'

load_dotenv(dotenv_path=local_dotenv, override=False)
if not os.getenv('OPENAI_API_KEY') and not os.getenv('OLLAMA_MODEL'):
    load_dotenv(dotenv_path=root_dotenv, override=False)

modelo_ollama = os.getenv('OLLAMA_MODEL', 'qwen2.5-coder:1.5b-base')
modelo_openai = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
api_key = os.getenv('OPENAI_API_KEY')

plantilla = PromptTemplate(
    input_variables=['nombre'],
    template='Saluda al usuario con su nombre.\nNombre del usuario: {nombre}\nAsistente:'
)

print('🧠 Ejecutando cadena avanzada...')
print(f'⚡ Intentando primero con Ollama ({modelo_ollama})...')

try:
    chat = ChatOllama(model=modelo_ollama, temperature=0.7)
    chain = plantilla | chat
    resultado = chain.invoke({'nombre': 'Carlos'})
    print('\n💬 Respuesta desde Ollama:')
    print(resultado.content)
except Exception as error:
    mensaje = str(error).lower()
    if '10061' in mensaje or 'connecterror' in mensaje or 'connection refused' in mensaje:
        print('\n⚠️ Ollama no está disponible en localhost.')
        print('Inicia el servidor con: ollama serve')
        print('Y asegúrate de que el modelo exista con: ollama pull ' + modelo_ollama)
    else:
        print(f'\n⚠️ Ollama no respondió: {error}')

    if not api_key:
        print('\n⚠️ No hay API key de OpenAI disponible en el archivo .env.')
        raise SystemExit('Falta OPENAI_API_KEY para usar OpenAI.')

    print(f'⚡ Consultando a OpenAI ({modelo_openai})...')
    try:
        chat = ChatOpenAI(model=modelo_openai, temperature=0.7, api_key=api_key)
        chain = plantilla | chat
        resultado = chain.invoke({'nombre': 'Carlos'})
        print('\n💬 Respuesta desde OpenAI:')
        print(resultado.content)
    except Exception as error:
        mensaje = str(error).lower()
        if '429' in mensaje or 'insufficient' in mensaje or 'quota' in mensaje or 'exhausted' in mensaje:
            print('\n⚠️ Tu saldo o cuota de OpenAI está agotado o no está disponible.')
            print('Revisa el crédito de tu cuenta en OpenAI Platform.')
        elif '401' in mensaje or 'invalid api key' in mensaje:
            print('\n⚠️ La API key de OpenAI no es válida.')
            print('Comprueba OPENAI_API_KEY en el archivo .env.')
        else:
            print(f'\n⚠️ Error al consultar OpenAI: {error}')
            raise