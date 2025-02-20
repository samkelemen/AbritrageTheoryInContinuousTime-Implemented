"""
Contains functions for various derivatives contracts.

Author: Sam Kelemen
Last modified: 02/20/2025
"""

def put_option(asset_price:float, strike_price:float):
    """
    A European put option.

    (float) asset_price: The current price of the asset
    (float) strike_price: The strike price of the put option
    """
    return max(0, strike_price - asset_price)

def call_option(asset_price:float, strike_price:float):
    """
    A European call option.

    (float) asset_price: The current price of the asset
    (float) strike_price: The strike price of the put option
    """
    return max(0, asset_price - strike_price)
