import re

class Method:
    def __init__(self,state,method=True,parameters=()):
        self.state=state
        self.method=method
        self.parameters=parameters

def check_tree(parameters,node,node_son,node_bro):
    """
        Args:
            context:输入的参数
            node：树上的节点
            son：节点的第一个儿子
            bro：节点的下一个兄弟
    """
    i = 0 #node
    j = 0 #para
    while True:
        if parameters[j]=='#ok' or i==-1 :
            break
        if node[i]!=parameters[j] and not (node[i]=='num' and parameters[j].isdigit()) and node[i]!='str':
            i=node_bro[i]
        else:
            i=node_son[i]
            j=j+1
    return i,parameters[j]=='#ok'#表示第一个不匹配的位置


def check_char(context):
    parameters = context.split(' ')#.char add str/.char edit STR num/.char gen/.char use str
    parameters.append('#ok')
    node =     [".char", "add", "edit", "use", "gen", 'STR', 'CON', 'SIZ', 'DEX', 'APP', 'INT', 'POW', 'KNO','LUC','str','num',"show"]
    node_son = [1,       14,     5,     14,     -1,   15,    15,    15,     15,    15,    15,   15,    15,    15,   -1,   -1,   -1]
    node_bro = [-1,       2,     3,      4,     16,    6,     7,     8,      9,    10,    11,   12,    13,    -1,   -1,   -1,   -1]
    p1,p2=check_tree(parameters,node,node_son,node_bro)
    if p2:
        if parameters[1]=='add':
            return Method(True, parameters[1], (parameters[2],))
        if parameters[1]=='edit':
            return Method(True, parameters[1], (parameters[2],int(parameters[3])))
        if parameters[1]=='use':
            return Method(True, parameters[1], (parameters[2],))
        if parameters[1]=='gen':
            return Method(True, parameters[1], None)
        if parameters[1]=='show':
            return Method(True, parameters[1], None)
    else:
        return Method(False, None,None)

def check_ra(context):
    parameters=context.split(' ')
    parameters.append('#ok')
    node=[".ra", 'str']
    node_son=[1,-1]
    node_bro=[-1,-1]
    p1,p2=check_tree(parameters,node,node_son,node_bro)
    if p2:
        return Method(True, parameters[1], ())
    else:
        return Method(False, None,None)

def check_rd(context):
    parameters=re.findall(r'\d+|[^\d]', context)#.rd .r1d10 .r10d .r1d100 h .r2d100 l
    parameters.append('#ok')
    node=    [".","r","num","d","num","h","l"]
    node_son=[  1,  2,    3,  4,    5, -1, -1]
    node_bro=[ -1, -1,    3, -1,    5,  6, -1]
    p1,p2=check_tree(parameters,node,node_son,node_bro)
    if parameters[2]=='d':
        parameters.insert(2,1)
    if parameters[-2]!='h' and parameters[-2]!='l':
        parameters.insert(-1,'o')
    if (parameters[-2]=='h' or parameters[-2]=='o' or parameters[-2]=='l') and not parameters[-3].isdigit():
        parameters.insert(4, 100)
    if p2:
        return Method(True, parameters[-2], (int(parameters[2]), int(parameters[4])))
    else:
        return Method(False, None,None)

def check_login(context):
    parameters=context.split(' ')
    parameters.append('#ok')
    node=[".login", 'str']
    node_son=[1,-1]
    node_bro=[-1,-1]
    p1,p2=check_tree(parameters,node,node_son,node_bro)
    if p2:
        return Method(True, parameters[1], ())
    else:
        return Method(False, None,None)
