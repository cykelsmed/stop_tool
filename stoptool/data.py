"""Data loading and fetching utilities for Stoptool."""


class PortfolioPosition:
    """Placeholder data class for a portfolio position."""

    def __init__(self, *args, **kwargs):  # pragma: no cover - placeholder
        self.args = args
        self.kwargs = kwargs


def load_portfolio(path):  # pragma: no cover - placeholder
    """Load the portfolio from the provided path.

    Step 2 will implement this function.
    """
    raise NotImplementedError("load_portfolio will be implemented in step 2")


def fetch_history(symbol, days=252):  # pragma: no cover - placeholder
    """Fetch historical market data for a symbol.

    Step 3 will implement this function.
    """
    raise NotImplementedError("fetch_history will be implemented in step 3")
