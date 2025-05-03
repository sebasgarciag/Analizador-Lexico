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
from typing import List, Optional
import os

# Definición de tipos de token y sus expresiones regulares
TOKEN_TYPES = [
    ("WHITESPACE", r"\s+"),                    # Espacios, tabs, saltos de línea
    ("COMMENT", r"//.*|/\*[\s\S]*?\*/"),      # Comentarios // y /* */
    ("NUMBER", r"\d+(?:\.\d+)?"),             # Enteros y decimales
    ("STRING", r'"(?:\\.|[^"\\])*"'),         # Strings con escape
    ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"), # Identificadores
    ("OPERATOR", r"\+|\-|\*|\/|==|!=|<=|>=|<|>"), # Operadores
    ("ASSIGN", r"="),                         # Asignación
    ("LPAREN", r"\("),                        # Paréntesis izquierdo
    ("RPAREN", r"\)"),                        # Paréntesis derecho
    ("LBRACE", r"{"),                         # Llave izquierda
    ("RBRACE", r"}"),                         # Llave derecha
    ("SEMICOLON", r";"),                      # Punto y coma
]

# Palabras reservadas del lenguaje
KEYWORDS = {"if", "else", "while", "return", "int", "float", "void"}

# Caracteres de escape permitidos
ESCAPE_CHARS = {
    'n': '\n',
    't': '\t',
    'r': '\r',
    '\\': '\\',
    '"': '"',
    "'": "'"
}

class Token:
    """
    Representa un token individual en el análisis léxico.
    
    Attributes:
        type (str): Tipo del token (ej: 'IDENTIFIER', 'NUMBER', etc.)
        value (str): Valor literal del token
        line (int): Número de línea donde se encontró el token
        column (int): Número de columna donde se encontró el token
    """
    
    def __init__(self, type: str, value: str, line: int, column: int):
        """
        Inicializa un nuevo token.
        
        Args:
            type: Tipo del token
            value: Valor literal del token
            line: Número de línea
            column: Número de columna
        """
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        """
        Retorna una representación string del token.
        
        Returns:
            str: Representación formateada del token
        """
        return f"Token({self.type}, {self.value!r}, line={self.line}, column={self.column})"

def process_string_literal(value: str) -> str:
    """
    Procesa un string literal, manejando caracteres de escape.
    
    Args:
        value (str): El string literal incluyendo las comillas
        
    Returns:
        str: El string procesado con los caracteres de escape interpretados
    """
    # Remover las comillas del inicio y final
    content = value[1:-1]
    result = []
    i = 0
    while i < len(content):
        if content[i] == '\\' and i + 1 < len(content):
            escape_char = content[i + 1]
            if escape_char in ESCAPE_CHARS:
                result.append(ESCAPE_CHARS[escape_char])
                i += 2
                continue
        result.append(content[i])
        i += 1
    return ''.join(result)

def tokenize(text: str) -> List[Token]:
    """
    Analiza el texto de entrada y lo convierte en una lista de tokens.
    
    Este método implementa el análisis léxico principal. Recorre el texto
    caracter por caracter, identificando y clasificando cada token según
    las reglas definidas en TOKEN_TYPES.
    
    Args:
        text (str): El código fuente a analizar
        
    Returns:
        List[Token]: Lista de tokens identificados
        
    Raises:
        ValueError: Si se encuentra un caracter no reconocido
    """
    tokens = []
    pos = 0
    line = 1
    col = 1
    length = len(text)
    
    while pos < length:
        match_found = False
        
        # Manejo especial para comentarios multilínea
        if text[pos:pos+2] == '/*':
            comment_level = 1
            comment_start = pos
            pos += 2
            col += 2
            
            while pos < length and comment_level > 0:
                if text[pos:pos+2] == '/*':
                    comment_level += 1
                    pos += 2
                    col += 2
                elif text[pos:pos+2] == '*/':
                    comment_level -= 1
                    pos += 2
                    col += 2
                else:
                    if text[pos] == '\n':
                        line += 1
                        col = 1
                    else:
                        col += 1
                    pos += 1
            
            if comment_level > 0:
                raise ValueError(f"Unclosed comment at line {line}, column {col}")
            continue
        
        # Intenta hacer match con cada tipo de token
        for token_type, regex in TOKEN_TYPES:
            pattern = re.compile(regex)
            match = pattern.match(text, pos)
            
            if match:
                match_found = True
                value = match.group(0)
                
                if token_type == "WHITESPACE":
                    # Actualizar línea y columna por saltos de línea
                    line_breaks = value.count("\n")
                    if line_breaks:
                        line += line_breaks
                        col = 1 + len(value) - (value.rfind("\n") + 1)
                    else:
                        col += len(value)
                elif token_type == "COMMENT":
                    # Solo procesar comentarios de línea simple
                    if value.startswith('//'):
                        line_breaks = value.count("\n")
                        if line_breaks:
                            line += line_breaks
                            col = 1 + len(value) - (value.rfind("\n") + 1)
                        else:
                            col += len(value)
                else:
                    # Procesar token normal
                    t_type = token_type
                    if token_type == "IDENTIFIER" and value in KEYWORDS:
                        t_type = value.upper()  # Convertir palabra reservada en tipo
                    elif token_type == "STRING":
                        value = process_string_literal(value)
                    tokens.append(Token(t_type, value, line, col))
                    col += len(value)
                
                pos = match.end()
                break
        
        if not match_found:
            raise ValueError(f"Unexpected character '{text[pos]}' at position {pos} (line {line}, column {col})")
    
    return tokens

if __name__ == "__main__":
    # Ejemplo de uso del analizador léxico
    
    # Obtener la ruta al archivo de ejemplo
    example_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "examples", "example1.txt")
    
    # Leer y analizar el archivo
    try:
        with open(example_path, encoding="utf-8") as f:
            code = f.read()
        tokens = tokenize(code)
        for token in tokens:
            print(token)
    except Exception as e:
        print(f"Error: {e}") 