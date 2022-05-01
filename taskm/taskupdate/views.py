from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.utils import timezone
from django_rest_passwordreset.signals import reset_password_token_created
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import timedelta, date, datetime
import pandas as pd
import pytz
from .serializers import loginSerializer
from .models import Products, Order
import json
import uuid
from django.contrib.auth import logout


@api_view(['POST', ])
def register(request):
    """
    url -> /auth/register/
    DataFormat -> {
        "email" : "",
        "first_name" : "",
        "last_name" : "",
        "password1" : "",
        "password2" : ""
    }
    Usage : API used for self-registering a user
    Parameter used to regsiter email-ID, firstname, lastname, password1 and password2
    """
    if "email" not in request.data or "first_name" not in request.data or "last_name" not in request.data or "password1" not in request.data or "password2" not in request.data:
        return Response(status = 400, data={"Msg": "Details missing for querying"})
    same_email = User.objects.filter(email=request.data['email'])
    if len(same_email):
        return Response(status=400, data={'msg': 'User already exists with given email address'})
    if request.data["password1"] != request.data["password2"]:
        return Response(status=400, data={'msg': 'Passwords not matching please try again'})
    try:
        user=User(
            username=request.data['email'], 
            first_name=request.data['first_name'], 
            last_name=request.data['last_name'], 
            email=request.data['email'], 
            password=request.data['password1'])
        user.save()
    except Exception as e:
        return Response(status=400, data={'Error': "Some error"})
    return Response(status=200, data={'Msg': request.data['email']+" was registered successfully."})


@api_view(["POST", ])
def login(request):
    """
    url -> /auth/login/
    DataFormat -> {
        "username" : "",
        "password" : "",
    }

    Usage : used to get access token for making next subsequent request 
    and also initating a valid session
    """
    serializer = loginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        if not user.is_active:
            return Response(status=401, data={'Msg': 'No longer access provided'})
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        refresh = str(refresh)
        return Response(data={'Msg': "Login Successful.", 'AccessToken':access, "RefreshToken":refresh})
    else:
        res = serializer.errors
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def logout1(request):
    """
    url -> /auth/me/
    Headers -> {
        Authorization : JWT JWT_TOKEN
    }

    Usage :  To logout a user and so could he ends his session
    """
    try:
        logout(request)
    except Exception as e:
        return Response({'Message': 'Logout Failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'Message': 'Logout Successful'})


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def getproduct(request):
    """
    url -> /getproduct/
    Headers -> {
        Authorization : JWT JWT_TOKEN
    }

    Note : It is a utility to get details of all the product that are present in DB
    """
    try:
        prod = list(Products.objects.all().values("pid", "name", "quantity", "price"))
    except Exception as e:
        return Response(status=400, data={'Error': "Error while fetching product from Database"})
    return Response(status=200, data=prod)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def searchproduct(request):
    """
    url -> /searchproduct/?word=word
    Headers -> {
        Authorization : JWT JWT_TOKEN
    }

    Note : It is a utility to get details of all the product having a word that are present in DB
    """
    word=request.query_params["word"]
    try:
        prod = list(Products.objects.filter(name__contains=word).values("pid", "name", "quantity", "price"))
    except Exception as e:
        return Response(status=400, data={'Error': "Error while fetching product from Database"})
    return Response(status=200, data=prod)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def addproduct(request):
    """
    url -> /addproduct/
    Headers -> {
        Authorization : JWT JWT_TOKEN
    }
    Data-> [
        {
            pid=pid,
            name = "Parle G 120 gms"
            price = 8
            qunatity = 500
        }
    ]
    Note : Here pid(product ID) is a unique 6 digit ID used for maintaining the product
    detials, prices and stock quantities

    if product not in DB dont provide pid it will be generated every time.
    if product is present then just stocks and prices can be updated as per requrement using pid.
    """
    if request.user.is_superuser:

        if len(request.data)==0:
            return Response({'Message': 'Data Empty'}, status=status.HTTP_400_BAD_REQUEST)

        for i in request.data:
            try:
                prod = Products.objects.filter(pid=i["pid"]).exists()
            except Exception as e:
                prod=False

            if prod:
                try:
                    prod = Products.objects.get(pid=i["pid"])
                    prod.quantity=prod.quantity+i["quantity"]
                    if "price" in i:
                        prod.price=i["price"]
                    prod.save()
                except Exception as e:
                    return Response(status=400, data={'Error': "Error while incrementing lot of prodcut"+i["pid"]+"."})

            else:
                try:
                    p1=Products(
                        pid="P"+uuid.uuid4().hex[:5].upper(),
                        name=(i["name"]).lower(), 
                        quantity=i["quantity"],
                        price=i["price"])
                    p1.save()
                except Exception as e:
                    return Response(status=400, data={'Error': "Error while adding product "+i["name"]+""})
        return Response(status=200, data={'Msg': "Product has been added successfully."})
    else:
        return Response(status=401, data={'Msg': 'Unauthorized Access Requested'})


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def paginateproduct(request):
    """
    url -> /paginateproduct/?pagination=36&page=1
    Headers -> {
        Authorization : JWT JWT_TOKEN
    }
    """
    try :
        p = int(request.query_params['pagination'])
    except Exception as e:
        p = 25

    try :
        page = int(request.query_params['page'])
    except Exception as e:
        page = 0

    try:
        prod = list(Products.objects.all().values("pid", "name", "quantity", "price"))
        prod = prod[page*p:(page+1)*p]
    except Exception as e:
        return Response(status=400, data={'Error': "Error while fetching product from Database"})
    return Response(status=200, data=prod)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def order(request):
    """
    url -> /paginateproduct/?pagination=36&page=1
    Headers -> {
        Authorization : JWT JWT_TOKEN
    }
    """
    if len(request.data)==0:
        return Response(status=400, data={'Error': "Your cart is empty."})

    res=[]
    price=0

    for i in request.data:
        
        try:
            prod = Products.objects.filter(pid=i["pid"]).exists()
        except Exception as e:
            prod=False

        if prod:
            prod1=Products.objects.get(pid=i["pid"])
            if prod1.quantity<i["quantity"]:
                return Response(status=400, data={'Error': i["name"]+" is out of stock"})
            else:
                prod1.quantity = prod1.quantity-i["quantity"]
                prod1.save()
                price+=(prod1.price*i["quantity"])
                res.append(i)
        else:
            return Response(status=400, data={'Error': i["name"]+" is not avialable"})

    curr_user = request.user
    
    try:
        order=Order(
            oid="O"+uuid.uuid4().hex[:7].upper(),
            detail = res,
            user = curr_user,
            ordered_date = datetime.now(),
            total=price)
        order.save()
    except Exception as e:
        return Response(status=400, data={'Error': "Error while placing the order."})
    return Response(status=200, data={'Msg': "Your order has been placed successfully."})


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def orderhistory(request):
    curr_user = request.user
    try:
        order=list(Order.objects.filter(user=curr_user).values("oid", "detail", "ordered_date", "total").order_by('-ordered_date'))
    except Exception as e:
        return Response(status=400, data={'Error': "Seems issue while fetch from DB"})
    return Response(status=200, data=order)