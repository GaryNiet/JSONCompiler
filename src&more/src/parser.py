import ply.yacc as yacc

from lex import tokens
import AST

vars = {}

def p_map(p):
    '''map : BEGIN '(' expression ',' expression ')' ';' programme END '''
    p[0] = AST.MapNode([p[3], p[5]] + p[8].children)

def p_name(p):
    '''name : NAME'''
    p[0] = AST.NameNode(p[1])

def p_programme_statement(p):
    ''' programme : statement '''
    p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
    ''' programme : statement ';' programme'''
    p[0] = AST.ProgramNode([p[1]]+p[3].children)


def p_statement(p):
    ''' statement : assignation
        | structure
        | geoelement'''
    p[0] = p[1]

def p_geoelement_ground(p):
    '''geoelement : GROUND '(' expression ',' expression ',' expression ')' '''
    p[0] = AST.GroundNode([p[3], p[5], p[7]])

def p_geoelement_mountain(p):
    '''geoelement : MOUNTAIN '(' expression ',' expression ',' expression ',' expression ')' '''
    p[0] = AST.MountainNode([p[3], p[5], p[7], p[9]])

def p_geoelement_water(p):
    '''geoelement : WATER '(' expression ')' '''
    p[0] = AST.WaterNode([p[3]])

def p_geoelement_river(p):
    '''geoelement : RIVER '(' expression ',' expression ',' expression ',' expression ')' '''
    p[0] = AST.RiverNode([p[3], p[5], p[7], p[9]])

def p_structure_ifelse(p):
    ''' structure : IF '(' expression ')' '{' programme '}' ELSE '{' programme '}' '''
    p[0] = AST.IfElseNode([p[3],p[6],p[10]])

def p_structure_if(p):
    ''' structure : IF '(' expression ')' '{' programme '}' '''
    p[0] = AST.IfNode([p[3], p[6]])

def p_structure_while(p):
    ''' structure : WHILE '(' expression ')' '{' programme '}' '''
    p[0] = AST.WhileNode([p[3],p[6]])

def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])
    	
def p_expression_num_or_var(p):
    '''expression : NUMBER
        | IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])
    	
def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]
    	
def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])
    	
def p_assign(p):
    ''' assignation : IDENTIFIER '=' expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Sytax error: unexpected end of file!")



precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),  
)

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys 
    	
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print (result)
            
        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name) 
        print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")
