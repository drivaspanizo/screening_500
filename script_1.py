# Create S&P 500 sample data for dashboard testing
import pandas as pd
import numpy as np
import random
import json
from datetime import datetime

# Create sample data generator for S&P 500 companies
def create_sample_data(num_companies=100):
    # S&P 500 sectors
    sectors = [
        "Information Technology", "Health Care", "Financials", "Consumer Discretionary",
        "Communication Services", "Industrials", "Consumer Staples", "Energy", 
        "Utilities", "Real Estate", "Materials"
    ]
    
    # Sample companies from each sector (using real S&P 500 companies)
    sample_companies = {
        "Information Technology": ["AAPL", "MSFT", "NVDA", "ADBE", "ORCL", "CRM", "CSCO", "INTC", "AMD", "PYPL"],
        "Health Care": ["JNJ", "PFE", "MRK", "UNH", "ABT", "LLY", "TMO", "AMGN", "BMY", "GILD"],
        "Financials": ["JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "AXP", "V", "MA"],
        "Consumer Discretionary": ["AMZN", "TSLA", "HD", "MCD", "NKE", "SBUX", "TGT", "LOW", "BKNG", "MAR"],
        "Communication Services": ["GOOGL", "META", "NFLX", "DIS", "CMCSA", "VZ", "T", "TMUS", "EA", "ATVI"],
        "Industrials": ["HON", "UNP", "UPS", "CAT", "GE", "MMM", "BA", "LMT", "RTX", "DE"],
        "Consumer Staples": ["PG", "KO", "PEP", "WMT", "COST", "PM", "MO", "EL", "CL", "KMB"],
        "Energy": ["XOM", "CVX", "COP", "EOG", "SLB", "PSX", "VLO", "OXY", "MPC", "KMI"],
        "Utilities": ["NEE", "DUK", "SO", "D", "AEP", "XEL", "ED", "EXC", "SRE", "PCG"],
        "Real Estate": ["AMT", "PLD", "CCI", "EQIX", "PSA", "O", "WELL", "DLR", "SPG", "SBAC"],
        "Materials": ["LIN", "ECL", "SHW", "APD", "FCX", "NEM", "NUE", "DD", "DOW", "VMC"]
    }
    
    # Company full names
    company_names = {
        "AAPL": "Apple Inc.", "MSFT": "Microsoft Corp.", "NVDA": "NVIDIA Corp.", "ADBE": "Adobe Inc.",
        "ORCL": "Oracle Corp.", "CRM": "Salesforce Inc.", "CSCO": "Cisco Systems Inc.", "INTC": "Intel Corp.",
        "AMD": "Advanced Micro Devices Inc.", "PYPL": "PayPal Holdings Inc.",
        "JNJ": "Johnson & Johnson", "PFE": "Pfizer Inc.", "MRK": "Merck & Co Inc.", "UNH": "UnitedHealth Group Inc.",
        "ABT": "Abbott Laboratories", "LLY": "Eli Lilly and Co.", "TMO": "Thermo Fisher Scientific Inc.",
        "AMGN": "Amgen Inc.", "BMY": "Bristol-Myers Squibb Co.", "GILD": "Gilead Sciences Inc.",
        "JPM": "JPMorgan Chase & Co.", "BAC": "Bank of America Corp.", "WFC": "Wells Fargo & Co.",
        "C": "Citigroup Inc.", "GS": "Goldman Sachs Group Inc.", "MS": "Morgan Stanley", "BLK": "BlackRock Inc.",
        "AXP": "American Express Co.", "V": "Visa Inc.", "MA": "Mastercard Inc.",
        "AMZN": "Amazon.com Inc.", "TSLA": "Tesla Inc.", "HD": "Home Depot Inc.", "MCD": "McDonald's Corp.",
        "NKE": "Nike Inc.", "SBUX": "Starbucks Corp.", "TGT": "Target Corp.", "LOW": "Lowe's Cos. Inc.",
        "BKNG": "Booking Holdings Inc.", "MAR": "Marriott International Inc.",
        "GOOGL": "Alphabet Inc. Class A", "META": "Meta Platforms Inc.", "NFLX": "Netflix Inc.",
        "DIS": "Walt Disney Co.", "CMCSA": "Comcast Corp.", "VZ": "Verizon Communications Inc.",
        "T": "AT&T Inc.", "TMUS": "T-Mobile US Inc.", "EA": "Electronic Arts Inc.", "ATVI": "Activision Blizzard Inc.",
        "HON": "Honeywell International Inc.", "UNP": "Union Pacific Corp.", "UPS": "United Parcel Service Inc.",
        "CAT": "Caterpillar Inc.", "GE": "General Electric Co.", "MMM": "3M Co.", "BA": "Boeing Co.",
        "LMT": "Lockheed Martin Corp.", "RTX": "Raytheon Technologies Corp.", "DE": "Deere & Co.",
        "PG": "Procter & Gamble Co.", "KO": "Coca-Cola Co.", "PEP": "PepsiCo Inc.", "WMT": "Walmart Inc.",
        "COST": "Costco Wholesale Corp.", "PM": "Philip Morris International Inc.", "MO": "Altria Group Inc.",
        "EL": "Estee Lauder Cos. Inc.", "CL": "Colgate-Palmolive Co.", "KMB": "Kimberly-Clark Corp.",
        "XOM": "Exxon Mobil Corp.", "CVX": "Chevron Corp.", "COP": "ConocoPhillips", "EOG": "EOG Resources Inc.",
        "SLB": "Schlumberger NV", "PSX": "Phillips 66", "VLO": "Valero Energy Corp.", "OXY": "Occidental Petroleum Corp.",
        "MPC": "Marathon Petroleum Corp.", "KMI": "Kinder Morgan Inc.",
        "NEE": "NextEra Energy Inc.", "DUK": "Duke Energy Corp.", "SO": "Southern Co.", "D": "Dominion Energy Inc.",
        "AEP": "American Electric Power Co. Inc.", "XEL": "Xcel Energy Inc.", "ED": "Consolidated Edison Inc.",
        "EXC": "Exelon Corp.", "SRE": "Sempra Energy", "PCG": "PG&E Corp.",
        "AMT": "American Tower Corp.", "PLD": "Prologis Inc.", "CCI": "Crown Castle Inc.",
        "EQIX": "Equinix Inc.", "PSA": "Public Storage", "O": "Realty Income Corp.",
        "WELL": "Welltower Inc.", "DLR": "Digital Realty Trust Inc.", "SPG": "Simon Property Group Inc.",
        "SBAC": "SBA Communications Corp.",
        "LIN": "Linde plc", "ECL": "Ecolab Inc.", "SHW": "Sherwin-Williams Co.", "APD": "Air Products and Chemicals Inc.",
        "FCX": "Freeport-McMoRan Inc.", "NEM": "Newmont Corp.", "NUE": "Nucor Corp.",
        "DD": "DuPont de Nemours Inc.", "DOW": "Dow Inc.", "VMC": "Vulcan Materials Co."
    }
    
    # Industries by sector
    sample_industries = {
        "Information Technology": ["Software", "Hardware", "Semiconductors", "IT Services"],
        "Health Care": ["Pharmaceuticals", "Biotechnology", "Medical Devices", "Health Services"],
        "Financials": ["Banks", "Capital Markets", "Insurance", "Consumer Finance"],
        "Consumer Discretionary": ["Retail", "Automobiles", "Restaurants", "Consumer Durables"],
        "Communication Services": ["Media", "Entertainment", "Telecom", "Interactive Media"],
        "Industrials": ["Aerospace", "Machinery", "Transportation", "Building Products"],
        "Consumer Staples": ["Food & Beverage", "Household Products", "Personal Products", "Food Retail"],
        "Energy": ["Oil & Gas", "Energy Equipment", "Refining", "Pipelines"],
        "Utilities": ["Electric Utilities", "Gas Utilities", "Water Utilities", "Renewable Energy"],
        "Real Estate": ["REITs", "Real Estate Management", "Real Estate Development", "Real Estate Services"],
        "Materials": ["Chemicals", "Metals & Mining", "Paper & Forest Products", "Construction Materials"]
    }
    
    # Create data structure
    data = []
    
    # Ensure balanced representation of sectors
    sector_quotas = {sector: max(3, int(num_companies * 0.09)) for sector in sectors}  # Minimum 3 companies per sector
    
    total_companies = 0
    for sector in sectors:
        sector_companies = sample_companies[sector]
        industry_list = sample_industries[sector]
        
        # Calculate how many companies to include from this sector
        sector_count = min(len(sector_companies), sector_quotas[sector])
        total_companies += sector_count
        
        for i in range(sector_count):
            symbol = sector_companies[i]
            company_name = company_names.get(symbol, f"Company {symbol}")
            
            # Generate realistic financial metrics based on sector
            # Assign different ranges to different sectors
            if sector in ["Information Technology", "Communication Services"]:
                pe_ratio = round(random.uniform(20, 35), 2)  # Higher PE for tech
                pb_ratio = round(random.uniform(3, 8), 2)  # Higher PB for tech
                earnings_growth = round(random.uniform(10, 25), 2)  # Higher growth
                revenue_growth = round(random.uniform(8, 20), 2)
            elif sector in ["Utilities", "Consumer Staples", "Real Estate"]:
                pe_ratio = round(random.uniform(12, 20), 2)  # Lower PE for defensive
                pb_ratio = round(random.uniform(1.5, 3.5), 2)  # Lower PB for defensive
                earnings_growth = round(random.uniform(2, 8), 2)  # Lower growth
                revenue_growth = round(random.uniform(1, 6), 2)
            else:
                pe_ratio = round(random.uniform(15, 25), 2)  # Moderate PE for others
                pb_ratio = round(random.uniform(2, 5), 2)  # Moderate PB for others
                earnings_growth = round(random.uniform(5, 15), 2)  # Moderate growth
                revenue_growth = round(random.uniform(3, 12), 2)
                
            # Other financial metrics
            ev_ebit = round(random.uniform(10, 30), 2)
            market_cap = round(random.uniform(5, 500), 2)  # in billions
            current_price = round(random.uniform(30, 300), 2)
            
            # Profitability metrics
            roe = round(random.uniform(5, 25), 2)
            roa = round(round(roe * 0.4, 2))  # ROA typically lower than ROE
            roic = round(random.uniform(roe * 0.6, roe * 0.9), 2)  # ROIC related to ROE
            operating_margin = round(random.uniform(10, 30), 2)
            
            # Cash flow metrics
            fcf_yield = round(random.uniform(1, 7), 2)
            debt_equity = round(random.uniform(0.2, 2), 2)
            dividend_yield = round(random.uniform(0, 4), 2)
            
            # DCF value gap calculation (positive means undervalued)
            fair_value = round(current_price * random.uniform(0.8, 1.2), 2)
            dcf_value_gap = round(((fair_value - current_price) / current_price) * 100, 2)
            
            # Classification logic
            if pe_ratio < 17 and pb_ratio < 2.5 and ev_ebit < 15:
                classification = "Value"
                if dcf_value_gap > 15:
                    valuation_tag = "VALUE – Undervalued"
                elif dcf_value_gap < -5:
                    valuation_tag = "VALUE – Overvalued"
                else:
                    valuation_tag = "VALUE – Fairly Valued"
            elif earnings_growth > 12 and revenue_growth > 8:
                classification = "Growth"
                if earnings_growth > 18:
                    valuation_tag = "GROWTH – Momentum"
                else:
                    valuation_tag = "GROWTH – Watchlist"
            else:
                classification = "Blend"
                valuation_tag = "BLEND – Mixed"
            
            company_data = {
                'Symbol': symbol,
                'Company': company_name,
                'Sector': sector,
                'Industry': random.choice(industry_list),
                'Current_Price': current_price,
                'Market_Cap_B': market_cap,
                'PE_Ratio': pe_ratio,
                'PB_Ratio': pb_ratio,
                'EV_EBIT': ev_ebit,
                'ROE': roe,
                'ROA': roa,
                'ROIC': roic,
                'Operating_Margin': operating_margin,
                'Earnings_Growth': earnings_growth,
                'Revenue_Growth': revenue_growth,
                'Debt_to_Equity': debt_equity,
                'FCF_Yield': fcf_yield,
                'Dividend_Yield': dividend_yield,
                'DCF_Value_Gap': dcf_value_gap,
                'Fair_Value': fair_value,
                'Classification': classification,
                'Valuation_Tag': valuation_tag
            }
            
            data.append(company_data)
    
    return data

# Generate sample data for 100 companies
sp500_data = create_sample_data(100)
df = pd.DataFrame(sp500_data)

# Save to CSV for dashboard use
df.to_csv("sp500_dashboard_data.csv", index=False)

# Convert to JSON for dashboard JavaScript use
js_data = df.to_json(orient='records', indent=2)
js_content = f"""// S&P 500 Sample Dataset
// Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Total companies: {len(df)}

const sp500Data = {js_data};
"""

with open("sp500_data.js", "w") as f:
    f.write(js_content)

# Display summary statistics
value_count = len(df[df['Classification'] == 'Value'])
growth_count = len(df[df['Classification'] == 'Growth'])
blend_count = len(df[df['Classification'] == 'Blend'])

print(f"Generated sample S&P 500 dataset with {len(df)} companies:")
print(f"- Value stocks: {value_count} ({value_count/len(df)*100:.1f}%)")
print(f"- Growth stocks: {growth_count} ({growth_count/len(df)*100:.1f}%)")
print(f"- Blend stocks: {blend_count} ({blend_count/len(df)*100:.1f}%)")
print(f"- Sectors represented: {df['Sector'].nunique()}")

print("\nFirst 10 rows of the dataset:")
print(df[['Symbol', 'Company', 'Sector', 'PE_Ratio', 'Classification', 'Valuation_Tag']].head(10))

print("\nData has been saved to:")
print("1. sp500_dashboard_data.csv - For dashboard import")
print("2. sp500_data.js - For JavaScript web use")