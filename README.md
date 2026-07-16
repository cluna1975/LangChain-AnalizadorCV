# CV Analyzer con LangChain

Aplicación Streamlit para analizar currículums y evaluar el ajuste con un puesto específico usando LangChain.

## Requisitos

- Python 3.11+
- Entorno virtual en `venv`
- Dependencias de `requirements.txt`

## Instalación

```powershell
cd c:\SOURCE\curso_LangChain
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Configuración

Copia el ejemplo y ajusta tu clave o el proveedor local:

```powershell
copy .env.example .env
```

Variables recomendadas:

```env
OPENAI_API_KEY=tu-api-key-aqui
OPENAI_MODEL=gpt-4o-mini
MODEL_PROVIDER=openai

# Si usas Ollama local:
OLLAMA_MODEL=qwen2.5-coder:1.5b-base
OLLAMA_BASE_URL=http://localhost:11434
```

## Ejecución

```powershell
cd .\cv_analyzer
$env:PYTHONPATH='.'
python -m streamlit run app.py
```

## Observaciones

- Si `OPENAI_API_KEY` está presente, la app usará OpenAI.
- Si no está presente pero `OLLAMA_MODEL` está configurado, usará Ollama local.
- Si `MODEL_PROVIDER=ollama`, prioriza Ollama sobre OpenAI.
