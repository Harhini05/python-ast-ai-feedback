import ast

class AIReview(ast.NodeVisitor): # 1. Inherit NodeVisitor
    def __init__(self):
        self.defined = set()
        self.used = set()

    def visit_Import(self, node): 
        for alias in node.names:
            self.defined.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            name_to_track = alias.asname or alias.name
            self.defined.add(name_to_track)
            print(f"DEBUG: Found import from {node.module}: {name_to_track}") 
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store): 
            self.defined.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)
        self.generic_visit(node)

    def reportOfUnused(self):
        unused = self.defined - self.used
        print('--- AI Review Report ---')
        if not unused:
            print("Everything is used! Good job bro!")
        for item in unused:
            print(f'Unused Item : {item}')

code = '''
import os 
import sys
from datetime import datetime, timedelta
score = 100
print(score)
'''

tree = ast.parse(code)
review = AIReview()
review.visit(tree) 
review.reportOfUnused()