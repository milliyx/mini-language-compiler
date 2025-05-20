%{
#include <stdio.h>

int line_num = 1;  // Contador de líneas

// Función para imprimir token reconocido
void print_token(const char* token_name, const char* lexeme) {
    if (lexeme)
        printf("Token: %-15s Lexema: %s\n", token_name, lexeme);
    else
        printf("Token: %s\n", token_name);
}
%}

DIGITO      [0-9]
LETRA       [a-zA-Z]
ID          {LETRA}({LETRA}|{DIGITO})*

%%

\n              { line_num++; }
"if"            { print_token("IF", yytext); }
"else"          { print_token("ELSE", yytext); }
"while"         { print_token("WHILE", yytext); }
"do"            { print_token("DO", yytext); }
"for"           { print_token("FOR", yytext); }
"int"           { print_token("INT", yytext); }
"bool"          { print_token("BOOL", yytext); }
"void"          { print_token("VOID", yytext); }
"read"          { print_token("READ", yytext); }
"print"         { print_token("PRINT", yytext); }

"true"          { print_token("TRUE", yytext); }
"false"         { print_token("FALSE", yytext); }

{ID}            { print_token("IDENTIFICADOR", yytext); }
{DIGITO}+       { print_token("NUMERO", yytext); }

"=="            { print_token("IGUALDAD", yytext); }
"!="            { print_token("DIFERENTE", yytext); }
"<="            { print_token("MENOR_IGUAL", yytext); }
">="            { print_token("MAYOR_IGUAL", yytext); }
"<"             { print_token("MENOR", yytext); }
">"             { print_token("MAYOR", yytext); }

"&&"            { print_token("AND", yytext); }
"||"            { print_token("OR", yytext); }
"!"             { print_token("NOT", yytext); }

"+"             { print_token("MAS", yytext); }
"-"             { print_token("MENOS", yytext); }
"*"             { print_token("MULTIPLICACION", yytext); }
"/"             { print_token("DIVISION", yytext); }

"("             { print_token("PARENTESIS_IZQ", yytext); }
")"             { print_token("PARENTESIS_DER", yytext); }
"{"             { print_token("LLAVE_IZQ", yytext); }
"}"             { print_token("LLAVE_DER", yytext); }
";"             { print_token("PUNTO_Y_COMA", yytext); }
","             { print_token("COMA", yytext); }

[ \t\r]+        { /* Ignorar espacios y tabulaciones */ }

.               {
                    fprintf(stderr, "Error léxico en línea %d: caracter inválido '%s'\n", line_num, yytext);
                  }

%%

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            perror("No se pudo abrir el archivo");
            return 1;
        }
        yyin = file;
    } else {
        printf("Analizador léxico Mini-Lenguaje\n");
        printf("Escribe o pega el código y presiona Ctrl+D (Linux/macOS) o Ctrl+Z (Windows) para terminar.\n\n");
    }

    yylex();

    if (yyin != stdin) {
        fclose(yyin);
    }

    printf("\nAnálisis terminado.\n");
    return 0;
}
