import pyscf
import numpy as np

mol = pyscf.M(atom="""
H 0 0 0
H 0 0 1
""", basis="sto-3G", verbose=4)

hf = mol.HF()
hf.run()

fock = np.diag(hf.mo_energy)

g_ao = mol.intor("int2e", aosym="s8")

c = hf.mo_coeff

eris = pyscf.ao2mo.incore.general(g_ao, (c, c, c, c), compact=False)

print(fock)
print(eris)

# fock.tofile("fock.dat")
# eris.tofile("eris.dat")
