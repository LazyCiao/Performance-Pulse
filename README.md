# Cryptocurrency Data Visualization and Analysis

![Equity Tracker](https://i.imgur.com/mnrz0m3.png)

![Crypto Market](https://i.imgur.com/kHsWJvo.png)

![Crypto Market](https://i.imgur.com/emHfzAV.png)

![Crypto Market](https://i.imgur.com/yhXktNn.png)

## Overview

Cryptocurrency Data Visualization and Analysis is a Django web application that allows users to explore and analyze cryptocurrency data. The application provides insights into various cryptocurrencies, including real-time market data, historical price charts, order book information, and detailed descriptions.

## Features

- **Cryptocurrency Listing:** View a list of cryptocurrencies with essential information, including name, symbol, market capitalization, daily price change, daily trading volume, and current price.

- **Pagination:** Navigate through multiple pages of cryptocurrency data, with ten cryptocurrencies displayed per page.

- **Interactive Candlestick Charts:** Explore historical price data for specific cryptocurrencies using interactive candlestick charts generated with Plotly. These charts display open, high, low, and close prices over a specified time frame (e.g., the last 3 months).

- **Order Book Information:** Access real-time order book data for selected cryptocurrencies, showing bid and ask orders.

- **Detailed Cryptocurrency Information:** Retrieve in-depth details about individual cryptocurrencies, including descriptions, names, symbols, and historical price charts generated with Matplotlib.

- **External APIs:** Utilize external cryptocurrency APIs to fetch up-to-date market data, coin details, order book data, and historical price information.

- **Error Handling:** Handle API request errors gracefully, providing users with informative error messages when data cannot be fetched or rate limits are reached.

- **Data Formatting:** Ensure consistency in API requests by formatting cryptocurrency names and symbols as needed for external data sources.

- **Session Management:** Store cryptocurrency data temporarily in user sessions, allowing seamless navigation between pages and eliminating redundant API calls.

## Usage

1. Clone this repository to your local environment.

   ``git clone https://github.com/your-username/your-repo-name.git``

2. Install the required dependencies:

   ``pip install -r requirements.txt``

3. Run the Django development server

   ``python manage.py runserver``
   Access the application in your web browser at ``http://localhost:8000``.

## Dependencies

   Django: Django
   Plotly: Plotly
   Matplotlib: Matplotlib
   
## Contributing

   Contributions to this project are welcome. Please follow the contribution guidelines for more information on how to get involved.

## License

   This project is licensed under the MIT License.
