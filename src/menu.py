def menu():
    print("Programa iniciado")
    print("Escolha qual autômato será executado:")
    print("1 - AFD\n2 - APD\n3 - MT/ALL")
    op = int(input("Digite sua escolha: "))

    caminho = str(input("Digite o caminho do arquivo de entrada:"))
    return op, caminho