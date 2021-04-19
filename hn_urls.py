from django.urls import path

from .views import DashboardTemplateView


app_name = "stats"

urlpatterns = [
    path('dashboard/', DashboardTemplateView.as_view(), name="charts_view"),

]


"""
This url file is the one i want to load the dashboard 
and then the dashboard template will be having the include xyz.html files


"""