from src.AFD import AFD

estados = {"q0", "q1", "q2"}
estadoInicial = "q0"
estadosFinais = {"q2"}
afd = AFD(estados, estadoInicial, estadosFinais)
afd.criaEstados()
afd.adicionaTransicao("q0", "a", "q1")
afd.adicionaTransicao("q1", "b", "q2")
afd.imprimeMaquina()