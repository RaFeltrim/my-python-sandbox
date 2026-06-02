import os
import sys
import google.generativeai as genai

# Tenta carregar a chave de um arquivo local api_key.txt (ignorado pelo git)
# Caso não exista, busca na variável de ambiente GEMINI_API_KEY
key_file = "api_key.txt"
api_key = None

if os.path.exists(key_file):
    with open(key_file, "r", encoding="utf-8") as f:
        api_key = f.read().strip()
else:
    api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Erro: Chave de API não encontrada.")
    print("Por favor, crie um arquivo 'api_key.txt' com a sua chave de API do Gemini ou configure a variável de ambiente GEMINI_API_KEY.")
    sys.exit(1)

genai.configure(api_key=api_key)

# Lê todos os arquivos de estudo locais para servir de contexto
context = ""
estudos_dir = ".estudos"

if os.path.exists(estudos_dir):
    for filename in os.listdir(estudos_dir):
        # Lê apenas os arquivos Markdown de referência
        if filename.endswith(".md") and "NotebookLM_" in filename:
            path = os.path.join(estudos_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                context += f"\n--- FONTE: {filename} ---\n{f.read()}\n"

# Verifica se a pergunta foi passada como argumento
if len(sys.argv) < 2:
    print("Uso: python ask_gemini.py \"Sua pergunta aqui\"")
    sys.exit(1)

pergunta = sys.argv[1]

# Envia o contexto junto com a pergunta para o Gemini
model = genai.GenerativeModel('gemini-3.5-flash')
prompt = f"""
Você é um assistente de prova. Use estritamente as fontes fornecidas abaixo para responder a pergunta.
Se as fontes não contiverem a informação, use seu conhecimento geral de DDD, SOLID e Python.

Fontes de referência:
{context}

Pergunta:
{pergunta}
"""

print("Consultando Gemini...")
try:
    response = model.generate_content(prompt)
    print("\n=== RESPOSTA ===")
    print(response.text)
except Exception as e:
    print(f"\nErro ao chamar a API do Gemini: {e}")
    print("Dica: Verifique se a sua chave de API está correta e ativa.")
