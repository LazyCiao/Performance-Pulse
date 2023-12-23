from django import forms


class CompanyForm(forms.Form):
    company_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Ticker Symbol or Stock Symbol'}))
