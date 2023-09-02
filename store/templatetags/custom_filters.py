from django import template
import json

register = template.Library()

@register.filter
def increase_ten_percentage(value):
    return format(value+0.11*value, ".2f")

@register.filter
def cart_count(cart,product_id):
        return cart[str(product_id)]

@register.filter
def total_price(cart,product):
    return product.product_price*cart[str(product.id)]

@register.filter
def final_total_price(cart,products):
    sum = 0
    for product in products:
        sum = sum + total_price(cart,product)
    return sum


@register.filter
def is_in_cart(product_id,cart):
    keys = cart.keys()
    print('keys',keys)
    print('cart',cart)
    if str(product_id) in keys:
        if cart[str(product_id)]>0:
            return True
    return False

@register.filter
def currency(value):
    return "रू "+str(value)

@register.filter
def total_cart(cart):
    values = cart.values()
    return sum(values)

@register.filter
def multiply(x,y):
    return x*y
