
from typing import List, Tuple, Union, Optional
from dataclasses import dataclass

class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}
        
    def agregar(self, identificador: str, tipo: str) -> None:
        self.simbolos[identificador] = {'tipo': tipo}
        
    def obtener_tipo(self, identificador: str) -> Optional[str]:
        return self.simbolos.get(identificador, {}).get('tipo')
        
    def existe(self, identificador: str) -> bool:
        return identificador in self.simbolos

@dataclass
class Instruccion:
    """Clase para representar una instrucción de código intermedio"""
    operacion: str
    resultado: str
    operando1: Optional[str] = None
    operando2: Optional[str] = None
    
    def __str__(self) -> str:
        if self.operacion == "label":
            return f"{self.resultado}:"
        elif self.operacion == "goto":
            return f"goto {self.resultado}"
        elif self.operacion == "if":
            return f"if {self.operando1} goto {self.resultado}"
        elif self.operacion == "print":
            return f"print {self.resultado}"
        elif self.operacion in ["+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="]:
            return f"{self.resultado} = {self.operando1} {self.operacion} {self.operando2}"
        else:
            return f"{self.resultado} = {self.operando1}"

class GeneradorCodigoIntermedio:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.codigo: List[Instruccion] = []
        self.tabla_simbolos = TablaSimbolos()
        
    def nuevo_temporal(self) -> str:
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
        
    def nueva_etiqueta(self) -> str:
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
        
    def agregar_codigo(self, instruccion: Instruccion) -> None:
        self.codigo.append(instruccion)

    def generar_expresion(self, nodo: Union[tuple, str, int, float]) -> str:
        if isinstance(nodo, (int, float)):
            return str(nodo)
            
        if isinstance(nodo, str):
            if not self.tabla_simbolos.existe(nodo):
                raise ValueError(f"Variable no declarada: {nodo}")
            return nodo
            
        if isinstance(nodo, tuple):
            if nodo[0] == 'operacion':
                _, operador, op1, op2 = nodo
                temp1 = self.generar_expresion(op1)
                temp2 = self.generar_expresion(op2)
                temp = self.nuevo_temporal()
                self.agregar_codigo(Instruccion(operador, temp, temp1, temp2))
                return temp
                
            elif nodo[0] == 'termino':
                return str(nodo[1])
                
        raise ValueError(f"Expresión no válida: {nodo}")

    def generar_declaracion(self, nodo: tuple) -> None:
        _, tipo, id, valor = nodo
        
        if self.tabla_simbolos.existe(id):
            raise ValueError(f"Variable ya declarada: {id}")
            
        self.tabla_simbolos.agregar(id, tipo)
        
        if valor:
            temp = self.generar_expresion(valor)
            self.agregar_codigo(Instruccion("=", id, temp))

    def generar_asignacion(self, nodo: tuple) -> None:
        _, id, valor = nodo
        
        if not self.tabla_simbolos.existe(id):
            raise ValueError(f"Variable no declarada: {id}")
            
        temp = self.generar_expresion(valor)
        self.agregar_codigo(Instruccion("=", id, temp))

    def generar_condicion(self, nodo: tuple) -> str:
        _, operador, op1, op2 = nodo
        temp1 = self.generar_expresion(op1)
        temp2 = self.generar_expresion(op2)
        temp = self.nuevo_temporal()
        self.agregar_codigo(Instruccion(operador, temp, temp1, temp2))
        return temp

    def generar_if(self, nodo: tuple) -> None:
        tipo_if = nodo[0]
        
        if tipo_if == 'si':  # if simple
            _, condicion, bloque = nodo
            etiq_verdadera = self.nueva_etiqueta()
            etiq_fin = self.nueva_etiqueta()
            
            temp_cond = self.generar_condicion(condicion)
            self.agregar_codigo(Instruccion("if", etiq_verdadera, temp_cond))
            self.agregar_codigo(Instruccion("goto", etiq_fin))
            
            self.agregar_codigo(Instruccion("label", etiq_verdadera))
            self.generar_bloque(bloque)
            self.agregar_codigo(Instruccion("label", etiq_fin))
            
        elif tipo_if == 'si_sino':  # if con else-if
            _, condicion1, bloque1, condicion2, bloque2 = nodo
            etiq_verdadera1 = self.nueva_etiqueta()
            etiq_verdadera2 = self.nueva_etiqueta()
            etiq_fin = self.nueva_etiqueta()
            
            # Primera condición (if)
            temp_cond1 = self.generar_condicion(condicion1)
            self.agregar_codigo(Instruccion("if", etiq_verdadera1, temp_cond1))
            
            # Segunda condición (sino)
            temp_cond2 = self.generar_condicion(condicion2)
            self.agregar_codigo(Instruccion("if", etiq_verdadera2, temp_cond2))
            self.agregar_codigo(Instruccion("goto", etiq_fin))
            
            # Primer bloque
            self.agregar_codigo(Instruccion("label", etiq_verdadera1))
            self.generar_bloque(bloque1)
            self.agregar_codigo(Instruccion("goto", etiq_fin))
            
            # Segundo bloque
            self.agregar_codigo(Instruccion("label", etiq_verdadera2))
            self.generar_bloque(bloque2)
            
            self.agregar_codigo(Instruccion("label", etiq_fin))
            
        elif tipo_if == 'si_sino_eoc':  # if con else-if y else
            _, condicion1, bloque1, condicion2, bloque2, bloque_eoc = nodo
            etiq_verdadera1 = self.nueva_etiqueta()
            etiq_verdadera2 = self.nueva_etiqueta()
            etiq_eoc = self.nueva_etiqueta()
            etiq_fin = self.nueva_etiqueta()
            
            # Primera condición (if)
            temp_cond1 = self.generar_condicion(condicion1)
            self.agregar_codigo(Instruccion("if", etiq_verdadera1, temp_cond1))
            
            # Segunda condición (sino)
            temp_cond2 = self.generar_condicion(condicion2)
            self.agregar_codigo(Instruccion("if", etiq_verdadera2, temp_cond2))
            self.agregar_codigo(Instruccion("goto", etiq_eoc))
            
            # Primer bloque
            self.agregar_codigo(Instruccion("label", etiq_verdadera1))
            self.generar_bloque(bloque1)
            self.agregar_codigo(Instruccion("goto", etiq_fin))
            
            # Segundo bloque
            self.agregar_codigo(Instruccion("label", etiq_verdadera2))
            self.generar_bloque(bloque2)
            self.agregar_codigo(Instruccion("goto", etiq_fin))
            
            # Bloque eoc
            self.agregar_codigo(Instruccion("label", etiq_eoc))
            self.generar_bloque(bloque_eoc)
            
            self.agregar_codigo(Instruccion("label", etiq_fin))
            
        elif tipo_if == 'si_eoc':  # if con else
            _, condicion, bloque, bloque_eoc = nodo
            etiq_verdadera = self.nueva_etiqueta()
            etiq_eoc = self.nueva_etiqueta()
            etiq_fin = self.nueva_etiqueta()
            
            temp_cond = self.generar_condicion(condicion)
            self.agregar_codigo(Instruccion("if", etiq_verdadera, temp_cond))
            self.agregar_codigo(Instruccion("goto", etiq_eoc))
            
            self.agregar_codigo(Instruccion("label", etiq_verdadera))
            self.generar_bloque(bloque)
            self.agregar_codigo(Instruccion("goto", etiq_fin))
            
            self.agregar_codigo(Instruccion("label", etiq_eoc))
            self.generar_bloque(bloque_eoc)
            
            self.agregar_codigo(Instruccion("label", etiq_fin))

    def generar_while(self, nodo: tuple) -> None:
        _, condicion, bloque = nodo
        etiq_inicio = self.nueva_etiqueta()
        etiq_cuerpo = self.nueva_etiqueta()
        etiq_fin = self.nueva_etiqueta()

        self.agregar_codigo(Instruccion("label", etiq_inicio))
        temp_cond = self.generar_condicion(condicion)
        self.agregar_codigo(Instruccion("if", etiq_cuerpo, temp_cond))
        self.agregar_codigo(Instruccion("goto", etiq_fin))
        
        self.agregar_codigo(Instruccion("label", etiq_cuerpo))
        self.generar_bloque(bloque)
        self.agregar_codigo(Instruccion("goto", etiq_inicio))
        self.agregar_codigo(Instruccion("label", etiq_fin))

    def generar_for(self, nodo: tuple) -> None:
        """
        Genera código intermedio para una estructura for
        
        Args:
            nodo: Tupla que contiene la información del bucle for
        """
        # Desempaquetar el nodo
        _, inicializacion, condicion, incremento, bloque = nodo
        
        # Generar código para la inicialización
        if inicializacion[0] == 'declaracion':
            self.generar_declaracion(inicializacion)
        elif inicializacion[0] == 'asignacion':
            self.generar_asignacion(inicializacion)
        
        # Crear etiquetas para el bucle
        etiq_inicio = self.nueva_etiqueta()
        etiq_cuerpo = self.nueva_etiqueta()
        etiq_fin = self.nueva_etiqueta()

        # Etiqueta de inicio del bucle
        self.agregar_codigo(Instruccion("label", etiq_inicio))
        
        # Generar código para la condición
        if isinstance(condicion, tuple) and condicion[0] == 'condicion':
            temp_cond = self.generar_condicion(condicion)
        else:
            temp_cond = self.generar_expresion(condicion)
        
        self.agregar_codigo(Instruccion("if", etiq_cuerpo, temp_cond))
        self.agregar_codigo(Instruccion("goto", etiq_fin))
        
        # Etiqueta y código del cuerpo del bucle
        self.agregar_codigo(Instruccion("label", etiq_cuerpo))
        self.generar_bloque(bloque)
        
        # Generar código para el incremento
        if isinstance(incremento, tuple):
            if incremento[0] == 'incremento':
                # Manejar incremento del tipo: i = i + 1
                _, var, op1, operador, op2 = incremento
                temp = self.nuevo_temporal()
                self.agregar_codigo(Instruccion(operador, temp, op1, str(op2)))
                self.agregar_codigo(Instruccion("=", var, temp))
            elif incremento[0] == 'incremento_simple':
                # Manejar incremento del tipo: i++
                _, var, operador = incremento
                temp = self.nuevo_temporal()
                self.agregar_codigo(Instruccion("+", temp, var, "1"))
                self.agregar_codigo(Instruccion("=", var, temp))
        
        # Volver al inicio del bucle
        self.agregar_codigo(Instruccion("goto", etiq_inicio))
        
        # Etiqueta de fin del bucle
        self.agregar_codigo(Instruccion("label", etiq_fin))

    def generar_bloque(self, bloque: List[tuple]) -> None:
        for instruccion in bloque:
            self.generar_codigo(instruccion)

    def generar_codigo(self, nodo: tuple) -> None:
        if not isinstance(nodo, tuple):
            return
            
        tipo_nodo = nodo[0]
        if tipo_nodo == 'declaracion':
            self.generar_declaracion(nodo)
        elif tipo_nodo == 'asignacion':
            self.generar_asignacion(nodo)
        elif tipo_nodo == 'si':
            self.generar_if(nodo)
        elif tipo_nodo == 'si_sino':
            self.generar_if(nodo)  # Aquí llamamos a la misma función para manejar si_sino
        elif tipo_nodo == 'si_sino_eoc':
            self.generar_if(nodo)  # Aquí también
        elif tipo_nodo == 'si_eoc':
            self.generar_if(nodo)  # Y aquí
        elif tipo_nodo == 'mientras':
            self.generar_while(nodo)
        elif tipo_nodo == 'para':
            self.generar_for(nodo)
        elif tipo_nodo == 'imprimir':
            temp = self.generar_expresion(nodo[1])
            self.agregar_codigo(Instruccion("print", temp))
        else:
            raise ValueError(f"Tipo de nodo no soportado: {tipo_nodo}")

def compilar(codigo_fuente: str) -> Tuple[Optional[List[str]], List[str]]:
    """
    Compila el código fuente y genera código intermedio
    
    Args:
        codigo_fuente: Código fuente a compilar
        
    Returns:
        Tuple[Optional[List[str]], List[str]]: (código intermedio, errores)
    """
    try:
        from lexer import lexer
        from parser import parser
        
        # Análisis sintáctico
        arbol = parser.parse(codigo_fuente, lexer=lexer)
        if not arbol:
            return None, ["Error en el análisis sintáctico"]

        # Generación de código intermedio
        generador = GeneradorCodigoIntermedio()
        if isinstance(arbol, list):
            for nodo in arbol:
                generador.generar_codigo(nodo)
        else:
            generador.generar_codigo(arbol)

        return [str(instr) for instr in generador.codigo], []

    except Exception as e:
        return None, [f"Error durante la compilación: {str(e)}"]

def guardar_codigo_intermedio(codigo: List[str], nombre_archivo: str) -> None:
    """
    Guarda el código intermedio generado en un archivo
    
    Args:
        codigo: Lista de instrucciones de código intermedio
        nombre_archivo: Nombre del archivo donde guardar el código
    """
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        for linea in codigo:
            f.write(linea + '\n')

if __name__ == "__main__":
    # Ejemplo 1: Operaciones aritméticas
    codigo1 = """
    entero a = 5;
    entero b = 3;
    entero c = a + b * 2;
    """
    
    print("Prueba 1: Operaciones aritméticas")
    codigo_intermedio, errores = compilar(codigo1)
    if errores:
        print("Errores encontrados:", errores)
    else:
        print("Código intermedio generado:")
        for linea in codigo_intermedio:
            print(linea)
    
    # Ejemplo 2: Estructura if-else
    codigo2 = """
    entero x = 4;
    si (x > 5) {
        x = x + 1;
    } sino (x<5){
        x = x - 1;
    }
    """
    
    print("\nPrueba 2: Estructura if-else")
    codigo_intermedio, errores = compilar(codigo2)
    if errores:
        print("Errores encontrados:", errores)
    else:
        print("Código intermedio generado:")
        for linea in codigo_intermedio:
            print(linea)
from typing import List, Tuple, Union, Optional
from dataclasses import dataclass

class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}
        
    def agregar(self, identificador: str, tipo: str) -> None:
        self.simbolos[identificador] = {'tipo': tipo}
        
    def obtener_tipo(self, identificador: str) -> Optional[str]:
        return self.simbolos.get(identificador, {}).get('tipo')
        
    def existe(self, identificador: str) -> bool:
        return identificador in self.simbolos

@dataclass
class Instruccion:
    """Clase para representar una instrucción de código intermedio"""
    operacion: str
    resultado: str
    operando1: Optional[str] = None
    operando2: Optional[str] = None
    
    def __str__(self) -> str:
        if self.operacion == "label":
            return f"{self.resultado}:"
        elif self.operacion == "goto":
            return f"goto {self.resultado}"
        elif self.operacion == "if":
            return f"if {self.operando1} goto {self.resultado}"
        elif self.operacion == "print":
            return f"print {self.resultado}"
        elif self.operacion in ["+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="]:
            return f"{self.resultado} = {self.operando1} {self.operacion} {self.operando2}"
        else:
            return f"{self.resultado} = {self.operando1}"

class GeneradorCodigoIntermedio:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.codigo: List[Instruccion] = []
        self.tabla_simbolos = TablaSimbolos()
        
    def nuevo_temporal(self) -> str:
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
        
    def nueva_etiqueta(self) -> str:
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
        
    def agregar_codigo(self, instruccion: Instruccion) -> None:
        self.codigo.append(instruccion)

    def generar_expresion(self, nodo: Union[tuple, str, int, float]) -> str:
        if isinstance(nodo, (int, float)):
            return str(nodo)
            
        if isinstance(nodo, str):
            if not self.tabla_simbolos.existe(nodo):
                raise ValueError(f"Variable no declarada: {nodo}")
            return nodo
            
        if isinstance(nodo, tuple):
            if nodo[0] == 'operacion':
                _, operador, op1, op2 = nodo
                temp1 = self.generar_expresion(op1)
                temp2 = self.generar_expresion(op2)
                temp = self.nuevo_temporal()
                self.agregar_codigo(Instruccion(operador, temp, temp1, temp2))
                return temp
                
            elif nodo[0] == 'termino':
                return str(nodo[1])
                
        raise ValueError(f"Expresión no válida: {nodo}")

    def generar_declaracion(self, nodo: tuple) -> None:
        _, tipo, id, valor = nodo
        
        if self.tabla_simbolos.existe(id):
            raise ValueError(f"Variable ya declarada: {id}")
            
        self.tabla_simbolos.agregar(id, tipo)
        
        if valor:
            temp = self.generar_expresion(valor)
            self.agregar_codigo(Instruccion("=", id, temp))

    def generar_asignacion(self, nodo: tuple) -> None:
        _, id, valor = nodo
        
        if not self.tabla_simbolos.existe(id):
            raise ValueError(f"Variable no declarada: {id}")
            
        temp = self.generar_expresion(valor)
        self.agregar_codigo(Instruccion("=", id, temp))

    def generar_condicion(self, nodo: tuple) -> str:
        _, operador, op1, op2 = nodo
        temp1 = self.generar_expresion(op1)
        temp2 = self.generar_expresion(op2)
        temp = self.nuevo_temporal()
        self.agregar_codigo(Instruccion(operador, temp, temp1, temp2))
        return temp

    def generar_if(self, nodo: tuple) -> None:
        tipo_if = nodo[0]
        
        if tipo_if == 'si':  # if simple
            _, condicion, bloque = nodo
            etiq_verdadera = self.nueva_etiqueta()
            etiq_fin = self.nueva_etiqueta()
            
            temp_cond = self.generar_condicion(condicion)
            self.agregar_codigo(Instruccion("if", etiq_verdadera, temp_cond))
            self.agregar_codigo(Instruccion("goto", etiq_fin))
            
            self.agregar_codigo(Instruccion("label", etiq_verdadera))
            self.generar_bloque(bloque)
            self.agregar_codigo(Instruccion("label", etiq_fin))
            
        elif tipo_if == 'si_sino':  # if con else-if
            _, condicion1, bloque1, condicion2, bloque2 = nodo
            etiq_verdadera1 = self.nueva_etiqueta()
            etiq_verdadera2 = self.nueva_etiqueta()
            etiq_fin = self.nueva_etiqueta()
            
            # Primera condición (if)
            temp_cond1 = self.generar_condicion(condicion1)
            self.agregar_codigo(Instruccion("if", etiq_verdadera1, temp_cond1))
            
            # Segunda condición (sino)
            temp_cond2 = self.generar_condicion(condicion2)
            self.agregar_codigo(Instruccion("if", etiq_verdadera2, temp_cond2))
            self.agregar_codigo(Instruccion("goto", etiq_fin))
            
            # Primer bloque
            self.agregar_codigo(Instruccion("label", etiq_verdadera1))
            self.generar_bloque(bloque1)
            self.agregar_codigo(Instruccion("goto", etiq_fin))
            
            # Segundo bloque
            self.agregar_codigo(Instruccion("label", etiq_verdadera2))
            self.generar_bloque(bloque2)
            
            self.agregar_codigo(Instruccion("label", etiq_fin))
            
        elif tipo_if == 'si_sino_eoc':  # if con else-if y else
            _, condicion1, bloque1, condicion2, bloque2, bloque_eoc = nodo
            etiq_verdadera1 = self.nueva_etiqueta()
            etiq_verdadera2 = self.nueva_etiqueta()
            etiq_eoc = self.nueva_etiqueta()
            etiq_fin = self.nueva_etiqueta()
            
            # Primera condición (if)
            temp_cond1 = self.generar_condicion(condicion1)
            self.agregar_codigo(Instruccion("if", etiq_verdadera1, temp_cond1))
            
            # Segunda condición (sino)
            temp_cond2 = self.generar_condicion(condicion2)
            self.agregar_codigo(Instruccion("if", etiq_verdadera2, temp_cond2))
            self.agregar_codigo(Instruccion("goto", etiq_eoc))
            
            # Primer bloque
            self.agregar_codigo(Instruccion("label", etiq_verdadera1))
            self.generar_bloque(bloque1)
            self.agregar_codigo(Instruccion("goto", etiq_fin))
            
            # Segundo bloque
            self.agregar_codigo(Instruccion("label", etiq_verdadera2))
            self.generar_bloque(bloque2)
            self.agregar_codigo(Instruccion("goto", etiq_fin))
            
            # Bloque eoc
            self.agregar_codigo(Instruccion("label", etiq_eoc))
            self.generar_bloque(bloque_eoc)
            
            self.agregar_codigo(Instruccion("label", etiq_fin))
            
        elif tipo_if == 'si_eoc':  # if con else
            _, condicion, bloque, bloque_eoc = nodo
            etiq_verdadera = self.nueva_etiqueta()
            etiq_eoc = self.nueva_etiqueta()
            etiq_fin = self.nueva_etiqueta()
            
            temp_cond = self.generar_condicion(condicion)
            self.agregar_codigo(Instruccion("if", etiq_verdadera, temp_cond))
            self.agregar_codigo(Instruccion("goto", etiq_eoc))
            
            self.agregar_codigo(Instruccion("label", etiq_verdadera))
            self.generar_bloque(bloque)
            self.agregar_codigo(Instruccion("goto", etiq_fin))
            
            self.agregar_codigo(Instruccion("label", etiq_eoc))
            self.generar_bloque(bloque_eoc)
            
            self.agregar_codigo(Instruccion("label", etiq_fin))

    def generar_while(self, nodo: tuple) -> None:
        _, condicion, bloque = nodo
        etiq_inicio = self.nueva_etiqueta()
        etiq_cuerpo = self.nueva_etiqueta()
        etiq_fin = self.nueva_etiqueta()

        self.agregar_codigo(Instruccion("label", etiq_inicio))
        temp_cond = self.generar_condicion(condicion)
        self.agregar_codigo(Instruccion("if", etiq_cuerpo, temp_cond))
        self.agregar_codigo(Instruccion("goto", etiq_fin))
        
        self.agregar_codigo(Instruccion("label", etiq_cuerpo))
        self.generar_bloque(bloque)
        self.agregar_codigo(Instruccion("goto", etiq_inicio))
        self.agregar_codigo(Instruccion("label", etiq_fin))

    def generar_for(self, nodo: tuple) -> None:
        _, inicializacion, condicion, incremento, bloque = nodo
        
        # Handle initialization
        if inicializacion[0] == 'declaracion':
            self.generar_declaracion(inicializacion)
        elif inicializacion[0] == 'asignacion':
            self.generar_asignacion(inicializacion)
        
        # Create and handle labels
        etiq_inicio = self.nueva_etiqueta()
        etiq_cuerpo = self.nueva_etiqueta()
        etiq_fin = self.nueva_etiqueta()
        
        self.agregar_codigo(Instruccion("label", etiq_inicio))
        
        # Handle condition
        temp_cond = self.generar_condicion(condicion) if isinstance(condicion, tuple) and condicion[0] == 'condicion' else self.generar_expresion(condicion)
        
        self.agregar_codigo(Instruccion("if", etiq_cuerpo, temp_cond))
        self.agregar_codigo(Instruccion("goto", etiq_fin))
        
        # Handle loop body
        self.agregar_codigo(Instruccion("label", etiq_cuerpo))
        self.generar_bloque(bloque)
        
        # Handle increment
        if isinstance(incremento, tuple):
            if incremento[0] == 'incremento':
                _, var, op1, operador, op2 = incremento
                temp = self.nuevo_temporal()
                self.agregar_codigo(Instruccion(operador, temp, op1, str(op2)))
                self.agregar_codigo(Instruccion("=", var, temp))
            elif incremento[0] == 'incremento_simple':
                _, var, operador = incremento
                temp = self.nuevo_temporal()
                self.agregar_codigo(Instruccion("+", temp, var, "1"))
                self.agregar_codigo(Instruccion("=", var, temp))
        
        self.agregar_codigo(Instruccion("goto", etiq_inicio))
        self.agregar_codigo(Instruccion("label", etiq_fin))

    def generar_incremento(self, nodo: tuple) -> None:
        _, var, op1, operador, op2 = nodo
        temp = self.nuevo_temporal()
        self.agregar_codigo(Instruccion(operador, temp, op1, str(op2)))
        self.agregar_codigo(Instruccion("=", var, temp))

    def generar_incremento_simple(self, nodo: tuple) -> None:
        _, var, operador = nodo
        temp = self.nuevo_temporal()
        if operador == '++':
            self.agregar_codigo(Instruccion("+", temp, var, "1"))
        elif operador == '--':
            self.agregar_codigo(Instruccion("-", temp, var, "1"))
        self.agregar_codigo(Instruccion("=", var, temp))

    def generar_bloque(self, bloque: List[tuple]) -> None:
        for instruccion in bloque:
            self.generar_codigo(instruccion)

    def generar_codigo(self, nodo: tuple) -> None:
        if not isinstance(nodo, tuple):
            return
            
        handlers = {
            'declaracion': self.generar_declaracion,
            'asignacion': self.generar_asignacion,
            'si': self.generar_if,
            'si_sino': self.generar_if,
            'si_sino_eoc': self.generar_if,
            'si_eoc': self.generar_if,
            'mientras': self.generar_while,
            'para': self.generar_for,
            'incremento': lambda n: self.generar_incremento(n),
            'incremento_simple': lambda n: self.generar_incremento_simple(n)
        }
            
        tipo_nodo = nodo[0]
        if tipo_nodo in handlers:
            handlers[tipo_nodo](nodo)
        elif tipo_nodo == 'imprimir':
            temp = self.generar_expresion(nodo[1])
            self.agregar_codigo(Instruccion("print", temp))
        else:
            raise ValueError(f"Tipo de nodo no soportado: {tipo_nodo}")

def compilar(codigo_fuente: str) -> Tuple[Optional[List[str]], List[str]]:
    """
    Compila el código fuente y genera código intermedio
    
    Args:
        codigo_fuente: Código fuente a compilar
        
    Returns:
        Tuple[Optional[List[str]], List[str]]: (código intermedio, errores)
    """
    try:
        from lexer import lexer
        from parser import parser
        
        # Análisis sintáctico
        arbol = parser.parse(codigo_fuente, lexer=lexer)
        if not arbol:
            return None, ["Error en el análisis sintáctico"]

        # Generación de código intermedio
        generador = GeneradorCodigoIntermedio()
        if isinstance(arbol, list):
            for nodo in arbol:
                generador.generar_codigo(nodo)
        else:
            generador.generar_codigo(arbol)

        return [str(instr) for instr in generador.codigo], []

    except Exception as e:
        return None, [f"Error durante la compilación: {str(e)}"]
