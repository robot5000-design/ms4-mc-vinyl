from django.shortcuts import render


def index(request):
    ''' Renders the home index template.

    Args:
        request (object): HTTP request object.
    Returns:
        Render of the index template.
    '''
    return render(request, 'home/index.html')
