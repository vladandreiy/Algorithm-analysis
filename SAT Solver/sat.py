import sys


class ClauseNode:
    def __init__(self, data):
        self.left = None
        self.right = None
        matrix = []
        for i in range(0, len(data)):
            line = []
            for j in range(0, len(data[i])):
                line.append(data[i][j])
            matrix.append(line)
        self.data = matrix


def read_cnf():
    matrix = sys.stdin.readline()
    matrix = matrix.rstrip()
    matrix = matrix.split("^")
    var_matrix = []
    for i in range(0, len(matrix)):
        matrix[i] = matrix[i][:-1]
        matrix[i] = matrix[i][1:]
        var_matrix.append(matrix[i].split("V"))
    fnc_matrix = []
    pos = 0
    dictionar = dict()
    for i in range(0, len(var_matrix)):
        for j in range(0, len(var_matrix[i])):
            if var_matrix[i][j][0] == "~":
                variable = var_matrix[i][j].strip("~")
            else:
                variable = var_matrix[i][j]
            if variable not in dictionar:
                dictionar[variable] = pos
                pos += 1
    variables_no = len(dictionar)

    for i in range(0, len(var_matrix)):
        fnc_line = list(0 for _ in range(variables_no))
        for j in range(0, len(var_matrix[i])):
            value = 1
            if var_matrix[i][j][0] == "~":
                value = -1
                variable = var_matrix[i][j].strip("~")
            else:
                variable = var_matrix[i][j]
            fnc_line[dictionar[variable]] = value
        fnc_matrix.append(fnc_line)
    return dictionar, fnc_matrix


def bkt(fnc_matrix, dictionar, index, interp):
    if index == len(dictionar):
        # toate variabilele au o valoare
        for i in range(0, len(fnc_matrix)):
            clause = 0
            for j in range(0, len(fnc_matrix[i])):
                if fnc_matrix[i][j] < 0:
                    if interp[j] == 0:
                        value = 1
                    else:
                        value = 0
                else:
                    value = fnc_matrix[i][j] * interp[j]
                clause = value or clause
                if clause == 1:
                    break
            if clause == 0:
                return False
        return True
    interp[index] = 0
    if bkt(fnc_matrix, dictionar, index + 1, interp):
        return True
    interp[index] = 1
    if bkt(fnc_matrix, dictionar, index + 1, interp):
        return True
    return False


def cnf_sat():
    dictionary, cnf_matrix = read_cnf()
    reverse_dictionary = {v: k for k, v in dictionary.items()}
    interp = [0] * len(dictionary)
    index = 0
    return bkt(cnf_matrix, reverse_dictionary, index, interp)


# Daca value = true => scot clauza
# Daca value = false => scot variabila
def bdd_sat():
    # root = Node(sys.stdin.readline())
    matrix = sys.stdin.readline()
    matrix = matrix.rstrip()
    matrix = matrix.split("^")
    var_matrix = []
    for i in range(0, len(matrix)):
        matrix[i] = matrix[i][:-1]
        matrix[i] = matrix[i][1:]
        var_matrix.append(matrix[i].split("V"))

    # Get first literal in first clause
    # Daca am true => scot clauza
    # Daca am false => scot variabila
    # Daca am clauze goale ( [] )=> FAIL
    # Daca matricea e complet goala => SUCCES

    variables = set()
    for clause in var_matrix:
        for literal in clause:
            if literal[0] == "~":
                variables.add(literal[1:])
            else:
                variables.add(literal)
    node = ClauseNode(var_matrix)
    if bdd_bkt(node.left, variables, node, 0):
        return True
    if bdd_bkt(node.right, variables, node, 1):
        return True
    return False


def bdd_bkt(node, variables: set, parent, son_index):
    node = ClauseNode(parent.data)
    if len(node.data) == 0:
        return True
    elif len(variables) == 0:
        return False
    variables_new = set(variables)
    variable = variables_new.pop()
    i = 0
    while i < len(node.data):
        j = 0
        while j < len(node.data[i]):
            if node.data[i][j] == variable:
                if son_index == 0:
                    node.data[i].remove(node.data[i][j])
                    break
                elif son_index == 1:
                    node.data.remove(node.data[i])
                    i -= 1
                    break
            elif node.data[i][j] == ("~" + variable):
                if son_index == 0:
                    node.data.remove(node.data[i])
                    i -= 1
                    break
                elif son_index == 1:
                    node.data[i].remove(node.data[i][j])
                    break
            j += 1
        i += 1
    if bdd_bkt(node.left, variables_new, node, 0):
        return True
    if bdd_bkt(node.right, variables_new, node, 1):
        return True
    return False


if __name__ == '__main__':
    print(cnf_sat())
    print(bdd_sat())
