import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from lexer import tokenize, Token

def test_simple():
    """
    Prueba el análisis de una expresión simple:
    - Declaración de variable entera
    - Asignación de valor numérico
    """
    code = 'int x = 5;'
    tokens = tokenize(code)
    assert [t.type for t in tokens] == ['TYPE', 'IDENTIFIER', 'OPERATOR', 'NUMBER', 'PUNCTUATION']
    assert tokens[0].value == 'int'
    assert tokens[1].value == 'x'
    assert tokens[3].value == '5'

def test_comment_and_whitespace():
    """
    Prueba el manejo de comentarios y espacios en blanco:
    - Comentario de línea simple (//)
    - Saltos de línea
    - Espacios y tabulaciones
    - Múltiples declaraciones
    """
    code = 'int x = 1; // comentario\nfloat y = x + 2.0;'
    tokens = tokenize(code)
    types = [t.type for t in tokens]
    assert 'COMMENT_START' not in types  # Los comentarios deben ser ignorados
    assert 'COMMENT_END' not in types    # Los comentarios deben ser ignorados
    assert 'LINE_COMMENT' not in types   # Los comentarios deben ser ignorados
    assert 'WHITESPACE' not in types     # Los espacios en blanco deben ser ignorados
    assert tokens[0].type == 'TYPE'      # Primera palabra reservada
    assert tokens[0].value == 'int'      # Valor de la primera palabra reservada

def test_unknown_token():
    """
    Prueba el manejo de caracteres no válidos:
    - Caracter especial no permitido ($)
    - Debe generar un token de error
    """
    code = 'int $x = 2;'
    tokens = tokenize(code)
    errors = [t for t in tokens if t.type == 'ERROR']
    assert len(errors) == 1
    assert "Unexpected character: $" in errors[0].value

def test_empty_string_literal():
    """
    Prueba el manejo de strings vacíos:
    - String literal sin contenido ("")
    - Debe ser reconocido como un token STRING válido
    """
    code = 'string s = "";'
    tokens = tokenize(code)
    assert any(t.type == 'STRING' and t.value == '' for t in tokens)

def test_unclosed_string():
    """
    Prueba el manejo de strings mal formados:
    - String sin comilla de cierre
    - Debe generar un token de error
    """
    code = 'string s = "no cierre;'
    tokens = tokenize(code)
    errors = [t for t in tokens if t.type == 'ERROR']
    assert len(errors) == 1
    assert "Unterminated string literal" in errors[0].value

def test_nested_comments():
    """
    Prueba el manejo de comentarios anidados:
    - Comentario multilínea externo /* */
    - Comentario multilínea interno /* */
    - Texto después del comentario
    - Debe generar un token de error por comentario anidado
    """
    code = '/* externo /* interno */ fin */ int x = 1;'
    tokens = tokenize(code)
    errors = [t for t in tokens if t.type == 'ERROR']
    assert len(errors) == 1
    assert "Nested comment detected" in errors[0].value
    
    # Verificar que el código después del comentario se procesa correctamente
    valid_tokens = [t for t in tokens if t.type != 'ERROR']
    assert len(valid_tokens) == 5  # TYPE, IDENTIFIER, OPERATOR, NUMBER, PUNCTUATION
    assert valid_tokens[0].type == 'TYPE'
    assert valid_tokens[0].value == 'int'
    assert valid_tokens[1].value == 'x'
    assert valid_tokens[2].value == '='
    assert valid_tokens[3].value == '1'

def test_invalid_number():
    """
    Prueba el manejo de números inválidos:
    - Número con múltiples puntos decimales
    - Debe generar un token de error
    """
    code = 'float x = 1.2.3;'
    tokens = tokenize(code)
    errors = [t for t in tokens if t.type == 'ERROR']
    assert len(errors) == 1
    assert "Invalid number format" in errors[0].value

def test_invalid_identifier():
    """
    Prueba el manejo de identificadores inválidos:
    - Identificador que comienza con número
    - Debe generar un token de error
    """
    code = 'int 123abc = 5;'
    tokens = tokenize(code)
    errors = [t for t in tokens if t.type == 'ERROR']
    assert len(errors) == 1
    assert "Invalid identifier (starts with number)" in errors[0].value 