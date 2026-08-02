import ast

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"SyntaxError in {filepath}: {e}")
        return

    for node in ast.walk(tree):
        # Missing return value:
        if isinstance(node, ast.FunctionDef):
            has_return = any(isinstance(n, ast.Return) for n in ast.walk(node))
            if has_return:
                for n in ast.walk(node):
                    if isinstance(n, ast.Return) and n.value is None:
                        print(f"{filepath}:{n.lineno}: Empty return in function {node.name}")

        # List index out of bounds: pop()
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'pop':
            print(f"{filepath}:{node.lineno}: Usage of pop()")
            
        # [0] without length check is hard to find with ast, let's look for Subscript with Constant 0 or -1
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, int):
            if node.slice.value in (0, -1):
                pass # print(f"{filepath}:{node.lineno}: Subscript [{node.slice.value}]")

for f in ['logic.py', 'models.py', 'audio.py', 'main.py']:
    check_file(f)
