import AST
import math
from AST import addToClass
from functools import reduce


operations = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
}

vars ={}
map = []
ground = []
mountain = []
river = []
water = []
    
@addToClass(AST.Node)
def compile(self):
    result = 0.0
    for c in self.children:
        try:
            result += float(c.compile())
        except:
            pass
    try:
        result = float(self.opcode())
    except:
        pass

    return result

@addToClass(AST.ProgramNode)
def opcode(self):
    return ""

@addToClass(AST.TokenNode)
def opcode(self):
    if isinstance(self.tok, str):
        return vars[self.tok]
    return "%s" % self.tok

@addToClass(AST.NameNode)
def opcode(self):
    return 0.0

@addToClass(AST.OpNode)
def opcode(self):
    result = ""
    if self.nbargs == 1:
        result += str(reduce(operations[self.op],[0, float(self.children[0].compile())]))
    else:
        result += str(reduce(operations[self.op],[float(self.children[0].compile()), float(self.children[1].compile())]))

    return result

@addToClass(AST.AssignNode)
def compile(self):
    vars[self.children[0].tok] = self.children[1].compile()

@addToClass(AST.WhileNode)
def compile(self):
    while self.children[0].compile():
        self.children[1].compile()

@addToClass(AST.IfElseNode)
def compile(self):
    if self.children[0].compile() != 0:
        self.children[1].compile()
    else:
        self.children[2].compile()

@addToClass(AST.IfNode)
def compile(self):
    if self.children[0].compile() != 0:
        self.children[1].compile()

@addToClass(AST.MapNode)
def compile(self):
    for r in self.children:
        r.compile()
    return createMap(self.children[0].compile(), self.children[1].compile())

@addToClass(AST.GroundNode)
def compile(self):
    ground.append([self.children[0].compile(), self.children[1].compile(), self.children[2].compile()])

@addToClass(AST.WaterNode)
def compile(self):
    water.append(self.children[0].compile())

@addToClass(AST.MountainNode)
def compile(self):
    mountain.append([self.children[0].compile(), self.children[1].compile(), self.children[2].compile(), self.children[3].compile()])

@addToClass(AST.RiverNode)
def compile(self):
    river.append([self.children[0].compile(), self.children[1].compile(), self.children[2].compile(), self.children[3].compile()])

def createMap(x,y):
    normalizer = (int(float(x)) if int(float(x)) > int(float(y)) else int(float(y))) - 1
    map = [[-1000 for k in range(int(float(x)))] for k in range(int(float(y)))]
    for g in ground:
        for i in range(int(float(x))):
            for j in range(int(float(y))):
                temp = float(g[0])+ i*float(g[1])+j*float(g[2])
                if temp > map[i][j]:
                    map[i][j] = temp

    for w in water:
        for i in range(int(float(x))):
            for j in range(int(float(y))):
                temp = float(w)
                if temp > map[i][j]:
                    map[i][j] = temp

    for m in mountain:
        for i in range(int(float(x))):
            for j in range(int(float(y))):
                temp = float(m[2]) + float(m[3]) * math.sqrt((i-float(m[0]))*(i-float(m[0])) + (j-float(m[1]))*(j-float(m[1])))
                if temp > map[i][j]:
                    map[i][j] = temp

    for r in river:
        i = float(r[0])
        j = float(r[1])
        min = 10000;
        continueFlag = True
        onBorder = False
        dejaParcouru = False
        parcouru = []
        parcouru.append([i,j])
            
        nexti = i
        nextj = j
        
        while min > float(water[0]) and continueFlag and not onBorder:

            parcouru.append([i,j])
            i = nexti
            j = nextj
            continueFlag = False
            for k in range(3):
                for l in range(3):
                    if (i+k-1)==len(map) or (i+k-1)<0 or (j+l-1)==len(map[int(i)]) or (j+l-1)<0:
                        onBorder = True
                    else:
                        temp = float(map[int(i + k-1)][int(j + l -1)])
                        if temp < min:
                            for p in parcouru:
                                if (i + k-1) == p[0] and (j + l-1) == p[1]:
                                    dejaParcouru = True
                            if not dejaParcouru:
                                min = temp
                                nexti = i + k -1
                                nextj = j + l-1
                                continueFlag = True
                            dejaParcouru = False

        for p in parcouru:
            for k in range(int(float(r[2]))):
                for l in range(int(float(r[2]))):
                    map[int(p[0]+k-(int(float(r[2])))/2)][int(p[1]+l-(int(float(r[2])))/2)] = map[int(p[0]+k-(int(float(r[2])))/2)][int(p[1]+l-(int(float(r[2])))/2)] - float(r[3])

    result = "{\"vertices\" : ["
    i = 0
    while i < len(map):
        j=0
        while j < len(map[i]):
            result += str(i/normalizer-0.5) + ", "
            result += str(j/normalizer-0.5) + ", "
            if i==len(map)-1 and j==len(map[i])-1:
                result += str(map[i][j]/normalizer)
            else:
                result += str(map[i][j]/normalizer) + ", "
            j+=1
        i+=1

    result += "], \n \"normals\" : ["
    i = 0
    while i < len(map):
        j=0
        while j < len(map[i]):
            vecteurs= []
            if j == 0:
                vecteurs.append( [0, -1, map[i][j]-map[i][j]])
            else:
                vecteurs.append([0, -1, map[i][j-1]-map[i][j]])
            
            if i == len(map)-1:
                vecteurs.append([1, 0, map[i][j]-map[i][j]])
            else:
                vecteurs.append([1, 0, map[i+1][j]-map[i][j]])
            
            if i == len(map)-1 or j == len(map[i])-1:
                vecteurs.append([1, 1, map[i][j]-map[i][j]])
            else:
                vecteurs.append([1, 1, map[i+1][j+1]-map[i][j]])
            
            if j == len(map[i])-1:
                vecteurs.append([0, 1, map[i][j]-map[i][j]])
            else:
                vecteurs.append([0, 1, map[i][j+1]-map[i][j]])
            
            if i==0:
                vecteurs.append([-1, 0, map[i][j]-map[i][j]])
            else:
                vecteurs.append([-1, 0, map[i-1][j]-map[i][j]])
            
            if i==0 or j==0:
                vecteurs.append([-1,-1, map[i][j]-map[i][j]])
            else:
                vecteurs.append([-1, -1, map[i-1][j-1]-map[i][j]])
            
            n = [0,0,0]
            for k in range(6):
                v = []
                if k==5:
                    v = produitVec(vecteurs[k], vecteurs[0])
                else:
                    v = produitVec(vecteurs[k], vecteurs[k+1])
                n[0] += v[0]
                n[1] += v[1]
                n[2] += v[2]
            n[0]/=6
            n[1]/=6
            n[2]/=6
            
            
            result += str(n[0]) + ", "
            result += str(n[1]) + ", "
            if i==len(map)-1 and j==len(map[i])-1:
                result += str(n[2])
            else:
                result += str(n[2]) + ", "
            j+=1
        i+=1
    

    result += "], \n \"indices\" : ["
    i = 0
    while i < len(map)-1:
        j=0
        while j < len(map[i])-1:
            result += str(i*len(map[i])+j) + ", "
            result += str((i+1)*len(map[i+1])+j) + ", "
            result += str((i+1)*len(map[i+1])+j+1) + ", "
            result += str(i*len(map[i])+j) + ", "
            result += str(i*len(map[i])+j+1) + ", "
            if i==len(map)-2 and j==len(map[i])-2:
                result += str((i+1)*len(map[i+1])+j+1)
            else:
                result += str((i+1)*len(map[i+1])+j+1) + ", "
            j+=1
        i+=1

    return result + "]}"

def produitVec(vec1, vec2):
    return [vec1[1]*vec2[2]-vec1[2]*vec2[1],-(vec1[0]*vec2[2]-vec1[2]*vec2[0]), vec1[0]*vec2[1]-vec1[1]*vec2[0]]

if __name__ == "__main__":
    from parser import parse
    import sys, os
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0]+'.json'
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print ("Wrote output to", name)