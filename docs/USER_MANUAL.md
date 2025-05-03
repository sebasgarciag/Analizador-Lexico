# Manual de Usuario - Analizador Léxico

Este manual proporciona una guía detallada sobre cómo utilizar el analizador léxico.

## Índice

1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Uso Básico](#uso-básico)
4. [Características Detalladas](#características-detalladas)
5. [Ejemplos Prácticos](#ejemplos-prácticos)
6. [Solución de Problemas](#solución-de-problemas)

## Introducción

El analizador léxico es una herramienta que convierte código fuente en una secuencia de tokens. Es útil para:
- Análisis de código
- Validación de sintaxis
- Primera fase de compilación
- Procesamiento de lenguajes

## Instalación

1. **Requisitos Previos**:
   - Python 3.6 o superior
   - pip (gestor de paquetes de Python)

2. **Pasos de Instalación**:
   ```bash
   # Clonar el repositorio
   git clone https://github.com/sebasgarciag/Analizador-Lexico.git
   cd Analizador-Lexico

   # Instalar dependencias
   pip install -r requirements.txt
   ```

## Uso Básico

### Como Script Independiente

1. Crear un archivo de texto con el código a analizar
2. Ejecutar el script:
   ```bash
   python src/lexer.py
   ```

### Como Módulo en tu Código

```python
from src.lexer import tokenize

# Analizar código directamente
codigo = '''
int main() {
    return 0;
}
'''
tokens = tokenize(codigo)

# Analizar desde un archivo
with open('mi_archivo.c', 'r') as f:
    codigo = f.read()
tokens = tokenize(codigo)
```

## Características Detalladas

### 1. Tipos de Tokens Soportados

- **Palabras Reservadas**:
  ```c
  if, else, while, return, int, float, void
  ```

- **Operadores**:
  ```c
  +, -, *, /, ==, !=, <=, >=, <, >
  ```

- **Delimitadores**:
  ```c
  (, ), {, }, ;
  ```

### 2. Manejo de Comentarios

- **Comentarios de línea**:
  ```c
  // Este es un comentario de línea
  ```

- **Comentarios multilínea**:
  ```c
  /* Este es un comentario
     que abarca múltiples
     líneas */
  ```

- **Comentarios anidados**:
  ```c
  /* Comentario externo
     /* Comentario interno */
     Continúa el comentario externo */
  ```
  Los comentarios anidados son útiles para comentar bloques de código que ya contienen comentarios.

### 3. Números y Literales

- **Enteros**:
  ```c
  42, 100, 0
  ```

- **Decimales**:
  ```c
  3.14, 0.5, 2.0
  ```

- **Strings**:
  ```c
  "Hello, World!", "Texto con \"comillas\"", ""
  ```

### 4. Strings y Caracteres de Escape

Los strings pueden contener caracteres especiales usando secuencias de escape:

- **Caracteres de Escape Soportados**:
  | Secuencia | Significado        | Ejemplo                    |
  |-----------|-------------------|----------------------------|
  | `\n`      | Nueva línea       | `"Línea 1\nLínea 2"`      |
  | `\t`      | Tabulación        | `"Columna1\tColumna2"`    |
  | `\r`      | Retorno de carro  | `"Texto\rSobreescrito"`   |
  | `\\`      | Barra invertida   | `"Ruta\\archivo"`         |
  | `\"`      | Comilla doble     | `"Texto \"citado\""`      |
  | `\'`      | Comilla simple    | `"It\'s working"`         |

- **Ejemplos de Uso**:
  ```c
  string mensaje = "Línea 1\nLínea 2";  // String con salto de línea
  string ruta = "C:\\Documentos\\archivo.txt";  // Ruta con barras invertidas
  string cita = "El dijo: \"¡Hola!\"";  // String con comillas
  ```

## Ejemplos Prácticos

### 1. Análisis de Función Simple

```c
int suma(int a, int b) {
    return a + b;
}
```

Tokens generados:
```python
Token(INT, 'int', line=1, column=1)
Token(IDENTIFIER, 'suma', line=1, column=5)
Token(LPAREN, '(', line=1, column=9)
Token(INT, 'int', line=1, column=10)
# ... etc
```

### 2. Manejo de Errores

```python
try:
    tokens = tokenize("int @var = 10;")
except ValueError as e:
    print(f"Error: {e}")
    # Imprime: Error: Unexpected character '@' at position 4 (line 1, column 5)
```

### 3. Manejo de Comentarios Anidados

```c
/* Función principal
   /* Comentario interno sobre
      los parámetros */
   que hace algo importante */
void main() {
    // Código aquí
}
```

### 4. Strings con Caracteres de Escape

```c
void imprimir_tabla() {
    string encabezado = "Nombre\tEdad\tCiudad\n";
    string datos = "Juan\t25\tMadrid\n";
    string ruta = "C:\\Datos\\tabla.txt";
}
```

## Solución de Problemas

### Problemas Comunes

1. **Error: Caracter no reconocido**
   - Causa: El código contiene caracteres que no son parte del lenguaje
   - Solución: Revisar y eliminar caracteres especiales no permitidos

2. **Error: String sin cerrar**
   - Causa: Falta la comilla de cierre en un string
   - Solución: Asegurarse de que todos los strings estén correctamente cerrados

3. **Error: Comentario multilínea sin cerrar**
   - Causa: Falta el cierre `*/` en un comentario
   - Solución: Asegurarse de cerrar todos los comentarios multilínea

### Mejores Prácticas

1. **Organización del Código**:
   - Usar indentación consistente
   - Separar secciones con líneas en blanco
   - Usar comentarios descriptivos

2. **Manejo de Archivos**:
   - Usar la codificación UTF-8
   - Verificar permisos de lectura
   - Cerrar archivos después de usarlos

3. **Depuración**:
   - Revisar la salida token por token
   - Verificar números de línea y columna
   - Usar try-except para capturar errores 