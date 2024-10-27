# Import necessary libraries
import numpy as np
import pandas as pd

class PnLCalculator:
    
    def __init__(self, trades, positions, market_data, funding_rate, greek_sensitivities):
        """
        Initialize the PnLCalculator with necessary data.
        
        trades: pd.DataFrame with columns ['buy_price', 'sell_price', 'quantity', 'transaction_cost']
        positions: pd.DataFrame with columns ['quantity', 'price_change', 'notional']
        market_data: pd.DataFrame with columns ['current_price', 'previous_price', 'model_price', 'previous_model_price']
        funding_rate: float representing the funding cost rate
        greek_sensitivities: dict with keys ['delta', 'gamma', 'vega'] representing sensitivities
        """
        self.trades = trades
        self.positions = positions
        self.market_data = market_data
        self.funding_rate = funding_rate
        self.greeks = greek_sensitivities
        
    def clean_pnl(self):
        """Calculate Clean PnL"""
        clean_pnl = ((self.trades['sell_price'] - self.trades['buy_price']) * 
                     self.trades['quantity'] - self.trades['transaction_cost']).sum()
        return clean_pnl
    
    def hypothetical_pnl(self):
        """Calculate Hypothetical PnL"""
        hypothetical_pnl = (self.positions['price_change'] * 
                            self.positions['quantity']).sum()
        return hypothetical_pnl
    
    def books_pnl(self):
        """Calculate Books PnL"""
        books_pnl = (self.positions['price_change'] * 
                     self.positions['quantity']).sum()
        # Add any necessary book-specific adjustments here
        return books_pnl
    
    def gl_pnl(self, fx_revaluation=0, provisions=0):
        """Calculate General Ledger PnL"""
        gl_pnl = self.books_pnl() + fx_revaluation + provisions
        return gl_pnl
    
    def volcker_pnl(self, market_making_pnl, hedging_pnl, proprietary_pnl):
        """Calculate Volcker PnL"""
        volcker_pnl = market_making_pnl + hedging_pnl - proprietary_pnl
        return volcker_pnl
    
    def finance_pnl(self, overhead_costs, capital_charges, allocations):
        """Calculate Finance PnL"""
        total_trading_pnl = self.clean_pnl() + self.hypothetical_pnl()
        finance_pnl = total_trading_pnl + overhead_costs + capital_charges + allocations
        return finance_pnl
    
    def funding_cost_pnl(self):
        """Calculate Funding Cost PnL"""
        funding_cost_pnl = (self.funding_rate * self.positions['notional']).sum()
        return funding_cost_pnl
    
    def greek_pnl(self, price_change, volatility_change):
        """Calculate Greek PnL (Delta, Gamma, Vega)"""
        delta_pnl = self.greeks['delta'] * price_change
        gamma_pnl = 0.5 * self.greeks['gamma'] * (price_change ** 2)
        vega_pnl = self.greeks['vega'] * volatility_change
        greek_pnl = delta_pnl + gamma_pnl + vega_pnl
        return greek_pnl
    
    def carry_pnl(self, interest_rate_diff, holding_period):
        """Calculate Carry PnL"""
        carry_pnl = (interest_rate_diff * self.positions['notional'] * holding_period).sum()
        return carry_pnl
    
    def cash_flow_pnl(self, cash_inflows, cash_outflows):
        """Calculate Cash Flow PnL"""
        cash_flow_pnl = sum(cash_inflows) - sum(cash_outflows)
        return cash_flow_pnl
    
    def mark_to_market_pnl(self):
        """Calculate Mark-to-Market PnL"""
        mtm_pnl = ((self.market_data['current_price'] - 
                    self.market_data['previous_price']) * 
                   self.positions['quantity']).sum()
        return mtm_pnl
    
    def mark_to_model_pnl(self):
        """Calculate Mark-to-Model PnL"""
        mark_to_model_pnl = ((self.market_data['model_price'] - 
                              self.market_data['previous_model_price']) * 
                             self.positions['quantity']).sum()
        return mark_to_model_pnl
    
    def aggregate_greeks_pnl(self, price_change, volatility_change):
        """Calculate Aggregate Greeks PnL using Delta, Gamma, Vega"""
        delta_pnl = self.greeks['delta'] * price_change
        gamma_pnl = 0.5 * self.greeks['gamma'] * (price_change ** 2)
        vega_pnl = self.greeks['vega'] * volatility_change
        greeks_pnl = delta_pnl + gamma_pnl + vega_pnl
        return greeks_pnl

# Example Usage:

# Sample data
trades = pd.DataFrame({
    'buy_price': [100, 105],
    'sell_price': [110, 108],
    'quantity': [10, 5],
    'transaction_cost': [1, 1]
})

positions = pd.DataFrame({
    'quantity': [10, 15],
    'price_change': [0.5, -0.2],
    'notional': [1000, 2000]
})

market_data = pd.DataFrame({
    'current_price': [110, 108],
    'previous_price': [105, 107],
    'model_price': [109, 107],
    'previous_model_price': [104, 106]
})

funding_rate = 0.02
greek_sensitivities = {'delta': 1.2, 'gamma': 0.5, 'vega': 0.3}

# Initialize the PnLCalculator
pnl_calc = PnLCalculator(trades, positions, market_data, funding_rate, greek_sensitivities)

# Calculate different PnLs
print("Clean PnL:", pnl_calc.clean_pnl())
print("Hypothetical PnL:", pnl_calc.hypothetical_pnl())
print("Books PnL:", pnl_calc.books_pnl())
print("GL PnL:", pnl_calc.gl_pnl(fx_revaluation=100, provisions=50))
print("Volcker PnL:", pnl_calc.volcker_pnl(market_making_pnl=200, hedging_pnl=150, proprietary_pnl=50))
print("Finance PnL:", pnl_calc.finance_pnl(overhead_costs=100, capital_charges=50, allocations=20))
print("Funding Cost PnL:", pnl_calc.funding_cost_pnl())
print("Greek PnL:", pnl_calc.greek_pnl(price_change=2, volatility_change=0.1))
print("Carry PnL:", pnl_calc.carry_pnl(interest_rate_diff=0.01, holding_period=30))
print("Cash Flow PnL:", pnl_calc.cash_flow_pnl(cash_inflows=[100, 200], cash_outflows=[50, 30]))
print("Mark-to-Market PnL:", pnl_calc.mark_to_market_pnl())
print("Mark-to-Model PnL:", pnl_calc.mark_to_model_pnl())
print("Aggregate Greeks PnL:", pnl_calc.aggregate_greeks_pnl(price_change=2, volatility_change=0.1))
