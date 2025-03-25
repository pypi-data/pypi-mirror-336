import ast
def sparta_9da2fc6f7c(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_3498f88296(script_text):return sparta_9da2fc6f7c(script_text)