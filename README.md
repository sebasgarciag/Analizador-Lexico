# Analizador Léxico (Lexer)

Este proyecto implementa un analizador léxico (lexer) robusto para un lenguaje de programación tipo C. El analizador es capaz de procesar código fuente y convertirlo en una secuencia de tokens que representan las unidades léxicas fundamentales del lenguaje.

## Características

- **Análisis de Tokens**:
  - Palabras reservadas (`if`, `else`, `while`, `return`, `int`, `float`, `void`)
  - Identificadores (variables y nombres de funciones)
  - Números (enteros y decimales)
  - Strings con soporte para caracteres de escape
  - Operadores aritméticos y de comparación
  - Símbolos de puntuación y delimitadores

- **Manejo de Comentarios**:
  - Comentarios de línea simple (`//`)
  - Comentarios multilínea (`/* */`)
  - Soporte para comentarios anidados

- **Seguimiento de Posición**:
  - Número de línea preciso
  - Número de columna preciso
  - Mensajes de error detallados con ubicación exacta

## Requisitos

- Python 3.6 o superior
- pytest (para ejecutar las pruebas)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/sebasgarciag/Analizador-Lexico.git
   cd Analizador-Lexico
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Como Módulo

```python
from src.lexer import tokenize

# Ejemplo de uso básico
code = '''
int main() {
    float x = 3.14;
    return 0;
}
'''

try:
    tokens = tokenize(code)
    for token in tokens:
        print(token)
except ValueError as e:
    print(f"Error léxico: {e}")
```

### Como Script

```bash
python src/lexer.py
```

Por defecto, el script analizará el archivo `examples/example1.txt`.

## Estructura del Proyecto

```
analizador_lexico/
├── src/
│   └── lexer.py          # Implementación principal del analizador
├── tests/
│   └── test_lexer.py     # Suite de pruebas
├── examples/
│   ├── example1.txt      # Ejemplo básico
│   ├── example2.txt      # Ejemplo con comentarios
│   ├── example3.txt      # Ejemplo con strings
│   └── example4.txt      # Ejemplo con operadores
├── docs/
│   └── USER_MANUAL.md    # Manual de usuario detallado
├── requirements.txt      # Dependencias del proyecto
└── README.md            # Este archivo
```

## Tipos de Tokens

El analizador reconoce los siguientes tipos de tokens:

| Tipo        | Descripción                    | Ejemplo                |
|-------------|--------------------------------|------------------------|
| IDENTIFIER  | Nombres de variables/funciones  | `variable`, `func`    |
| NUMBER      | Números enteros o decimales    | `42`, `3.14`          |
| STRING      | Cadenas de texto con escape    | `"Hello\nWorld"`      |
| OPERATOR    | Operadores                     | `+`, `-`, `*`, `/`    |
| KEYWORD     | Palabras reservadas            | `if`, `while`, `int`  |
| DELIMITER   | Símbolos de puntuación         | `{`, `}`, `;`        |

### Caracteres de Escape en Strings

Los strings soportan los siguientes caracteres de escape:
- `\n`: Nueva línea
- `\t`: Tabulación
- `\r`: Retorno de carro
- `\\`: Barra invertida
- `\"`: Comilla doble
- `\'`: Comilla simple

## Ejemplos

### Código Simple
```c
int main() {
    int x = 42;
    return x;
}
```

### Con Comentarios
```c
// Este es un comentario de línea
/* Este es un
   comentario multilínea */
int x = 10;
```

### Con Strings y Operadores
```c
string msg = "Hello!";
float y = 3.14 * 2;
```

## Pruebas

El proyecto incluye una suite completa de pruebas unitarias que verifican todas las funcionalidades del analizador:

### Tipos de Pruebas

1. **Análisis Básico**:
   - Tokenización de expresiones simples
   - Identificación de palabras reservadas
   - Manejo de identificadores y números

2. **Manejo de Comentarios**:
   - Comentarios de línea simple
   - Comentarios multilínea
   - Comentarios anidados
   - Preservación de números de línea

3. **Procesamiento de Strings**:
   - Strings básicos
   - Caracteres de escape
   - Strings vacíos
   - Detección de strings sin cerrar

4. **Manejo de Errores**:
   - Caracteres no reconocidos
   - Tokens malformados
   - Comentarios sin cerrar
   - Posicionamiento preciso de errores

### Ejecutar las Pruebas

```bash
# Ejecutar todas las pruebas
python -m pytest tests/test_lexer.py -v

# Ejecutar una prueba específica
python -m pytest tests/test_lexer.py::test_nested_comments -v
```

## Manejo de Errores

El analizador proporciona mensajes de error detallados cuando encuentra caracteres no reconocidos:

```python
try:
    tokens = tokenize("int $x = 10;")
except ValueError as e:
    print(e)  # Imprime: "Unexpected character '$' at position 4 (line 1, column 5)"
```

## Funcionamiento Interno

El analizador léxico funciona siguiendo estos pasos:

1. **Inicialización**: 
   - Se define una lista de patrones de tokens usando expresiones regulares
   - Cada patrón corresponde a un tipo específico de token (números, identificadores, etc.)

2. **Análisis**:
   - El texto se procesa secuencialmente, caracter por caracter
   - Para cada posición, se intentan hacer coincidir los patrones definidos
   - Cuando se encuentra una coincidencia, se crea un token con:
     * Tipo de token
     * Valor literal
     * Número de línea
     * Número de columna

3. **Manejo Especial**:
   - Los espacios en blanco y comentarios se procesan pero no generan tokens
   - Las palabras reservadas se identifican después de coincidir como identificadores
   - Se mantiene un seguimiento preciso de la posición en el código

4. **Gestión de Errores**:
   - Si se encuentra un caracter no reconocido, se lanza una excepción
   - La excepción incluye la posición exacta del error 