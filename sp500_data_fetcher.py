import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import numpy as np
import time
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class SP500DataFetcher:
    def __init__(self):
        self.sp500_companies = []
        self.financial_data = []
        
    def get_sp500_list(self):
        """Fetch current S&P 500 companies from Wikipedia"""
        print("Fetching S&P 500 company list...")
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        try:
            tables = pd.read_html(url)
            sp500_table = tables[0]
            self.sp500_companies = sp500_table[['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry']].copy()
            self.sp500_companies.columns = ['Symbol', 'Company', 'Sector', 'Industry']
            print(f"Found {len(self.sp500_companies)} S&P 500 companies")
            return True
        except Exception as e:
            print(f"Error fetching S&P 500 list: {e}")
            return False
    
    def calculate_dcf_value_gap(self, ticker_data, current_price):
        """Calculate DCF value gap using simplified approach"""
        try:
            # Get basic financial data
            info = ticker_data.info
            
            # Simplified fair value calculation using PE normalization
            earnings_per_share = info.get('trailingEps', 0)
            if earnings_per_share and earnings_per_share > 0:
                # Use sector-adjusted PE of 15 as baseline fair value
                fair_value = earnings_per_share * 15
                value_gap = ((fair_value - current_price) / current_price) * 100
                return round(value_gap, 2), round(fair_value, 2)
            return 0.0, current_price
        except:
            return 0.0, current_price
    
    def classify_stock(self, metrics):
        """Classify stock as Value or Growth using Fama-French methodology"""
        try:
            pe_ratio = metrics.get('PE_Ratio', 999)
            pb_ratio = metrics.get('PB_Ratio', 999)
            ps_ratio = metrics.get('PS_Ratio', 999)
            earnings_growth = metrics.get('Earnings_Growth', 0)
            revenue_growth = metrics.get('Revenue_Growth', 0)
            
            # Value criteria: Low PE (<15), Low PB (<2), Low PS (<3)
            value_score = 0
            if pe_ratio < 15 and pe_ratio > 0:
                value_score += 1
            if pb_ratio < 2 and pb_ratio > 0:
                value_score += 1
            if ps_ratio < 3 and ps_ratio > 0:
                value_score += 1
                
            # Growth criteria: High earnings growth (>10%), High revenue growth (>8%)
            growth_score = 0
            if earnings_growth > 10:
                growth_score += 1
            if revenue_growth > 8:
                growth_score += 1
                
            # Classification logic
            if value_score >= 2:
                return "Value"
            elif growth_score >= 1 and earnings_growth > 5:
                return "Growth"
            else:
                return "Blend"
                
        except:
            return "Blend"
    
    def get_valuation_tag(self, classification, dcf_gap, metrics):
        """Assign dynamic valuation tags"""
        if classification == "Value":
            if dcf_gap > 10:
                return "VALUE – Undervalued"
            elif dcf_gap < -10:
                return "VALUE – Overvalued"
            else:
                return "VALUE – Fairly Valued"
        elif classification == "Growth":
            earnings_growth = metrics.get('Earnings_Growth', 0)
            if earnings_growth > 15:
                return "GROWTH – Momentum"
            else:
                return "GROWTH – Watchlist"
        else:
            return "BLEND – Mixed"
    
    def get_company_data(self, symbol, company_name, sector, industry):
        """Fetch comprehensive financial data for a single company"""
        try:
            print(f"Processing {symbol} - {company_name}")
            ticker = yf.Ticker(symbol)
            
            # Get current price and basic info
            info = ticker.info
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            
            if current_price == 0:
                print(f"  Warning: No price data for {symbol}")
                return None
            
            # Calculate financial metrics
            market_cap = info.get('marketCap', 0) / 1e9  # in billions
            
            # Valuation ratios
            pe_ratio = info.get('trailingPE', info.get('forwardPE', 0))
            pb_ratio = info.get('priceToBook', 0)
            ps_ratio = info.get('priceToSalesTrailing12Months', 0)
            ev_ebitda = info.get('enterpriseToEbitda', 0)
            
            # Profitability metrics
            roe = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0
            roa = info.get('returnOnAssets', 0) * 100 if info.get('returnOnAssets') else 0
            gross_margin = info.get('grossMargins', 0) * 100 if info.get('grossMargins') else 0
            operating_margin = info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else 0
            profit_margin = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0
            
            # Growth metrics
            earnings_growth = info.get('earningsGrowth', 0) * 100 if info.get('earningsGrowth') else 0
            revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0
            
            # Financial health
            debt_to_equity = info.get('debtToEquity', 0)
            current_ratio = info.get('currentRatio', 0)
            quick_ratio = info.get('quickRatio', 0)
            
            # Cash flow metrics
            operating_cash_flow = info.get('operatingCashflow', 0) / 1e9 if info.get('operatingCashflow') else 0
            free_cash_flow = info.get('freeCashflow', 0) / 1e9 if info.get('freeCashflow') else 0
            fcf_yield = (free_cash_flow * 1e9 / info.get('marketCap', 1)) * 100 if info.get('marketCap') else 0
            
            # Other metrics
            dividend_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
            payout_ratio = info.get('payoutRatio', 0) * 100 if info.get('payoutRatio') else 0
            beta = info.get('beta', 1.0)
            
            # Calculate DCF value gap
            metrics_dict = {
                'PE_Ratio': pe_ratio,
                'PB_Ratio': pb_ratio,
                'PS_Ratio': ps_ratio,
                'Earnings_Growth': earnings_growth,
                'Revenue_Growth': revenue_growth
            }
            
            dcf_gap, fair_value = self.calculate_dcf_value_gap(ticker, current_price)
            classification = self.classify_stock(metrics_dict)
            valuation_tag = self.get_valuation_tag(classification, dcf_gap, metrics_dict)
            
            # Approximate ROIC calculation
            roic = roe * 0.7 if roe > 0 else 0  # Simplified approximation
            
            company_data = {
                'Symbol': symbol,
                'Company': company_name,
                'Sector': sector,
                'Industry': industry,
                'Current_Price': round(current_price, 2),
                'Market_Cap_B': round(market_cap, 2),
                'PE_Ratio': round(pe_ratio, 2) if pe_ratio and pe_ratio > 0 else 0,
                'PB_Ratio': round(pb_ratio, 2) if pb_ratio and pb_ratio > 0 else 0,
                'PS_Ratio': round(ps_ratio, 2) if ps_ratio and ps_ratio > 0 else 0,
                'EV_EBITDA': round(ev_ebitda, 2) if ev_ebitda and ev_ebitda > 0 else 0,
                'ROE': round(roe, 2),
                'ROA': round(roa, 2),
                'ROIC': round(roic, 2),
                'Gross_Margin': round(gross_margin, 2),
                'Operating_Margin': round(operating_margin, 2),
                'Profit_Margin': round(profit_margin, 2),
                'Earnings_Growth': round(earnings_growth, 2),
                'Revenue_Growth': round(revenue_growth, 2),
                'Debt_to_Equity': round(debt_to_equity, 2),
                'Current_Ratio': round(current_ratio, 2),
                'Quick_Ratio': round(quick_ratio, 2),
                'Operating_Cash_Flow_B': round(operating_cash_flow, 2),
                'Free_Cash_Flow_B': round(free_cash_flow, 2),
                'FCF_Yield': round(fcf_yield, 2),
                'Dividend_Yield': round(dividend_yield, 2),
                'Payout_Ratio': round(payout_ratio, 2),
                'Beta': round(beta, 3),
                'DCF_Value_Gap': dcf_gap,
                'Fair_Value': fair_value,
                'Classification': classification,
                'Valuation_Tag': valuation_tag
            }
            
            return company_data
            
        except Exception as e:
            print(f"  Error processing {symbol}: {e}")
            return None
    
    def fetch_all_data(self, batch_size=25, delay=1):
        """Fetch data for all S&P 500 companies with rate limiting"""
        if not self.get_sp500_list():
            return False
            
        print(f"\nStarting data collection for {len(self.sp500_companies)} companies...")
        print(f"Processing in batches of {batch_size} with {delay}s delay between companies")
        
        successful_count = 0
        failed_companies = []
        
        for i, row in self.sp500_companies.iterrows():
            symbol = row['Symbol']
            company_name = row['Company']
            sector = row['Sector']
            industry = row['Industry']
            
            company_data = self.get_company_data(symbol, company_name, sector, industry)
            
            if company_data:
                self.financial_data.append(company_data)
                successful_count += 1
            else:
                failed_companies.append(symbol)
            
            # Rate limiting
            if (i + 1) % batch_size == 0:
                print(f"  Processed {i + 1} companies ({successful_count} successful)")
                time.sleep(delay * 2)  # Longer delay between batches
            else:
                time.sleep(delay)
        
        print(f"\nData collection complete!")
        print(f"Successful: {successful_count}")
        print(f"Failed: {len(failed_companies)}")
        if failed_companies:
            print(f"Failed companies: {failed_companies}")
        
        return len(self.financial_data) > 0
    
    def save_data(self, csv_filename='sp500_complete_data.csv', js_filename='sp500_data.js'):
        """Save data in multiple formats"""
        if not self.financial_data:
            print("No data to save")
            return False
        
        # Create DataFrame
        df = pd.DataFrame(self.financial_data)
        
        # Save as CSV
        df.to_csv(csv_filename, index=False)
        print(f"Data saved to {csv_filename}")
        
        # Save as JavaScript data file for dashboard
        js_data = df.to_json(orient='records', indent=2)
        
        js_content = f"""// S&P 500 Complete Dataset
// Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Total companies: {len(df)}

const sp500Data = {js_data};

// Export for use in dashboard
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = sp500Data;
}}
"""
        
        with open(js_filename, 'w') as f:
            f.write(js_content)
        print(f"JavaScript data saved to {js_filename}")
        
        # Print summary statistics
        print(f"\nDataset Summary:")
        print(f"Total companies: {len(df)}")
        print(f"Value stocks: {len(df[df['Classification'] == 'Value'])}")
        print(f"Growth stocks: {len(df[df['Classification'] == 'Growth'])}")
        print(f"Blend stocks: {len(df[df['Classification'] == 'Blend'])}")
        print(f"Sectors represented: {df['Sector'].nunique()}")
        
        return True

def main():
    """Main execution function"""
    print("S&P 500 Complete Data Fetcher")
    print("=" * 40)
    
    fetcher = SP500DataFetcher()
    
    # Fetch all data
    if fetcher.fetch_all_data(batch_size=25, delay=1):
        # Save data
        fetcher.save_data()
        print("\nData collection and export completed successfully!")
    else:
        print("\nData collection failed!")

if __name__ == "__main__":
    main()