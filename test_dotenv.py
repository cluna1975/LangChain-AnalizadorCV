from dotenv import load_dotenv
import os

print("🔍 Probando carga del archivo .env...")

# Cargar .env
load_dotenv()

# Leer la variable
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("✅ ¡El archivo .env se cargó correctamente!")
    print(f"   OPENAI_API_KEY encontrada: {api_key[:8]}...{api_key[-4:]}")
else:
    print("❌ No se pudo encontrar OPENAI_API_KEY en el .env")
