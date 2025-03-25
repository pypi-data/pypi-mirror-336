import time
import optionvisualizer_wrapper as ovw
import plotly.graph_objects as go
import numpy as np
from typing import Literal, TypedDict, List, Union, Tuple


class Leg(TypedDict):
    strike: float
    quantity: int  # Positive for long, negative for short
    put_call: Literal["put", "call"]


def plot_strategy_greek_surface_price_time(
    spot: Union[float, int],
    strategy: List[Leg],
    r: float = 0.01,
    sigma: float = 0.2,
    price_range: Tuple[float, float] | None = None,
    time_range: Tuple[float, float] = (0.0027, 7 / 365),
    num_prices: int = 100,
    num_times: int = 100,
    colorscale: str = "viridis",
    mm: bool = False,
    greek: Literal[
        "delta",
        "gamma",
        "theta",
        "vega",
        "rho",
        "vomma",
        "vanna",
        "charm",
        "zomma",
        "speed",
        "color",
        "ultima",
        "vega bleed",
        "price",
    ] = "delta",
) -> go.Figure:
    """
    Plots a 3D surface of a specified Greek for any option strategy
    vs. Underlying Price and Time to Expiration.

    Args:
        spot: Current price of the underlying asset
        strategy: List of option legs, each with strike, quantity, and put_call type
        r: Fixed interest rate
        sigma: Fixed volatility
        price_range: Tuple (min_price, max_price) for the underlying price range.
            If None, automatically calculates based on spot price and strategy strikes
        time_range: Tuple (min_time, max_time) for the time to expiration range (in years)
        num_prices: Number of price points
        num_times: Number of time points
        colorscale: Plotly colorscale (e.g., 'viridis', 'plasma', 'magma')
        mm: If True, plot the market maker's view (opposite sign)
        greek: The Greek to plot

    Returns:
        go.Figure: The Plotly figure object
    """
    wrapper = ovw.OptionVisualizerWrapper()

    # Set default price range if not provided
    if price_range is None:
        strikes = [leg["strike"] for leg in strategy]
        min_strike = min(strikes)
        max_strike = max(strikes)
        range_width = max_strike - min_strike
        # Set price range to be 30% below lowest strike and 30% above highest strike
        price_range = (
            min(spot * 0.7, min_strike * 0.7),
            max(spot * 1.3, max_strike * 1.3),
        )

    prices = np.linspace(price_range[0], price_range[1], num_prices)
    times = np.linspace(time_range[0], time_range[1], num_times)
    price_grid, time_grid = np.meshgrid(prices, times)
    greek_values = np.zeros_like(price_grid)

    # Generate a strategy name based on the legs
    strategy_name = ""
    for i, leg in enumerate(strategy):
        prefix = "+" if leg["quantity"] > 0 else ""
        strategy_name += (
            f"{prefix}{leg['quantity']} {leg['put_call'].upper()} {leg['strike']}"
        )
        if i < len(strategy) - 1:
            strategy_name += ", "

    for i in range(price_grid.shape[0]):
        for j in range(price_grid.shape[1]):
            net_greek = 0

            for leg in strategy:
                # Calculate Greek for this leg
                leg_greek = wrapper.sensitivities(
                    greek=greek,
                    S=price_grid[i, j],
                    K=leg["strike"],
                    T=time_grid[i, j],
                    r=r,
                    sigma=sigma,
                    option=leg["put_call"],
                )

                # Add to net Greek value (accounting for quantity)
                net_greek += leg_greek * leg["quantity"]

            # Apply market maker view if mm=True
            greek_values[i, j] = -net_greek if mm else net_greek

    # Create the 3D surface plot
    fig = go.Figure(
        data=[
            go.Surface(
                z=greek_values, x=price_grid, y=time_grid * 365, colorscale=colorscale
            )
        ]
    )

    # Format the time range for display
    min_days = time_range[0] * 365
    max_days = time_range[1] * 365
    time_label = f"{min_days:.1f}-{max_days:.1f} days"

    title_prefix = "Market Maker's " if mm else ""
    fig.update_layout(
        title=(
            title := (
                f"{title_prefix}{greek.title()} vs. Price and Time | "
                f"Strategy: {strategy_name} | Spot: {spot} | "
                f"DTE: {time_label}"
            )
        ),
        meta={"title": title},
        scene={
            "xaxis_title": "Underlying Price",
            "yaxis_title": "Time to Expiration (Days)",
            "zaxis_title": greek.title(),
            "xaxis": {
                "backgroundcolor": "rgb(230, 230, 200)",
                "gridcolor": "white",
                "showbackground": True,
                "zerolinecolor": "white",
            },
            "yaxis": {
                "backgroundcolor": "rgb(200, 200, 230)",
                "gridcolor": "white",
                "showbackground": True,
                "zerolinecolor": "white",
            },
            "zaxis": {
                "backgroundcolor": "rgb(230, 200, 230)",
                "gridcolor": "white",
                "showbackground": True,
                "zerolinecolor": "white",
            },
        },
    )
    fig.update_scenes(yaxis_autorange="reversed")
    return fig


def plot_strategy_greek_surface_vol_price(
    spot: Union[float, int],
    strategy: List[Leg],
    T: float,
    r: float = 0.01,
    price_range: Tuple[float, float] | None = None,
    vol_range: Tuple[float, float] = (0.1, 0.5),
    num_prices: int = 100,
    num_vols: int = 100,
    colorscale: str = "viridis",
    mm: bool = False,
    greek: Literal[
        "delta",
        "gamma",
        "theta",
        "vega",
        "rho",
        "vomma",
        "vanna",
        "charm",
        "zomma",
        "speed",
        "color",
        "ultima",
        "vega bleed",
        "price",
    ] = "delta",
) -> go.Figure:
    """
    Plots a 3D surface of a specified Greek for any option strategy
    vs. Underlying Price and Implied Volatility.

    Args:
        spot: Current price of the underlying asset
        strategy: List of option legs, each with strike, quantity, and put_call type
        T: Fixed time to expiration (in years).
        r: Fixed interest rate
        price_range: Tuple (min_price, max_price) for the underlying price range.
            If None, automatically calculates based on spot price and strategy strikes
        vol_range: Tuple (min_vol, max_vol) for the volatility range.
        num_prices: Number of price points
        num_vols: Number of volatility points.
        colorscale: Plotly colorscale (e.g., 'viridis', 'plasma', 'magma').
        mm: If True, plot the market maker's view (opposite sign)
        greek: The Greek to plot

    Returns:
        go.Figure: The Plotly figure object.
    """
    wrapper = ovw.OptionVisualizerWrapper()

    # Set default price range if not provided
    if price_range is None:
        strikes = [leg["strike"] for leg in strategy]
        min_strike = min(strikes)
        max_strike = max(strikes)
        range_width = max_strike - min_strike
        # Set price range to be 30% below lowest strike and 30% above highest strike
        price_range = (
            min(spot * 0.7, min_strike * 0.7),
            max(spot * 1.3, max_strike * 1.3),
        )

    prices = np.linspace(price_range[0], price_range[1], num_prices)
    vols = np.linspace(vol_range[0], vol_range[1], num_vols)
    price_grid, vol_grid = np.meshgrid(prices, vols)
    greek_values = np.zeros_like(price_grid)

    # Generate a strategy name based on the legs
    strategy_name = ""
    for i, leg in enumerate(strategy):
        prefix = "+" if leg["quantity"] > 0 else ""
        strategy_name += (
            f"{prefix}{leg['quantity']} {leg['put_call'].upper()} {leg['strike']}"
        )
        if i < len(strategy) - 1:
            strategy_name += ", "

    for i in range(price_grid.shape[0]):
        for j in range(vol_grid.shape[1]):
            net_greek = 0
            for leg in strategy:
                # Calculate Greek for this leg
                leg_greek = wrapper.sensitivities(
                    greek=greek,
                    S=price_grid[i, j],
                    K=leg["strike"],
                    T=T,
                    r=r,
                    sigma=vol_grid[i, j],
                    option=leg["put_call"],
                )
                # Add to net Greek (accounting for quantity)
                net_greek += leg_greek * leg["quantity"]

            # Apply market maker view if mm=True
            greek_values[i, j] = -net_greek if mm else net_greek

    fig = go.Figure(
        data=[
            go.Surface(z=greek_values, x=price_grid, y=vol_grid, colorscale=colorscale)
        ]
    )

    title_prefix = "Market Maker's " if mm else ""
    fig.update_layout(
        title=(
            title := (
                f"{title_prefix}{greek.title()} vs. Price and Volatility | "
                f"Strategy: {strategy_name} | Spot: {spot} | Time: {T * 365:.1f} days"
            )
        ),
        meta={"title": title},
        scene={
            "xaxis_title": "Underlying Price",
            "yaxis_title": "Volatility",
            "zaxis_title": greek.title(),
            "xaxis": {
                "backgroundcolor": "rgb(230, 230, 200)",
                "gridcolor": "white",
                "showbackground": True,
                "zerolinecolor": "white",
            },
            "yaxis": {
                "backgroundcolor": "rgb(200, 200, 230)",
                "gridcolor": "white",
                "showbackground": True,
                "zerolinecolor": "white",
            },
            "zaxis": {
                "backgroundcolor": "rgb(230, 200, 230)",
                "gridcolor": "white",
                "showbackground": True,
                "zerolinecolor": "white",
            },
        },
    )
    return fig


if __name__ == "__main__":
    # Example Usage for a collar strategy:
    # Spot is at 5750
    # Long 5565 Put, Short 4700 Put, Short 6165 Call
    spot = 5750

    # Define the collar strategy
    collar_strategy = [
        {"strike": 4700, "quantity": -1, "put_call": "put"},  # Short put
        {"strike": 5565, "quantity": 1, "put_call": "put"},  # Long put
        {"strike": 6165, "quantity": -1, "put_call": "call"},  # Short call
    ]

    # Market Maker's view of Gamma for collar
    fig_gamma_mm = plot_strategy_greek_surface_price_time(
        spot=spot,
        strategy=collar_strategy,
        r=0.01,
        sigma=0.2,
        greek="gamma",
        mm=True,
        time_range=(0.0027, 20 / 365),
    )
    fig_gamma_mm.show()

    # Example of a different strategy (butterfly spread)
    butterfly_strategy = [
        {"strike": 5500, "quantity": 1, "put_call": "call"},  # Long call
        {"strike": 5750, "quantity": -2, "put_call": "call"},  # Short 2 calls
        {"strike": 6000, "quantity": 1, "put_call": "call"},  # Long call
    ]

    # Customer's view of Delta for butterfly
    fig_delta_butterfly = plot_strategy_greek_surface_price_time(
        spot=spot,
        strategy=butterfly_strategy,
        r=0.01,
        sigma=0.2,
        greek="delta",
        mm=False,
        time_range=(0.0027, 30 / 365),
    )
    fig_delta_butterfly.show()

    spot = 5750
    collar_strategy = [
        {"strike": 4700, "quantity": -1, "put_call": "put"},  # Short put
        {"strike": 5565, "quantity": 1, "put_call": "put"},  # Long put
        {"strike": 6165, "quantity": -1, "put_call": "call"},  # Short call
    ]
    fig_gamma_mm = plot_strategy_greek_surface_vol_price(
        spot=spot, strategy=collar_strategy, T=7 / 365, greek="gamma", mm=True
    )
    fig_gamma_mm.show()

    # Example with a different strategy (butterfly spread)
    butterfly_strategy = [
        {"strike": 5500, "quantity": 1, "put_call": "call"},  # Long call
        {"strike": 5750, "quantity": -2, "put_call": "call"},  # Short 2 calls
        {"strike": 6000, "quantity": 1, "put_call": "call"},  # Long call
    ]
    fig_delta_butterfly = plot_strategy_greek_surface_vol_price(
        spot=spot, strategy=butterfly_strategy, T=7 / 365, greek="delta", mm=False
    )
    fig_delta_butterfly.show()

    # Example with custom ranges and more points
    fig_vega = plot_strategy_greek_surface_vol_price(
        spot=spot,
        strategy=butterfly_strategy,
        T=30 / 365,
        greek="vega",
        mm=False,
        price_range=(5000, 6500),
        vol_range=(0.1, 0.4),
        num_prices=150,
        num_vols=120,
        colorscale="plasma",
    )
    fig_vega.show()
