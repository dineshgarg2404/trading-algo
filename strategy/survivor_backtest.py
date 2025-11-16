import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategy.survivor import SurvivorStrategy
from logger import logger

class SurvivorBacktestStrategy(SurvivorStrategy):
    """
    Survivor Options Trading Strategy adapted for backtesting.

    This class inherits from the original `SurvivorStrategy` and overrides methods
    that interact with a live broker. Instead of making live API calls, it uses the
    simulated broker provided by the backtesting engine.

    KEY MODIFICATIONS:
    ==================

    1. **Broker Interface**:
       - All calls to `self.broker` are now directed to the simulated broker
         in the backtesting engine.

    2. **Order Placement**:
       - `_place_order` now calls the backtester's `place_order` method, which
         simulates the trade instead of executing it live.

    3. **Data Retrieval**:
       - `_nifty_quote` and other data-related methods are adapted to use
         historical data provided by the backtester.

    4. **Initialization**:
       - The `__init__` method is simplified to work without a live broker connection.
    """

    def __init__(self, broker, config, order_manager):
        """
        Initialize the backtesting strategy.

        This method sets up the strategy for a backtesting environment.
        """
        # Assign config values from parent __init__
        for k, v in config.items():
            setattr(self, f'strat_var_{k}', v)

        # Assign dependencies from parent __init__
        self.broker = broker
        self.symbol_initials = self.strat_var_symbol_initials
        self.order_manager = order_manager

        # Backtest-specific initializations
        self.instruments = None
        self.strike_difference = 50  # Assume a fixed strike difference

        # Call the state initializer
        self._initialize_state()

    def _nifty_quote(self):
        """
        Get the current NIFTY quote from the backtesting engine.

        This method is not used in the backtest, as the price is passed directly
        to `on_ticks_update`.
        """
        pass

    def _initialize_state(self):
        """
        Initialize the strategy's state for the backtest.

        This method is simplified to work without a live quote.
        """
        self.pe_reset_gap_flag = 0
        self.ce_reset_gap_flag = 0

        # Use a starting price from the historical data
        self.nifty_pe_last_value = 24500
        self.nifty_ce_last_value = 24500

        logger.info(f"Nifty PE Start Value: {self.nifty_pe_last_value}, "
                   f"Nifty CE Start Value: {self.nifty_ce_last_value}")

    def _get_strike_difference(self, symbol_initials):
        """
        Return a fixed strike difference for backtesting.
        """
        return self.strike_difference

    def _find_nifty_symbol_from_gap(self, option_type, ltp, gap):
        """
        Find a suitable option symbol for backtesting.

        This method returns a dummy instrument for the backtest.
        """
        target_strike = ltp + (gap if option_type == 'CE' else -gap)
        return {
            'tradingsymbol': f'NIFTY{option_type}{target_strike}',
            'strike': target_strike
        }

    def _place_order(self, symbol, quantity):
        """
        Place a simulated order through the backtesting engine.
        """
        self.broker.place_order(
            symbol,
            quantity,
            price=20,  # Assume a fixed price for simplicity
            transaction_type=self.strat_var_trans_type,
            order_type=self.strat_var_order_type
        )
