from django.shortcuts import render


def profile(request):
    """ A view to show a user profile """

    return render(request, 'profiles/profile.html')
