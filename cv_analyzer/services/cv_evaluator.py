import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from models.cv_model import AnalisisCV
from prompts.cv_prompts import crear_sistema_prompts

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env", override=False)


def _crear_modelo_base():
    api_key = os.getenv("OPENAI_API_KEY")
    provider = os.getenv("MODEL_PROVIDER", "openai").strip().lower()

    if provider == "ollama":
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "qwen2.5-coder:1.5b-base"),
            temperature=0.1,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        )

    if api_key:
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.4,
            api_key=api_key,
        )

    ollama_model = os.getenv("OLLAMA_MODEL")
    if ollama_model:
        return ChatOllama(
            model=ollama_model,
            temperature=0.1,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        )

    raise ValueError(
        "No hay proveedor configurado. Define OPENAI_API_KEY o OLLAMA_MODEL "
        "en el archivo .env."
    )


@lru_cache(maxsize=1)
def crear_evaluador_cv():
    modelo_base = _crear_modelo_base()
    modelo_estructurado = modelo_base.with_structured_output(AnalisisCV)
    chat_prompt = crear_sistema_prompts()
    return chat_prompt | modelo_estructurado


def evaluar_candidato(texto_cv: str, descripcion_puesto: str) -> AnalisisCV:
    try:
        cadena_evaluacion = crear_evaluador_cv()
        resultado = cadena_evaluacion.invoke({
            "texto_cv": texto_cv,
            "descripcion_puesto": descripcion_puesto,
        })
        return resultado

    except Exception:
        return AnalisisCV(
            nombre_candidato="Error en procesamiento.",
            experiencia_años=0,
            habilidades_clave=["Error al procesar CV"],
            education="No se puede determinar.",
            experiencia_relevante="Error durante el análisis.",
            fortalezas=["Requiere revisión manual del CV"],
            areas_mejora=["Verificar formato y legibilidad del PDF"],
            porcentaje_ajuste=0,
        )
