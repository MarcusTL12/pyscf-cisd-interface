import pyscf
import numpy as np

dummy_mol = pyscf.M(atom="""
H 0 0 0
H 0 0 1
""", basis="sto-3G")

dummy_hf = dummy_mol.HF()
dummy_hf.run()

ci = dummy_hf.CISD()
ci.verbose = 5
eris = ci.ao2mo(ci.mo_coeff)

class DummySCF:
    def __init__(self, e_hf):
        self.mo_coeff = None
        self.e_tot = e_hf
        self.converged = True

no = 2
nv = 3
nm = no + nv

mo_occ = np.zeros(nm)
mo_occ[:no] = 2.0

ci.mol = None
ci._scf = DummySCF(0.0)
ci.mo_occ = mo_occ
ci.mo_coeff = None
ci.nocc = no

eris.mol = None
eris.mo_coeffs = None
eris.nocc = no
eris.fock = None
eris.mo_energy = np.diag(eris.fock)

eris.oooo = None
eris.ovoo = None
eris.oovv = None
eris.ovvo = None
eris.ovov = None

ovvv = None
vvvv = None

eris.ovvv = pyscf.lib.pack_tril(ovvv.reshape(-1,nv,nv)).reshape(no,nv,-1)
eris.vvvv = pyscf.ao2mo.restore(4, vvvv, nv)

ci.kernel(None, eris)

rdm1 = ci.make_rdm1()
rdm2 = ci.make_rdm2()

print(rdm1)
print(rdm2)
