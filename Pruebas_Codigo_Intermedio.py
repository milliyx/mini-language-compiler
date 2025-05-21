# main.py
from lexer import lexer
from parser import parser
from intermediate_code import compilar

def main():
    # Código fuente de ejemplo
    codigo_fuente = """
    para(entero y=0; y<20; y=y+1) {
        print(y);
    }
    """

    # Compilar el código
    codigo_intermedio, errores = compilar(codigo_fuente)

    # Imprimir resultados
    if errores:
        print("Errores durante la compilación:")
        for error in errores:
            print(error)
    else:
        print("Código Intermedio Generado:")
        for instruccion in codigo_intermedio:
            print(instruccion)

if __name__ == "__main__":
    main()