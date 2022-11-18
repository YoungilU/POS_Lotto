from datetime import datetime

from django.shortcuts import render

from POSApp.models import POSDB


# Create your views here.
def index(request):
    if request.method == "POST":
        pos = POSDB()
        # 이전 개수 - 현재 개수 DB에 저장
        prev_pension_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_1000']
        prev_pension_lottery_5000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_5000']
        prev_instant_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_1000']
        prev_instant_lottery_2000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_2000']
        curr_pension_lottery_1000 = prev_pension_lottery_1000 - int(request.POST.get('pension_lottery_1000_Qty'))
        curr_pension_lottery_5000 = prev_pension_lottery_5000 - int(request.POST.get('pension_lottery_5000_Qty'))
        curr_instant_lottery_1000 = prev_instant_lottery_1000 - int(request.POST.get('instant_lottery_1000_Qty'))
        curr_instant_lottery_2000 = prev_instant_lottery_2000 - int(request.POST.get('instant_lottery_2000_Qty'))
        pos.pension_lottery_1000 = curr_pension_lottery_1000
        pos.pension_lottery_5000 = curr_pension_lottery_5000
        pos.instant_lottery_1000 = curr_instant_lottery_1000
        pos.instant_lottery_2000 = curr_instant_lottery_2000

        # 판매금액
        sale = int(request.POST.get('pension_lottery_1000_Qty'))*1000 + int(request.POST.get('pension_lottery_5000_Qty'))*5000 + int(request.POST.get('instant_lottery_1000_Qty'))*1000 + int(request.POST.get('instant_lottery_2000_Qty'))*2000
        pos.sale = sale

        # 지급금액
        pay = int(request.POST.get('pay_price'))
        pos.pay = pay

        # 잔고
        prev_balance = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['balance']
        pos.balance = prev_balance + sale + pay

        # 판매시간
        pos.sale_time = datetime.now().replace(microsecond=0)

        pos.save()
    return render(request, "index.html")

def stock(request):
    return render(request, "stock.html")