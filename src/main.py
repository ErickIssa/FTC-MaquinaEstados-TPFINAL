from AFD import AFD

estados = {"a", "b", "c", "d", "e"}
estadoInicial = "a"
estadosFinais = {"a", "e"}

afd = AFD(estados, estadoInicial, estadosFinais)

# Transições a partir do estado 'a'
afd.adicionaTransicao("a", "1", "b")
afd.adicionaTransicao("a", "a", "d")

afd.adicionaTransicao("b", "0", "c")
afd.adicionaTransicao("b", "1", "e")

afd.adicionaTransicao("c", "0", "c")
afd.adicionaTransicao("c", "1", "d")


afd.adicionaTransicao("d", "0", "d")
afd.adicionaTransicao("d", "1", "d")

afd.adicionaTransicao("e", "0", "e")
afd.adicionaTransicao("e", "1", "e")

afd.imprimeMaquina()

afd.processaEntrada("001")
afd.processaEntrada("1000")
afd.processaEntrada("") # ver depois como que vai ser a ideia de entrada vazia
afd.processaEntrada("10000011")
afd.processaEntrada("111")
afd.processaEntrada("1")