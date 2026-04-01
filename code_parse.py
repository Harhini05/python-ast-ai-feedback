# code_parse.py
import ast

def parse_code(code: str):
    try:
        tree = ast.parse(code)
        return {"success": True, "tree": tree}
    except SyntaxError as e:
        return {"success": False, "error": {"message": f"Syntax Error: {str(e)}"}}






































































        