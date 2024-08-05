from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import bstat, Sdrate
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .effective_rate import user_amount_display, all_banks_sd
from .fd_effective_rate import user_fdrate_display, all_banks_fd
import json

@api_view(['GET'])
def home(request):
    """
    This function returns a home page of the API.
    """
    context = {"page": "this is a home page."}
    return Response(context)

@api_view(['GET'])
def effective_rate(request):
    """
    This view returns effective rate for given amount.
    """
    # print(request.body)
    # print("this is ")
    amt = request.GET.get("amount")
    value = amt.replace(',', '')
    amount = float(value)
    # print(value, amount)
    # print(request.body)
    # print(amount)
    effective_rate_dict = user_amount_display(amount=amount)
    # print(len(effective_rate_dict))
    json_response = json.dumps(effective_rate_dict)
    # if request.method=='POST':
    #     amount = float(request.POST.get('amount', "0000"))
    #     effective_rate_dict = user_amount_display(amount=amount)
    #     print(len(effective_rate_dict))
    #     json_response = JsonResponse(effective_rate_dict)
    return HttpResponse(json_response, content_type="application/json")
    # return render(request, "effective_rate.html", {'amount': amount, "effective_rate_dict":effective_rate_dict})
    return JsonResponse({'error': 'invalid request method'})

@api_view(['GET'])
def fd_effective_rate(request):
    fdrate = user_fdrate_display()
    json_response = json.dumps(fdrate)
    return HttpResponse(json_response, content_type="application/json")
    # return JsonResponse({"fdrate": "mandem"})


@api_view(['GET'])
def fdrate_banks_list(request):
    all_bank_list = all_banks_fd()
    json_response = json.dumps(all_bank_list)
    return HttpResponse(json_response, content_type="application/json")


api_view(['GET'])
def sdrate_banks_info(request):
    all_sdrate_info = all_banks_sd()
    json_response = json.dumps(all_sdrate_info)
    return HttpResponse(json_response, content_type="application/json")