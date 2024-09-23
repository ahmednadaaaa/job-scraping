from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_page, name='job_search_page'),
    path('jobs/<str:search_job>/<int:page_num>/', views.scrape_jobs, name='scrape_jobs_search'),    
    path('register/' ,views.register, name="register"),
    path('login/' ,views.userLogin, name="login"),
    path('logout/' ,views.userLogout, name="logout"),
    
    path('about/', views.about, name='about'),
    path('contact/', views.about, name='contact'),
    path('index/', views.index, name='index'),

]