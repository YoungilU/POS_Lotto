from django.shortcuts import render

from POSApp.models import POSDB


# Create your views here.
def index(request):
    if request.method == "POST":
        pos = POSDB()
        prev_pension_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_1000']
        prev_pension_lottery_5000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_5000']
        prev_instant_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_1000']
        prev_instant_lottery_2000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_2000']
        prev_balance = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['balance']
        curr_pension_lottery_1000 = prev_pension_lottery_1000 - int(request.POST.get('pension_lottery_1000_Qty'))
        curr_pension_lottery_5000 = prev_pension_lottery_5000 - int(request.POST.get('pension_lottery_5000_Qty'))
        curr_instant_lottery_1000 = prev_instant_lottery_1000 - int(request.POST.get('instant_lottery_1000_Qty'))
        curr_instant_lottery_2000 = prev_instant_lottery_2000 - int(request.POST.get('instant_lottery_2000_Qty'))

        pos.pension_lottery_1000 = curr_pension_lottery_1000
        pos.pension_lottery_5000 = curr_pension_lottery_5000
        pos.instant_lottery_1000 = curr_instant_lottery_1000
        pos.instant_lottery_2000 = curr_instant_lottery_2000
        pos.balance = prev_balance - int(request.POST.get('pension_lottery_1000_Qty'))*1000 - int(request.POST.get('pension_lottery_5000_Qty'))*5000 - int(request.POST.get('instant_lottery_1000_Qty'))*1000 - int(request.POST.get('instant_lottery_2000_Qty'))*2000
        pos.save()
        print('연금1000 개수 :', request.POST.get('pension_lottery_1000_Qty'))
        print('연금5000 개수 :', request.POST.get('pension_lottery_5000_Qty'))
        print('즉석1000 개수 :', request.POST.get('instant_lottery_1000_Qty'))
        print('즉석2000 개수 :', request.POST.get('instant_lottery_2000_Qty'))
        print('지급 가격 :', request.POST.get('pay_price'))
    return render(request, "index.html")

def test(request):
    return render(request, "index.html")