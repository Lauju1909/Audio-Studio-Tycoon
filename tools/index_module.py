import ast, sys
src = open('game_data.py', encoding='utf-8-sig').read()
t = ast.parse(src)
out = []
for n in t.body:
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        name = n.name
    elif isinstance(n, ast.Assign):
        name = ",".join(getattr(x, 'id', '?') for x in n.targets)
    elif isinstance(n, ast.AnnAssign):
        name = n.target.id
    else:
        name = type(n).__name__
    out.append(f"{n.lineno}-{n.end_lineno}:{name}")
print("\n".join(out))
