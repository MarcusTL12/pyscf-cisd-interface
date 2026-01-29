import pyscf
import numpy as np
import sys

#### Reading file parameters ####

no = int(sys.argv[1])
nv = int(sys.argv[2])
nm = no + nv

file_1e = sys.argv[3]
file_2e = sys.argv[4]

fock = np.fromfile(file_1e).reshape(nm, nm)
eri_full = np.fromfile(file_2e).reshape(nm, nm, nm, nm)

#### Setting up dummy variables ####

dummy_mol = pyscf.M(atom="""
H 0 0 0
H 0 0 1
""", basis="sto-3G", verbose=0)

dummy_hf = dummy_mol.HF()
dummy_hf.run()

ci = dummy_hf.CISD()
ci.verbose = 0
eris = ci.ao2mo(ci.mo_coeff)

class DummySCF:
    def __init__(self):
        self.mo_coeff = None
        self.e_tot = 0.0
        self.converged = True

#### Overwriting parameters and integrals ####

mo_occ = np.zeros(nm)
mo_occ[:no] = 2.0

ci.mol = None
ci._scf = DummySCF()
ci.mo_occ = mo_occ
ci.mo_coeff = None
ci.nocc = no

eris.mol = None
eris.mo_coeffs = None
eris.nocc = no
eris.fock = fock
eris.mo_energy = np.diag(eris.fock)

eris.oooo = eri_full[:no, :no, :no, :no].copy()
eris.ovoo = eri_full[:no, no:, :no, :no].copy()
eris.oovv = eri_full[:no, :no, no:, no:].copy()
eris.ovvo = eri_full[:no, no:, no:, :no].copy()
eris.ovov = eri_full[:no, no:, :no, no:].copy()

ovvv = eri_full[:no, no:, no:, no:].copy()
vvvv = eri_full[no:, no:, no:, no:].copy()

eris.ovvv = pyscf.lib.pack_tril(ovvv.reshape(-1,nv,nv)).reshape(no,nv,-1)
eris.vvvv = pyscf.ao2mo.restore(4, vvvv, nv)

ci.kernel(None, eris)

ci.make_rdm1().tofile(file_1e)
ci.make_rdm2().tofile(file_2e)
