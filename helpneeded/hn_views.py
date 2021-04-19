import sys

sys.path.append('..')  # Adding a higher directory to python modules path.  python3.9 relative paths
import posts

from posts.models import post

from django.http import JsonResponse
from django.db.models import Sum
from django.db.models import Count, Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, TemplateView




# I NEED THIS TO BE THE INITIAL VIEW FROM WHICH THE REST WILL SIT
class DashboardTemplateView(TemplateView):
    template_name = "stats/hn_dashboard.html"





# This is for the 4 cards on top of the dashboard. Counting the status numbers
# I NEED 4 CARDS DISPLAYING FROM THIS VIEW ON THE DASHBOARD
@login_required
def post_basic_stats(request):
    """get the count of all the post queries-- solved, unsolved and inprogres"""
    template_name = "stats/hn_dashboard.html"
    total = post.objects.all().filter(profile__user=request.user).count()  # count those of current user
    pending = post.objects.all().filter(profile__user=request.user).filter(post_status__icontains='pending').count()
    inprogress = post.objects.all().filter(profile__user=request.user).filter(post_status__icontains='inprogress').count()
    solved = post.objects.all().filter(profile__user=request.user).filter(post_status__icontains='solved').count()
    dataset = post.objects.filter(profile__user=request.user).values('post_category').annotate(
        total=Count('post_status'),
        solved=Count('post_status', filter=Q(post_status='solved')),
        unsolved=Count('post_status', filter=Q(post_status='unsolved')),
        inprogress=Count('post_status', filter=Q(post_status='inprogres'))).order_by('-timestamp')

    context = {'total': total,
               'solved': solved,
               'pending': pending,
               'inprogress': inprogress,
               'dataset': dataset,
               }
    return render(request, template_name, context)




# I NEED A PIE-CHART FROM THIS VIEW DISPLAYING ON THE DASHBOARD
@login_required
def category_n_nums_pie_chart(request):
    template_name = 'stats/hn_dashboard.html'
    categories = []
    nums = []

    total_hh = post.objects.filter(profile__user=request.user) \
        .filter(post_category__icontains="hh").count()
    total_EE = post.objects.filter(profile__user=request.user) \
        .filter(post_category__icontains="EE").count()
    total_YY = post.objects.filter(profile__user=request.user) \
        .filter(post_category__icontains="YY").count()
    total_AA = post.objects.filter(profile__user=request.user) \
        .filter(post_category__icontains="AA").count()

    qs = post.objects.all()
    for x in qs:
        categories.append(x.post_category)

    nums.append(total_hh)
    nums.append(total_EE)
    nums.append(total_YY)
    nums.append(total_AA)

    context = {
        'labels': categories,
        'data': nums,
    }
    return render(request, template_name, context)





# I NEED A BAR/COLUMN CHART FROM THIS VIEW DISPLAYING ON THE DASHBOARD
def cats_vs_the_totals_therein(request):
    cats = ["AA", "EE", "hh", "YY"]
    the_totals = [aa_total, ee_total, hh_total, yy_total]

    data = {'categories': [], 'values': []}

    data['categories'].append(cats)
    data['values'].append(the_totals)

    print(data)   # this works===>> output: {'categories': [['AA', 'EE', 'hh', 'YY']], 'values': [[4, 2, 0, 3]]}

    return render(request, 'stats/hn_dashboard.html', data)





# I NEED A PIE-CHART FROM THIS VIEW DISPLAYING ON THE DASHBOARD
def posts_chart(request):
    """ In this fn() we want to draw a bar graph of numbers of posts from the regions"""
    labels = []
    data = []
    cats = post.objects.filter(Q(post_category__icontains="HH") |
                                     Q(post_category__icontains="EE") |
                                     Q(post_category__icontains="YY") |
                                     Q(post_category__icontains="AA")
                                     )
    cats = cats.strip()
    for x in cats:
        dataset = post.objects.filter(profile__user=request.user).filter(x).annotate(Count(post.post))
        data.append(dataset)

    labels.append(cats)

    return JsonResponse(data={'labels': labels, 'data': data, })




# I NEED A TABLE FROM THIS VIEW DISPLAYING ON THE DASHBOARD
class RegionalpostCountForTableView(ListView, LoginRequiredMixin):
    template_name = 'stats/hn_dashboard.html'

    def get_queryset(self):
        return post.objects.all()

    def get_context_data(self, *args, object_list=None, **kwargs):

        # AA
        # TOTALS >>
        # rows
        "aa_total": aa_total,
        "ee_total": ee_total,
        "hh_total": hh_total,
        "yy_total": yy_total

        # cols
        "north_total": north_total,
        "east_total": east_total,
        "central_total": central_total,
        "south_total": south_total,
        "west_total": west_total,
 
        return context





# I NEED A PIE-CHART FROM THIS VIEW DISPLAYING ON THE DASHBOARD
def regions_vs_totals_there(request):
    template_name = "stats/hn_dashboard.html"
    labels = []
    data = []

    cats = ["AA", "EE", "hh", "YY"]
    the_totals = [aa_total, ee_total, hh_total, yy_total]

    labels.append(cats)
    data.append(the_totals)
    
    return JsonResponse(data={'labels': labels, 'data': data, })




"""
THE PROBLEM WITH ALL OF THIS CODE 
IS THAT IT STILL NEVER PRINTS TO THE HIGHCHARTS LIB INSIDE OF THE TEMPLATES

ANY IDEAS ON HOW TO INTEGRATE HIGHCHARTS WOULD BE APPRECIATED

I SPECIFICALLY WANT HIGHCHARTS BECAUSE THEY PROVIDE EXPLICIT OPTIONS TO EXPORT THE CHARTS AS SAY .png or .pdf etc...
"""