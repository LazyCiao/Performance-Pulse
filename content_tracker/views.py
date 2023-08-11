from django.shortcuts import render


def profile_search(request):
    return render(request, 'content_tracker/search_profile.html')