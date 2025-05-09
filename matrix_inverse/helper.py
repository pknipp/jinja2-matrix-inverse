import cmath, copy, random, json

def my_int(x):
    return int(x) if int(x) == x else x

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

# Translated from fortran version in "Numerical Recipes" book.
def ludcmp(a_in):
    a = copy.deepcopy(a_in)
    n = len(a)
    indx = [None] * n
    n_max = 100
    tiny = 1e-20
    parity = True
    vv = []
    for i in range(n):
        a_max = 0
        for j in range(n):
            this_abs = abs(a[i][j])
            a_max = a_max if a_max > this_abs else this_abs
        if not a_max:
            return {"determinant": 0}
        vv.append(1/a_max)
    for j in range(n):
        for i in range(j):
            sum = a[i][j]
            for k in range(i):
                sum -= a[i][k] * a[k][j]
            a[i][j] = sum
        a_max = 0
        for i in range(j, n):
            sum = a[i][j]
            for k in range(j):
                sum -= a[i][k] * a[k][j]
            a[i][j] = sum
            dum = vv[i] * abs(sum)
            if dum >= a_max:
                i_max = i
                a_max = dum
        if not j == i_max:
            for k in range(n):
                [a[i_max][k], a[j][k]] = [a[j][k], a[i_max][k]]
            parity = not parity
            vv[i_max] = vv[j]
        indx[j] = i_max
        det = None
        if not a[j][j]:
            det = 0
            a[j][j] = tiny
        if not j == n:
            dum = 1/a[j][j]
            for i in range(j + 1, n):
                a[i][j] *= dum
        if det == None:
            det = 1 if parity else -1
            for i in range(n):
                det *= a[i][i]
    return {"determinant": det, "lu": a, "indx":indx}

def lubskb(a, indx, b_in):
    b = copy.deepcopy(b_in)
    n = len(a)
    ii = -1
    for i in range(n):
        ll = indx[i]
        sum = b[ll]
        b[ll] = b[i]
        if not ii == -1:
            for j in range(ii, i):
                sum -= a[i][j] * b[j]
        elif sum:
            ii = i
        b[i] = sum
    for i in range(n - 1, -1, -1):
        sum = b[i]
        if i < n - 1:
            for j in range(i + 1, n):
                sum -= a[i][j] * b[j]
        b[i] = sum / a[i][i]
    return b

# Following is not used.
def invert(a):
    n = len(a)
    identity = []
    zero_row = [0] * n
    for i in range(n):
        zero_copy = list(zero_row)
        zero_copy[i] = 1
        identity.append(zero_copy)
    results = ludcmp(a)
    a_inv_transpose = []
    for j in range(n):
        a_inv_transpose.append(lubskb(results["lu"], results["indx"], identity[j]))
    a_transpose = []
    for i in range(n):
        a_transpose.append(list(zero_row))
        for j in range(n):
            a_transpose[i][j] = a_inv_transpose[j][i]
    return a_transpose

def parse(is_json, square_in, rect_in = '[]'):
    try:
        a = json.loads(square_in)
    except:
        return {'error': {"message": "There is something wrong with your matrix 'A' as typed after the '/' symbol in the address bar above.", "strings": [square_in]}}
    if not isinstance(a, list):
        return {'error': {"message": 'Your matrix should be a comma-separated list of lists, with both the inner- and outer lists enclosed by square brackets.  Please double-check how you have typed it in the address bar above.', "strings": [square_in]}}
    n = len(a)
    number_of_wrong_lists = 0
    strings1 = []
    number_of_wrong_lengths = 0
    strings2 = []
    for inner_list in a:
        if not isinstance(inner_list, list):
            number_of_wrong_lists += 1
            strings1.append(json.dumps(inner_list))
        else:
            if not len(inner_list) == n:
                number_of_wrong_lengths += 1
                strings2.append(json.dumps(inner_list))
    if number_of_wrong_lists:
        return {'error': {"message": str(number_of_wrong_lists) + ' of your inner lists have/has something wrong with them/it.', "strings": strings1}}
    if number_of_wrong_lengths:
        return {'error': {"message": str(number_of_wrong_lengths) + ' of your inner lists have/has the wrong length, ie have/has a length other than ' + str(n) + ". Recall that 'A' must be a square matrix.", "strings": strings2}}
    try:
        rect_in = json.loads(rect_in)
    except:
        return {"error": {"message": "There is something wrong with your inhomogeneous part ('b').", "strings": [rect_in]}}
    if rect_in:
        if not isinstance(rect_in[0], list):
            rect_in = [rect_in]
        number_of_wrong_lists = 0
        strings1 = []
        number_of_wrong_lengths = 0
        strings2 = []
        for inner_list in rect_in:
            if not isinstance(inner_list, list):
                number_of_wrong_lists += 1
                strings1.append(json.dumps(inner_list))
            else:
                if not len(inner_list) == n:
                    number_of_wrong_lengths += 1
                    strings2.append(json.dumps(inner_list))
        if number_of_wrong_lists:
            return {"error": {"message": str(number_of_wrong_lists) + " of the inner lists for your inhomogeneous part have/has something wrong with them/it.", "strings": strings1}}
        if number_of_wrong_lengths:
            return {"error": {"message": str(number_of_wrong_lengths) + " of the inner lists for your inhomogeneous part have/has the wrong length, ie have/has a length other  than " + str(n) + ".", "strings": strings2}}
    results = ludcmp(a)
    if results['determinant']:
        zero_row = [0] * n
        identity = []
        for i in range(n):
            row = list(zero_row)
            row[i] = 1
            identity.append(row)
        a_inv_transpose = []
        for j in range(n):
            a_inv_transpose.append(lubskb(results['lu'], results['indx'], identity[j]))
        a_inv = []
        for i in range(n):
            a_inv.append(list(zero_row))
            for j in range(n):
                a_inv[i][j] = a_inv_transpose[j][i]
        results['inverse matrix'] = a_inv
    elif rect_in:
        results["warning"] = "Because the determinant is zero, some/all solutions may be huge."
    solutions = []
    if rect_in:
        for row in rect_in:
            solution = lubskb(results["lu"], results["indx"], row)
            for i in range(len(solution)):
                solution[i] = my_int(solution[i])
            solutions.append(solution)
    results.pop('lu')
    results.pop('indx')
    results['original matrix'] = a
    results['inhomogeneous part'] = rect_in
    results['solutions'] = solutions
    results['determinant'] = my_int(results["determinant"])
    for i in range(n):
        if results["determinant"]:
            for j in range(n):
                results["inverse matrix"][i][j] = my_int(results["inverse matrix"][i][j])
    return results
