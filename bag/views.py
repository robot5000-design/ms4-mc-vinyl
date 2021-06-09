from django.shortcuts import render


def view_bag(request):
    """ A view that renders the bag contents page """

    template = 'bag/bag.html'

    return render(request, template)
