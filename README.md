# ⚽ FTC-MAQUINAESTADOS-TPFINAL ⚽
## Simulador de Autômatos, Autômatos de Pilha e Máquinas de Turing

Este projeto consiste em um interpretador e simulador de modelos de computação formais desenvolvido para a disciplina de **Fundamentos da Teoria da Computação (FTC)** da UFV - Campus Florestal. O programa possui uma interface temática inspirada em futebol ("Vai Brasil!", "Tática", "Escalação", "Apito Inicial"), onde é possível configurar autômatos finitos, autômatos de pilha e máquinas de Turing através de arquivos de texto estruturados e processar cadeias de teste.

---

## 📋 Sumário
1. [Máquinas Suportadas](#-máquinas-suportadas)
2. [Interface e Modos de Execução](#-interface-e-modos-de-execução)
3. [Especificação do Arquivo de Entrada](#-especificação-do-arquivo-de-entrada)
   - [Campos do Cabeçalho](#campos-do-cabeçalho)
   - [Formatos de Transição](#formatos-de-transição)
4. [Exemplos Práticos](#-exemplos-práticos)
5. [Como Executar](#-como-executar)
6. [Estrutura do Projeto](#-estrutura-do-projeto)

---

## ⚙️ Máquinas Suportadas

O simulador suporta uma ampla variedade de modelos de computação, incluindo as especificações básicas e as funcionalidades extras do trabalho prático:

| Tipo | Descrição | Classe/Módulo Relacionado | Reconhecimento por |
| :--- | :--- | :--- | :--- |
| **`@AFD`** | Autômato Finito Determinístico | [AFD](file:///c:/Users/erick/Desktop/FTC-MAQUINAESTADOS-TPFINAL/src/AFD.py) | Estado Final |
| **`@AFN`** | Autômato Finito Não Determinístico (com transições vazias/lambda `\`) | [AFN](file:///c:/Users/erick/Desktop/FTC-MAQUINAESTADOS-TPFINAL/src/AFN.py) | Estado Final |
| **`@APD`** | Autômato de Pilha Determinístico | [APD](file:///c:/Users/erick/Desktop/FTC-MAQUINAESTADOS-TPFINAL/src/apd.py) | Pilha Vazia + Estado Final |
| **`@APNP`** | Autômato de Pilha Não Determinístico | [APN](file:///c:/Users/erick/Desktop/FTC-MAQUINAESTADOS-TPFINAL/src/apn.py) | Pilha Vazia + Estado Final |
| **`@APNPV`** | Autômato de Pilha Não Determinístico por Pilha Vazia | [APN](file:///c:/Users/erick/Desktop/FTC-MAQUINAESTADOS-TPFINAL/src/apn.py) | Pilha Vazia apenas |
| **`@MT`** | Máquina de Turing Determinística | [turing](file:///c:/Users/erick/Desktop/FTC-MAQUINAESTADOS-TPFINAL/src/turing.py) | Parada em Estado Final (Fita Infinita) |
| **`@ALL`** | Autômato Linearmente Limitado | [turing](file:///c:/Users/erick/Desktop/FTC-MAQUINAESTADOS-TPFINAL/src/turing.py) | Parada em Estado Final (Fita Limitada por `<` e `>`) |

---

## 🎮 Interface e Modos de Execução

Ao iniciar o programa com `python src/main.py`, você entra no menu de "táticas de jogo":

1. **`1 - Jogada Rápida`**: O programa lê o caminho do arquivo de entrada digitado pelo usuário. A primeira linha do arquivo deve conter a tag da máquina (ex: `@AFD`, `@MT`) para que o simulador identifique automaticamente o modelo.
2. **`2 - Tática Completa`**: O usuário escolhe a tag da máquina que deseja instanciar (ex: `@AFD`, `@AFN`, `@APD`, `@APNP`, `@APNPV`, `@MT`, `@ALL`) e, em seguida, informa o caminho do arquivo de entrada.

---

## 📄 Especificação do Arquivo de Entrada

Os arquivos de entrada possuem uma sintaxe estrita que define a máquina e seus casos de teste.

### Campos do Cabeçalho
Cada linha inicial do arquivo configura um aspecto da máquina:

- **`Q:`**: Especifica os nomes de todos os estados do autômato separados por espaços. Os nomes dos estados devem conter apenas caracteres alfanuméricos (`a-z`, `A-Z`, `0-9`) com no máximo **7 caracteres** cada.
- **`S:`**: *(Alfabeto de Entrada - Opcional/Extra 1)* Define a sequência de caracteres aceitos na fita. Seus caracteres não devem ser separados por espaço (ex: `S: 01` ou `S: abc`).
- **`G:`**: *(Alfabeto da Pilha / Fita)*
  - Para Autômatos de Pilha (**`AP`**): Alfabeto da pilha (ex: `G: ZU`).
  - Para Máquinas de Turing / ALL (**`MT`/`ALL`**): Símbolos exclusivos da fita (não pertencentes ao alfabeto de entrada `S`).
- **`I:`**: Estado inicial do autômato.
  - Para modelos deterministas (**`AFD`, `APD`, `MT`, `ALL`**): Apenas um estado.
  - Para modelos não deterministas (**`AFN`, `APN`**): Podem ser definidos múltiplos estados iniciais separados por espaço.
- **`F:`**: Especifica a lista de estados finais separados por espaço.
- **`---`**: Linha divisória obrigatória. Todo conteúdo antes dela configura a máquina; todo conteúdo depois representa palavras de teste (uma por linha).

### Formatos de Transição
As transições são escritas no formato: `origem -> destino | regras`

1. **Autômatos Finitos (`@AFD`, `@AFN`)**:
   As regras são os caracteres que ativam a transição, separados por espaços.
   - *Exemplo:* `q0 -> q1 | 0 1` (transiciona de `q0` para `q1` lendo `0` ou `1`).
   - *Transição Lambda:* No caso de `@AFN`, usa-se `\` (barra invertida) para transições sem consumir símbolo. Ex: `q0 -> q1 | \`

2. **Autômatos de Pilha (`@APD`, `@APNP`, `@APNPV`)**:
   As regras seguem o formato `simboloLido,desempilha/empilha`.
   - *Exemplo:* `q -> q | (,\/X` (lê `(`, não desempilha nada `\`, e empilha `X`).
   - *Exemplo:* `q -> q | ),X/\` (lê `)`, desempilha `X`, e empilha nada `\`).

3. **Máquinas de Turing e ALL (`@MT`, `@ALL`)**:
   As regras seguem o formato `simboloLido/simboloEscritoDirecao`, onde a direção é `D` (Direita/Right) ou `E` (Esquerda/Left).
   - O símbolo de espaço em branco é representado por `_`.
   - Os delimitadores de início e fim da fita no ALL são `<` e `>` respectivamente.
   - *Exemplo:* `A -> B | 1/aD` (lê `1`, escreve `a` e move a cabeça para a direita).
   - *Exemplo:* `A -> X | _/_E` (lê espaço em branco `_`, escreve `_` e move para a esquerda).

---

## 💡 Exemplos Práticos

### 1. Autômato Finito Determinístico (`@AFD`)
Reconhece palavras sobre o alfabeto `{0, 1}` que terminam com `01` ou com paridade específica:

```text
@AFD
Q: a b c d e
S: 01
I: a
F: a d
a -> b | 1
a -> d | 0
b -> c | 0
b -> e | 1
c -> c | 0
c -> d | 1
d -> d | 0 1
e -> e | 0 1
---
001
1000
10000011
```

**Saída correspondente:**
```text
OK
X
OK
```

### 2. Autômato de Pilha Determinístico (`@APD`)
Reconhece strings de parênteses balanceados:

```text
@APD
Q: q
S: ()
G: X
I: q
F: q
q -> q | (,\/X
q -> q | ),X/\
---
()
(())
(()
```

**Saída correspondente:**
```text
OK
OK
X
```

### 3. Máquina de Turing (`@MT`)
Apaga `0` da fita e altera `1` por `a` ou `b`, parando no estado final `X`:

```text
@MT
Q: A B X
S: 10
G: ab
I: A
F: X
A -> A | 0/_D
A -> B | 1/aD
B -> A | 1/bD
B -> B | 0/_D
A -> X | _/_E
---
1000111
0111000
```

**Saída correspondente:**
*(A saída exibe o veredito e o conteúdo final da fita até a última posição não vazia)*
```text
OK <a___bab
X <_aba
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10 ou superior.

### Executando o simulador
No terminal, a partir do diretório raiz do projeto, execute:

```bash
python -m src.main
```

Ou execute diretamente o arquivo principal:

```bash
python src/main.py
```

### Rodando Testes inclusos
O repositório possui diversos arquivos de teste na pasta `testes/`. Você pode selecioná-los inserindo o caminho relativo. Exemplo:
- Para testar um AFD: `testes/AFD/AFD.txt`
- Para testar um APD: `testes/entradaAPD.txt`
- Para testar uma Máquina de Turing: `testes/Teste.txt`

---

## 📁 Estrutura do Projeto

```text
FTC-MAQUINAESTADOS-TPFINAL/
│
├── testes/                      # Pasta com arquivos de exemplo de entrada
│   ├── AFD/
│   │   ├── AFD.txt
│   │   ├── contem_substring_abc.txt
│   │   ├── multiplo_de_tres.txt
│   │   ├── paridade_de_zeros.txt
│   │   └── termina_com_01.txt
│   ├── ALL.txt
│   ├── entradaAPD.txt
│   └── teste_afn.txt
│
├── src/                         # Código-fonte do simulador
│   ├── __init__.py
│   ├── __main__.py
│   ├── main.py                  # Ponto de entrada e fluxo do menu interativo
│   ├── leituraArquivos.py       # Parser dos arquivos de entrada estruturados
│   ├── AFD.py                   # Classe do Autômato Finito Determinístico
│   ├── AFN.py                   # Classe do Autômato Finito Não Determinístico
│   ├── apd.py                   # Classe do Autômato de Pilha Determinístico
│   ├── apn.py                   # Classe do Autômato de Pilha Não Determinístico
│   └── turing.py                # Implementação de Máquina de Turing e ALL
│
├── requirements.txt             # Dependências (vazio, usa apenas stdlib)
└── README.md                    # Documentação do projeto
```

## *Readme criado usando IA