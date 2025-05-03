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
    assert [t.type for t in tokens] == ['INT', 'IDENTIFIER', 'ASSIGN', 'NUMBER', 'SEMICOLON']
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
    assert 'COMMENT' not in types      # Los comentarios deben ser ignorados
    assert 'WHITESPACE' not in types   # Los espacios en blanco deben ser ignorados
    assert tokens[0].type == 'INT'     # Primera palabra reservada
    assert tokens[5].type == 'FLOAT'   # Segunda palabra reservada
    assert tokens[-1].type == 'SEMICOLON'

def test_unknown_token():
    """
    Prueba el manejo de caracteres no válidos:
    - Caracter especial no permitido ($)
    - Debe lanzar un error con mensaje descriptivo
    """
    code = 'int $x = 2;'
    with pytest.raises(ValueError) as excinfo:
        tokenize(code)
    assert "Unexpected character '$'" in str(excinfo.value)

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
    - Debe lanzar un error de validación
    """
    code = 'string s = "no cierre;'
    with pytest.raises(ValueError):
        tokenize(code)

def test_nested_comments():
    """
    Prueba el manejo de comentarios anidados:
    - Comentario multilínea externo /* */
    - Comentario multilínea interno /* */
    - Texto después del comentario
    - Debe ignorar todo el contenido del comentario
    """
    code = '/* externo /* interno */ fin */ int x = 1;'
    tokens = tokenize(code)
    assert len(tokens) == 5  # INT, IDENTIFIER, ASSIGN, NUMBER, SEMICOLON
    assert tokens[0].type == 'INT'
    assert tokens[1].type == 'IDENTIFIER'
    assert tokens[1].value == 'x'
    assert tokens[2].type == 'ASSIGN'
    assert tokens[3].type == 'NUMBER'
    assert tokens[3].value == '1'
    assert tokens[4].type == 'SEMICOLON'

def test_string_escape_chars():
    """
    Prueba el manejo de caracteres de escape en strings:
    - Nueva línea (\n)
    - Tabulación (\t)
    - Retorno de carro (\r)
    - Barra invertida (\\)
    - Comillas (\", \')
    """
    code = 'string s = "\\n\\t\\r\\\\\\"\\\'";'
    tokens = tokenize(code)
    string_token = next(t for t in tokens if t.type == 'STRING')
    assert string_token.value == '\n\t\r\\"\''

def test_multiple_string_escapes():
    """
    Prueba el manejo de múltiples strings con escapes:
    - Dos declaraciones de string en la misma línea
    - Diferentes combinaciones de caracteres de escape
    - Verificación de valores procesados correctamente
    """
    code = 'string s1 = "\\n\\t"; string s2 = "\\r\\\\";'
    tokens = tokenize(code)
    string_tokens = [t for t in tokens if t.type == 'STRING']
    assert string_tokens[0].value == '\n\t'
    assert string_tokens[1].value == '\r\\' 