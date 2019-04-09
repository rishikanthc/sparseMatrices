import sys
from scipy import sparse
import numpy as np

DATASTRING = "double Val"
ARRSTRING = "[] = {"
ROWSTRING = "int RowPtr"
COLSTRING = "int Col"
TERMSTRING = "};\n"

def loadWeights(fname):
    matx = []
    with open(fname) as fp:
        for lines in fp:
            w = np.array(lines.strip().split(' '), dtype=float)
            matx.append(w)
    
    spmatx = sparse.csr_matrix(matx)
    #print(spmatx.todense())
    return spmatx

def writeWeights(fp, sp_matx, idx):
    dat = np.array2string(sp_matx.data,separator=',').strip('[]')
    indices = np.array2string(sp_matx.indices,separator=',').strip('[]')
    indptr = np.array2string(sp_matx.indptr,separator=',').strip('[]')


    fp.write(COLSTRING + idx + ARRSTRING + indices + TERMSTRING)
    fp.write(ROWSTRING + idx + ARRSTRING + indptr + TERMSTRING)
    fp.write(DATASTRING + idx + ARRSTRING + dat + TERMSTRING)

    #np.savetxt(fname + '_indices', sp_matx.indices)
    #np.savetxt(fname + '_indptr', sp_matx.indptr)
    #np.savetxt(fname + '_data', sp_matx.data)

def writeFullWeights(fp, fullmat, idx):
    if idx == 0:
        fp.write("double fweight" + str(idx) + "[][VECSIZE] = {")
    else:
        fp.write("double fweight" + str(idx) + "[][WSIZE] = {")

    for arr in fullmat:
        data = np.array2string(arr, separator=',').strip('][')
        fp.write(data+",")
    fp.write(TERMSTRING)

def genSparse(m, n, nz):
    matx = np.random.rand(m, n)
    fullmat = matx

    sp = int(m * n * nz / 100)
    for i in range(sp):
        ridx = np.random.randint(m)
        cidx = np.random.randint(100) % n
        matx[ridx][cidx] = 0.0

    matx = sparse.csr_matrix(matx)
    print("generated sparse matrix")
    print(matx.todense())
    return matx, fullmat
    
if __name__ == '__main__':
    fp = open('../decisionTrees/sparseMatrices/src/sparseWeights.h', 'w')
    fp.write("#define WSIZE " + str(sys.argv[1]) + '\n')
    fp.write("#define VECSIZE " + str(4) + '\n')
    w0, wf0 = genSparse(int(sys.argv[1]), 4, int(sys.argv[2]))
    w1, wf1 = genSparse(4, int(sys.argv[1]), int(sys.argv[2]))
    writeWeights(fp, w0, '0')
    writeWeights(fp, w1, '1')
    arr = np.random.rand(4)
    vector = np.array2string(arr, separator=',').strip('[]')
    fp.write("double vector[VECSIZE] = {" + vector + "};\n")
    writeFullWeights(fp, wf0, 0)
    writeFullWeights(fp, wf1, 1)
    fp.close()
    t = wf0.dot(arr)
    print(wf1.dot(t))
    #w0 = loadWeights(sys.argv[1])
    #writeWeights('sp_weights0', w0)
    #w1 = loadWeights(sys.argv[2])
    #writeWeights('sp_weights1', w1)
    #w1 = loadWeights(sys.argv[2])

