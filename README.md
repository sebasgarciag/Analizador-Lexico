# Analizador Léxico (Lexer)

Este proyecto implementa un analizador léxico (lexer) robusto para un lenguaje de programación tipo C. El analizador es capaz de procesar código fuente y convertirlo en una secuencia de tokens que representan las unidades léxicas fundamentales del lenguaje.

## Características

- **Análisis de Tokens**:
  - Palabras reservadas (`if`, `else`, `while`, `return`, `int`, `float`, `void`)
  - Identificadores (variables y nombres de funciones)
  - Números (enteros y decimales)
  - Strings
  - Operadores aritméticos y de comparación
  - Símbolos de puntuación y delimitadores

- **Manejo de Comentarios**:
  - Comentarios de línea simple (`//`)
  - Comentarios multilínea (`/* */`)
  - Detección de comentarios anidados (reportados como error)

- **Seguimiento de Posición**:
  - Número de línea preciso
  - Número de columna precisa
  - Tokens de error con información detallada

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

## Estructura del Proyecto

```
analizador_lexico/
├── src/
│   └── lexer.py          # Implementación principal del analizador
├── tests/
│   └── test_lexer.py     # Suite de pruebas unitarias
├── examples/
│   ├── example1.txt      # Ejemplo básico de código válido
│   ├── example2.txt      # Ejemplo con error de carácter inválido
│   ├── example3.txt      # Ejemplo con error de comentario anidado
│   └── example4.txt      # Ejemplo con múltiples errores
├── test_examples.py      # Script para probar todos los archivos de ejemplo
├── requirements.txt      # Dependencias del proyecto
└── README.md            # Este archivo
```

## Uso

### 1. Como Módulo en tu Código

```python
from src.lexer import tokenize

# Ejemplo de uso básico
code = '''
int main() {
    float x = 3.14;
    return 0;
}
'''

tokens = tokenize(code)
for token in tokens:
    if token.type == 'ERROR':
        print(f"Error en línea {token.line}, columna {token.column}: {token.value}")
    else:
        print(f"Token: {token.type}, Valor: {token.value}")
```

### 2. Ejecutar el Analizador Directamente

```bash
python src/lexer.py
```
Este comando analizará el archivo `examples/example1.txt` y mostrará los tokens encontrados.

### 3. Ejecutar los Ejemplos

```bash
python test_examples.py
```
Este script ejecutará el analizador sobre los cuatro archivos de ejemplo y mostrará los resultados detallados.

### 4. Ejecutar las Pruebas Unitarias

```bash
python -m pytest tests/test_lexer.py -v
```
Este comando ejecutará todas las pruebas unitarias con información detallada.

## Tipos de Tokens

El analizador reconoce los siguientes tipos de tokens:

| Tipo        | Descripción                    | Ejemplo                |
|-------------|--------------------------------|------------------------|
| IDENTIFIER  | Nombres de variables/funciones  | `variable`, `func`    |
| NUMBER      | Números enteros o decimales    | `42`, `3.14`          |
| STRING      | Cadenas de texto               | `"Hello World"`       |
| OPERATOR    | Operadores                     | `+`, `-`, `*`, `/`    |
| KEYWORD     | Palabras reservadas            | `if`, `while`, `int`  |
| DELIMITER   | Símbolos de puntuación         | `{`, `}`, `;`        |
| ERROR       | Tokens con errores             | Errores léxicos       |

## Manejo de Errores

El analizador detecta y reporta los siguientes tipos de errores como tokens de tipo 'ERROR':

1. **Identificadores Inválidos**:
   - Identificadores que comienzan con números
   - Ejemplo: `123abc`
   - Error: "Invalid identifier (starts with number): 123abc"

2. **Números Inválidos**:
   - Números con múltiples puntos decimales
   - Ejemplo: `1.2.3`
   - Error: "Invalid number format: 1.2.3"

3. **Strings Sin Cerrar**:
   - Strings que no tienen la comilla de cierre
   - Ejemplo: `"texto incompleto`
   - Error: "Unterminated string literal"

4. **Comentarios Anidados**:
   - Comentarios multilínea dentro de otros comentarios
   - Ejemplo: `/* externo /* interno */ fin */`
   - Error: "Nested comment detected at line X, column Y"

5. **Caracteres Inválidos**:
   - Caracteres que no son parte del lenguaje
   - Ejemplo: `$`, `@`, `#`
   - Error: "Unexpected character: $"

## Ejemplos de Código

### 1. Código Válido (example1.txt)
```c
int main() {
    int x = 42;
    float y = x + 3.14;
    // Esto es un comentario
    if (x > 0) {
        y = y * 2;
    }
}
```

### 2. Código con Error de Carácter (example2.txt)
```c
int a = 10;
$var = 20; // Token desconocido: $
/* Comentario
   Comentario */
```

### 3. Código con Comentario Anidado (example3.txt)
```c
/* Comentario externo /* comentario interno */ fin */
string vacia = "";
```

### 4. Código con Múltiples Errores (example4.txt)
```c
int 123abc = 5;        // Error: identificador inválido
float x = 1.2.3;       // Error: número inválido
string fail = "sin cerrar; // Error: string sin cerrar
```

## Pruebas Unitarias

El proyecto incluye pruebas unitarias que verifican:

1. **Análisis Básico**:
   - Tokenización de expresiones simples
   - Identificación de palabras reservadas
   - Manejo de identificadores y números

2. **Manejo de Comentarios**:
   - Comentarios de línea simple
   - Comentarios multilínea
   - Detección de comentarios anidados

3. **Procesamiento de Strings**:
   - Strings básicos
   - Strings vacíos
   - Detección de strings sin cerrar

4. **Manejo de Errores**:
   - Identificadores inválidos
   - Números malformados
   - Caracteres no reconocidos
   - Comentarios anidados

## Formato de Salida

El analizador proporciona una salida detallada que incluye:

1. **Tokens Válidos**:
   ```
   TYPE         | Línea  1, Col  1 | 'int'
   IDENTIFIER   | Línea  1, Col  5 | 'main'
   ```

2. **Errores**:
   ```
   Error en línea 1, columna 5: Invalid identifier (starts with number): 123abc
   ``` 