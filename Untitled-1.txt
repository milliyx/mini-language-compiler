%{
#include <stdio.h>
#include <stdlib.h>

// Declaración del analizador léxico
int yylex();
void yyerror(const char *s);
%}

/* Tokens desde el lexer */
%token INT BOOL TRUE FALSE IF ELSE WHILE DO FOR RETURN READ PRINT
%token ID NUM
%token AND OR NOT
%token EQ NE LE GE LT GT
%token ASSIGN
%token PLUS MINUS TIMES DIV
%token LPAREN RPAREN LBRACE RBRACE SEMICOLON COMMA

%start programa

%%

programa
    : lista_sentencias
    ;

lista_sentencias
    : lista_sentencias sentencia
    | sentencia
    ;

sentencia
    : declaracion SEMICOLON
    | asignacion SEMICOLON
    | lectura SEMICOLON
    | impresion SEMICOLON
    | sentencia_if
    | sentencia_while
    | bloque
    ;

bloque
    : LBRACE lista_sentencias RBRACE
    ;

declaracion
    : INT ID
    | BOOL ID
    ;

asignacion
    : ID ASSIGN expresion
    ;

lectura
    : READ ID
    ;

impresion
    : PRINT expresion
    ;

sentencia_if
    : IF LPAREN expresion RPAREN bloque
    ;

sentencia_while
    : WHILE LPAREN expresion RPAREN bloque
    ;

expresion
    : expresion PLUS expresion
    | expresion MINUS expresion
    | expresion TIMES expresion
    | expresion DIV expresion
    | expresion AND expresion
    | expresion OR expresion
    | NOT expresion
    | expresion EQ expresion
    | expresion NE expresion
    | expresion LE expresion
    | expresion GE expresion
    | expresion LT expresion
    | expresion GT expresion
    | LPAREN expresion RPAREN
    | ID
    | NUM
    | TRUE
    | FALSE
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error sintáctico: %s\n", s);
}
