import os
from pathlib import Path

import ollama
import streamlit as st
from dotenv import load_dotenv
from google import genai
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from openai import OpenAI

# Carga del .env más cercano al script
script_dir = Path(__file__).resolve().parent
local_dotenv = script_dir / '.env'
root_dotenv = script_dir.parent / '.env'
load_dotenv(dotenv_path=local_dotenv, override=False)
if not (
    os.getenv('OPENAI_API_KEY')
    or os.getenv('GEMINI_API_KEY')
    or os.getenv('GOOGLE_API_KEY')
    or os.getenv('OLLAMA_MODEL')
):
    load_dotenv(dotenv_path=root_dotenv, override=False)


def _format_history(history):
    texto = []
    for item in history:
        if item["role"] == "user":
            texto.append(f"Usuario: {item['content']}")
        else:
            texto.append(f"Asistente: {item['content']}")
    return "\n".join(texto)


def _build_chat_model(provider, temperature, model_name):
    if provider == "OpenAI":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Falta OPENAI_API_KEY en el archivo .env.")
        return ChatOpenAI(model=model_name, temperature=temperature, api_key=api_key)

    if provider == "Gemini":
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Falta GEMINI_API_KEY o GOOGLE_API_KEY en el archivo .env.")
        return ChatGoogleGenerativeAI(model=model_name, temperature=temperature, api_key=api_key)

    return ChatOllama(model=model_name, temperature=temperature)


def _get_ollama_models():
    default_model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:1.5b-base")
    try:
        response = ollama.list()
        models = getattr(response, "models", [])
        names = [model.model for model in models if getattr(model, "model", None)]
        return names or [default_model]
    except Exception:
        return [default_model]


def _get_openai_models():
    default_models = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return default_models

    try:
        client = OpenAI(api_key=api_key)
        page = client.models.list()
        data = getattr(page, "data", None) or list(page)
        names = []
        for item in data:
            model_id = getattr(item, "id", None) or item.get("id")
            if model_id:
                names.append(model_id)
        return names or default_models
    except Exception:
        return default_models


def _get_gemini_models():
    default_models = ["gemini-2.5-flash", "gemini-2.0-flash"]
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return default_models

    try:
        client = genai.Client(api_key=api_key)
        pager = client.models.list()
        items = list(pager)
        names = []
        for item in items:
            name = getattr(item, "name", None)
            if name:
                names.append(name.replace("models/", ""))
        return names or default_models
    except Exception:
        return default_models


def _provider_status_label(provider):
    if provider == "OpenAI":
        return "🟢 OpenAI" if os.getenv("OPENAI_API_KEY") else "🔴 OpenAI"
    if provider == "Gemini":
        return "🟢 Gemini" if (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")) else "🔴 Gemini"
    ollama_models = _get_ollama_models()
    return "🟢 Ollama" if ollama_models else "🟡 Ollama"


# Configuración inicial
st.set_page_config(page_title="Chatbot MultiProveedor", page_icon="🤖")
st.title("🤖 Chatbot MultiProveedor con LangChain")
st.markdown("Prueba Ollama, OpenAI y Gemini desde la misma interfaz. Elige el proveedor, ajusta la temperatura y chatea.")

with st.sidebar:
    st.header("Configuración")
    provider = st.selectbox("Proveedor", ["OpenAI", "Gemini", "Ollama"])
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)

    if provider == "OpenAI":
        openai_models = _get_openai_models()
        model_name = st.selectbox("Modelo", openai_models)
    elif provider == "Gemini":
        gemini_models = _get_gemini_models()
        model_name = st.selectbox("Modelo", gemini_models)
    else:
        ollama_models = _get_ollama_models()
        model_name = st.selectbox("Modelo Ollama", ollama_models)

    st.caption("Estado del proveedor: " + _provider_status_label(provider))

    if st.button("🧪 Probar conexión", use_container_width=True):
        try:
            test_model = _build_chat_model(provider, temperature, model_name)
            st.success(f"Conexión preparada con {provider} usando {model_name}.")
        except Exception as error:
            st.error(f"No se pudo preparar la conexión: {error}")

# Inicializar historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""Eres un asistente útil y amigable llamado ChatBot Pro.

Historial de conversación:
{historial}

Responde de manera clara y concisa a la siguiente pregunta: {mensaje}"""
)

try:
    chat_model = _build_chat_model(provider, temperature, model_name)
except Exception as error:
    st.warning(str(error))
    st.stop()

cadena = prompt_template | chat_model

for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

if st.button("🗑️ Nueva conversación"):
    st.session_state.mensajes = []
    st.rerun()

pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            for chunk in cadena.stream(
                {
                    "mensaje": pregunta,
                    "historial": _format_history(st.session_state.mensajes),
                }
            ):
                content = getattr(chunk, "content", str(chunk))
                full_response += content
                response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_response))

    except Exception as error:
        mensaje = str(error).lower()
        if provider == "OpenAI" and (
            '429' in mensaje or 'insufficient' in mensaje or 'quota' in mensaje or 'exhausted' in mensaje
        ):
            st.error("Tu saldo o cuota de OpenAI está agotado o no está disponible.")
        elif provider == "Gemini" and (
            '429' in mensaje or 'resource_exhausted' in mensaje or 'prepayment credits' in mensaje
        ):
            st.error("Tu cuenta de Gemini no tiene saldo disponible o los créditos están agotados.")
        elif provider == "Gemini" and ('api key not valid' in mensaje or 'api_key_invalid' in mensaje):
            st.error("La API key de Gemini no es válida.")
        elif provider == "OpenAI" and ('api key' in mensaje and 'invalid' in mensaje):
            st.error("La API key de OpenAI no es válida.")
        else:
            st.error(f"Error al generar respuesta: {error}")

        st.info("Revisa la configuración del proveedor en el archivo .env o en la configuración del sidebar.")