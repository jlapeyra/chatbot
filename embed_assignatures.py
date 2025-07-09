from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

assignatures = [
    {"nom": "Xarxes Neuronals", "desc": "Aprenentatge profund i xarxes convolucionals."},
    {"nom": "Processament de Llenguatge Natural", "desc": "Tècniques per entendre el llenguatge humà."},
    {"nom": "Computació Gràfica", "desc": "Visualització 3D i motors de renderitzat."},
]


# Creem documents
from langchain.schema import Document

print('Embedding')
docs = [
    Document(page_content=f"{a['nom']}: {a['desc']}", metadata=a)
    for a in assignatures
]

# Indexem els documents
vectorstore = FAISS.from_documents(docs, embedding_model)

def cercar_assignatura(state):
    pregunta = state["input"]
    similars = vectorstore.similarity_search(pregunta, k=1)

    if similars:
        state["resposta"] = f"Sí! L'assignatura més propera és: {similars[0].metadata['nom']}"
    else:
        state["resposta"] = "No s'ha trobat cap assignatura relacionada."
    return state
