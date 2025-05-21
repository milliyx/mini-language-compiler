class OptimizadorCodigo:
    def __init__(self):
        self.codigo = []
        self.variables_usadas = set()
        self.etiquetas_usadas = set()
        
    def optimizar(self, codigo_intermedio):
        """
        Realiza optimizaciones básicas en el código intermedio:
        1. Elimina asignaciones redundantes consecutivas
        2. Mantiene el seguimiento de etiquetas
        3. Preserva la estructura del código
        """
        codigo_optimizado = []
        ultima_asignacion = {}  # Para rastrear la última asignación de cada variable
        
        # Primera pasada: identificar etiquetas y variables usadas
        for linea in codigo_intermedio:
            if linea.endswith(':'):  # Es una etiqueta
                self.etiquetas_usadas.add(linea[:-1])
            elif 'goto' in linea:  # Es un salto
                partes = linea.split()
                if len(partes) > 1:
                    self.etiquetas_usadas.add(partes[-1])
            elif '=' in linea:  # Es una asignación
                var = linea.split('=')[0].strip()
                self.variables_usadas.add(var)
        
        # Segunda pasada: optimización básica
        for i, linea in enumerate(codigo_intermedio):
            # Siempre mantener etiquetas
            if linea.endswith(':'):
                codigo_optimizado.append(linea)
                continue
                
            # Siempre mantener saltos y condiciones
            if 'goto' in linea or linea.startswith('if'):
                codigo_optimizado.append(linea)
                continue
                
            # Siempre mantener prints
            if linea.startswith('print'):
                codigo_optimizado.append(linea)
                continue
                
            # Procesar asignaciones
            if '=' in linea:
                var, expr = [x.strip() for x in linea.split('=')]
                
                # Verificar si es una asignación redundante
                if var in ultima_asignacion and ultima_asignacion[var] == expr:
                    continue
                    
                ultima_asignacion[var] = expr
                codigo_optimizado.append(linea)
                continue
                
            # Mantener cualquier otra instrucción sin modificar
            codigo_optimizado.append(linea)
        
        return codigo_optimizado

def optimizar_codigo(codigo_intermedio):
    """Función auxiliar para optimizar el código"""
    optimizador = OptimizadorCodigo()
    return optimizador.optimizar(codigo_intermedio)

# Ejemplo de uso
if __name__ == "__main__":
    # Código intermedio de ejemplo
    codigo_ejemplo = [
        "x = 5",
        "y = 3",
        "t1 = y * 2",
        "z = x + t1",
        "if z > 10 goto L1",
        "if z < 5 goto L2",
        "goto L3",
        "L1:",
        "print z",
        "goto L3",
        "L2:",
        "print y",
        "L3:"
    ]
    
    # Optimizar el código
    codigo_optimizado = optimizar_codigo(codigo_ejemplo)
    
    print("Código original:")
    for linea in codigo_ejemplo:
        print(linea)
    
    print("\nCódigo optimizado:")
    for linea in codigo_optimizado:
        print(linea)