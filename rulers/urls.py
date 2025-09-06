from django.urls import path
from rulers import api, views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/monarch/by-year/', api.MonarchByYearView.as_view(), name='monarch_by_year'),
    path('api/monarch/by-name/', api.MonarchByNameView.as_view(), name='monarch_by_name'),
    path('api/capital/by-year/', api.CapitalByYearView.as_view(), name='capital_by_year'),
    path('api/monarch/add/', api.AddMonarchView.as_view(), name='add_monarch'),
]