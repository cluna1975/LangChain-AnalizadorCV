import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

script_dir = Path(__file__).resolve().parent
local_dotenv = script_dir / '.env'
root_dotenv = script_dir.parent / '.env'

load_dotenv(dotenv_path=local_dotenv, override=False)
if not os.getenv('GEMINI_API_KEY') and not os.getenv('GOOGLE_API_KEY'):
    load_dotenv(dotenv_path=root_dotenv, override=False)

modelo_ollama = os.getenv('OLLAMA_MODEL', 'qwen2.5-coder:1.5b-base')
modelo_gemini = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
pregunta = 'Escribe una función en Python que verifique si una palabra es un palíndromo'

print(f'🧠 Pregunta: {pregunta}')
print(f'⚡ Intentando primero con Ollama ({modelo_ollama})...')

try:
    llm = ChatOllama(model=modelo_ollama, temperature=0.7)
    respuesta = llm.invoke(pregunta)
    print('\n💬 Respuesta desde Ollama:')
    print(respuesta.content)
except Exception as error:
    mensaje = str(error).lower()
    if '10061' in mensaje or 'connecterror' in mensaje or 'connection refused' in mensaje:
        print('\n⚠️ Ollama no está disponible en localhost.')
        print('Inicia el servidor con: ollama serve')
        print('Y asegúrate de que el modelo exista con: ollama pull ' + modelo_ollama)
    else:
        print(f'\n⚠️ Ollama no respondió: {error}')

    if not api_key:
        print('\n⚠️ No hay API key de Gemini disponible en el archivo .env.')
        raise SystemExit('Falta GEMINI_API_KEY o GOOGLE_API_KEY para usar Gemini.')

    print(f'⚡ Consultando a Gemini ({modelo_gemini})...')
    try:
        llm = ChatGoogleGenerativeAI(model=modelo_gemini, temperature=0.7, api_key=api_key)
        respuesta = llm.invoke(pregunta)
        print('\n💬 Respuesta desde Gemini:')
        print(respuesta.content)
    except Exception as error:
        mensaje = str(error).lower()
        if '429' in mensaje or 'resource_exhausted' in mensaje or 'prepayment credits' in mensaje:
            print('\n⚠️ Tu cuenta de Gemini no tiene saldo disponible o los créditos están agotados.')
            print('Recarga o revisa tu proyecto en Google AI Studio.')
        elif '401' in mensaje or 'invalid api key' in mensaje or 'api_key_invalid' in mensaje:
            print('\n⚠️ La API key de Gemini no es válida.')
            print('Comprueba GEMINI_API_KEY o GOOGLE_API_KEY en el archivo .env.')
        else:
            print(f'\n⚠️ Error al consultar Gemini: {error}')
            raise
