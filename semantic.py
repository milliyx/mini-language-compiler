class AnalizadorSemantico:
    def __init__(self):
        self.tabla_simbolos = {}
        self.temp_counter = 0
        self.label_counter = 0
        self.codigo_intermedio = []
        self.errores = []
        self.constantes = {}

    def nuevo_temporal(self):
        """Genera un nuevo nombre de variable temporal"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def nueva_etiqueta(self):
        """Genera una nueva etiqueta"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def agregar_codigo(self, codigo):
        """Agrega una línea de código intermedio"""
        self.codigo_intermedio.append(codigo)

    def optimizar_constantes(self, valor):
        """Optimiza expresiones constantes"""
        if isinstance(valor, (int, float)):
            return str(valor)
        if isinstance(valor, str) and valor.isdigit():
            return valor
        if str(valor) in self.constantes:
            return self.constantes[str(valor)]
        return None

    def analizar_nodo(self, nodo):
        """Analiza un nodo del AST"""
        if not isinstance(nodo, tuple):
            # Si es un valor literal o identificador
            if isinstance(nodo, (int, float)):
                return str(nodo)
            elif isinstance(nodo, str):
                if nodo in self.tabla_simbolos:
                    return self.tabla_simbolos[nodo].get('valor', nodo)
            return nodo

        tipo_nodo = nodo[0]
        if tipo_nodo == 'declaracion':
            return self.procesar_declaracion(nodo)
        elif tipo_nodo == 'operacion':
            return self.procesar_operacion(nodo)
        elif tipo_nodo == 'asignacion':
            return self.procesar_asignacion(nodo)
        elif tipo_nodo == 'si':
            return self.procesar_si(nodo)
        elif tipo_nodo == 'si_sino':
            return self.procesar_si_sino(nodo)
        elif tipo_nodo == 'si_sino_eoc':
            return self.procesar_si_sino_eoc(nodo)
        elif tipo_nodo == 'si_eoc':
            return self.procesar_si_eoc(nodo)
        elif tipo_nodo == 'mientras':
            return self.procesar_mientras(nodo)
        elif tipo_nodo == 'para':
            return self.procesar_para(nodo)
        elif tipo_nodo == 'imprimir':
            return self.procesar_imprimir(nodo)
        elif tipo_nodo == 'condicion':
            return self.procesar_condicion(nodo)
        return None

    def procesar_declaracion(self, nodo):
        """Procesa una declaración de variable"""
        _, tipo, identificador, *valor = nodo
        
        # Verificar si la variable ya existe
        if identificador in self.tabla_simbolos:
            self.errores.append(f"Error: Variable '{identificador}' ya declarada")
            return None
        
        # Registrar la variable en la tabla de símbolos
        self.tabla_simbolos[identificador] = {
            'tipo': tipo,
            'valor': None,
            'constante': False
        }
        
        # Procesar valor inicial si existe
        if valor and valor[0] is not None:
            valor_optimizado = self.optimizar_constantes(valor[0])
            if valor_optimizado:
                self.agregar_codigo(f"{identificador} = {valor_optimizado}")
                self.tabla_simbolos[identificador]['valor'] = valor_optimizado
            else:
                valor_temp = self.analizar_nodo(valor[0])
                if valor_temp:
                    self.agregar_codigo(f"{identificador} = {valor_temp}")
                    self.tabla_simbolos[identificador]['valor'] = valor_temp
        
        return identificador

    def procesar_asignacion(self, nodo):
        """Procesa una asignación"""
        _, identificador, valor = nodo
        
        if identificador not in self.tabla_simbolos:
            self.errores.append(f"Error: Variable '{identificador}' no declarada")
            return None
        
        if self.tabla_simbolos[identificador]['constante']:
            self.errores.append(f"Error: No se puede modificar la constante '{identificador}'")
            return None
        
        valor_optimizado = self.optimizar_constantes(valor)
        if valor_optimizado:
            self.agregar_codigo(f"{identificador} = {valor_optimizado}")
            self.tabla_simbolos[identificador]['valor'] = valor_optimizado
        else:
            valor_temp = self.analizar_nodo(valor)
            if valor_temp:
                self.agregar_codigo(f"{identificador} = {valor_temp}")
                self.tabla_simbolos[identificador]['valor'] = valor_temp
        
        return identificador

    def procesar_operacion(self, nodo):
        """Procesa una operación aritmética"""
        _, operador, op1, op2 = nodo
        
        val1 = self.optimizar_constantes(op1)
        val2 = self.optimizar_constantes(op2)
        
        if val1 and val2:
            try:
                resultado = eval(f"{val1} {operador} {val2}")
                self.constantes[str(resultado)] = str(resultado)
                return str(resultado)
            except:
                pass

        temp1 = val1 if val1 else self.analizar_nodo(op1)
        temp2 = val2 if val2 else self.analizar_nodo(op2)
        
        if temp1 and temp2:
            temp = self.nuevo_temporal()
            self.agregar_codigo(f"{temp} = {temp1} {operador} {temp2}")
            return temp
        return None

    def procesar_condicion(self, nodo):
        """Procesa una condición"""
        _, operador, op1, op2 = nodo
        temp1 = self.analizar_nodo(op1)
        temp2 = self.analizar_nodo(op2)
        
        if temp1 and temp2:
            return f"{temp1} {operador} {temp2}"
        return None

    def procesar_si(self, nodo):
        """Procesa una estructura if simple"""
        _, condicion, bloque = nodo
        
        etiq_verdadera = self.nueva_etiqueta()
        etiq_fin = self.nueva_etiqueta()
        
        cond_temp = self.procesar_condicion(condicion)
        self.agregar_codigo(f"if {cond_temp} goto {etiq_verdadera}")
        self.agregar_codigo(f"goto {etiq_fin}")
        
        self.agregar_codigo(f"{etiq_verdadera}:")
        for inst in bloque:
            self.analizar_nodo(inst)
        
        self.agregar_codigo(f"{etiq_fin}:")

    def procesar_si_sino(self, nodo):
        """Procesa una estructura if-else"""
        _, condicion, bloque_verdadero, condicion2, bloque_falso = nodo
        
        etiq_verdadera = self.nueva_etiqueta()
        etiq_falsa = self.nueva_etiqueta()
        etiq_fin = self.nueva_etiqueta()
        
        cond_temp = self.procesar_condicion(condicion)
        self.agregar_codigo(f"if {cond_temp} goto {etiq_verdadera}")
        
        cond_temp2 = self.procesar_condicion(condicion2)
        self.agregar_codigo(f"if {cond_temp2} goto {etiq_falsa}")
        self.agregar_codigo(f"goto {etiq_fin}")
        
        self.agregar_codigo(f"{etiq_verdadera}:")
        for inst in bloque_verdadero:
            self.analizar_nodo(inst)
        self.agregar_codigo(f"goto {etiq_fin}")
        
        self.agregar_codigo(f"{etiq_falsa}:")
        for inst in bloque_falso:
            self.analizar_nodo(inst)
        
        self.agregar_codigo(f"{etiq_fin}:")

    def procesar_mientras(self, nodo):
        """Procesa una estructura while"""
        _, condicion, bloque = nodo
        
        etiq_inicio = self.nueva_etiqueta()
        etiq_cuerpo = self.nueva_etiqueta()
        etiq_fin = self.nueva_etiqueta()
        
        self.agregar_codigo(f"{etiq_inicio}:")
        cond_temp = self.procesar_condicion(condicion)
        self.agregar_codigo(f"if {cond_temp} goto {etiq_cuerpo}")
        self.agregar_codigo(f"goto {etiq_fin}")
        
        self.agregar_codigo(f"{etiq_cuerpo}:")
        for inst in bloque:
            self.analizar_nodo(inst)
        self.agregar_codigo(f"goto {etiq_inicio}")
        
        self.agregar_codigo(f"{etiq_fin}:")

    def procesar_para(self, nodo):
        """Procesa una estructura for"""
        _, inicializacion, condicion, incremento, bloque = nodo
        
        # Procesar inicialización
        self.analizar_nodo(inicializacion)
        
        etiq_inicio = self.nueva_etiqueta()
        etiq_cuerpo = self.nueva_etiqueta()
        etiq_fin = self.nueva_etiqueta()
        
        self.agregar_codigo(f"{etiq_inicio}:")
        cond_temp = self.procesar_condicion(condicion)
        self.agregar_codigo(f"if {cond_temp} goto {etiq_cuerpo}")
        self.agregar_codigo(f"goto {etiq_fin}")
        
        self.agregar_codigo(f"{etiq_cuerpo}:")
        for inst in bloque:
            self.analizar_nodo(inst)
        self.analizar_nodo(incremento)
        self.agregar_codigo(f"goto {etiq_inicio}")
        
        self.agregar_codigo(f"{etiq_fin}:")

    def procesar_imprimir(self, nodo):
        """Procesa una instrucción de impresión"""
        _, expresion = nodo
        temp = self.analizar_nodo(expresion)
        if temp:
            self.agregar_codigo(f"print {temp}")

# Ejemplo de uso
if __name__ == "__main__":
    # Código de prueba
    codigo_prueba = """
    entero x = 5;
    entero y = 3;
    entero z = x + y;
    print(z);
    """
    
    analizador = AnalizadorSemantico()
    # Asumiendo que tienes el parser configurado
    # ast = parser.parse(codigo_prueba)
    # for nodo in ast:
    #     analizador.analizar_nodo(nodo)
    
    # Imprimir código intermedio
    print("\nCódigo intermedio generado:")
    for linea in analizador.codigo_intermedio:
        print(linea)
    
    # Imprimir tabla de símbolos
    print("\nTabla de símbolos:")
    for var, info in analizador.tabla_simbolos.items():
        print(f"{var}: {info}")