# C:\Users\mloga\performance_pulse\crypto_pulse\templatetags\custom_filters.py

from django import template

register = template.Library()

def remove_commas(value):
    return value.replace(',', '')

@register.filter
def shorten_market_cap(market_cap):
    if market_cap is None:
        return ""

    # Remove commas from market_cap before converting to float
    market_cap = remove_commas(market_cap)

    # Convert market_cap to a float or int before comparing
    market_cap = float(market_cap)

    if market_cap >= 1_000_000_000:
        return "{:.2f}B".format(market_cap / 1_000_000_000)
    elif market_cap >= 1_000_000:
        return "{:.2f}M".format(market_cap / 1_000_000)
    elif market_cap >= 1_000:
        return "{:.2f}K".format(market_cap / 1_000)
    else:
        return str(market_cap)
