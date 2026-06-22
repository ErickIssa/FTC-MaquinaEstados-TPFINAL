from .leituraArquivos import leArquivo
from .AFN import *
from .apn import *
from .AFD import *
from .apd import *
from .turing import *
def main():
    VERDE = "\033[92m"
    AMARELO = "\033[93m"
    AZUL = "\033[94m"
    BRANCO = "\033[97m"
    VERMELHO = "\033[91m"
    RESET = "\033[0m"
    arte = f"""
        {VERDE}==========================================
        |{AMARELO}                   /\\                   {VERDE}|
        |{AMARELO}                 /    \\                 {VERDE}|
        |{AMARELO}               /        \\               {VERDE}|
        |{AMARELO}             /    {AZUL}(  ){AMARELO}    \\             {VERDE}|
        |{AMARELO}               \\        /               {VERDE}|
        |{AMARELO}                 \\    /                 {VERDE}|
        |{AMARELO}                   \\/                   {VERDE}|
        ==========================================
        {BRANCO}               VAI BRASIL!                {RESET}
        """
    print(arte)
    print(f"{VERDE}Apito Inicial! Começou o Jogo.{RESET}\n")
    print(f"{AZUL}Qual é a tática para essa partida?{RESET}")
    print(f" {AMARELO}1{RESET} - Jogada Rápida (Somente o caminho do arquivo)")
    print(f" {AMARELO}2{RESET} - Tática Completa (Nome da máquina e o caminho do arquivo)")
    try:
        resultadoLeitura = None
        x = int(input(f"\n{VERDE}Escolha sua jogada (1 ou 2): {RESET}"))
        if x == 2:
            print(f"\n{AZUL}Escalação de Máquinas disponíveis(digite @ seguido do nome da maquina):{RESET}")
            print("1 - @AFD\n2 - @AFN\n3 - @APD\n4 - @APNP\n5 - @APNPV(reconhecimento por pilha vazia)\n6 - @MT\n7 - @ALL")

            op = str(input(f"{AMARELO}Digite o nome da máquina escalada: {RESET}"))
            caminho = input(f"{AMARELO}Digite o caminho do arquivo de entrada: {RESET}")

            resultadoLeitura = leArquivo(caminho, op)

        elif x == 1:
            caminho = input(f"\n{AMARELO}Digite o caminho do arquivo de entrada: {RESET}")
            resultadoLeitura = leArquivo(caminho)
        else:
            print(f"\n{VERMELHO}Cartão Vermelho! O juiz apitou: Não temos essa opção!{RESET}")
            return

        if resultadoLeitura is not None:

            maqCriada, listaEntradas, tipoMaq = resultadoLeitura
            print(maqCriada)

            print(f"\n{VERDE}Rola a bola! A máquina {tipoMaq} entrou em campo.{RESET}\n")

            for entrada in listaEntradas:
                entrada_limpa = entrada.strip()

                if tipoMaq == "@AFD":
                    maqCriada.processaEntrada(entrada_limpa)

                elif tipoMaq in ["@MT", "@ALL"]:
                    maqCriada.aceita(entrada_limpa)

                elif tipoMaq == "@APD":
                    maqCriada.processaPalavras(entrada_limpa)

                elif tipoMaq == "@AFN":
                    processaPalavrasAFN(entrada_limpa,maqCriada)

                elif tipoMaq == "@APNP":
                    processaPalavrasAPN(entrada_limpa,maqCriada, exigir_estado_final=True)

                elif tipoMaq == "@APNPV":
                    processaPalavrasAPN(entrada_limpa, maqCriada, exigir_estado_final=False)

        else:
            print(f"\n{VERMELHO}[VAR] Falha na escalação! O arquivo não pôde ser lido corretamente.{RESET}")

    except ValueError:
        print(f"\n{VERMELHO} Falta! Por favor, digite apenas números válidos.{RESET}")
if __name__ == "__main__":
    main()