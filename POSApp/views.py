import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from POSApp.models import POSDB
from django.contrib.auth.models import User
from django.contrib import auth

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

        # 판매 수량
        pos.pension_lottery_1000_Qty = int(request.POST.get('pension_lottery_1000_Qty'))
        pos.pension_lottery_5000_Qty = int(request.POST.get('pension_lottery_5000_Qty'))
        pos.instant_lottery_1000_Qty = int(request.POST.get('instant_lottery_1000_Qty'))
        pos.instant_lottery_2000_Qty = int(request.POST.get('instant_lottery_2000_Qty'))

        # 판매금액
        sale = int(request.POST.get('pension_lottery_1000_Qty'))*1000 + int(request.POST.get('pension_lottery_5000_Qty'))*5000 + int(request.POST.get('instant_lottery_1000_Qty'))*1000 + int(request.POST.get('instant_lottery_2000_Qty'))*2000
        pos.sale = sale

        # 지급금액
        pay = int(request.POST.get('pay_price'))
        pos.pay = pay

        # 판매시간
        pos.sale_time = datetime.datetime.now().replace(microsecond=0)

        # 금일 영업 시작 시간
        pos.daily_sale_start = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['daily_sale_start']

        # 기본 시제금
        pos.base_balance = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['base_balance']

        # 재고 수정은 false
        pos.ismodify = False

        # category
        if sale>0 and pay<0: pos.category = "판매/지급"
        elif sale > 0: pos.category = "판매"
        elif pay < 0: pos.category = "지급"

        pos.save()
        return render(request, "index.html")

    pension_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_1000']
    pension_lottery_5000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_5000']
    instant_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_1000']
    instant_lottery_2000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_2000']
    context = {
        'pension_lottery_1000': pension_lottery_1000,
        'pension_lottery_5000': pension_lottery_5000,
        'instant_lottery_1000': instant_lottery_1000,
        'instant_lottery_2000': instant_lottery_2000
    }
    return render(request, "index.html", context)

def stock(request):
    pension_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_1000']
    pension_lottery_5000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_5000']
    instant_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_1000']
    instant_lottery_2000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_2000']
    # balance = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['balance']

    daily_list = POSDB.objects.filter(daily_sale_start=POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['daily_sale_start']).values()

    base_balance = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['base_balance']
    daily_sale = 0
    daily_pay = 0
    for i in range(len(daily_list)):
        daily_sale += daily_list[i]['sale']
        daily_pay += daily_list[i]['pay']

    daily_sale_start = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['daily_sale_start']
    context = {
        'pension_lottery_1000': pension_lottery_1000,
        'pension_lottery_5000': pension_lottery_5000,
        'instant_lottery_1000': instant_lottery_1000,
        'instant_lottery_2000': instant_lottery_2000,
        'daily_sale': daily_sale,
        'daily_pay': daily_pay,
        'sale_plus_pay': daily_sale + daily_pay,
        'base_balance': base_balance,
        'daily_balance': base_balance + daily_sale + daily_pay,
        'daily_sale_start': daily_sale_start,
    }
    return render(request, "stock.html", context)

def adminpage(request):
    # 0jun@chlrh / 0junWkd
    if request.method == "POST":
        if request.POST.get('pension_lottery_1000'):
            pos = POSDB()
            pos.pension_lottery_1000 = int(request.POST.get('pension_lottery_1000'))
            pos.pension_lottery_5000 = int(request.POST.get('pension_lottery_5000'))
            pos.instant_lottery_1000 = int(request.POST.get('instant_lottery_1000'))
            pos.instant_lottery_2000 = int(request.POST.get('instant_lottery_2000'))
            pos.base_balance = int(request.POST.get('base_balance'))
            pos.sale_time = datetime.datetime.now().replace(microsecond=0)
            pos.daily_sale_start = datetime.datetime.now().replace(microsecond=0)
            pos.pay = 0
            pos.sale = 0
            pos.ismodify = True
            pos.pension_lottery_1000_Qty = 0
            pos.pension_lottery_5000_Qty = 0
            pos.instant_lottery_1000_Qty = 0
            pos.instant_lottery_2000_Qty = 0
            pos.category = "재고수정"
            pos.save()
            return render(request, 'adminpage.html')
        elif request.POST.get('useremail'):
            useremail = request.POST.get('useremail', None)
            password = request.POST.get('password', None)
            user = auth.authenticate(username=useremail, password=password)
            if user is not None:
                auth.login(request, user)
                if request.user.is_authenticated:
                    pension_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_1000']
                    pension_lottery_5000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_5000']
                    instant_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_1000']
                    instant_lottery_2000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_2000']
                    daily_list = POSDB.objects.filter(daily_sale_start=POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['daily_sale_start']).values()

                    base_balance = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['base_balance']
                    daily_sale = 0
                    daily_pay = 0
                    for i in range(len(daily_list)):
                        daily_sale += daily_list[i]['sale']
                        daily_pay += daily_list[i]['pay']
                    context = {
                        'logineduser': request.user,
                        'pension_lottery_1000': pension_lottery_1000,
                        'pension_lottery_5000': pension_lottery_5000,
                        'instant_lottery_1000': instant_lottery_1000,
                        'instant_lottery_2000': instant_lottery_2000,
                        'sale_plus_pay': daily_sale + daily_pay,
                        'base_balance': base_balance,
                    }
                return render(request, 'adminpage.html', context)
            else:
                return render(request, 'adminpage.html', {'error': '※ 사용자 아이디 또는 패스워드가 틀립니다.'})
    else:
        return render(request, 'adminpage.html', )

def signup(request):
    res_data = None
    if request.method == 'POST':
        useremail = request.POST.get('useremail')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        password = request.POST.get('password')
        re_password = request.POST.get('confirm_password')
        res_data = {}
        if User.objects.filter(username=useremail):
            res_data['error'] = '※ 이미 가입된 이메일 주소 입니다.'
        elif password != re_password:
            res_data['error'] = '※ 비밀번호가 다릅니다.'
        else:
            user = User.objects.create_user(username=useremail,
                                            first_name=firstname,
                                            last_name=lastname,
                                            password=password)
            auth.login(request, user)
            return redirect("POSApp:index")
    return render(request, 'signup.html', res_data)

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect("POSApp:index")

def refund(request):
    if request.method == 'POST':
        refund_seq = POSDB.objects.filter(seq=request.POST.get('refund_seq'))

        prev_pension_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_1000']
        prev_pension_lottery_5000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_5000']
        prev_instant_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_1000']
        prev_instant_lottery_2000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_2000']
        pension_lottery_1000 = prev_pension_lottery_1000 + refund_seq.all().values()[0]['pension_lottery_1000_Qty']
        pension_lottery_5000 = prev_pension_lottery_5000 + refund_seq.all().values()[0]['pension_lottery_5000_Qty']
        instant_lottery_1000 = prev_instant_lottery_1000 + refund_seq.all().values()[0]['instant_lottery_1000_Qty']
        instant_lottery_2000 = prev_instant_lottery_2000 + refund_seq.all().values()[0]['instant_lottery_2000_Qty']
        sale_time = datetime.datetime.now().replace(microsecond=0)
        pay = -refund_seq.all().values()[0]['pay']
        sale = -refund_seq.all().values()[0]['sale']
        daily_sale_start = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['daily_sale_start']
        base_balance = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['base_balance']
        ismodify = False
        pension_lottery_1000_Qty = -refund_seq.all().values()[0]['pension_lottery_1000_Qty']
        pension_lottery_5000_Qty = -refund_seq.all().values()[0]['pension_lottery_5000_Qty']
        instant_lottery_1000_Qty = -refund_seq.all().values()[0]['instant_lottery_1000_Qty']
        instant_lottery_2000_Qty = -refund_seq.all().values()[0]['instant_lottery_2000_Qty']
        category = "환불"

        refund_seq.delete()

        pos = POSDB()
        pos.pension_lottery_1000 = pension_lottery_1000
        pos.pension_lottery_5000 = pension_lottery_5000
        pos.instant_lottery_1000 = instant_lottery_1000
        pos.instant_lottery_2000 = instant_lottery_2000
        pos.sale_time = sale_time
        pos.pay = pay
        pos.sale = sale
        pos.daily_sale_start = daily_sale_start
        pos.base_balance = base_balance
        pos.ismodify = ismodify
        pos.pension_lottery_1000_Qty = pension_lottery_1000_Qty
        pos.pension_lottery_5000_Qty = pension_lottery_5000_Qty
        pos.instant_lottery_1000_Qty = instant_lottery_1000_Qty
        pos.instant_lottery_2000_Qty = instant_lottery_2000_Qty
        pos.category = category
        pos.save()


    sale_pay_lists = POSDB.objects.order_by('-seq')
    paginator = Paginator(sale_pay_lists, 20)
    page = request.GET.get('page', 1)  # 페이지
    page_obj = paginator.get_page(page)


    context = {
        'sale_pay_list': page_obj,
    }
    return render(request, 'refund.html', context)
