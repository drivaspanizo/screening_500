# Equity Value Intelligence: S&P 500 Tracker

A comprehensive dashboard for tracking and analyzing S&P 500 companies with value/growth classification and fundamental valuation metrics.

## Features

- **Complete S&P 500 Coverage**: Tracks all 500+ companies in the S&P 500 index
- **Fama-French Classification**: Categorizes stocks as Value or Growth using rigorous methodology
- **DCF Valuation Analysis**: Calculates intrinsic value and value gaps for each company
- **Interactive Visualizations**: Dynamic charts and tables for in-depth analysis
- **Comparative Analysis**: Multi-dimensional comparison of selected companies
- **Historical Trends**: Track valuation metrics over time against 5-year averages
- **Advanced Filtering**: Comprehensive filtering by sector, industry, valuation status and more
- **Export Capabilities**: Export data to CSV, Excel, and PDF formats

## Repository Contents

- `sp500_dashboard.html` - The main dashboard file
- `sp500_data_fetcher.py` - Python script to fetch and process S&P 500 data
- `sp500_dashboard_data.csv` - Sample data for dashboard testing
- `sp500_data.js` - JavaScript data file for the dashboard

## Getting Started

### Option 1: Quick Start with Sample Data

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/sp500-dashboard.git
   cd sp500-dashboard
   ```

2. Open `sp500_dashboard.html` in your web browser to view the dashboard with sample data.

### Option 2: Fetch Live Data

1. Install required Python packages:
   ```
   pip install pandas yfinance requests beautifulsoup4
   ```

2. Run the data fetcher script:
   ```
   python sp500_data_fetcher.py
   ```

3. Open `sp500_dashboard.html` in your web browser to view the dashboard with live data.

## GitHub Pages Deployment

To host the dashboard on GitHub Pages:

1. Go to your repository on GitHub
2. Navigate to Settings > Pages
3. Select the branch to publish from (usually `main`)
4. Save to publish the dashboard

## Customization

- Adjust classification thresholds in the Settings modal
- Modify alert parameters for P/E ratios and DCF gaps
- Configure data refresh frequency

## License

MIT License

## Acknowledgements

- Data powered by Yahoo Finance API
- Visualization using Chart.js
- Bootstrap 5 for UI components
