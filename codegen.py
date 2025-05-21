class GeneradorCodigoPython:
  def __init__(self):
      self.codigo_python = []  # Lista para almacenar las líneas de código generadas
      self.indentacion = 0  # Nivel de indentación actual
      self.codigo_intermedio = []  # Código intermedio para ayudar en la generación de código
      self.variables_declaradas = set()  # Conjunto de variables declaradas en el programa
      self.variables_temporales = set()  # Conjunto de variables temporales detectadas

  def agregar_linea(self, linea):
      """Agrega una línea de código con la indentación correcta"""
      self.codigo_python.append("    " * self.indentacion + linea)

  def generar_codigo(self, ast, codigo_intermedio, nombre_archivo="output.py"):
      """Genera código Python a partir del AST y código intermedio"""
      self.codigo_intermedio = codigo_intermedio
      self.codigo_python = []
      self.variables_declaradas = set()
      self.variables_temporales = set()
      
      # Analizar variables temporales en el código intermedio
      for linea in codigo_intermedio:
          if '=' in linea:
              var = linea.split('=')[0].strip()
              if var.startswith('t'):
                  self.variables_temporales.add(var)
      
      # Iniciar el archivo
      self.agregar_linea("def main():")
      self.indentacion += 1
      
      # Declarar variables temporales al inicio
      if self.variables_temporales:
          self.agregar_linea(f"# Variables temporales")
          for temp in self.variables_temporales:
              self.agregar_linea(f"{temp} = None")
          self.agregar_linea("")
      
      # Procesar el AST
      if isinstance(ast, list):
          for nodo in ast:
              self.procesar_nodo(nodo)
      else:
          self.procesar_nodo(ast)
      
      # Agregar punto de entrada
      self.indentacion = 0
      self.agregar_linea("\nif __name__ == '__main__':")
      self.indentacion += 1
      self.agregar_linea("main()")
      
      # Escribir archivo
      with open(nombre_archivo, 'w') as f:
          f.write("\n".join(self.codigo_python))

  def procesar_nodo(self, nodo):
      """Procesa un nodo del AST"""
      if not isinstance(nodo, tuple):
          return str(nodo)
      
      tipo_nodo = nodo[0]
      
      if tipo_nodo == 'declaracion':
          return self.procesar_declaracion(nodo)
      elif tipo_nodo == 'asignacion':
          return self.procesar_asignacion(nodo)
      elif tipo_nodo == 'si_sino':
        return self.procesar_si_sino(nodo)
      elif tipo_nodo == 'si_sino_eoc':
        return self.procesar_si_sino_eoc(nodo)
      elif tipo_nodo == 'si_eoc':  # Agregamos el caso si_eoc
        return self.procesar_si_eoc(nodo)
      elif tipo_nodo == 'mientras':
          return self.procesar_mientras(nodo)
      elif tipo_nodo == 'para':
          return self.procesar_para(nodo)
      elif tipo_nodo == 'imprimir':
          return self.procesar_imprimir(nodo)
      elif tipo_nodo == 'operacion':
          return self.procesar_operacion(nodo)

  def procesar_declaracion(self, nodo):
      """Procesa una declaración de variable"""
      _, tipo, identificador, valor = nodo
      self.variables_declaradas.add(identificador)
      
      if isinstance(valor, tuple) and valor[0] == 'operacion':
          # Buscar en código intermedio
          for linea in self.codigo_intermedio:
              if linea.startswith('t'):
                  # Agregar la operación temporal
                  self.agregar_linea(linea)
              elif linea.startswith(identificador):
                  # Agregar la asignación final
                  self.agregar_linea(linea)
                  return
      else:
          valor_procesado = self.procesar_nodo(valor)
          self.agregar_linea(f"{identificador} = {valor_procesado}")

  def procesar_asignacion(self, nodo):
      """Procesa una asignación"""
      _, identificador, valor = nodo
      valor_procesado = self.procesar_nodo(valor)
      self.agregar_linea(f"{identificador} = {valor_procesado}")

  def procesar_operacion(self, nodo):
      """Procesa una operación"""
      _, operador, op1, op2 = nodo
      return f"{self.procesar_nodo(op1)} {operador} {self.procesar_nodo(op2)}"

  def procesar_condicion(self, nodo):
      """Procesa una condición"""
      _, operador, op1, op2 = nodo
      return f"{self.procesar_nodo(op1)} {operador} {self.procesar_nodo(op2)}"

  def procesar_mientras(self, nodo):
      """Procesa una estructura while"""
      _, condicion, bloque = nodo
      
      # Generar la condición del while
      cond = self.procesar_condicion(condicion)
      self.agregar_linea(f"while {cond}:")
      
      # Procesar el bloque del while
      self.indentacion += 1
      for instruccion in bloque:
          self.procesar_nodo(instruccion)
      self.indentacion -= 1

  def procesar_si(self, nodo):
      """Procesa una estructura if simple"""
      _, condicion, bloque = nodo
      cond = self.procesar_condicion(condicion)
      self.agregar_linea(f"if {cond}:")
      self.indentacion += 1
      for instruccion in bloque:
          self.procesar_nodo(instruccion)
      self.indentacion -= 1

  def procesar_si_sino(self, nodo):
      """Procesa una estructura if-elif"""
      _, condicion1, bloque1, condicion2, bloque2 = nodo
      
      # Procesar if
      cond1 = self.procesar_condicion(condicion1)
      self.agregar_linea(f"if {cond1}:")
      self.indentacion += 1
      for instruccion in bloque1:
          self.procesar_nodo(instruccion)
      self.indentacion -= 1
      
      # Procesar elif
      cond2 = self.procesar_condicion(condicion2)
      self.agregar_linea(f"elif {cond2}:")
      self.indentacion += 1
      for instruccion in bloque2:
          self.procesar_nodo(instruccion)
      self.indentacion -= 1
 #esto es del if else
  def procesar_si_eoc(self, nodo):
    """Procesa una estructura if-else"""
    _, condicion, bloque1, bloque2 = nodo
    
    # Procesar if
    cond = self.procesar_condicion(condicion)
    self.agregar_linea(f"if {cond}:")
    self.indentacion += 1
    for instruccion in bloque1:
        self.procesar_nodo(instruccion)
    self.indentacion -= 1
    
    # Procesar else
    self.agregar_linea("else:")
    self.indentacion += 1
    for instruccion in bloque2:
        self.procesar_nodo(instruccion)
    self.indentacion -= 1

  def procesar_si_sino_eoc(self, nodo):
    """Procesa una estructura if-elif-else"""
    _, condicion1, bloque1, condicion2, bloque2, bloque3 = nodo
    
    # Procesar if
    cond1 = self.procesar_condicion(condicion1)
    self.agregar_linea(f"if {cond1}:")
    self.indentacion += 1
    for instruccion in bloque1:
        self.procesar_nodo(instruccion)
    self.indentacion -= 1
    
    # Procesar elif
    cond2 = self.procesar_condicion(condicion2)
    self.agregar_linea(f"elif {cond2}:")
    self.indentacion += 1
    for instruccion in bloque2:
        self.procesar_nodo(instruccion)
    self.indentacion -= 1
    
    # Procesar else
    self.agregar_linea("else:")
    self.indentacion += 1
    for instruccion in bloque3:
        self.procesar_nodo(instruccion)
    self.indentacion -= 1

  def procesar_para(self, nodo):
      """Procesa una estructura for"""
      _, inicializacion, condicion, incremento, bloque = nodo
      
      # Procesar inicialización
      var_control = inicializacion[2] if isinstance(inicializacion, tuple) else inicializacion
      valor_inicial = self.procesar_nodo(inicializacion[3]) if isinstance(inicializacion, tuple) else "0"
      
      # Extraer límite de la condición
      _, op, _, limite = condicion
      limite_valor = self.procesar_nodo(limite)
      
      # Generar for en Python
      self.agregar_linea(f"for {var_control} in range({valor_inicial}, {limite_valor}):")
      self.indentacion += 1
      
      for instruccion in bloque:
          self.procesar_nodo(instruccion)
      
      self.indentacion -= 1

  def procesar_imprimir(self, nodo):
      """Procesa una instrucción print"""
      _, expresion = nodo
      valor = self.procesar_nodo(expresion)
      self.agregar_linea(f"print({valor})")

if __name__ == "__main__":
  # Ejemplo de AST y código intermedio
  ast_ejemplo = [
      ('declaracion', 'entero', 'x', 5),
      ('mientras', 
          ('condicion', '>', 'x', 0),
          [
              ('imprimir', 'x'),
              ('asignacion', 'x', ('operacion', '-', 'x', 1))
          ]
      )
  ]
  
  codigo_intermedio_ejemplo = [
      "x = 5",
      "L0:",
      "t0 = x > 0",
      "if t0 goto L1",
      "goto L2",
      "L1:",
      "print x",
      "t1 = x - 1",
      "x = t1",
      "goto L0",
      "L2:"
  ]
  
  generador = GeneradorCodigoPython()
  generador.generar_codigo(ast_ejemplo, codigo_intermedio_ejemplo, "programa.py")