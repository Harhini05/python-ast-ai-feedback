import ast


class CodeAnalyzer(ast.NodeVisitor):

    def visit_Assign(self, node):
        print("Found an assignment statement")
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        print(f"Found a function: {node.name}")
        self.generic_visit(node)

    def visit_For(self, node):
        print("Found a for loop")
        self.generic_visit(node)

    def visit_If(self, node):
        print("Found an if statement")
        self.generic_visit(node)


def analyze_code(user_code):
    try:
        # Parse the code into AST
        tree = ast.parse(user_code)

        print("\n AST Structure:")
        print(ast.dump(tree, indent=4))

        print("\n Code Analysis:")
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)

        print("\n Formatted Code:")
        formatted_code = ast.unparse(tree)
        print(formatted_code)

    except Exception as e:
        print(" Syntax Error:", e)


if __name__ == "__main__":
    print("Enter Python code (type END to finish):")
    
    lines = []
    while True:
        line = input()
        if line == "END":
            break
        lines.append(line)

    code = "\n".join(lines)

    analyze_code(code)
