
class Estado:
    def __init__(self, nome):
        self.transicoes: dict[str, tuple[str, str]] = {} # dicionario de transições no formato (estado_destino,simbolo)


class AFD:
    def __init__(self,estadoNomes: set[str], estadoInicial: str, estadosFinais: set[str]):
        self.estadoNomes = estadoNomes #so recebe set, para nao repetir estados
        self.estadoInicial = estadoInicial #so recebe set, para nao repetir estados
        self.estadosFinais = estadosFinais #so recebe set, para nao repetir estados
        self.estados = {} #dicionario de estados, onde a chave é o nome do estado e o valor é um objeto do tipo Estado


    def criaEstados(self): #adiciona os estados que estão em estadoNomes ao dicionário de estados 
        for nome in self.estadoNomes:
            self.estados[nome] = Estado(nome) #objeto estados[chave de busca no dict] = typecast para Estado(nomeDoEstado)
    
    def adicionaTransicao(self, estadoOrigem: str, simbolo: str, estadoDestino: str):
        if estadoOrigem not in self.estadoNomes:
            print(f"Estado de origem '{estadoOrigem}' não existe.")
        if estadoDestino not in self.estadoNomes:
           print(f"Estado de destino '{estadoDestino}' não existe.")
        else:
            self.estados[estadoOrigem].transicoes[simbolo] = (estadoDestino, simbolo) #adiciona a transição ao dicionário de transições do estado de origem
       
       