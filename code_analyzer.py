# code_analyzer.py

from codereviewer.code_parse import parse_code
from codereviewer.ai_suggestor import get_ai_suggestion
import autopep8
import ast
import re


class PrintFixer(ast.NodeTransformer):
    """Fix empty print() by inserting the first assigned variable."""
    def __init__(self, first_var):
        self.first_var = first_var

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            if len(node.args) == 0 and self.first_var:
                node.args.append(ast.Name(id=self.first_var, ctx=ast.Load()))
        return self.generic_visit(node)


def fix_syntax_errors(code: str) -> str:
    """
    Simple syntax fixer:
    - Adds missing colons after if, for, while, def, class
    - Ensures basic indentation fixes
    """
    lines = code.splitlines()
    fixed_lines = []

    for line in lines:
        stripped = line.strip()
        # Add colon if missing in common statements
        if re.match(r"(if |for |while |def |class ).*[^:]\s*(#.*)?$", stripped):
            line += ":"
        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def analyze_code(code: str) -> str:
    """Analyze code: syntax check, AI suggestions, auto-format, fix prints & syntax."""
    report_sections = []

    # 1️⃣ Syntax check
    try:
        syntax_result = parse_code(code)
        if not syntax_result.get("success", False):
            report_sections.append("❌ Syntax Error Detected:")
            report_sections.append(syntax_result["error"]["message"])
            # Attempt basic auto-fix
            code = fix_syntax_errors(code)
            report_sections.append("➡️ Attempted automatic syntax fixes applied.")
        else:
            report_sections.append("✅ Syntax Check Passed")
    except Exception as e:
        report_sections.append(f"❌ Syntax Check Failed: {str(e)}")

    # 2️⃣ AI suggestions
    try:
        ai_suggestion = get_ai_suggestion(code)
        report_sections.append("\n💡 AI Suggestions & Analysis:")
        report_sections.append(ai_suggestion)
    except Exception as e:
        report_sections.append(f"\n⚠️ AI Suggestion Error: {str(e)}")

    # 3️⃣ Auto-format code
    try:
        corrected_code = autopep8.fix_code(code)
    except Exception:
        corrected_code = code

    # 4️⃣ Fix empty print() calls
    try:
        parsed_ast = ast.parse(corrected_code)
        first_var = None

        # Find first assigned variable
        for stmt in parsed_ast.body:
            if isinstance(stmt, ast.Assign) and isinstance(stmt.targets[0], ast.Name):
                first_var = stmt.targets[0].id
                break

        if first_var:
            fixer = PrintFixer(first_var)
            fixed_ast = fixer.visit(parsed_ast)
            ast.fix_missing_locations(fixed_ast)
            try:
                corrected_code = ast.unparse(fixed_ast)
            except Exception:
                pass
    except Exception:
        pass  # fallback

    # 5️⃣ Ensure final corrected code is visible
    report_sections.append("\n--- Corrected / Rectified Code ---\n")
    report_sections.append(corrected_code)

    return "\n".join(report_sections)