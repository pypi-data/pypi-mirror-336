import time
import optionvisualizer_wrapper as ovw
import plotly.graph_objects as go
import numpy as np
from typing import Literal, TypedDict, List, Union, Tuple


class Leg(TypedDict):
    strike: float
    quantity: int  # Positive for long, negative for short
    put_call: Literal["put", "call"]


def plot_gamma_projection(
    spot: Union[float, int],
    strategy: List[Leg],
    r: float = 0.01,
    sigma: float = 0.2,
    time_range: Tuple[float, float] = (0.0027, 7 / 365),
    num_times: int = 100,
    price_range: Tuple[float, float] | None = None,
    num_prices: int = 100,
    mm: bool = False,
) -> go.Figure:
    """
    Projects the peak, trough, and zero Gamma values of an option strategy
    onto a 2D plane, with time on the x-axis and spot price on the y-axis.

    Args:
        spot: Current price of the underlying asset.
        strategy: List of option legs (strike, quantity, put/call).
        r: Interest rate.
        sigma: Volatility.
        time_range: Tuple (min_time, max_time) in years.
        num_times: Number of time points for the x-axis.
        price_range: Price range. If None, calculates from the strategy
        num_prices: Number of prices, used internally.
        mm: Market maker (True) or customer (False) view.

    Returns:
        go.Figure: Plotly figure object.
    """
    wrapper = ovw.OptionVisualizerWrapper()

    times = np.linspace(time_range[0], time_range[1], num_times)

    # Use the same method as in the surface plotting function to determine price range
    if price_range is None:
        strikes = [leg["strike"] for leg in strategy]
        min_strike = min(strikes)
        max_strike = max(strikes)
        # Set price range to be 30% below lowest strike and 30% above highest strike
        price_range = (
            min(spot * 0.7, min_strike * 0.7),
            max(spot * 1.3, max_strike * 1.3),
        )
    prices = np.linspace(price_range[0], price_range[1], num_prices)
    price_grid, time_grid = np.meshgrid(prices, times)
    # Store results.  Lists, because we might have multiple crossings.
    zero_crossings = []
    peak_crossings = []  # (time, price)
    trough_crossings = []  # (time, price)

    for t_idx, t in enumerate(times):
        gamma_values_at_t = []
        for p_idx, p in enumerate(prices):
            net_gamma = 0
            for leg in strategy:
                leg_gamma = wrapper.sensitivities(
                    greek="gamma",
                    S=p,
                    K=leg["strike"],
                    T=t,
                    r=r,
                    sigma=sigma,
                    option=leg["put_call"],
                )
                net_gamma += leg_gamma * leg["quantity"]
            gamma_values_at_t.append(
                -net_gamma if mm else net_gamma
            )  # Apply MM and store

        # Find zero crossings.  Check for sign changes.
        gamma_values_at_t = np.array(gamma_values_at_t)

        # Find zero crossings (improved to handle multiple crossings)
        zero_crossings_indices = np.where(np.diff(np.sign(gamma_values_at_t)))[0]
        for idx in zero_crossings_indices:
            # Linear interpolation for better accuracy
            p1 = prices[idx]
            p2 = prices[idx + 1]
            g1 = gamma_values_at_t[idx]
            g2 = gamma_values_at_t[idx + 1]
            crossing_price = p1 + (p2 - p1) * (0 - g1) / (g2 - g1)
            zero_crossings.append((t * 365, crossing_price))  # Days for plotting

        # Find Peaks (local maxima)
        peak_indices = (
            np.where((np.diff(np.sign(np.diff(gamma_values_at_t))) < 0))[0] + 1
        )
        for idx in peak_indices:
            # Linear interpolation for better accuracy
            p1 = prices[idx - 1]
            p2 = prices[idx]
            p3 = prices[idx + 1]

            g1 = gamma_values_at_t[idx - 1]
            g2 = gamma_values_at_t[idx]  # gamma value at the peak.
            g3 = gamma_values_at_t[idx + 1]

            # https://en.wikipedia.org/wiki/Quadratic_interpolation
            y_predicted = g2 - 0.25 * (g3 - g1) * (g1 - g3) / (g1 - 2 * g2 + g3)
            x_predicted = p2 - 0.5 * (p3 - p1) * (g1 - g3) / (g1 - 2 * g2 + g3)

            peak_crossings.append((t * 365, x_predicted))

        # Find Troughs (local minima)
        trough_indices = (
            np.where((np.diff(np.sign(np.diff(gamma_values_at_t))) > 0))[0] + 1
        )
        for idx in trough_indices:
            p1 = prices[idx - 1]
            p2 = prices[idx]
            p3 = prices[idx + 1]

            g1 = gamma_values_at_t[idx - 1]
            g2 = gamma_values_at_t[idx]  # gamma value at the peak.
            g3 = gamma_values_at_t[idx + 1]
            # https://en.wikipedia.org/wiki/Quadratic_interpolation
            y_predicted = g2 - 0.25 * (g3 - g1) * (g1 - g3) / (g1 - 2 * g2 + g3)
            x_predicted = p2 - 0.5 * (p3 - p1) * (g1 - g3) / (g1 - 2 * g2 + g3)
            trough_crossings.append((t * 365, x_predicted))  # Days for plotting

    # Create Plotly figure
    fig = go.Figure()

    # Add zero crossings as a scatter plot
    if zero_crossings:  # Only add if there are crossings
        zero_times, zero_prices = zip(*zero_crossings)  # Unzip for plotting
        fig.add_trace(
            go.Scatter(
                x=zero_times,
                y=zero_prices,
                mode="lines",
                name="Zero Gamma",
                line=dict(color="blue"),
            )
        )

    # Add peak crossings
    if peak_crossings:
        peak_times, peak_prices = zip(*peak_crossings)
        fig.add_trace(
            go.Scatter(
                x=peak_times,
                y=peak_prices,
                mode="lines",
                name="Gamma Peak",
                line=dict(color="green"),
            )
        )

    # Add trough crossings
    if trough_crossings:
        trough_times, trough_prices = zip(*trough_crossings)
        fig.add_trace(
            go.Scatter(
                x=trough_times,
                y=trough_prices,
                mode="lines",
                name="Gamma Trough",
                line=dict(color="yellow"),
            )
        )
    # Generate a strategy name based on the legs for the legend
    strategy_name = ""
    for i, leg in enumerate(strategy):
        prefix = "+" if leg["quantity"] > 0 else ""
        strategy_name += (
            f"{prefix}{leg['quantity']} {leg['put_call'].upper()} {leg['strike']}"
        )
        if i < len(strategy) - 1:
            strategy_name += ", "

    # Add vertical line at the current spot price
    fig.add_vline(x=min(times) * 365, line_width=1, line_dash="dash", line_color="gray")

    fig.update_layout(
        title=f"Gamma Extrema Projection | Strategy: {strategy_name} | Spot: {spot}",
        xaxis_title="Time to Expiration (Days)",
        yaxis_title="Underlying Price",
        legend=dict(x=0, y=1, traceorder="normal"),
        template="plotly_dark",
    )

    return fig


if __name__ == "__main__":
    # Example Usage:
    spot = 5750
    collar_strategy = [
        {"strike": 4700, "quantity": -1, "put_call": "put"},
        {"strike": 5565, "quantity": 1, "put_call": "put"},
        {"strike": 6165, "quantity": -1, "put_call": "call"},
    ]

    fig = plot_gamma_projection(
        spot=spot,
        strategy=collar_strategy,
        r=0.01,
        sigma=0.2,
        time_range=(0.0027, 25 / 365),
        mm=False,  # Customer view
        num_times=200,
        num_prices=200,
    )
    fig.show()

    # ButterFly example
    butterfly_strategy = [
        {"strike": 5500, "quantity": 1, "put_call": "call"},  # Long call
        {"strike": 5750, "quantity": -2, "put_call": "call"},  # Short 2 calls
        {"strike": 6000, "quantity": 1, "put_call": "call"},  # Long call
    ]
    fig_butterfly = plot_gamma_projection(
        spot=spot,
        strategy=butterfly_strategy,
        r=0.01,
        sigma=0.2,
        time_range=(0.0027, 25 / 365),
        num_times=200,
        num_prices=200,
    )
    fig_butterfly.show()
