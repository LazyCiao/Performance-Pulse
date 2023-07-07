from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CompanyForm
from .alpha_vantage import fetch_financial_data, params, API_BASE_URL


def home(request):
    return render(request, 'financial_pulse/home.html')


def search_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            params['symbol'] = company_name  # Update the symbol parameter
            financial_data = fetch_financial_data(API_BASE_URL, params)

            # Check if financial data is available
            if financial_data is not None and 'quarterlyReports' in financial_data:
                annual_reports = financial_data['quarterlyReports']
                if annual_reports:
                    revenue_list = []
                    fiscal_date_list = []
                    net_Income_list = []
                    operating_expenses_list = []
                    
                    for report in annual_reports:
                        revenue = report.get('totalRevenue')
                        fiscal_date = report.get('fiscalDateEnding')
                        net_Income = report.get('netIncomeFromContinuingOperations')
                        operating_expenses = report.get('operatingExpenses')
                        
                        if revenue:
                            revenue_list.append(revenue)
                            fiscal_date_list.append(fiscal_date)
                            net_Income_list.append(net_Income)
                            operating_expenses_list.append(operating_expenses)
                            print(revenue_list)
                            # Store the fetched data in the session
                    request.session['company_data'] = {
                        'company_name': company_name,
                        'revenue_list': revenue_list,
                        'fiscal_date_list': fiscal_date_list,
                        'net_Income_list': net_Income_list,
                        'operating_expenses_list': operating_expenses_list,
                    }

                    # Redirect to the company_data URL
                    return redirect('company_data')

            messages.error(request, 'No financial data found for the entered company symbol.')

    else:
        form = CompanyForm()

    return render(request, 'financial_pulse/search.html', {'form': form})


def company_data(request):
    company_data = request.session.get('company_data')

    # Clear the session data
    request.session['company_data'] = None

    if company_data:
        return render(request, 'financial_pulse/company_data.html', {'company_data': company_data})
    else:
        return redirect('search')


def test(request):
    # revenue_list = []
    # fiscal_date_list = []
    # net_Income_list = []
    # operating_expenses_list = []
    # financial_data = fetch_financial_data(API_BASE_URL, params)
    # formatted_data = json.dumps(financial_data, indent=2)
    # annual_reports = financial_data.get('quarterlyReports', [])
    
 
    # for report in annual_reports:
    #     revenue = report.get('totalRevenue')
    #     fiscal_date = report.get('fiscalDateEnding')
    #     net_Income = report.get('netIncomeFromContinuingOperations')
    #     operating_expenses = report.get('operatingExpenses')
    #     if revenue:
    #         revenue_list.append(revenue)
    #         fiscal_date_list.append(fiscal_date)
    #         net_Income_list.append(net_Income)
    #         operating_expenses_list.append(operating_expenses)
        
        
    # print(f'fiscal {fiscal_date_list}')
    # print(f'net {net_Income_list}') 
    # print(f'operating {operating_expenses_list}')     
    # print(f'revenue {revenue_list}')
    return render(request, 'financial_pulse/test.html')
