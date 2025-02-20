"""
An implementation of the Binomial Model, as described in 
Chapter 2 of "Arbitrage Theory in Continuous Time", by 
Tomas Djork.

Author: Sam Kelemen
Last modified: 02/20/2025
"""
from collections.abc import Callable


class BinaryTree:
    def __init__(self, T: int):
        """
        (int T): The number of time steps for the model 
            or date of contract epiration).
        """
        num_nodes = int((T + 1) * (T + 2) / 2)
        self.data = [None] * num_nodes

    def _bt_index(self, t: int, k: int) -> int:
        """
        (int) t: the time step of the model, indexed from 0
        (int) k: the number of up steps to get to the node

        Returns the index of the node at time t, 
        after k up steps. t is indexed starting at 0.
        """
        return int((t * (t + 1) / 2) + k)

    def set_data(self, value: float, t: int, k: int) -> None:
        """
        (int) t: the time step of the model, indexed from 0
        (int) k: the number of up steps to get to the node

        Sets the data of the node at time t, after
        k up steps.
        """
        index = self._bt_index(t, k)
        self.data[index] = value

    def get_data(self, t: int, k: int) -> float:
        """
        (int) t: the time step of the model, indexed from 0
        (int) k: the number of up steps to get to the node

        Gets the data of the node at time t, after
        k up steps.
        """
        index = self._bt_index(t, k)
        return self.data[index]

class BinomialModel:
    def __init__(self, T: int, u: float, d: float, S: float, R: float, pu: float = 0.5, pd: float = 0.5) -> None:
        """
        (int)    T: number of periods
        (float)  u: up movement value
        (float)  d: down movement value
        (float) pu: probability of upwards movement
        (float) pd: probability of downwards movement
        (float)  S: initial value of stock
        (float)  R: interest rate on the bond
        """
        # Assert that {pu, pd} is a probability measure.
        assert pu + pd == 1

        # Assert that u > d.
        assert u > d

        self.T = T
        self.u, self.d = u, d
        #self.pu, self.pd = pu, pd
        self.S = S
        self.R = R

        self.price_process = BinaryTree(T)
        self._compute_price_process() # Now, fill the null value with the actual prices

    def compute_martingale_measure(self) -> tuple[float, float]:
        """
        Calculate the martingale measure for the binomial
        model.
        """
        qu = ((1 + self.R) - self.d) / (self.u - self.d)
        qd = (self.u - (1 + self.R)) / (self.u - self.d)
        return qu, qd

    def _compute_price_process(self) -> None:
        """
        Compute price of stock for all nodes in the binary tree.
        """
        # Iterate over the layers of the binary tree
        for t in range(self.T + 1):
            # Iterate over the nodes in the layer of the bt
            for k in range(t + 1):
                # t - k is number of down steps
                price_process = self.S * (self.u ** k) * (self.d ** (t - k))
                self.price_process.set_data(price_process, t, k)

    def _compute_value_at_node(self, t: int, k: int, phi: Callable[[float], float], value_process: BinaryTree) -> float:
        """
        (int) t       : the time step of the model, indexed from 0
        (int) k       : the number of up steps to get to the node
        (function) phi: The contract function for the contingent claim

        Computes the value of the node at time t after k up steps.
        """
        # Compute and return the value if at the expiration date, T
        if (t == self.T):
            price_process = self.price_process.get_data(t, k)
            return phi(price_process)

        # Compute at return the value if not at the expiration date, T    
        qu, qd = self.compute_martingale_measure()
        payoff = qu * value_process.get_data(t + 1, k + 1) + qd * value_process.get_data(t + 1, k)
        return (1 / 1 + self.R) * (payoff) # Discounted payoff is the value

    def compute_value_process(self, phi: Callable[[float], float]) -> BinaryTree:
        """
        (function) phi: The contract function for the contingent claim

        Computes the value process for the binomial model.
        """
        value_process = BinaryTree(self.T)

        # Iterate over the layers of the binary tree
        for t in range(self.T, -1, -1):
            # Iterate over the nodes in the layer of the bt
            for k in range(t, -1, -1):
                value = self._compute_value_at_node(t, k, phi, value_process)
                value_process.set_data(value, t, k)

        return value_process

    def compute_hedging_portfolio_at_node(self, t: int, k: int, phi: Callable[[float], float]) -> tuple[float, float]:
        """
        (int) t       : the time step of the model, indexed from 0
        (int) k       : the number of up steps to get to the node
        (function) phi: The contract function for the contingent claim

        Computes the hedging profile for a given contingent claim at
        time t and after k up steps.
        """
        value_process = self.compute_value_process(phi)

        V_u = value_process.get_data(t + 1, k + 1)
        V_d = value_process.get_data(t + 1, k)
        x = (1 / 1 + self.R) * (self.u * V_d - self.d * V_u) / (self.u - self.d)

        S = self.price_process.get_data(t, k)
        y = (1 / S) * (V_u - V_d) / (self.u - self.d)

        return x, y

    def compute_all_hedging_portfolios(self, phi: Callable[[float], float]) -> BinaryTree:
        """
        (function) phi: The contract function for the contingent claim

        Computes the hedging pofile for the given contingent claim
        at all nodes in the tree for the event space.
        """
        hedging_portfolios = BinaryTree(self.T - 1)

        # Iterate over the layers of the binary tree (excluding the last layer)
        for t in range(self.T):
            # Iterate over the nodes in the layer of the bt
            for k in range(t + 1):
                x, y = self.compute_hedging_portfolio_at_node(t, k, phi)
                hedging_portfolios.set_data((x, y), t, k)

        return hedging_portfolios

    def is_complete(self):
        """
        Returns True, as the binomial model is always complete.
        """
        return True

    def is_arbitrage_free(self):
        """
        Returns True if the model is arbitrage free, and False if
        the model contains arbitrage opportunies.
        """
        return (self.d < 1 + self.R) and (self.u > (1 + self.R))
    
    def is_arbitrage_portfolio(self):
        pass

    def find_arbitrage_porffolio(self):
        pass
