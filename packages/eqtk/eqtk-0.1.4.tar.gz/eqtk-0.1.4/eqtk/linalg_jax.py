import jax.numpy as jnp
import constants
# from . import constants

def _normalize_rows(A):
    """Multiply each row of `A` by a scalar such that the 2-norm of
    each row is unity."""
    B = jnp.empty(A.shape)

    for i in range(A.shape[0]):
        B = B.at[i, :].set(A[i, :] / jnp.sqrt(jnp.linalg.norm(A[i, :])))

    return B


def _orthonormalize_rows(A):
    """Convert rows of matrix `A` to orthnormal basis."""
    U, s, V = jnp.linalg.svd(A)
    return V[: A.shape[0]]


def diag_multiply(A, d):
    """Compute the D . A . D, where d is the diagonal of diagonal
    matrix D.
    """
    B = jnp.empty_like(A)

    for j in range(len(d)):
        B = B.at[:, j].set(d[j] * A[:, j])

    for i in range(len(d)):
        B = B.at[i, :].set(d[i] * B[i, :])

    return B


def lower_tri_solve(L, b):
    """
    Solves the lower triangular system Lx = b.
    Uses column-based forward substitution, outlined in algorithm
    3.1.3 of Golub and van Loan.
    Parameters
    ----------
    L : ndarray
        Square lower triangulatar matrix (including diagonal)
    b : ndarray, shape L.shape[0]
        Right hand side of Lx = b equation being solved.
    Returns
    -------
    x : ndarray
        Solution to Lx = b.
    """
    n = L.shape[0]

    # Solve Lx = b.
    x = jnp.copy(b)
    for j in range(n - 1):
        if abs(L[j, j]) > constants._float_eps:
            x = x.at[j].divide(L[j, j])
            for i in range(j + 1, n):
                x = x.at[i].add(-x[j] * L[i, j])
        else:
            x = x.at[j].set(0.0)

    if n > 0:
        if abs(L[n - 1, n - 1]) > constants._float_eps:
            x = x.at[n-1].divide(L[n - 1, n - 1])
        else:
            x = x.at[n - 1].set(0.0)

    return x


def upper_tri_solve(U, b):
    """
    Solves the lower triangular system Ux = b.
    Uses column-based forward substitution, outlined in algorithm
    3.1.4 of Golub and van Loan.

    Parameters
    ----------
    U: ndarray
        Square upper triangulatar matrix (including diagonal)
    b : ndarray, shape L.shape[0]
        Right hand side of Ux = b equation being solved.
    Returns
    -------
    x : ndarray
        Solution to Ux = b.
    """
    n = U.shape[0]

    # Solve Ux = b by back substitution.
    x = jnp.copy(b)
    for j in range(n - 1, 0, -1):
        if abs(U[j, j]) > constants._float_eps:
            x = x.at[j].divide(U[j, j])
            for i in range(0, j):
                x = x.at[i].add(-x[j] * U[i, j])
        else:
            x = x.at[j].set(0.0)

    if n > 0:
        if abs(U[0, 0]) > constants._float_eps:
            x = x.at[0].divide(U[0, 0])
        else:
            x = x.at[0].set(0.0)

    return x


def modified_cholesky(A):
    """
    Modified Cholesky decomposition.
    Performs modified Cholesky decomposition based on the algorithm
    GMW81 in Fang, O'Leary, 2006. Modified Cholesky Algorithms: A Catalog
    with New Approaches. From the matrix A

    Parameters
    ----------
    A : ndarray
        Symmetric, real, positive definite or positive semidefinite
        matrix.

    Returns
    -------
    L : ndarray, shape A.shape
        Lower triangulatar matrix with Cholesky decomposition
    p : ndarray, shape A.shape[0]
        Permutation vector defining which columns of permutation matrix
        have ones.
    success : bool
        True if Cholesky decomposition was successful and False otherwise,
        usually due to matrix not being positive semidefinite.

    Notes
    -----
    .. A check of symmetry is not necessary in the context of EQTK,
       since we only work with symmetric matrices.
    """
    n = A.shape[0]

    L = jnp.copy(A)
    p = jnp.arange(n)

    # Keep track if factorization was successful.
    success = True

    xi = 0
    for i in range(n):
        for j in range(i):
            temp = abs(L[i, j])
            xi = max(xi, temp)

    eta = 0
    for i in range(n):
        temp = abs(L[i, i])
        eta = max(eta, temp)

    if n > 1:
        beta = jnp.sqrt(max(eta, xi / jnp.sqrt(n * n - 1)))
    else:
        beta = jnp.sqrt(eta)
    beta = max(beta, constants._float_eps)

    for k in range(n):
        # Pick a pivot.
        mu_val = L[k, k]
        mu = k
        for i in range(k + 1, n):
            temp = L[i, i]
            if mu_val < temp:
                mu = i
                mu_val = temp

        # Diagonal pivot k <=> mu
        i = p[mu]
        p = p.at[mu].set(p[k])
        p = p.at[k].set(i)

        for i in range(k):
            temp = L[k, i]
            L = L.at[k, i].set(L[mu, i])
            L = L.at[mu, i].set(temp)

        temp = L[k, k]
        L = L.at[k, k].set(L[mu, mu])
        L = L.at[mu, mu].set(temp)
        for i in range(k + 1, mu):
            temp = L[i, k]
            L = L.at[i, k].set(L[mu, i])
            L = L.at[mu, i].set(temp)

        for i in range(mu + 1, n):
            temp = L[i, k]
            L = L.at[i, k].set(L[i, mu])
            L = L.at[i, mu].set(temp)

        # Compute c_sum
        c_sum = 0
        for i in range(k + 1, n):
            c_sum = max(c_sum, abs(L[i, k]))
        c_sum /= beta
        c_sum = c_sum * c_sum

        # Make sure L is semi-positive definite.
        if L[k, k] < 0:
            # Otherwise the factorization was not completed successfully.
            success = False

        temp = abs(L[k, k])
        temp = max(temp, constants._float_eps * eta)
        temp = max(temp, c_sum)
        L = L.at[k, k].set(jnp.sqrt(temp))

        # Compute the current column of L.
        for i in range(k + 1, n):
            L = L.at[i, k].divide(L[k, k])

        # Adjust the \bar{L}
        for j in range(k + 1, n):
            for i in range(j, n):
                L = L.at[i, j].add(-L[i, k] * L[j, k])

        # Just keep lower triangle
        for i in range(0, n - 1):
            L = L.at[i, i + 1 :].set(0.0)

    return L, p, success


def modified_cholesky_solve(L, p, b):
    """
    Solve system Ax = b, with P A P^T = L L^T post-Cholesky decomposition.
    Parameters
    ----------
    L : ndarray
        Square lower triangulatar matrix from Cholesky decomposition
    p : ndarray, shape L.shape[0]
        Permutation vector defining which columns of permutation matrix
        have ones.
    b : ndarray, shape L.shape[0]
        Right hand side of Ax = b equation being solved.
    Returns
    -------
    x : ndarray, shape L.shape[0]
        Solution to Ax = b.
    """
    n = L.shape[0]

    U = L.transpose()
    xp = jnp.zeros(n)
    for i in range(n):
        xp = xp.at[i].set(b[p[i]])

    # Solve Ly = b storing y in xp.
    x = lower_tri_solve(L, xp)

    # Solve L^T x = y by back substitution.
    xp = upper_tri_solve(U, x)

    for i in range(n):
        x = x.at[p[i]].set(xp[i])

    return x


def solve_pos_def(A, b):
    """Solve A x = b, where A is known to be positive definite.

    Parameters
    ----------
    A : ndarray, shape (n, n)
        Symmetric, real, positive definite or positive semidefinite
        matrix.
    b : ndarray, shape (n,)
        Array of real numbers.

    Returns
    -------
    output : ndarray, shape (n,)
        Solution x to A x = b.
    success : bool
        False if Cholesky decomposition failed.
    """
    L, p, success = modified_cholesky(A)

    if not success:
        return jnp.zeros(len(b)), success

    return modified_cholesky_solve(L, p, b), success


def nullspace_svd(A, tol=1e-12):
    """
    Calculate a basis for the approximate null space of A, consider any
    eigenvalue less than tolerance as 0

    Parameters
    ----------
    A : ndarray
        A matrix of shape (M, N) M <= N
    tol :
        The floor in absolute value for eigenvalues to be considered
        non-zero

    Returns
    -------
    N : ndarray
        A matrix of shape (N, K) where K is the rank of the null space,
        at least N - M. This means that the *rows* of the output span
        the nullspace of A.

        Every element in jnp.dot(A, N.T) should be approximately 0
    """
    u, sigma, v_trans = jnp.linalg.svd(A)
    nonzero_inds = (sigma >= tol).sum()
    return v_trans[nonzero_inds:, :]
