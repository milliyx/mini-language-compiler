from semantic import AnalizadorSemantico
from lexer import lexer
from parser import parser, TablaSimbolos
from intermediate_code import GeneradorCodigoIntermedio
from codegen import GeneradorCodigoPython
class Compilador:
  """
  Clase principal que implementa un compilador para un mini lenguaje de programación.
  Realiza las fases de análisis léxico, sintáctico, semántico y generación de código.
  """
  def __init__(self):
      """
      Inicializa el compilador con sus componentes principales:
      - Analizador semántico
      - Generador de código intermedio
      - Generador de código Python
      - Lista de errores
      """
      self.analizador_semantico = AnalizadorSemantico()
      self.generador_intermedio = GeneradorCodigoIntermedio()
      self.generador = GeneradorCodigoPython()
      self.errores = []
    
  def analisis_lexico(self, codigo_fuente):
      """
      Realiza el análisis léxico del código fuente.
      
      Args:
          codigo_fuente (str): Código fuente a analizar
          
      Returns:
          bool: True si el análisis fue exitoso, False si se encontraron errores
      
      Proceso:
      1. Tokeniza el código fuente
      2. Almacena los tokens encontrados
      3. Detecta errores léxicos
      """
      print("\n=== ANÁLISIS LÉXICO ===")
      lexer.input(codigo_fuente)
      tokens = []
      errores_lexicos = []
      
      # Obtiene todos los tokens del código fuente
      while True:
          tok = lexer.token()
          if not tok:
              break
          tokens.append(f"Token: {tok.type}, Valor: {tok.value}, Línea: {tok.lineno}")
      
      # Manejo de errores y resultados
      if errores_lexicos:
          print("Errores léxicos encontrados:")
          for error in errores_lexicos:
              print(f"- {error}")
          return False
      else:
          print("Tokens encontrados:")
          for token in tokens:
              print(token)
          return True

  def analisis_sintactico(self, codigo_fuente):
      """
      Realiza el análisis sintáctico y genera el AST.
      
      Args:
          codigo_fuente (str): Código fuente a analizar
          
      Returns:
          ast: Árbol de sintaxis abstracta o None si hay errores
          
      Proceso:
      1. Parsea el código fuente
      2. Genera el AST
      3. Imprime el AST generado
      """
      print("\n=== ANÁLISIS SINTÁCTICO ===")
      try:
          ast = parser.parse(codigo_fuente, lexer=lexer)
          if not ast:
              print("Error: No se pudo generar el AST")
              return None
          print("AST generado exitosamente:")
          self.imprimir_ast(ast)
          return ast
      except Exception as e:
          print(f"Error sintáctico: {str(e)}")
          return None

  def analisis_semantico(self, ast):
      """
      Realiza el análisis semántico del AST.
      
      Args:
          ast: Árbol de sintaxis abstracta
          
      Returns:
          bool: True si el análisis fue exitoso, False si se encontraron errores
          
      Proceso:
      1. Analiza cada nodo del AST
      2. Verifica errores semánticos
      3. Construye la tabla de símbolos
      """
      print("\n=== ANÁLISIS SEMÁNTICO ===")
      try:
          if isinstance(ast, list):
              for nodo in ast:
                  self.analizador_semantico.analizar_nodo(nodo)
          else:
              self.analizador_semantico.analizar_nodo(ast)
          
          # Verifica errores semánticos
          if self.analizador_semantico.errores:
              print("Errores semánticos encontrados:")
              for error in self.analizador_semantico.errores:
                  print(f"- {error}")
              return False
          
          # Muestra la tabla de símbolos
          print("Tabla de símbolos:")
          for var, info in self.analizador_semantico.tabla_simbolos.items():
              print(f"- {var}: {info}")
          return True
      except Exception as e:
          print(f"Error durante el análisis semántico: {str(e)}")
          return False

  def generar_codigo_intermedio(self, ast):
      """
      Genera el código intermedio a partir del AST.
      
      Args:
          ast: Árbol de sintaxis abstracta
          
      Returns:
          list: Lista de instrucciones de código intermedio o None si hay errores
          
      Proceso:
      1. Procesa el AST
      2. Genera instrucciones intermedias
      3. Retorna el código intermedio generado
      """
      print("\n=== GENERACIÓN DE CÓDIGO INTERMEDIO ===")
      try:
          if isinstance(ast, list):
              for nodo in ast:
                  self.generador_intermedio.generar_codigo(nodo)
          else:
              self.generador_intermedio.generar_codigo(ast)
          
          codigo_intermedio = [str(instr) for instr in self.generador_intermedio.codigo]
          print("Código intermedio generado:")
          for linea in codigo_intermedio:
              print(f"- {linea}")
          return codigo_intermedio
      except Exception as e:
          print(f"Error en la generación de código intermedio: {str(e)}")
          return None

  def generar_codigo_final(self, ast, codigo_intermedio, nombre_archivo):
      """
      Genera el código final en Python.
      
      Args:
          ast: Árbol de sintaxis abstracta
          codigo_intermedio: Lista de instrucciones intermedias
          nombre_archivo (str): Nombre del archivo de salida
          
      Returns:
          bool: True si la generación fue exitosa, False si hubo errores
      """
      print("\n=== GENERACIÓN DE CÓDIGO FINAL ===")
      try:
          self.generador.generar_codigo(ast, codigo_intermedio, nombre_archivo)
          print(f"Código Python generado exitosamente en: {nombre_archivo}")
          return True
      except Exception as e:
          print(f"Error en la generación de código final: {str(e)}")
          return False

  def imprimir_ast(self, ast, nivel=0):
        """
        Imprime el AST en el formato específico mostrado en la imagen
        """
        print("\nEstructura del programa:")
        print("=" * 55)
        
        def formato_nodo(nodo):
            if isinstance(nodo, tuple):
                return str(nodo)
            elif isinstance(nodo, list):
                return str(nodo)
            else:
                return str(nodo)
        
        if isinstance(ast, list):
            for nodo in ast:
                print(f"Declaracion: {formato_nodo(nodo)}")
        else:
            print(f"Declaracion: {formato_nodo(ast)}")
        
        print("\nAnalisis sintactico completado exitosamente!")

  def compilar(self, codigo_fuente, nombre_archivo_salida="output.py"):
      """
      Ejecuta el proceso completo de compilación.
      
      Args:
          codigo_fuente (str): Código fuente a compilar
          nombre_archivo_salida (str): Nombre del archivo de salida
          
      Returns:
          bool: True si la compilación fue exitosa, False si hubo errores
          
      Proceso:
      1. Análisis léxico
      2. Análisis sintáctico
      3. Análisis semántico
      4. Generación de código intermedio
      5. Generación de código final
      """
      print("\n=== INICIO DE COMPILACIÓN ===")
      print("Código fuente a compilar:")
      print(codigo_fuente)
      
      # Ejecuta cada fase de la compilación
      if not self.analisis_lexico(codigo_fuente):
          return False
      
      ast = self.analisis_sintactico(codigo_fuente)
      if not ast:
          return False
      
      if not self.analisis_semantico(ast):
          return False
      
      codigo_intermedio = self.generar_codigo_intermedio(ast)
      if not codigo_intermedio:
          return False
      
      if not self.generar_codigo_final(ast, codigo_intermedio, nombre_archivo_salida):
          return False
      
      print("\n=== COMPILACIÓN EXITOSA ===")
      return True

def compilar_y_ejecutar(codigo_fuente, nombre_archivo_salida="output.py"):
  """
  Función auxiliar que compila y ejecuta el código fuente.
  
  Args:
      codigo_fuente (str): Código fuente a compilar y ejecutar
      nombre_archivo_salida (str): Nombre del archivo de salida
      
  Proceso:
  1. Crea una instancia del compilador
  2. Compila el código
  3. Ejecuta el código compilado si la compilación fue exitosa
  """
  compilador = Compilador()
  
  if compilador.compilar(codigo_fuente, nombre_archivo_salida):
      print("\n=== EJECUTANDO PROGRAMA COMPILADO ===")
      try:
          with open(nombre_archivo_salida, "r") as f:
              exec(f.read())
      except Exception as e:
          print(f"Error durante la ejecución: {str(e)}")
  else:
      print("\n=== LA COMPILACIÓN FALLÓ ===")
      
      

# Ejemplo de uso
#para el codigo notarás que añadí todas las instrucciones de una vez

#Declaracón variables, while, if, elsif, for
#En terminos de else, no hay no else XD
#Wacha
if __name__ == "__main__":
  codigo_prueba = """
  entero x = 5;
    entero y = 3;
    entero z = x + y*2;
    si (z < 5) {
      print(y);
    }
    sino (z > 5) {
      print(x);
    }
  para (entero i = 0; i < 3; i = i + 1) {
      print(i);
  }
  mientras (x > 0) {
      x = x - 1;
        print(x);
  }
  """
compilar_y_ejecutar(codigo_prueba, "programa_compilado.py")