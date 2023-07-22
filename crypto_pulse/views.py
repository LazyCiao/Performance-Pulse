from django.shortcuts import render

def crypto(request):
    return render(request, 'crypto_pulse/crypto.html')
