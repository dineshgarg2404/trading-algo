import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from backtester import Backtester
from strategy.survivor_backtest import SurvivorBacktestStrategy
from data_manager import DataManager

class BacktesterGUI(tk.Tk):
    """
    Graphical User Interface for the backtesting tool.

    This class provides a user-friendly interface for running backtests and viewing
    performance results. It allows users to configure backtesting parameters,
    initiate a backtest, and visualize the portfolio performance over time.

    GUI COMPONENTS:
    ==============

    1. **Configuration Panel**:
       - Input fields for setting backtesting parameters such as initial capital,
         and strategy-specific settings.

    2. **Control Buttons**:
       - "Run Backtest" button to start the simulation.
       - "Quit" button to exit the application.

    3. **Results Display**:
       - A chart to visualize the portfolio value over the backtest period.
       - A text area to display performance metrics.

    WORKFLOW:
    =========

    1. **Initialization**:
       - The GUI is launched, and default backtesting parameters are displayed.

    2. **Configuration**:
       - The user can modify the parameters in the configuration panel.

    3. **Run Backtest**:
       - When the "Run Backtest" button is clicked, the GUI:
         - Initializes the `DataManager` to get historical data.
         - Initializes the `Backtester` with the `SurvivorBacktestStrategy`.
         - Runs the backtest.
         - Displays the performance chart and metrics.
    """

    def __init__(self):
        super().__init__()
        self.title("NIFTY Options Backtester")

        self._create_widgets()

    def _create_widgets(self):
        """
        Create and arrange the GUI widgets.
        """
        # Configuration Frame
        config_frame = ttk.LabelFrame(self, text="Configuration")
        config_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # Initial Capital
        ttk.Label(config_frame, text="Initial Capital:").pack(pady=5)
        self.initial_capital = tk.StringVar(value="100000")
        ttk.Entry(config_frame, textvariable=self.initial_capital).pack()

        # Run Button
        run_button = ttk.Button(config_frame, text="Run Backtest", command=self._run_backtest)
        run_button.pack(pady=20)

        # Results Frame
        results_frame = ttk.LabelFrame(self, text="Results")
        results_frame.pack(side=tk.RIGHT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Performance Chart
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=results_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Performance Metrics
        self.metrics_text = tk.Text(results_frame, height=4)
        self.metrics_text.pack(side=tk.BOTTOM, fill=tk.X)

    def _run_backtest(self):
        """
        Run the backtest and display the results.
        """
        initial_capital = float(self.initial_capital.get())

        # Get historical data
        data_manager = DataManager()
        data = data_manager.get_historical_data()

        # Run the backtest
        backtester = Backtester(SurvivorBacktestStrategy, data, initial_capital)
        backtester.run()

        # Get performance report
        report = backtester.generate_performance_report()

        # Display results
        self._plot_performance(report)
        self._display_metrics(backtester)

    def _plot_performance(self, report):
        """
        Plot the portfolio value over time.
        """
        self.ax.clear()
        report['portfolio_value'].plot(ax=self.ax)
        self.ax.set_title("Portfolio Value Over Time")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Portfolio Value")
        self.canvas.draw()

    def _display_metrics(self, backtester):
        """
        Display the performance metrics.
        """
        total_return = (backtester.portfolio_value / backtester.initial_capital - 1) * 100

        metrics = (
            f"Initial Capital: {backtester.initial_capital}\n"
            f"Final Portfolio Value: {backtester.portfolio_value:.2f}\n"
            f"Total Return: {total_return:.2f}%"
        )

        self.metrics_text.delete(1.0, tk.END)
        self.metrics_text.insert(tk.END, metrics)

if __name__ == '__main__':
    app = BacktesterGUI()
    app.mainloop()
