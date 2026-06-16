from estado import *

MAX_TAM = 10**9

class turing():

    def __init__( self, alfabeto, estados, est_inicial, alfabeto_fita, est_finais, usar_fita_finita=False):
        self.alfabeto = alfabeto
        self.estados = estados
        self.estados.append(estado('?'))

        self.estado_inicial = est_inicial
        self.estados_finais = est_finais
        self.alfabeto_fita = alfabeto_fita

        self.simb_inicio = '<'
        self.simb_branco = '_'
        self.simb_final = '>'

        self.fita = ""
        self.cabeca = 0
        self.estado_atual = self.estado_inicial

        self.usar_fita_finita = usar_fita_finita
        self.extrapolou = False

    def aceita(self, cadeia):

        if len(cadeia) > MAX_TAM:
            return None

        self.extrapolou = False

        if self.usar_fita_finita:
            self.fita = self.simb_inicio + cadeia + self.simb_final
        else:
            self.fita = self.simb_inicio + cadeia + self.simb_branco

        self.estado_atual = self.estado_inicial

        # começa lendo o primeiro símbolo da palavra
        self.cabeca = 1

        while True:

            if self.cabeca < 0:
                self.extrapolou = True
                break

            if self.usar_fita_finita:

                if self.cabeca >= len(self.fita):
                    self.extrapolou = True
                    break

            else:

                if self.cabeca >= len(self.fita):

                    if len(self.fita) >= MAX_TAM:
                        self.extrapolou = True
                        break

                    self.fita += self.simb_branco

            if not self.programa():
                break

        ultima_pos = len(self.fita) - 1

        while (
            ultima_pos > 0 and
            self.fita[ultima_pos] == self.simb_branco
        ):
            ultima_pos -= 1

        fita_saida = self.fita[:ultima_pos + 1]

        if (
            not self.extrapolou and
            self.estado_atual in self.estados_finais
        ):
            print("OK", fita_saida)
        else:
            print("X", fita_saida)

        return fita_saida

    def programa(self):

        estado = self.get_estado(self.estado_atual)

        if estado is None:
            return False

        transicao = estado.get_transicao(
            self.fita[self.cabeca]
        )

        if transicao is None:
            return False

        if transicao[1] is not None:

            aux = list(self.fita)
            aux[self.cabeca] = transicao[1]
            self.fita = ''.join(aux)

        if transicao[2] == 'D':
            self.cabeca += 1

        elif transicao[2] == 'E':
            self.cabeca -= 1

        if transicao[3] is not None:
            self.estado_atual = transicao[3]

        return True

    def get_estado(self, nome):

        for estado in self.estados:

            if estado.get_nome() == nome:
                return estado

        return None