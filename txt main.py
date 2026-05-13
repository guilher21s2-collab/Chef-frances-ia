# ============================================
# CHEF FRANCÊS IA
# Angelo Maia, Paulo Guilherme e Rangel Santos
# ============================================

# Instalação das bibliotecas:
# pip install langchain langchain-groq langchain-community beautifulsoup4

import os

from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Define um identificador para evitar bloqueios no site
os.environ['USER_AGENT'] = 'ChefFrancesIA/1.0'

# Coloque sua chave da API Groq aqui
os.environ['GROQ_API_KEY'] = 'SUA_CHAVE_AQUI'

# Inicializa o modelo de IA
chat = ChatGroq(model='llama-3.3-70b-versatile')

# Site usado como base de conhecimento
loader = WebBaseLoader(
    'https://acozinhafrancesa.com.br/cozinha-francesa/')

# Carrega o conteúdo do site
lista_documentos = loader.load()

# Junta todo o conteúdo em um único texto
documento = ' '.join(
    [doc.page_content for doc in lista_documentos]
)

# Limita o tamanho do texto
documento = documento[:8000]

# Criação da persona do chatbot
template = ChatPromptTemplate.from_messages([

    ("system", """
    Você é um Chefe de Culinária Francesa.

    Responda apenas perguntas sobre culinária francesa,
    incluindo:

      - pratos típicos
    - ingredientes
    - técnicas
    - receitas
    - história gastronômica
    - regiões da França
    - dicas de preparo

    Utilize como base principal o conteúdo do site informado.

    Caso a pergunta não seja sobre culinária francesa,
    responda educadamente:

    "Desculpe, eu sou especialista apenas em culinária francesa."
    """),

    ("user", """
    Conteúdo do site:

    {documentos_informados}

    Pergunta do usuário:

    {pergunta_do_usuario}
    """)
])

# Junta o prompt com o modelo
chain = template | chat

# Mensagem inicial
print("=" * 50)
print("🤖 Bem-vindo ao Chef Francês IA!")
print("Faça perguntas sobre culinária francesa.")
print("Digite 'alura' para sair.")
print("=" * 50)

# Loop principal do chatbot
while True:

    pergunta = input("\nVocê: ")

    if pergunta.lower() == 'alura':
        print("\nChef Francês IA: Au revoir! Conversa encerrada.")
        break

    resposta = chain.invoke({
        "documentos_informados": documento,
        "pergunta_do_usuario": pergunta
    })

    print("\nChef Francês IA:")
    print(resposta.content)

    print("\n" + "-" * 50)
