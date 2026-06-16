from turing import *

alfabeto = ['0', '1']
alfabeto_fita = ['a', 'b']

trans_A = [
    ['0', '_', 'D', 'A'],
    ['1', 'a', 'D', 'B'],
    ['_', '_', 'E', 'X']
]

trans_B = [
    ['0', '_', 'D', 'B'],
    ['1', 'b', 'D', 'A']
]

trans_X = []

A = estado('A', trans_A)
B = estado('B', trans_B)
X = estado('X', trans_X, is_final=True)

mt = turing(
    alfabeto,
    [A, B, X],
    'A',
    alfabeto_fita,
    ['X'],
    usar_fita_finita=False
)

print("=== MT ===")
mt.aceita("1000111")
mt.aceita("0111000")

alfabeto = ['0', '1']
alfabeto_fita = []

trans_x = [
    ['0', '_', 'D', 'x'],
    ['1', '1', 'D', 'x'],
    ['>', '>', 'E', 'fim']
]

trans_fim = []

x = estado('x', trans_x)
fim = estado('fim', trans_fim, is_final=True)

all = turing(
    alfabeto,
    [x, fim],
    'x',
    alfabeto_fita,
    ['fim'],
    usar_fita_finita=True
)

print("=== ALL ===")
all.aceita("1000111")
all.aceita("0111000")