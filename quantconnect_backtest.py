# region imports
from AlgorithmImports import *
import pandas as pd
from cvxopt import matrix, solvers
import numpy as np
# endregion

class LSGlobalMacro(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2017, 3, 1)
        self.set_end_date(2024, 3, 1)
        self.set_cash(1000000)
        # self.set_warm_up(120)

        # Set Brokerage:
        self.set_brokerage_model(BrokerageName.ALPHA_STREAMS)
        # self.set_brokerage_model(BrokerageName.QUANTCONNECT_BROKERAGE) # Defaults to margin account
        # self.set_brokerage_model(BrokerageName.TD_AMERITRADE, AccountType.MARGIN)
        # self.set_brokerage_message_handler(MyBrokerageModel())
        # security.set_buying_power_model(MyBuyingPowerModel())

        # Process Symbols
        self.symbols = []
        self.etfs = ["SPY", "FXE", "EWJ", "GLD", "QQQ", "SHV", "DBA", "USO", "XBI", "ILF", "EPP", "FEZ"]
        for i in range(len(self.etfs)):
            # self.symbols.append(self.add_equity(self.etfs[i],Resolution.DAILY).symbol)
            self.add_equity(self.etfs[i],Resolution.DAILY, leverage=10)
            # self.symbols.append(Symbol.create(self.etfs[i], SecurityType.EQUITY, Market.USA))

        # Set Benchmark
        self.spy = self.add_equity("SPY", Resolution.DAILY).symbol
        self.set_benchmark(self.spy)

        # Set leverage
        self.universe_settings.leverage = 10

        # Set Manual Universe
        # self.add_universe_selection(ManualUniverseSelectionModel(self.symbols))

        # Set Portfolio Construction
        # self.set_portfolio_construction(EqualWeightingPortfolioConstructionModel())

        # Set Execution
        self.set_execution(ImmediateExecutionModel())

        # Set Strategy Params
        self.target_beta = 1
        self.look_back = 120

        self.schedule.on(
            self.date_rules.week_start(),
            self.time_rules.after_market_open("SPY"),
            self.rebalance)

    def rebalance(self) -> None:
        qb = self

        history = qb.history(qb.securities.keys(), self.look_back+1, Resolution.DAILY)
        spy_history = qb.history(self.spy, self.look_back+1, Resolution.DAILY)

        if history.empty: return

        rets = history['close'].unstack(level=0).pct_change().iloc[1:]
        spy_rets = spy_history['close'].unstack(level=0).pct_change().iloc[1:].squeeze()
        
        cov_matrix_annualized = rets.cov() * 252
        expected_returns_annualized = rets.mean() * 252

        # Estimate the betas
        n = len(rets.columns)
        betas = {}
        market_variance = np.var(spy_rets)
        for asset in rets.columns:
                cov_i = rets[asset].cov(spy_rets)
                beta_pi = cov_i / market_variance
                betas[asset] = beta_pi
        betas = pd.Series(betas).astype(float)
        target_beta = self.target_beta
        
        reg_factor = 1e-6
        P = matrix(cov_matrix_annualized.values + reg_factor * np.eye(n))
        q = matrix(-expected_returns_annualized.values)
        G = matrix(np.vstack((-np.eye(n), np.eye(n))))
        h = matrix(np.hstack((0.5 * np.ones(n), 0.5 * np.ones(n))))
        A = matrix(np.vstack((np.ones(n), betas.values)), tc='d')
        b = matrix([1, target_beta], (2, 1), tc='d')

        sol = solvers.qp(P, q, G, h, A, b)
        optimal_weights = pd.Series(sol['x'], index=rets.columns)

        # self.debug(f"Optimal Weights {optimal_weights}")
        self.debug(f"Prev Trading date: {rets.index[-1]}")
        for asset, weight in optimal_weights.items():
            self.debug(f"Target Weight of {asset}: {weight:4f}")

        portfolio_targets = []
        for asset, weight in optimal_weights.items():
            portfolio_targets.append(PortfolioTarget(asset, weight))

        self.liquidate(tag = "Liquidated")
        self.set_holdings(portfolio_targets, True)