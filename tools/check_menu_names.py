import ast, builtins, sys, pathlib, importlib
sys.path.insert(0, '.')
import menus  # noqa

bad = 0
menu_files = [f for f in pathlib.Path('menus').rglob('*.py') if f.name not in ('__init__.py', '_linking.py')]

for f in sorted(menu_files):
    rel = f.relative_to(pathlib.Path('.')).with_suffix('')
    mod_name = '.'.join(rel.parts)
    try:
        m = importlib.import_module(mod_name)
    except Exception as e:
        print(f"Import error in {mod_name}: {e}")
        bad += 1
        continue

    tree = ast.parse(f.read_text(encoding='utf-8'))
    defined = set(vars(m)) | set(dir(builtins))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined.add(node.name)
            if hasattr(node, 'args'):
                a = node.args
                for x in a.args + a.kwonlyargs + a.posonlyargs:
                    defined.add(x.arg)
                if a.vararg: defined.add(a.vararg.arg)
                if a.kwarg: defined.add(a.kwarg.arg)
        elif isinstance(node, ast.Lambda):
            a = node.args
            for x in a.args + a.kwonlyargs + a.posonlyargs:
                defined.add(x.arg)
            if a.vararg: defined.add(a.vararg.arg)
            if a.kwarg: defined.add(a.kwarg.arg)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            defined.add(node.id)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            defined.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for al in node.names:
                defined.add((al.asname or al.name).split('.')[0])
        elif isinstance(node, ast.comprehension):
            for n in ast.walk(node.target):
                if isinstance(n, ast.Name): defined.add(n.id)

    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id not in defined:
            print(f, node.lineno, node.id)
            bad += 1

print('undefined across all menus:', bad)
sys.exit(1 if bad else 0)
