from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CompanyForm
from .alpha_vantage import fetch_income_statement, fetch_balance_sheet, fetch_news_sentiment, fetch_overview, params, API_BASE_URL, news_sentiment_params
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64
import json
from datetime import datetime
import numpy as np
import nltk


def search_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            params['symbol'] = company_name  # Update the symbol parameter
            news_sentiment_params['tickers'] = [company_name]  # Update the tickers parameter for news sentiment
            income_statement_data = fetch_income_statement(API_BASE_URL, params)
            balance_sheet_data = fetch_balance_sheet(API_BASE_URL, params)
            news_sentiment_data = fetch_news_sentiment(API_BASE_URL, news_sentiment_params)
            overview_data = fetch_overview(API_BASE_URL, params)
            
            # Check if the response contains information about reaching the daily limit
            if income_statement_data and 'Information' in income_statement_data:
                messages.error(request, "This application is for learning and testing purposes only. "
                       "The maximum daily fetch requests have been reached for this API. "
                       "Please try again tomorrow.")
                return render(request, 'financial_pulse/search_company.html', {'form': form})
            
            # Check if news and sentiment data is available
            if news_sentiment_data is not None and 'feed' in news_sentiment_data:
                news_sentiment = news_sentiment_data['feed']
                if news_sentiment:
                    news_items = []

                    # Define the maximum number of characters you want to show for each title
                    max_title_length = 50

                    # Limit the number of articles to 3
                    for report in news_sentiment[:3]:
                        news_title = report.get('title')
                        news_link = report.get('url')

                        if news_title and news_link:
                            # Check if the title length exceeds the maximum allowed length
                            if len(news_title) > max_title_length:
                                # Find the last space before reaching the maximum length
                                last_space_index = news_title.rfind(' ', 0, max_title_length)
                                if last_space_index != -1:
                                    # Shorten the title up to the last space
                                    shortened_title = news_title[:last_space_index] + '...'
                                else:
                                    # If there are no spaces within the limit, simply truncate the title
                                    shortened_title = news_title[:max_title_length - 3] + '...'
                            else:
                                # If the title is already short, keep it as is
                                shortened_title = news_title

                            # Append the shortened title and link to the list
                            news_items.append((shortened_title, news_link))

                    # If there are less than 3 articles, fill the list with empty tuples
                    while len(news_items) < 3:
                        news_items.append(('', ''))


            # Check if business overview data is available
            if overview_data is not None and 'Description' in overview_data and 'Name' in overview_data:
                description = overview_data['Description']
                name = overview_data['Name']

                # Use NLTK to tokenize the description into sentences
                sentences = nltk.sent_tokenize(description)

                # Select the first three sentences (or less if the description is shorter)
                first_three_sentences = ' '.join(sentences[:2])

                # Update the description with the shortened version
                description = first_three_sentences.strip() 
                
            
            # Check if balance sheet data is available
            if balance_sheet_data is not None and 'quarterlyReports' in balance_sheet_data:
                balance_sheet_reports = balance_sheet_data['quarterlyReports']
                if balance_sheet_reports:
                    total_assets_list = []
                    total_liabilities_list = []
                    total_shareholder_equity_list = []
                    
                    for report in balance_sheet_reports:
                        total_assets = report.get('totalAssets')
                        total_liabilities = report.get('totalLiabilities')
                        shareholder_equity = report.get('totalShareholderEquity')
                        
                        if total_assets:
                            total_assets_list.append(int(total_assets))
                        if total_liabilities:
                            total_liabilities_list.append(int(total_liabilities))
                        if shareholder_equity:
                            total_shareholder_equity_list.append(int(shareholder_equity))
                    
            # Check if income statement data is available
            if income_statement_data is not None and 'quarterlyReports' in income_statement_data:
                income_statement_reports = income_statement_data['quarterlyReports']
                if income_statement_reports:
                    revenue_list = []
                    fiscal_date_list = []
                    net_income_list = []
                    operating_expenses_list = []
                    gross_profit_list = []
                    operating_income_list = []

                    for report in income_statement_reports:
                        revenue = report.get('totalRevenue')
                        fiscal_date = report.get('fiscalDateEnding')
                        net_income = report.get('netIncomeFromContinuingOperations')
                        operating_expenses = report.get('operatingExpenses')
                        gross_profit = report.get('grossProfit')
                        operating_income = report.get('operatingIncome')
                        total_assets = report.get('totalAssets')
                        total_liabilities = report.get('totalLiabilities')
                        shareholder_equity = report.get('totalShareholderEquity')
                        
                        if revenue:
                            revenue_list.append(int(revenue))
                            fiscal_date_list.append(fiscal_date)
                            net_income_list.append(int(net_income))
                            operating_expenses_list.append(int(operating_expenses))
                            gross_profit_list.append(int(gross_profit))
                            operating_income_list.append(int(operating_income))

                        if total_assets:
                            total_assets_list.append(int(total_assets))
                        if total_liabilities:
                            total_liabilities_list.append(int(total_liabilities))
                        if shareholder_equity:
                            total_shareholder_equity_list.append(int(shareholder_equity))
                        
                    # Net profit margin
                    net_profit_margin = [(net_income / revenue) * 100 for net_income, revenue in zip(net_income_list, revenue_list)]
                    rounded_net_profit_margin = [round(margin, 2) for margin in net_profit_margin]
                    formatted_net_profit_margin = [f'{margin:.2f}%' for margin in rounded_net_profit_margin]
                    net_profit_margin_clean = [int(float(value.strip('%'))) for value in formatted_net_profit_margin]
                    
                    # Operating profit margin
                    operating_profit_margin = [(operating_income / revenue) * 100 for operating_income, revenue in zip(operating_expenses_list, revenue_list)]
                    rounded_operating_margin = [round(margin, 2) for margin in operating_profit_margin]
                    formatted_operating_profit_margin = [f'{margin:.2f}%' for margin in rounded_operating_margin]
                    operating_profit_margin_clean = [int(float(value.strip('%'))) for value in formatted_operating_profit_margin]

                    # Gross profit margin
                    gross_profit_margin = [(gross_profit / revenue) * 100 for gross_profit, revenue in zip(gross_profit_list, revenue_list)]
                    rounded_profit_margin = [round(margin, 2) for margin in gross_profit_margin]
                    formatted_gross_profit_margin = [f'{margin:.2f}%' for margin in rounded_profit_margin]
                    gross_profit_margin_clean = [int(float(value.strip('%'))) for value in formatted_gross_profit_margin]
                    
                    # Reverse lists' data
                    revenue_final = revenue_list[::-1]
                    net_income_final = net_income_list[::-1]
                    operating_expenses_final = operating_income_list[::-1]
                    gross_profit_margin_final = gross_profit_margin_clean[::-1]
                    operating_profit_margin_final = operating_profit_margin_clean[::-1]
                    net_profit_margin_final = net_profit_margin_clean[::-1]
                    total_assets_final = total_assets_list[::-1]
                    total_liabilities_final = total_liabilities_list[::-1]
                    total_shareholder_equity_final = total_shareholder_equity_list[::-1]
                    
                    # Format dates for x axis
                    fiscal_date_list_datetime = [datetime.strptime(date, '%Y-%m-%d').date() for date in fiscal_date_list]
                    fiscal_date_final = [str(date) for date in fiscal_date_list_datetime[::-1]]
                    x_ticks = np.array(fiscal_date_final, dtype='datetime64')
                    bar_x_ticks = [datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m') for date in fiscal_date_final]

                    # Clear plots
                    plt.clf()
                    plt.figure(figsize=(10, 6))

                    # Creating line chart
                    plt.plot(x_ticks, revenue_final, color='#FF6347', label='Revenue', marker='h', markersize=10 , linewidth=3)
                    plt.plot(x_ticks, net_income_final, color='#FF8A73', label='Net Income', marker='h', markersize=10 , linewidth=3)
                    plt.plot(x_ticks, operating_expenses_final, color='#D40B00', label='Expenses', marker='h', markersize=10 , linewidth=3)

                    # Plot info and style
                    plt.style.use('_mpl-gallery')
                    plt.xlabel(' ', color='white', fontsize=17)  # Increase font size to 12
                    plt.ylabel('Amount (USD)', color='white', fontsize=17)  # Increase font size to 12
                    plt.title(f'{company_name} Financial Metrics over Time', color='white', fontsize=17)  # Increase font size to 16
                    plt.tight_layout()
                    
                    # Remove the grid from both axes
                    plt.grid(False)

                    # Style tick labels on both axes to have a white font color and increase font size to 10
                    plt.tick_params(axis='x', colors='white', labelsize=16)  
                    plt.tick_params(axis='y', colors='white', labelsize=16)

                    # Style legend and increase font size to 10
                    legend = plt.legend(fontsize=18) 
                    legend.get_frame().set_facecolor('none')
                    # Loop through all legend texts and set the color to white
                    for text in legend.get_texts():
                        text.set_color('white')

                    # Convert the plot to an image
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png', transparent=True)
                    buffer.seek(0)
                    line_chart_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    buffer.close()

                    # Clear plots for the next chart
                    plt.clf()

                    # Create an array of indices
                    x_indices = np.arange(len(bar_x_ticks))

                    # Set the width of each bar
                    bar_width = 0.25

                    # Adjust the x positions for each bar
                    x_ticks_gross = x_indices - bar_width
                    x_ticks_operating = x_indices
                    x_ticks_net = x_indices + bar_width

                    # Rotating x values
                    plt.xticks(rotation=45)

                    # Creating bar chart
                    plt.bar(x_ticks_gross, gross_profit_margin_final, color='#FF6347', label='Gross Profit Margin', width=bar_width)
                    plt.bar(x_ticks_operating, operating_profit_margin_final, color='#FF8A73', label='Operating Profit Margin', width=bar_width)
                    plt.bar(x_ticks_net, net_profit_margin_final, color='#D40B00', label='Net Profit Margin', width=bar_width)

                    plt.style.use('_mpl-gallery')
                    plt.xlabel(' ', color='white', fontsize=18)  # Increase font size to 12
                    plt.ylabel('Margin (%)', color='white', fontsize=18)  # Increase font size to 12
                    plt.title(f'{company_name} Gross, Operating, and Net Profit Margin', color='white', fontsize=18)  # Increase font size to 16
                    plt.tight_layout()

                    # Remove the grid from both axes
                    plt.grid(False)

                    # Style tick labels on both axes to have a white font color and increase font size to 10
                    plt.tick_params(axis='x', colors='white', labelsize=16)  
                    plt.tick_params(axis='y', colors='white', labelsize=16)

                    # Style legend and increase font size to 10
                    legend = plt.legend(fontsize=18) 
                    legend.get_frame().set_facecolor('none')
                    # Loop through all legend texts and set the color to white
                    for text in legend.get_texts():
                        text.set_color('white')

                    # Convert the plot to an image
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png', transparent=True)
                    buffer.seek(0)
                    bar_chart_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    buffer.close()

                    # Set the x-tick locations and labels
                    plt.xticks(x_indices, bar_x_ticks)  

                    # Convert the plot to an image
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png', transparent=True)
                    buffer.seek(0)
                    bar_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    buffer.close()

                    # Clear plots for the next chart
                    plt.clf()

                    # Create the area chart
                    plt.fill_between(x_ticks, total_assets_final, color='#FF0000', alpha=0.5, label="Total Assets")
                    plt.fill_between(x_ticks, total_liabilities_final, color='#FF8A73', alpha=0.5, label="Total Liabilities")
                    plt.fill_between(x_ticks, total_shareholder_equity_final, color='#A9A9A9', alpha=0.5, label="Total Shareholder Equity")

                    # Customize the chart
                    plt.style.use('_mpl-gallery') 
                    plt.xlabel(' ', color='white', fontsize=17)  # Increase font size to 12
                    plt.ylabel("Amount (USD)", color='white', fontsize=17)  # Increase font size to 12
                    plt.title(f'{company_name} Financial Metrics over Time', color='white', fontsize=17)  # Increase font size to 16

                    # Remove the grid from both axes
                    plt.grid(False)

                    # Style tick labels on both axes to have a white font color and increase font size to 10
                    plt.tick_params(axis='x', colors='white', labelsize=16)  
                    plt.tick_params(axis='y', colors='white', labelsize=16)

                    # Style legend and increase font size to 10
                    legend = plt.legend(fontsize=18) 
                    legend.get_frame().set_facecolor('none') 
                    # Loop through all legend texts and set the color to white
                    for text in legend.get_texts():
                        text.set_color('white')

                    # Convert the plot to an image
                    buffer = BytesIO()
                    plt.savefig(buffer, format='png', transparent=True)
                    buffer.seek(0)
                    area_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    buffer.close()

   
                    # Store the fetched data in the session
                    request.session['company_data'] = {
                        'company_name': company_name,
                        'description': description,
                        'name' : name,
                        'line_chart_image_base64': line_chart_image_base64,
                        'bar_chart_image_base64': bar_image_base64,
                        'area_chart_image_base64': area_image_base64,
                        'revenue_list': revenue_final,
                        'fiscal_date_list': fiscal_date_final,
                        'net_Income_list': net_income_final,
                        'operating_expenses_list': operating_expenses_final,
                        'gross_profit_margin': gross_profit_margin_final,
                        'operating_profit_margin': operating_profit_margin_final,
                        'net_profit_margin': net_profit_margin_final,
                        'news_items': news_items, 
                    }

                    # Redirect to the company_data URL
                    return redirect('financial_pulse:company_data')

                messages.error(request, 'No financial data found for the entered company symbol.')

    else:
        form = CompanyForm()

    return render(request, 'financial_pulse/search_company.html', {'form': form})


def company_data(request):
    company_data = request.session.get('company_data')

    # Clear the session data
    request.session['company_data'] = None

    if company_data:
        return render(request, 'financial_pulse/company_data.html', {'company_data': company_data})
    else:
        return redirect('financial_pulse:search_company')


def test(request):
    return render(request, 'financial_pulse/test.html')