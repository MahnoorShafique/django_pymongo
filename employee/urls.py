from django.urls import path

from employee import views

urlpatterns=[
    path('create/',views.Employee.as_view({'post':'create_employee'},name='abc')),
    path('view',views.Employee.as_view({'get':'view_employee'},name='abuy7c')),
    path('view_all',views.Employee.as_view({'get':'view_all_emp'},name='jyjj')),
    path('delete_emp',views.Employee.as_view({'delete':'delete_emp'},name='jyjj')),
    path('update_emp/',views.Employee.as_view({'patch':'update_emp'},name='jyjj')),
    path('filter_data',views.Employee.as_view({'get':'filter_data'},name='jyjvrej')),


]