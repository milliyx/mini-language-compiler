import ply.yacc as yacc
from lexer import tokens

class TablaSimbolos:
  def __init__(self):
      self.simbolos = {}
      
  def agregar(self, nombre, tipo, valor=None):
      if nombre in self.simbolos:
          raise Exception(f"Error semántico: La variable '{nombre}' ya ha sido declarada")
      self.simbolos[nombre] = {'tipo': tipo, 'valor': valor}
      
  def obtener(self, nombre):
      if nombre not in self.simbolos:
          raise Exception(f"Error semántico: La variable '{nombre}' no ha sido declarada")
      return self.simbolos[nombre]
  
  def limpiar(self):
      self.simbolos.clear()

tabla_simbolos = TablaSimbolos()

# Reglas de precedencia
precedence = (
  ('left', 'SUMA', 'RESTA'),
  ('left', 'MULT', 'DIV'),
)

def p_programa(p):
  '''programa : declaraciones'''
  p[0] = p[1]

def p_declaraciones(p):
  '''declaraciones : declaraciones declaracion
                  | declaracion'''
  if len(p) == 3:
      if not isinstance(p[1], list):
          p[1] = [p[1]]
      if p[2] is not None:  # Solo agregar si no es None
          p[0] = p[1] + [p[2]]
      else:
          p[0] = p[1]
  else:
      if p[1] is not None:  # Solo crear lista si no es None
          p[0] = [p[1]]
      else:
          p[0] = []

def p_declaracion(p):
  '''declaracion : declaracion_variable
                | asignacion
                | estructura_control
                | imprimir'''
  p[0] = p[1]

def p_declaracion_variable(p):
  '''declaracion_variable : tipo IDENTIFICADOR ASIG expresion PUNTOCOMA'''
  tabla_simbolos.agregar(p[2], p[1], p[4])
  p[0] = ('declaracion', p[1], p[2], p[4])

def p_tipo(p):
  '''tipo : TIPO_ENTERO
          | TIPO_DECIMAL
          | TIPO_CARACTER
          | TIPO_BOOLEANO'''
  p[0] = p[1]

def p_asignacion(p):
  '''asignacion : IDENTIFICADOR ASIG expresion PUNTOCOMA'''
  if tabla_simbolos.obtener(p[1]) is None:
      raise Exception(f"Error semántico: Variable '{p[1]}' no declarada")
  p[0] = ('asignacion', p[1], p[3])

def p_estructura_control(p):
  '''estructura_control : estructura_si
                      | estructura_mientras
                      | estructura_para'''
  p[0] = p[1]
#aqui esta el problema de los if, else
#lo que agregué hace que ya no marque error el if else
#pero no genera el else en la tabla de parse
# Es que copilot le sabe

def p_estructura_si(p):
  '''estructura_si : SI PARIZQ condicion PARDER LLAVEIZQ declaraciones LLAVEDER
                  | SI PARIZQ condicion PARDER LLAVEIZQ declaraciones LLAVEDER SINO PARIZQ condicion PARDER LLAVEIZQ declaraciones LLAVEDER
                  | SI PARIZQ condicion PARDER LLAVEIZQ declaraciones LLAVEDER SINO PARIZQ condicion PARDER LLAVEIZQ declaraciones LLAVEDER EOC LLAVEIZQ declaraciones LLAVEDER
                  | SI PARIZQ condicion PARDER LLAVEIZQ declaraciones LLAVEDER EOC LLAVEIZQ declaraciones LLAVEDER'''
  if len(p) == 8:  # si simple
      p[0] = ('si', p[3], p[6])
  elif len(p) == 15:  # si-sino
      p[0] = ('si_sino', p[3], p[6], p[10], p[13])
      #simon, ya cheque el archivo, esta bien, al final es lo que se ocupa
  elif len(p) == 18:  # si-sino-eoc
      # Asegurarse de que los bloques sean listas
      bloque1 = p[6] if isinstance(p[6], list) else [p[6]]
      bloque2 = p[13] if isinstance(p[13], list) else [p[13]]
      bloque3 = p[16] if isinstance(p[16], list) else [p[16]]
      #tecnicamente esto si declarado, pero no lo reconoce
      p[0] = ('si_sino_eoc', 
          p[3],        # Primera condición
          bloque1,     # Primer bloque
          p[10],       # Segunda condición
          bloque2,     # Segundo bloque
          bloque3      # Bloque eoc
      )
      


def p_estructura_mientras(p):
  '''estructura_mientras : MIENTRAS PARIZQ condicion PARDER LLAVEIZQ declaraciones LLAVEDER'''
  p[0] = ('mientras', p[3], p[6])

def p_estructura_para(p):
  '''estructura_para : PARA PARIZQ inicializacion_para PUNTOCOMA condicion PUNTOCOMA incremento_para PARDER LLAVEIZQ declaraciones LLAVEDER'''
  p[0] = ('para', p[3], p[5], p[7], p[10])

def p_inicializacion_para(p):
  '''inicializacion_para : tipo IDENTIFICADOR ASIG expresion
                       | IDENTIFICADOR ASIG expresion'''
  if len(p) == 5:
      tabla_simbolos.agregar(p[2], p[1], p[4])
      p[0] = ('declaracion', p[1], p[2], p[4])
  else:
      p[0] = ('asignacion', p[1], p[3])

def p_incremento_para(p):
  '''incremento_para : IDENTIFICADOR ASIG IDENTIFICADOR SUMA NUMERO
                    | IDENTIFICADOR ASIG IDENTIFICADOR RESTA NUMERO
                    | IDENTIFICADOR SUMA SUMA
                    | IDENTIFICADOR RESTA RESTA'''
  if len(p) == 6:
      p[0] = ('asignacion', p[1], ('operacion', p[4], p[3], p[5]))
  else:
      p[0] = ('asignacion', p[1], ('operacion', '+', p[1], 1))

def p_condicion(p):
  '''condicion : expresion IGUAL expresion
              | expresion DIFERENTE expresion
              | expresion MENOR expresion
              | expresion MAYOR expresion
              | expresion MENORIGUAL expresion
              | expresion MAYORIGUAL expresion'''
  p[0] = ('condicion', p[2], p[1], p[3])

def p_expresion(p):
  '''expresion : expresion SUMA termino
              | expresion RESTA termino
              | expresion MULT termino
              | expresion DIV termino
              | termino'''
  if len(p) == 4:
      p[0] = ('operacion', p[2], p[1], p[3])
  else:
      p[0] = p[1]

def p_termino(p):
  '''termino : IDENTIFICADOR
             | NUMERO
             | DECIMAL
             | CARACTER
             | TRUE
             | FALSE
             | PARIZQ expresion PARDER'''
  if len(p) == 4:
      p[0] = p[2]
  else:
      p[0] = p[1]

def p_imprimir(p):
  '''imprimir : PRINT PARIZQ expresion PARDER PUNTOCOMA'''
  p[0] = ('imprimir', p[3])

def p_error(p):
  if p:
      raise Exception(f"Error de sintaxis en línea {p.lineno}: Token inesperado '{p.value}'")
  else:
      raise Exception("Error de sintaxis: Final inesperado del archivo")

# Crear el parser
parser = yacc.yacc()

# Función para analizar código
def analizar(codigo):
  try:
      return parser.parse(codigo)
  except Exception as e:
      print(f"Error durante el análisis: {str(e)}")
      return None

if __name__ == "__main__":
  #aqui por ejemplo ya esta implementado el while.
  #antes no funcionaba el while, ni el if
  # ahora mira como generá el AST (investigue y el ast es una forma de crear tokens, y revisar que existan)
  #ahora mira funciona con solo if, y elseif
  #funciona para infinitos si
  #pero para infinitos sino, no xd
  #puedes poner mil si, solo un sino por si, y el else no jala xd
  #ve la tabla de parse, no funciona el eoc
  #si ves tampoco funciona si es if else solamente xd
  #Estos comentarios se quedan, al final nadie los va a ver xd
  #esta es la rama main, asi que solo seria pull request

  # Código de prueba
  codigo_prueba = """
  entero x = 5;
  entero y = 3;
  entero z = x + y;
  si (x > 0) {
      x = x - 1;
      print(x);
      }
   sino (x<0){
      print(y);
      }  
  """
  
  resultado = analizar(codigo_prueba)
  if resultado:
      print("\nAST generado:")
      print(resultado)