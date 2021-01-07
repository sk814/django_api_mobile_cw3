from django.urls import include, path
from . import views

urlpatterns = [
    # path('vaccine', views.ProductLists.as_view()),
    path('signup', views.signup),
    path('login', views.login),
    path('adminlogin', views.adminlogin),
    path('volunteers', views.VolunteersViews.as_view()),
    path('all_result', views.AllResult.as_view()),
    path('result', views.FilterView.as_view()),
    path('maker', views.VacMaker.as_view()),
    #FilterView
    #VacMaker
]
