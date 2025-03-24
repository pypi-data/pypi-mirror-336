# solver.py
import pypipre as pipre
import sys, re, os
#import json
import commentjson as json

fnA = sys.argv[1]
fnb = sys.argv[2]
config = sys.argv[3]

params = json.load(open(config))

A = pipre.ParCSRMatrix()
A.loadFromFile(fnA)
b = pipre.ParMatrix()
b.loadFromFile(fnb)
if b.getSize() == 0:
    b.resize(A.getRows(), 1)
    b.fill(1)

# transfer the matrix and vector to gpu 0.
dev = pipre.Device("cuda:0")
A = A.toDevice(dev)
b = b.toDevice(dev)

# use gpu 0 to finish the computation.
precond = pipre.createPrecond(params["preconditioner"])
precond.setup(A)
solver = pipre.createSolver(params["solver"])
solver.setup(A)

out = solver.solve(precond, A, b)