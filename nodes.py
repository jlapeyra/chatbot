from abc import ABC, abstractmethod
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

from estudiant import USUARI

llm = ChatOllama(model="openhermes")
class Node(ABC):
    name:str
    desc:str|None
    successor:'Node'=None
    created:bool = False

    @abstractmethod
    def action(self, state):
        pass

    
    def create(self, builder:StateGraph):
        if self.__class__.created:
            return
        self.__class__.created = True
        builder.add_node(self.name, RunnableLambda(self.action))
        if self.successor:
            builder.add_edge(self.name, self.successor.name)
            self.successor.create(builder)


class ClassificationNode(Node):
    successors:list['Node']

    def create(self, builder:StateGraph):
        if self.__class__.created:
            return
        self.__class__.created = True
        builder.add_node(self.name, RunnableLambda(self.action))
        builder.add_conditional_edges(self.name, lambda state: state['next'])
        for succ in self.successors:
            succ.create(builder)

    def list_successors(self):
        return '\n'.join(f'    - {choice.name} → si {choice.desc}' for choice in self.successors)

    @abstractmethod
    def get_prompt(self, pregunta):
        pass


    def action(self, state):
        entrada = state["input"]
        prompt = self.get_prompt(entrada)
        resposta = llm.invoke([HumanMessage(content=prompt)])
        state["next"] = resposta.content.strip().lower()
        print("state:", state["next"])
        return state

class FinalNode(Node):
    name='final'


    def action(self, state):
        print("Resposta:")
        print(state["resposta"])
        return state


class ClassificacioInicial(ClassificationNode):
    name='classificacio_inicial'

    def get_prompt(self, pregunta):
        print("Pregunta:", pregunta)

        return f"""
Classifica la pregunta de l'usuari en una de les següents categories:
{self.list_successors()}

Pregunta: "{pregunta}"
Resposta (només una paraula): 
        """
    
    def __init__(self):
        self.successors = [InfoMatricula(), InfoAssigMatriculada()]

class InfoMatricula(Node):
    name='matricula'
    desc="l'usuari demana informació sobre la matrícula"
    successor = FinalNode()


    def action(self, state):
        entrada = state["input"]
        # Carrega informació de fitxer
        with open("data/matricula.txt", encoding="utf-8") as f:
            contingut = f.read()

        prompt = f"""
    Contesta la pregunta de l'usuari segons el següent text i context:
    TEXT:
    {contingut}

    CONTEXT:
    L'usuari és un {USUARI.desc()}.

    PREGUNTA:
    {entrada}
        """
        resposta = llm.invoke([HumanMessage(content=prompt)])
        state["resposta"] = resposta.content.strip()
        return state

class InfoAssigMatriculada(Node):
    name='info_assig'
    desc=f"l'usuari demana informació sobre alguna d'aquestes assignatures: {
        ', '.join(f'{a['nom']} ({a['sigles']})' for a in USUARI.matriculades)
    }"
    successor = FinalNode()

    def action(self, state):
        entrada = state["input"]
        # Carrega informació de fitx

        prompt = f"""
    Contesta la pregunta de l'usuari segons les següents dades i context. Si no trobes informació digues que pot consultar el web de l'assignatura ("web"), el Racó o la web de la fib ("url_fib")
    DADES:
    {USUARI.matriculades}

    CONTEXT:
    L'usuari és un {USUARI.desc()}.

    PREGUNTA:
    {entrada}
        """
        resposta = llm.invoke([HumanMessage(content=prompt)])
        state["resposta"] = resposta.content.strip()
        return state
    

def create_graph():
    builder = StateGraph(dict)

    ClassificacioInicial().create(builder)
    builder.set_entry_point(ClassificacioInicial.name)

    graf = builder.compile()
    
    return graf

graf = create_graph()
graf.invoke({"input": "Quants crèdits té PRO1?"})
graf.invoke({"input": "Quin dia m'he de matricular?"})