import os
from src.lexer import tokenize

def test_example(file_path):
    print(f"\nProbando archivo: {file_path}")
    print("=" * 50)
    
    try:
        # Leer y mostrar contenido del archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        print("Contenido del archivo:")
        print(code.rstrip())
        
        # Procesar tokens
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
        
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

def main():
    # Probar cada archivo de ejemplo
    examples_dir = os.path.join(os.path.dirname(__file__), "examples")
    for i in range(1, 5):
        file_path = os.path.join(examples_dir, f"example{i}.txt")
        test_example(file_path)

if __name__ == "__main__":
    main() 