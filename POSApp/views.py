from django.shortcuts import render

from POSApp.models import POSDB


# Create your views here.
def index(request):
    if request.method == "POST":
        # TODO: 전달받은 값 DB에 저장
        print('연금1000 개수 :', request.POST.get('pension_lottery_1000_Qty'))
        print('연금5000 개수 :', request.POST.get('pension_lottery_5000_Qty'))
        print('즉석1000 개수 :', request.POST.get('instant_lottery_1000_Qty'))
        print('즉석2000 개수 :', request.POST.get('instant_lottery_2000_Qty'))
        print('지급 가격 :', request.POST.get('pay_price'))
    return render(request, "index.html")

def test(request):
    return render(request, "index.html")