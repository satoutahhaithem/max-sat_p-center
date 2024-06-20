from pysat.formula import IDPool, WCNF
vpool = IDPool()
def var_a_ijk(i, j, k):
    return vpool.id((i, j, k))
print (var_a_ijk(1,2,2))