from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from products.models import *
from .serializers import *

# Create your views here.

class CartView(APIView):
    #permission_classes = [IsAuthenticated]
    def get(self,r):
        user = r.user
        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItems.objects.filter(cart=cart)
        serializer = CartItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self,r):
        data = r.data
        user = r.user
        cart,_= Cart.objects.get_or_create(user=user,ordered = False )
        product = Product.objects.get(id = data.get('product'))
        price = product.price
        quantity = data.get('quantity')
        cart_items = CartItems( cart=cart,user=user, product=product, price=price, quantity=quantity)
        cart_items.save()

        cart_items = CartItems.objects.filter(user=user, cart=cart.id)
        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()

        return Response({"success":"Items Added to your cart"})

    def put(self,r):
        data =r.data
        cart_item = CartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({"success":"Items updated"})

    def delete(self,r):
        user = r.user
        data=r.data
        cart_item = CartItems.objects.get(id=data.get('id'))
        cart_item.delete()
        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItems.objects.filter(cart=cart)
        serializer = CartItemSerializer(queryset, many=True)


        return Response(serializer.data)


class OrderAPI(APIView):
    def get(self,r):
        queryset = Orders.objects.filter(user = r.user)
        serializer = OrderSerializer(queryset, many = True)
        return Response(serializer.data)
