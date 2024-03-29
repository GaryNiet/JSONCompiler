import ply.lex as lex

reserved_words = (
	'while',
    'if',
	'else',
)

tokens = (
	'GROUND',
	'WATER',
	'MOUNTAIN',
    'RIVER',
    'ADD_OP',
    'MUL_OP',
    'NUMBER',
    'IDENTIFIER',
    'BEGIN',
    'END',
    'NAME',
) + tuple(map(lambda s:s.upper(),reserved_words))

literals = '();={},'

def t_GROUND(t):
    r'GROUND'
    return t

def t_MOUNTAIN(t):
    r'MOUNTAIN'
    return t

def t_WATER(t):
    r'WATER'
    return t

def t_RIVER(t):
    r'RIVER'
    return t

def t_BEGIN(t):
    r'BEGIN'
    return t

def t_END(t):
    r'END'
    return t

def t_ADD_OP(t):
	r'[+-]'
	return t
	
def t_MUL_OP(t):
	r'[*/]'
	return t

def t_NUMBER(t):
	r'\d+(\.\d+)?'
	try:
		t.value = float(t.value)    
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = 0
	return t

def t_IDENTIFIER(t):
	r'[a-z][A-Za-z_]\w*'
	if t.value in reserved_words:
		t.type = t.value.upper()
	return t

def t_NAME(t):
    r'[A-Z][A-Za-z_]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t
	
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
