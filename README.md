# AbritrageTheoryInContinuousTime-Implemented
An implementation of the models presented in the text, "Arbitrage Theory In Continuous Time (fourth edition)" by Tomas Bjork.

Currently, only the discrete time models (up to, but not including, Chapter 4) have been implemented. Continuous time models, including the Black Scholes model are in progress.

*Discret Time Models*
---
**The Binomial Model**

**Functionality:** Performs all computations for a Binomial Model with one asset with interest rate R (ie. a bank account or bond) and one stochastic asset (ie. stock) that either goes up a predetermined amount, u, or down a predetermined amount, d, with probability p_u and p_d, respecively. The asset price process, martingale measures, value process and hedging portfolio for a given contract, completeness, and arbitrage freeness of the model can all be computed.

  **Step 1.** - Import the model and contingent claim module (if needed)
  ```python
  import binomial_model as bm
  import contingent_claim as cc
  ```
  
  **Step 2.** - Consruct the model with the desired parameter values.
  ```python
  market_model = bm.BinomialModel(3, 1.5, 0.5, 80, 0, pu=0.6, pd=0.4)
  ```
  This creates the model, and automatically computes the price process for
  the asset.
  
  **Step 3.** - Define a derivative contract.
  ```python
  call_contract = partial(cc.call_option, strike_price=80)
  ```
  
  **Step 4.** - Example use case (find a hedging porfolio for the above call contract).
  ```python
hedging_portfolio = market_model.compute_all_hedging_portfolios(call_contract)
```

**The Binomial Model**

**Functionality:** Can compute, given a D bar matrix, model completeness and arbitrage-free-ness. Addition contingent claims coming soon...

  **Step 1.** - Import the model and contingent claim module (if needed)
  ```python
  import numpy as np
  import general_one_period_model as gopm
  ```
  
  **Step 2.** - Consruct the model with the desired D_bar matrix.
  ```python
  # Create a boring D_bar matrix with 3 states of the world and 3 stocks. 
  D_bar = np.ones(shape=(3, 4))

  # Create the model.
  market_model = gopm.GeneralOnePeriodModel(D_bar)
  ```
  
  **Step 3.** - Example use case (compute arbitrage-free-ness and completeness).
  ```python
  complete = market_model.is_complete()
  arbitrage_free = market_model.is_arbitrage_free()
```

