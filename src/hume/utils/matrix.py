import numpy as np

# import scipy


argmax = np.argmax


def as_array(l):
    return np.asarray(l)


def shape(U):
    return U.shape


def dagger(U):
    return U.T.conj()


def eig(U):
    return np.linalg.eig(U)


def rvs(dim): # TODO: add reference
    random_state = np.random
    H = np.eye(dim)
    D = np.ones((dim,))
    for n in range(1, dim):
        x = random_state.normal(size=(dim - n + 1,))
        D[n - 1] = np.sign(x[0])
        x[0] -= D[n - 1] * np.sqrt((x * x).sum())
        # Householder transformation
        Hx = (np.eye(dim - n + 1) - 2. * np.outer(x, x) / (x * x).sum())
        mat = np.eye(dim)
        mat[n - 1:, n - 1:] = Hx
        H = np.dot(H, mat)
        # Fix the last sign such that the determinant is 1
    D[-1] = (-1) ** (1 - (dim % 2)) * D.prod()
    # Equivalent to np.dot(np.diag(D), H) but faster, apparently
    H = (D * H.T).T
    return H


def random_transformation(n):
    U = rvs(2 ** n)

    def f_direct(state):
        assert (len(state) == 2 ** n)
        s = U @ state
        for k in range(len(s)):
            state[k] = s[k]

    def f_inverse(state):
        assert (len(state) == 2 ** n)
        s = dagger(U) @ state
        for k in range(len(s)):
            state[k] = s[k]

    return f_direct, f_inverse
