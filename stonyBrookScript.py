# Jose Rodriguez 107927299
#
# WolfieScript HW5
# -----------------------------------------------------------------------------
#Helper class
class Node:
	def __init__(self):
		print("init node")
	def evaluate(self):
		return 0
	def execute(self):
		return 0

#Can be real or integers
class NumberNode(Node):
	def __init__(self, v):
		self.value = v
	def evaluate(self):
		return self.value
#For a string type, does not have ''
class StringNode(Node):
	def __init__(self, v):
		self.value = v

	def evaluate(self):
		return self.value

#for a node of type list
class ListNode(Node):
	def __init__(self, v):
		self.value = v
	def evaluate(self):
		return self.value

class NameNode(Node):
	def __init__(self, v):
		self.value = v

	def evaluate(self):
		if self.value in names:
			return names[self.value]
		else:
			raise SemanticError()

#used to print for later
class PrintNode(Node):
	def __init__(self, v):
		self.value = v

	def execute(self):
		self.value = self.value.evaluate()
		print(self.value)

#evaluates operations based on type
class BopNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op


    def evaluate(self):
    	operation = self.op
    	value1 = self.v1.evaluate()
    	value2 = self.v2.evaluate()
    	if (operation == '+'):
        	if((isinstance(value1, str) and isinstance(value2, str)) 
        		or (isinstance(value1, ( int, float )) and isinstance(value2, ( int, float ))) 
        		or (isinstance(value1, list) and isinstance(value2, list))):
        		return value1 + value2
        	else:
        		raise SemanticError()
    	elif (isinstance(value1, ( int, float )) and isinstance(value2, ( int, float ))):
        	if (operation == '-'):
        		return value1 - value2
        	elif(operation=='//'):
        		return value1 // value2
        	elif(operation =='**'):
        		return value1 ** value2
        	elif(operation == '%'):
        		return value1 % value2
        	elif (operation == '*'):
        		return value1 * value2
        	elif (operation == '/'):
        		if(value2 == 0):
        			raise SemanticError()
        		return value1 / value2
    	else:
    		raise SemanticError()

#for conditions primitive
class ConditionalNode(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
    	operation = self.op
    	value1 = self.v1.evaluate()
    	value2 = self.v2.evaluate()
    	if (isinstance(value1, ( int, float )) and isinstance(value2, ( int, float ))):
    		if operation == '<':
    			if value1 < value2:
    				return 1
    			else:
    				return 0
    		elif operation == '<=':
    			if value1 <= value2:
    				return 1
    			else:
    				return 0
    		elif operation == '==':
    			if value1 == value2:
    				return 1
    			else:
    				return 0 
    		elif operation == '<>':
    			if value1 != value2:
    				return 1
    			else:
    				return 0     				   				
    		elif operation == '>':
    			if value1 > value2:
    				return 1
    			else:
    				return 0 
    		elif operation == '>=':
    			if value1 >= value2:
    				return 1
    			else:
    				return 0
    		else:
    			raise SemanticError()
    	else:
    		raise SemanticError()

#This is for boolean more recent
class BooleanNode(Node):
	def __init__(self, op, v1, v2):
		self.v1 = v1
		self.v2 = v2
		self.op = op

	def evaluate(self):
		operation = self.op
		value1 = self.v1.evaluate()
		value2 = self.v2.evaluate()
		if (isinstance(value1, int) and isinstance(value2, int)):
			if operation == 'and':
				if((value1 and value2) == 0):
					return 0
				else:
					return 1
			elif operation == 'or':
				if((value1 or value2) == 0):
					return 0
				else:
					return 1
			else:
				raise SemanticError()
		elif(isinstance(value2, (str,list))):
			if(isinstance(value1,str) or isinstance(value2,list)):
				if operation == 'in':
					if((value1 in value2)):
						return 1
					else:
						return 0
				else:
					raise SemanticError()
			else:
				raise SemanticError()
		else:
			raise SemanticError()

#just for the special case of not
class BooleanNotNode(Node):
	def __init__(self, v):
		self.v = v

	def evaluate(self):
		value = self.v.evaluate()
		if (isinstance(value, int)):
			if((not value) == 0):
				return 0
			else:
				return 1
		else:
			raise SemanticError()
class AssignmentNode(Node):
	def __init__(self, v1, v2):
		self.v1 = v1
		self.v2 = v2

	def execute(self):
		v1 = self.v1
		v2 = self.v2.evaluate()
		#check if what we got is a name node, get its value
		if isinstance(v1,NameNode):
			names[v1.value] = v2
		#check if its an indexnode with a name node, then we assign it
		elif isinstance(v1,IndexNode):
			if isinstance(v1.v1,NameNode):
				index = v1.v2.evaluate()
				variable = v1.v1.value
				item = names[variable]
				#cannot assign to string
				if isinstance(item, str):
					raise SemanticError()
				#check for index out of bounds
				if(len(item) > index):
					names[variable][index] = v2
				else:
					raise SemanticError()
			else:
				raise SemanticError()
		else:
			# print("its something else")
			raise SemanticError()

class WhileNode(Node):
	def __init__(self, v1, v2):
		self.v1 = v1
		self.v2 = v2

	def execute(self):
		import copy
		test = copy.deepcopy(self.v2)
		while(self.v1.evaluate() == 1):
			test.execute()
			test = copy.deepcopy(self.v2)

# #evaluates based on index given
class IndexNode(Node):
	def __init__(self, v1, v2):
		self.v1 = v1
		self.v2 = v2
	def evaluate(self):
		v1 = self.v1.evaluate()
		v2 = self.v2.evaluate()

		if isinstance(v1, (str,list)) and isinstance(v2, int):
			return v1[v2]
		else: 
			raise SemanticError()

class PrintNode(Node):
	def __init__(self, v):
		self.value = v

	def execute(self):
		self.value = self.value.evaluate()
		print(self.value)

class OneStatementNode(Node):
	def __init__(self, v):
		self.v1 = v

	def execute(self):
		self.v1.execute()

class MoreStatementNode(Node):
	def __init__(self, v1, v2):
		self.v1 = v1
		self.v2 = v2

	def execute(self):
		self.v1.execute()
		self.v2.execute()

class IfNode(Node):
	def __init__(self, v1, v2):
		self.v1 = v1
		self.v2 = v2
		self.els = None

	def execute(self):
		if(self.v1.evaluate() == 1):
			self.v2.execute()
		elif(self.els != None):
			self.els.execute()

class ElseNode(Node):
	def __init__(self, v):
		self.v = v
	def execute(self):
		self.v.execute()

class BlockNode(Node):
	def __init__(self, v):
		self.v = v
	def execute(self):
		self.v.execute()

#for those that we dont want to do anything
class EmptyNode(Node):
	def __init__(self):
		'''Empty'''

	def evaluate(self):
		pass

	def execute(self):
		pass

#main class for exceptions and errors
class Error(Exception):
    '''Base class for exceptions in this module.'''
    pass

#raised for different exeptions
class SemanticError(Error):
    '''Exception raised for errors in the input.'''
    pass  

import ply.lex as lex
#LEX RULES
reserved = {
   'in' : 'IN',
   'or' : 'OR',
   'not' : 'NOT',
   'and' : 'AND',
   'print': 'PRINT',
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : "WHILE"
}

tokens = ['INTEGER','REAL','STRING','LPAREN','RPAREN','LBRACKET',
	'RBRACKET','TIMES','DIVIDE','MODULO','EXPONENT','FLOORDIVISION','PLUS',
	'MINUS','LESSTHAN','LESSTHANEQUAL','EQUAL','NOTEQUAL','GREATERTHAN',
	'GREATERTHANEQUAL','COMMA','SEMICOLON','RCURLY','LCURLY','ASSIGMENT','ID']+ list(reserved.values())

# Tokens
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_EXPONENT = r'\*\*'
t_TIMES   = r'\*'
t_FLOORDIVISION = r'//'
t_DIVIDE  = r'/'
t_MODULO = r'%'
t_LESSTHANEQUAL = r'<='
t_LESSTHAN = r'<'
t_EQUAL = r'=='
t_ASSIGMENT = r'='
t_NOTEQUAL = r'<>'
t_GREATERTHANEQUAL = r'>='
t_GREATERTHAN = r'>'
t_COMMA = r','
t_SEMICOLON = r';'

def t_REAL(t):
	r'(\d+\.\d*|\d*\.\d+)'
	t.value = NumberNode(float(t.value))
	return t

def t_INTEGER(t):
	r'\d+'
	t.value = NumberNode(int(t.value))
	return t

def t_STRING(t):
	r'\"(.*?)\"'
	t.value = StringNode(str(t.value[1:-1]))
	return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#checks if the words is reserved
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    if t.type == 'ID':
    	t.value = NameNode(t.value)
    return t

# Error handling rule
def t_error(t):
    t.lexer.skip(1)
    raise SyntaxError

# data = '''
# 3 + 4 * 10
#   + -20 *2 + 9.123 in not \\ ** * <> < >= <= print and "testing123jasdahjsd123h12j3bhj1v23ghabdhh12bh1"
# '''

# Build the lexer
lexer = lex.lex()

#for testing of token creation
# lexer.input(data)
# # # Tokenize
# for tok in lexer:
#     print(tok)

# Parsing rules
#precedence from lowest to highest , those in the same line have equal precedence
precedence = (
	('left','OR'),
	('left','AND'),
	('left','NOT'),
	('left','LESSTHAN','LESSTHANEQUAL','EQUAL','NOTEQUAL','GREATERTHAN','GREATERTHANEQUAL'),
	('left','IN'),
    ('left','PLUS','MINUS'),
    ('left','FLOORDIVISION'),
    ('left','EXPONENT'),
    ('left','MODULO'),
    ('left','TIMES','DIVIDE')
    )

# dictionary of names
names = { }
#######################BLOCK##############################################
def p_block(t):
	'''block : LCURLY statements RCURLY'''
	t[0] = BlockNode(t[2])

def p_block_empty(t):
	'''block : LCURLY RCURLY'''
	t[0] = EmptyNode()

#######################STATEMENTS##############################################
def p_statements_more(t):
	'''statements : statement statements'''
	t[0] = MoreStatementNode(t[1], t[2])

def p_statements_one(t):
	'''statements : statement'''
	t[0] = OneStatementNode(t[1])

def p_statement_expr(t):
    '''statement : printsmt
    				| ifstatement
    				| whilestatement
    				| elsestatement
    				| block'''
    t[0] = OneStatementNode(t[1])

def p_statement_assign(t):
    '''statement : expression ASSIGMENT expression SEMICOLON'''
    t[0] = AssignmentNode(t[1],t[3])

def p_bodystatement_onestatement(t):
	'''bodystatement : statement'''
	t[0] = t[1]

def p_printsmt_smt(t):
    '''printsmt : PRINT LPAREN expression RPAREN SEMICOLON'''
    t[0] = PrintNode(t[3])

def p_whilestatement_while(t):
	'''whilestatement : WHILE LPAREN expression RPAREN bodystatement'''

	t[0] = WhileNode(t[3], t[5])

def p_ifstatement_if(t):
	'''ifstatement : IF LPAREN expression RPAREN bodystatement'''
	t[0] = IfNode(t[3],t[5])


def p_elsestatement_ifelse(t):
	'''elsestatement : ifstatement ELSE bodystatement'''
	t[1].els = ElseNode(t[3])
	t[0] = t[1]

#######################OPERATORS##############################################
def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression FLOORDIVISION expression
                  | expression EXPONENT expression
                  | expression MODULO expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    t[0] = BopNode(t[2], t[1], t[3])

def p_expression_conditional(t):
    '''expression : expression LESSTHAN expression
                  | expression LESSTHANEQUAL expression
                  | expression EQUAL expression
                  | expression NOTEQUAL expression
                  | expression GREATERTHAN expression
                  | expression GREATERTHANEQUAL expression'''
    t[0] = ConditionalNode(t[2], t[1], t[3])

def p_expression_booleans(t):
	'''expression : expression OR expression
				| expression AND expression
				| expression IN expression'''
	t[0] = BooleanNode(t[2],t[1], t[3])

def p_expression_not(t):
	'''expression : NOT expression'''
	t[0] = BooleanNotNode(t[2])

def p_expression_plusnum(t):
	'''expression : PLUS expression'''
	t[0] = t[2]

#######################INDEX##############################################
def p_index_list(t):
	'''index : list bracket'''
	t[0] = IndexNode(t[1],t[2])

def p_index_string(t):
	'''index : STRING bracket'''
	t[0] = IndexNode(t[1],t[2])

def p_index_id(t):
	'''index : ID bracket'''
	t[0] = IndexNode(t[1],t[2])

def p_index_expression(t):
	'''index : expression bracket'''
	t[0] = IndexNode(t[1],t[2])

def p_index_indeces(t):
	'''index : indices'''
	t[0] = t[1]

def p_indices_indices(t):
	'''indices : index bracket'''
	t[0] = IndexNode(t[1], t[2])

def p_bracket(t):
	'''bracket : LBRACKET expression RBRACKET'''
	t[0] = t[2]	

#######################LIST##############################################
def p_list_empty(t):
	'''list : LBRACKET RBRACKET'''
	t[0] = ListNode([])

def p_list_expr(t):
	'''list : bracket'''
	t[0] = ListNode([t[2]])

def p_list_bracket(t):
	'''list : LBRACKET commalist RBRACKET'''
	t[0] = ListNode(t[2])

def p_commalist_list(t):
	'''commalist : expression'''
	t[0] = [t[1].evaluate()]

def p_commalist_recursive(t):
	'''commalist : expression COMMA commalist'''
	t[0] =  [t[1].evaluate()] + t[3]


#######################TERMINALS##############################################
def p_expression_factor(t):
	'''expression : factor'''
	t[0] = t[1]

def p_factor_paren(t):
	'''factor : LPAREN expression RPAREN'''
	t[0] = t[2]

def p_factor_type(t):
    '''factor : INTEGER
                  | REAL
                  | STRING
                  | ID 
                  | list
                  | index'''
    t[0] = t[1]


def p_error(t):
	raise SyntaxError()

import ply.yacc as yacc
import sys
yacc.yacc()
r = open(sys.argv[1], "r")
code = ""

for line in r:
    code += line
try:
	lex.input(code)
	ast = yacc.parse(code)
	ast.execute()
except IOError:
	print("Error opening the file")
except SyntaxError:
	print("SYNTAX ERROR")
except SemanticError:
	print("SEMANTIC ERROR")


