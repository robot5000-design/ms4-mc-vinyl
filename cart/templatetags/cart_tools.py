from django import template

register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    ''' Calculates price * quantity

    Returns:
        price * quantity
    '''
    return price * quantity
