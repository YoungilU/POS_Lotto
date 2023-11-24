import datetime
import pandas as pd

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from POSApp.models import POSDB
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def index(request):
    if request.method == "POST":
        pos = POSDB()

        # 아무 입력 없이 확인만 눌렀을 경우
        if int(request.POST.get('pension_lottery_1000_Qty')) == 0 and int(request.POST.get('pension_lottery_5000_Qty')) == 0 and \
                int(request.POST.get('instant_lottery_1000_Qty')) == 0 and int(request.POST.get('instant_lottery_2000_Qty')) == 0 and \
                int(request.POST.get('pay_price')) == 0:
            pension_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_1000']
            pension_lottery_5000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_5000']
            instant_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_1000']
            instant_lottery_2000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_2000']
            daily_list = POSDB.objects.filter(daily_sale_start=POSDB.objects.all().values()[len(POSDB.objects.all()) - 1][
                    'daily_sale_start']).values()
            base_balance = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['base_balance']
            daily_sale = 0
            daily_pay = 0
            for i in range(len(daily_list)):
                daily_sale += daily_list[i]['sale']
                daily_pay += daily_list[i]['pay']

            context = {
                'pension_lottery_1000': pension_lottery_1000,
                'pension_lottery_5000': pension_lottery_5000,
                'instant_lottery_1000': instant_lottery_1000,
                'instant_lottery_2000': instant_lottery_2000,
                'daily_balance': base_balance + daily_sale + daily_pay,
                'daily_pay': daily_pay,
            }
            return render(request, "index.html", context)

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
            'pension_lottery_1000': pension_lottery_1000,
            'pension_lottery_5000': pension_lottery_5000,
            'instant_lottery_1000': instant_lottery_1000,
            'instant_lottery_2000': instant_lottery_2000,
            'daily_balance': base_balance + daily_sale + daily_pay,
            'daily_pay': daily_pay,
        }
        return render(request, "index.html", context)

    pension_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_1000']
    pension_lottery_5000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['pension_lottery_5000']
    instant_lottery_1000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_1000']
    instant_lottery_2000 = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['instant_lottery_2000']

    daily_list = POSDB.objects.filter(
        daily_sale_start=POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['daily_sale_start']).values()
    base_balance = POSDB.objects.all().values()[len(POSDB.objects.all()) - 1]['base_balance']
    daily_sale = 0
    daily_pay = 0
    for i in range(len(daily_list)):
        daily_sale += daily_list[i]['sale']
        daily_pay += daily_list[i]['pay']

    context = {
        'pension_lottery_1000': pension_lottery_1000,
        'pension_lottery_5000': pension_lottery_5000,
        'instant_lottery_1000': instant_lottery_1000,
        'instant_lottery_2000': instant_lottery_2000,
        'daily_balance': base_balance + daily_sale + daily_pay,
        'daily_pay': daily_pay,
    }
    return render(request, "index.html", context)

def stock(request):
    if request.POST.get('daterange'):
        # 선택 날짜 slicing
        start_date = request.POST.get('daterange')[:request.POST.get('daterange').find(' -')]
        start_date = start_date[6:10] + '-' + start_date[0:2] + '-' + start_date[3:5]
        end_date = request.POST.get('daterange')[request.POST.get('daterange').find('- ')+2:]
        end_date = end_date[6:10] + '-' + end_date[0:2] + '-' + end_date[3:5]

        # DB 데이터프레임으로
        df = pd.DataFrame(POSDB.objects.all().values())

        # 날짜 형식: 0000-00-00
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # 선택된 날짜만 데이터프레임으로
        selected_df = df[(df.sale_time.dt.date >= start_date) & (df.sale_time.dt.date <= end_date)]

        # 0000-00-00 형식 날짜 컬럼 추가
        selected_df['sale_time_ymd'] = selected_df['sale_time'].dt.date

        # 날짜별 합계 계산
        groupby_selected_df = selected_df.groupby('sale_time_ymd').sum()
        groupby_selected_df['sale_plus_pay'] = groupby_selected_df['sale'] + groupby_selected_df['pay']

        # 선택된 날짜별로 각각 리스트 생성
        sale_list = groupby_selected_df.sale.to_list()
        pay_list = groupby_selected_df.pay.to_list()
        sale_plus_pay_list = groupby_selected_df.sale_plus_pay.to_list()
        pension_lottery_5000_Qty_list = groupby_selected_df.pension_lottery_5000_Qty.to_list()
        instant_lottery_1000_Qty_list = groupby_selected_df.instant_lottery_1000_Qty.to_list()
        instant_lottery_2000_Qty_list = groupby_selected_df.instant_lottery_2000_Qty.to_list()

        # 선택된 날짜별 합계
        sale = selected_df.sale.sum()
        pay = selected_df.pay.sum()
        sale_plus_pay = sale + pay
        pension_lottery_5000_Qty = selected_df.pension_lottery_5000_Qty.sum()
        instant_lottery_1000_Qty = selected_df.instant_lottery_1000_Qty.sum()
        instant_lottery_2000_Qty = selected_df.instant_lottery_2000_Qty.sum()

        # 0000-00-00 형식의 리스트
        date = []
        for i in range(len(selected_df.sale_time.dt.date.unique())):
            date.append(selected_df.sale_time.dt.date.unique()[i].strftime("%Y-%m-%d %a"))
        selected_date = date

        context = {
            'sale': sale,
            'pay': pay,
            'sale_plus_pay': sale_plus_pay,
            'pension_lottery_5000_Qty': pension_lottery_5000_Qty,
            'instant_lottery_1000_Qty': instant_lottery_1000_Qty,
            'instant_lottery_2000_Qty': instant_lottery_2000_Qty,
            'selected_date': selected_date,
            'sale_list': sale_list,
            'pay_list': pay_list,
            'sale_plus_pay_list': sale_plus_pay_list,
            'pension_lottery_5000_Qty_list': pension_lottery_5000_Qty_list,
            'instant_lottery_1000_Qty_list': instant_lottery_1000_Qty_list,
            'instant_lottery_2000_Qty_list': instant_lottery_2000_Qty_list,
        }

        return render(request, "stock.html", context)
    return render(request, "stock.html")

def adminpage(request):
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
        elif request.POST.get('delete_data'):   # 삭제 버튼을 눌렀을 때
            # pos = POSDB.objects.get(seq=7180)
            # print(pos.seq)
            # pos.delete()
            # pos.seq = 10000
            # pos.save()
            #### 프로세스 ####
            # 한 달 이상 된 데이터는 csv로 따로 저장
            # 한 달 이상 된 데이터 DB에서 삭제
            # 한 달치의 데이터 seq 1부터 부여
            # 저장 PATH 경로 재설정 필요
            ################

            # 한 달 이전 날짜
            before_one_month = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(days=30)

            # 현재 날짜로부터 한 달치 데이터
            one_month_data = POSDB.objects.filter(sale_time__range=[before_one_month, datetime.datetime.now().replace(microsecond=0)]).values().all()

            # 현재 날짜로부터 한 달 이상 지난 데이터
            except_one_month_data = POSDB.objects.filter(sale_time__range=[datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(days=30000),
                                                                           before_one_month]).values().all()
            except_one_month_data_df = pd.DataFrame(except_one_month_data)

            # 삭제하는 데이터 csv로 저장
            save_name1 = str(datetime.datetime.now().replace(microsecond=0))[:11].replace('-','_') # 저장명용 변수
            save_name2 = str(datetime.datetime.now().replace(microsecond=0))[11:].replace(':','_')
            save_name = save_name1 + '__' + save_name2
            save_name = (save_name + '.csv').replace(' ', '') # 파일명 합칠 때 공백 제거
            except_one_month_data_df.to_csv('D:\\' + save_name, encoding='utf-8-sig', index=False)

            # 한 달 이상 된 데이터 DB에서 삭제
            for row in except_one_month_data:
                pos = POSDB.objects.get(seq=row['seq'])
                pos.delete()

            # 한 달치의 데이터 seq 1부터 부여
            count_seq = 1
            for row in one_month_data:
                pos = POSDB.objects.get(seq=row['seq'])
                pos.delete()
                pos.seq = count_seq
                count_seq += 1
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
        # 환불 선택 -> 카테고리 환불완료로 수정
        selected = POSDB.objects.get(seq=refund_seq.all().values()[0]['seq'])
        selected.category = selected.category + '(환불완료)'
        selected.save()

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

        # refund_seq.delete()

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
