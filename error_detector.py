import ast

class AIReview(ast.NodeVisitor):
    def __init__(self):
        self.defined = set()
        self.used = set()

    def visit_Import(self, node):
        for alias in node.names:
            self.defined.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.defined.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)
        self.generic_visit(node)

    def reportOfUnused(self):
        unused = self.defined - self.used
        if not unused:
            return "No unused variables found ✅"
        return "Unused Variables: " + ", ".join(unused)


# ✅ THIS WAS MISSING
def detect_errors(code):
    try:
        tree = ast.parse(code)
        analyzer = AIReview()
        analyzer.visit(tree)
        return analyzer.reportOfUnused()
    except Exception as e:
        return f"Error: {str(e)}"