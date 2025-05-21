import ply.lex as lex

# Lista de tokens
tokens = (
    'IDENTIFICADOR',
    'NUMERO',
    'DECIMAL',
    'CARACTER',
    'SUMA',
    'RESTA',
    'MULT',
    'DIV',
    'ASIG',
    'IGUAL',
    'DIFERENTE',
    'MENOR',
    'MAYOR',
    'MENORIGUAL',
    'MAYORIGUAL',
    'PARIZQ',
    'PARDER',
    'LLAVEIZQ',
    'LLAVEDER',
    'PUNTOCOMA',
    'AND',
    'OR',
    'NOT',
)

# Palabras reservadas
reserved = {
    'entero': 'TIPO_ENTERO',
    'decimal': 'TIPO_DECIMAL',
    'caracter': 'TIPO_CARACTER',
    'booleano': 'TIPO_BOOLEANO',
    'si': 'SI',
    'sino': 'SINO',
    'eoc': 'EOC',
    'para': 'PARA',
    'mientras': 'MIENTRAS',
    'print': 'PRINT',
    'true': 'TRUE',
    'false': 'FALSE'
    
}

tokens = tokens + tuple(reserved.values())

# Reglas para tokens simples
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_ASIG = r'='
t_IGUAL = r'=='
t_DIFERENTE = r'!='
t_MENOR = r'<'
t_MAYOR = r'>'
t_MENORIGUAL = r'<='
t_MAYORIGUAL = r'>='
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_PUNTOCOMA = r';'
#Estas funciones definen tokens más complejos
#Convierte el valor capturado en un número de punto flotante.
def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
#Convierte el valor capturado en un número entero.
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t
#Extrae el carácter encapsulado entre comillas simples.
def t_CARACTER(t):
    r'\'[a-zA-Z]\''
    t.value = t.value[1:-1]
    return t
#Reconoce cadenas que inician con una letra o subrayado y están compuestas por letras, números o subrayados. 
#Si coinciden con una palabra reservada, se clasifica como tal.
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')
    return t
#Actualiza el número de línea cuando se encuentra una o más nuevas líneas.
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
#Omite espacios en blanco y tabulaciones durante el análisis léxico.
t_ignore = ' \t'
#Imprime un mensaje de error si encuentra un carácter no reconocido y avanza al siguiente carácter.
def t_error(t):
    print(f"Error léxico en línea {t.lexer.lineno}: Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)
#Se crea una instancia del analizador léxico utilizando la función lex().
lexer = lex.lex()
