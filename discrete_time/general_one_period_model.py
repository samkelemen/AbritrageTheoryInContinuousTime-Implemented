"""
An implementation of the General One Period Model from
Chapter 3 of 'Arbitrage Theory in Continuous Time'
"""
import numpy as np
from numpy.typing import NDArray
from scipy.optimize import linprog


class GeneralOnePeriodModel:
    """
    An implementation of the General One Period Model from
    Chapter 3 of 'Arbitrage Theory in Continuous Time'
    """
    def __init__(self, D_bar: NDArray[np.float64]) -> None:
        """
        (numpy NDArray) D: D matrix as defined in Chapter 3 of
        'Arbitrage Theory in Continuous Time'.
        """
        self.D_bar = D_bar

    def get_D(self):
        """
        Returns the D matrix.
        """
        return self.D_bar[:, 1:]

    def get_S_0(self):
        """
        Returns the price vector at time 0.
        """
        return self.D_bar[:, 0]

    def normalize(self, matrix) -> NDArray[np.float64]:
        """
        Computes the matrix, using the first asset as the numeraire.
        """
        normalized_matrix = np.copy(matrix)
        for col in range(normalized_matrix.shape[1]):
            normalized_matrix[:, col] /= normalized_matrix[0, col]
        return normalized_matrix

    def is_complete(self) -> bool:
        """
        Returns True, as the binomial model is always complete.

        Utilizes the Thm. that if the rows of D span R^m, where
        m is the size of the probability space, then the market
        is complete.

        Note: Implemented with numpy.linalg.rank, which approximates
        the SVD of the D matrix to find the rank. This is done
        numerically and may incure associated errors.
        """
        D = self.D_bar[:, :-1]
        probability_space_size = D.shape()[1]

        if np.linalg.matrix_rank(D) == probability_space_size:
            return True
        return False

    def is_arbitrage_free(self) -> bool:
        """
        Returns True if the model is arbitrage free and False
        otherwise.

        Utilizes the Thm that the market is arbitrage free iff
        there exists a martingale measure.

        Approaches this problem with linear programming.
        """
        D_z = self.normalize(self.get_D())
        S_0 = self.get_S_0().flatten()

        # Objective function should have all zero coefficients
        c = np.zeros(shape=D_z.shape[1])

        # Constraint equation
        A_eq = np.vstack( (D_z, np.ones((1, D_z.shape[1]))) )
        b_eq = np.concatenate( (S_0, np.array([1])) )
        q_bounds = (0, 1)

        solution = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=q_bounds)

        if solution.status == 0:
            return True
        if solution.status == 2:
            return False
        return "Solver could not decide."

    def find_arbitrage_porffolio(self) -> list:
        """
        Finds an arbitrage porfolio if the market is not
        arbitrage free.
        """
        pass
