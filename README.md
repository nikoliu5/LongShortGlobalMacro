# Global Macro Long/Short Strategy with Target Beta
This project implements and analyzes a Global Macro Long/Short strategy based on portfolio optimization with a target beta. The strategy aims to understand the impact of different target betas and the length of the look-back period used for estimating the covariance matrix and expected returns on the portfolio's performance and risk characteristics.

## Investment Strategy

The strategy optimizes a portfolio of 12 ETFs, representing various asset classes and geographies, using a quadratic solver in Python.

The optimization problem is set up with an objective function that minimizes risk while targeting a specific portfolio beta. The portfolio is subject to holding constraints, limiting the weight of each asset between -0.5 and 0.5.

The strategy is backtested over the period from March 2017 to February 2024, with weekly rebalancing. Four different look-back periods (30, 60, 90 and 120 data points) are used to estimate the covariance matrix and expected returns, and two target beta values (0 and 1) are considered. This results in a total of six scenarios to be analyzed.

Optimize a portfolio using the following structure:

- **Objective**: Minimize quadratic function 
  $$
  \frac{1}{2} \omega^T \Sigma \omega - \rho^T \omega
  $$

- **Constraints**: 
  $$
  \beta_p^T \omega = \beta_T
  $$
  $$
  \sum_{i=1}^{n} \omega_i = 1
  $$
  $$
  -0.5 \leq \omega_i \leq 0.5
  $$

- **Inputs**:
  - \( \Sigma \): Sample covariance matrix of returns
  - \( \rho \): Vector of expected returns
  - \( \beta_p \): Portfolio beta relative to S&P 500 (SPY ETF)
  - \( \beta_T \): Target beta (e.g., 0 or 1)

## Assumptions and Analysis Setup

1. **Weekly Rebalancing**: Portfolio is re-optimized every week from March 2017 to February 2024.
2. **Look-back Periods**:
   - Long-Term: 120 data points
   - Medium-Term: 90 data points
   - Medium-Short Term: 60 data points
   - Short-Term: 30 data points
3. **Target Beta Values**: 0 and 1

## Data and Tools
The strategy uses historical data for 12 ETFs, downloaded from Yahoo Finance using Python. The daily returns are calculated and annualized for the analysis. The optimization problem is solved using the CVXOPT quadratic solver in Python.

1. CurrencyShares Euro Trust (FXE)
2. iShares MSCI Japan Index (EWJ)
3. SPDR GOLD Trust (GLD)
4. Powershares NASDAQ-100 Trust (QQQ)
5. SPDR S&P 500 (SPY)
6. iShares Lehman Short Treasury Bond (SHV)
7. PowerShares DB Agriculture Fund (DBA)
8. United States Oil Fund LP (USO)
9. SPDR S&P Biotech (XBI)
10. iShares S&P Latin America 40 Index (ILF)
11. iShares MSCI Pacific ex-Japan Index Fund (EPP)
12. SPDR DJ Euro Stoxx 50 (FEZ)


## Backtesting Results

[PlaceHolder]

## QuantConnect Results

[PlaceHolder]

## Performance and Risk Analysis

The performance and risk of the strategy are evaluated using various metrics, including cumulative return, daily mean return, maximum drawdown, Sharpe ratio, volatility, skewness, kurtosis, Value at Risk (VaR), and Conditional Value at Risk (CVaR). 

The analysis focuses on understanding the sensitivity of the strategy to the choice of target beta and the length of the look-back period used for estimating the covariance matrix and expected returns. 

This strategy explores the sensitivity of a Global Macro Long/Short portfolio to target beta and look-back periods, providing insights into the impact of these factors on the portfolio's performance and risk characteristics.