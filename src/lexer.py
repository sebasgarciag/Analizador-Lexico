"""
Analizador Léxico (Lexer)

Este módulo implementa un analizador léxico para un lenguaje de programación tipo C.
El analizador convierte el código fuente en una secuencia de tokens que representan
las unidades léxicas fundamentales del lenguaje.

Características principales:
- Reconocimiento de palabras reservadas
- Identificación de identificadores
- Manejo de números (enteros y decimales)
- Procesamiento de strings
- Reconocimiento de operadores y símbolos
- Manejo de comentarios (línea simple y multilínea)
- Seguimiento preciso de línea y columna

"""

import re
from typing import List, NamedTuple
import os

# Definición de tipos de tokens
TOKEN_TYPES = [
    ('WHITESPACE', r'\s+'),
    ('COMMENT_START', r'/\*'),
    ('COMMENT_END', r'\*/'),
    ('LINE_COMMENT', r'//.*'),
    ('INVALID_IDENTIFIER', r'\d+[a-zA-Z_][a-zA-Z0-9_]*'),  # Identificadores que empiezan con número
    ('INVALID_NUMBER', r'\d+\.\d+\.\d+'),  # Números inválidos como 1.2.3
    ('NUMBER', r'\d+(\.\d+)?'),
    ('STRING', r'"[^"\n]*"?'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('OPERATOR', r'[+\-*/=<>!&|]+'),
    ('PUNCTUATION', r'[(){}\[\];,.]'),
    ('UNKNOWN', r'.')  # Captura cualquier carácter no reconocido
]

# Palabras reservadas y tipos
RESERVED_WORDS = {
    'if', 'else', 'while', 'for', 'return'
}

TYPE_WORDS = {
    'int', 'float', 'string', 'void'
}

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

def validate_token(token: Token) -> List[Token]:
    """Valida un token y retorna una lista de tokens o errores."""
    if token.type == 'INVALID_IDENTIFIER':
        return [Token('ERROR', f'Invalid identifier (starts with number): {token.value}', token.line, token.column)]
    elif token.type == 'INVALID_NUMBER':
        return [Token('ERROR', f'Invalid number format: {token.value}', token.line, token.column)]
    elif token.type == 'IDENTIFIER':
        # Convertir palabras reservadas y tipos
        if token.value in RESERVED_WORDS:
            return [Token(token.value.upper(), token.value, token.line, token.column)]
        elif token.value in TYPE_WORDS:
            return [Token('TYPE', token.value, token.line, token.column)]
    elif token.type == 'STRING':
        # Validar strings
        if not token.value.endswith('"'):
            return [Token('ERROR', 'Unterminated string literal', token.line, token.column)]
        # Remover las comillas para el valor final
        return [Token('STRING', token.value[1:-1], token.line, token.column)]
    elif token.type == 'UNKNOWN':
        return [Token('ERROR', f'Unexpected character: {token.value}', token.line, token.column)]
    return [token]

def tokenize(text: str) -> List[Token]:
    """Convierte el texto de entrada en una lista de tokens."""
    tokens = []
    pos = 0
    line = 1
    column = 1
    comment_stack = []  # Pila para rastrear comentarios anidados
    
    while pos < len(text):
        match = None
        
        # Si estamos dentro de un comentario, buscar inicio/fin de comentario
        if comment_stack:
            if text[pos:pos+2] == '/*':
                # Detectar comentario anidado
                comment_stack.append((line, column))
                if len(comment_stack) > 1:
                    tokens.append(Token('ERROR', 
                                     f'Nested comment detected at line {line}, column {column} ' +
                                     f'(outer comment started at line {comment_stack[0][0]}, column {comment_stack[0][1]})',
                                     line, column))
                pos += 2
                column += 2
                continue
            elif text[pos:pos+2] == '*/':
                if comment_stack:
                    comment_stack.pop()
                pos += 2
                column += 2
                continue
            else:
                if text[pos] == '\n':
                    line += 1
                    column = 1
                else:
                    column += 1
                pos += 1
                continue
        
        # Procesar tokens normales
        for token_type, pattern in TOKEN_TYPES:
            regex = re.compile(pattern)
            match = regex.match(text, pos)
            if match:
                value = match.group(0)
                
                if token_type == 'COMMENT_START':
                    comment_stack.append((line, column))
                    pos = match.end()
                    column += len(value)
                    break
                elif token_type == 'WHITESPACE' or token_type == 'LINE_COMMENT':
                    # Actualizar posición y contadores
                    for char in value:
                        if char == '\n':
                            line += 1
                            column = 1
                        else:
                            column += 1
                    pos = match.end()
                    break
                else:
                    # Validar y agregar el token
                    token = Token(token_type, value, line, column)
                    tokens.extend(validate_token(token))
                    pos = match.end()
                    column += len(value)
                break
        
        if not match and not comment_stack:
            # Si no hay coincidencia y no estamos en un comentario, es un error
            token = Token('UNKNOWN', text[pos], line, column)
            tokens.extend(validate_token(token))
            pos += 1
            column += 1
    
    # Verificar si hay comentarios sin cerrar al final del archivo
    if comment_stack:
        start_line, start_col = comment_stack[0]
        tokens.append(Token('ERROR', 
                          f'Unclosed comment block starting at line {start_line}, column {start_col}',
                          line, column))
    
    return tokens

def main():
    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    example_path = os.path.join(current_dir, "examples", "example1.txt")
    
    try:
        with open(example_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f"\nAnalizando archivo: {example_path}")
        print("=" * 50)
        print("Contenido del archivo:")
        print(code.rstrip())
        
        print("\nTokens encontrados:")
        tokens = tokenize(code)
        
        # Mostrar errores primero
        errors = [t for t in tokens if t.type == 'ERROR']
        if errors:
            print("\nErrores:")
            for error in errors:
                print(f"  Línea {error.line}, Columna {error.column}: {error.value}")
        
        # Mostrar tokens válidos
        print("\nTokens válidos:")
        valid_tokens = [t for t in tokens if t.type != 'ERROR']
        for token in valid_tokens:
            print(f"  {token.type:12} | Línea {token.line:2}, Col {token.column:2} | {token.value!r}")
        
        print("=" * 50)
        
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {example_path}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main() 