# 🤖 Chatbot UPC - Informació Acadèmica Personalitzada

Aquest projecte implementa un chatbot orientat a respondre preguntes sobre assignatures i processos acadèmics de la **Facultat d'Informàtica de Barcelona (FIB, UPC)**, amb respostes adaptades al perfil d'estudiant que el fa servir.

El sistema utilitza LangChain amb el model `openhermes` via Ollama per generar respostes, i es basa en un flux de nodes de decisió per classificar i respondre adequadament les consultes.

---

## 🧠 Exemple d'ús

```text
Pregunta: Quants crèdits té PRO1?
state: info_assig
Resposta:
La assignatura "Programació I" té 7.5 crèdits.

Pregunta: Quin dia m'he de matricular?
state: matricula
Resposta:
Per matricular-te, es basa en el grau que estàs estudiant i la fase en què estàs: Grau en Enginyeria Informàtica (GEI). Si ets un estudiant del GEI en fase inicial amb 0 ECTS superats i matriculat a F, FM, IC, PRO1, el dia per matricular-te és el 24 de juliol de 2025.

A partir del 4 de juliol, es podrà consultar l'e-secretaria la data i hora específica que t'ha sigut assignada per a la matrícula. Si no pots fer-ho en el dia i hora assignat, caldrà sol·licitar a l’eSecretaria una nova data en què pugs matricular-te. L'hora de matrícula es calcula a partir de les dades disponibles el dia abans del càlcul i no tenen en compte les assignatures no qualificades en aquell moment.

Pots trobar més informació sobre com es calcula l'ordre de matrícula a la pestanya "Normativa Associada".
```

---

## 📁 Estructura del projecte

* `nodes.py`: Defineix la graella de nodes (classificació, accions finals, etc.) i el flux de converses.
* `estudiant.py`: Carrega i descriu el perfil de l'estudiant (grau, fase, assignatures matriculades, etc.).
* `embed_assignatures.py`: Fa cerques semàntiques d'assignatures amb embeddings i FAISS.
* `data_mining/assignatures_basic.py`: Raspallador HTML per obtenir assignatures i metadades bàsiques.
* `data_mining/assignatures_detall.py`: Extreu informació detallada de cada assignatura a partir del seu enllaç.
* `data/`: Conté fitxers `.json` i `.txt` amb dades prèviament extretes (com la matrícula o assignatures).

---

## ⚙️ Requisits i dependències

Aquest projecte requereix Python 3.9+ i les següents biblioteques:

* `langchain`
* `langgraph`
* `langchain_ollama`
* `huggingface_hub`
* `faiss-cpu`
* `tqdm`

Instal·la-les amb:

```bash
pip install -r requirements.txt
```

---

## 🚀 Execució

1. **Prepara el teu entorn:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. **Assegura't que `ollama` està funcionant i tens el model `openhermes` descarregat:**

```bash
ollama run openhermes
```

3. **Executa el fitxer principal:**

```bash
python nodes.py
```

---

## ✨ Com funciona

* Es defineix un usuari (per defecte: `aitor.tilla`, GEI, fase inicial).
* Es classifica la pregunta de l’usuari a través del node `ClassificacioInicial`, i segons el resultat, s’envia a un node com `InfoMatricula` o `InfoAssigMatriculada`.
* El node executa un prompt basat en context real (fase, assignatures matriculades, etc.).
* S’utilitza un model LLM per generar la resposta de manera contextualitzada.

---

## 🛠 Altres utilitats

Per tornar a generar les dades d’assignatures:

```bash
python assignatures_basic.py
python assignatures_detall.py
```

Per provar cerca semàntica d’assignatures (exemple amb embeddings):

```bash
python embed_assignatures.py
```

---

## 📄 Llicència

Projecte d'ús acadèmic. Pots reutilitzar-lo i adaptar-lo lliurement amb finalitats educatives.


