from AFD import AFD

estados = {"q0", "q1", "q2", "q3"}
estadoInicial = "q0"
estadosFinais = {"q3"}
afd = AFD(estados, estadoInicial, estadosFinais)
afd.criaEstados()
afd.adicionaTransicao("q0", "a", "q1")
afd.adicionaTransicao("q1", "b", "q2")
afd.adicionaTransicao("q2", "b", "q3")
afd.imprimeMaquina()

entrada = "abb"
if afd.processaEntrada(entrada):
    print(f"A entrada '{entrada}' é aceita pelo AFD.")
else:
    print(f"A entrada '{entrada}' é rejeitada pelo AFD.")