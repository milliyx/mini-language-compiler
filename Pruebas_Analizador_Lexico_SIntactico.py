import ply.lex as lex
from lexer import tokens, lexer

# Código de prueba que utiliza diferentes características del lenguaje
codigo_prueba = """

entero numero1 = 42;
decimal numero2 = 3.14;
caracter letra = 'A';
booleano flag = true;


si (numero1 > 40) {
  print(numero1);
  numero1 = numero1 + 1;
} sino (numero1 < 40) {
  print(numero2);
} eoc {
  print(letra);
}


mientras (numero1 < 50) {
  numero1 = numero1 + 1;
  print(numero1);
}

para (entero i = 0; i < 5; i++) {
  print(i);
}
"""

class NodoAST:
  def __init__(self, tipo, valor=None, hijos=None):
      self.tipo = tipo
      self.valor = valor
      self.hijos = hijos if hijos else []

def mostrar_arbol(nodo, nivel=0):
  """Muestra el árbol sintáctico de forma visual"""
  print("  " * nivel + f"|_{str(nodo.tipo)}", end="")
  if nodo.valor:
      print(f": {nodo.valor}")
  else:
      print()
  for hijo in nodo.hijos:
      mostrar_arbol(hijo, nivel + 1)

def analizar_lexico(codigo):
  """
  Realiza el análisis léxico del código y muestra los tokens encontrados
  """
  lexer.input(codigo)
  
  print("\nAnálisis Léxico:")
  print("TOKEN\t\t\tVALOR\t\tLÍNEA\tPOSICIÓN")
  print("-" * 60)
  
  while True:
      tok = lexer.token()
      if not tok:
          break
      print(f"{tok.type:<20} {str(tok.value):<15} {tok.lineno:<8} {tok.lexpos}")

def analizar_sintactico(codigo):
  """
  Realiza el análisis sintáctico del código y muestra la estructura detallada
  """
  from parser import parser
  
  print("\nAnálisis Sintáctico:")
  print("-" * 60)
  
  try:
      # Intentar realizar el análisis sintáctico
      resultado = parser.parse(codigo, lexer=lexer)
      
      print("\nEstructura del programa:")
      print("=" * 60)
      
      # Analizar cada declaración en el programa
      for declaracion in resultado:
          if isinstance(declaracion, dict):
              print(f"\nTipo de declaración: {declaracion.get('tipo', 'Desconocido')}")
              for key, value in declaracion.items():
                  if key != 'tipo':
                      print(f"  {key}: {value}")
          else:
              print(f"Declaración: {declaracion}")
      
      print("\nAnálisis sintáctico completado exitosamente!")
      return True
      
  except Exception as e:
      print("\nError en el análisis sintáctico:")
      print(f"{'=' * 60}")
      print(f"Tipo de error: {type(e).__name__}")
      print(f"Descripción: {str(e)}")
      
      # Intentar obtener más información sobre el error
      if hasattr(e, 'lineno'):
          print(f"Línea: {e.lineno}")
      if hasattr(e, 'pos'):
          print(f"Posición: {e.pos}")
      
      # Mostrar el contexto del error
      lineas = codigo.split('\n')
      if hasattr(e, 'lineno') and e.lineno <= len(lineas):
          print("\nContexto del error:")
          print(f"Línea {e.lineno}: {lineas[e.lineno-1]}")
          print(" " * (e.pos-1) + "^" if hasattr(e, 'pos') else "")
      
      return False

def main():
  # Mostrar el código a analizar
  print("Código a analizar:")
  print("=" * 60)
  print(codigo_prueba)
  print("=" * 60)

  # Realizar análisis léxico
  analizar_lexico(codigo_prueba)

  # Realizar análisis sintáctico
  exito = analizar_sintactico(codigo_prueba)

  if not exito:
      print("\nEl análisis no pudo completarse debido a errores sintácticos.")
  else:
      print("\nAnalisis sintáctico completado con éxito.")

if __name__ == "__main__":
  main()