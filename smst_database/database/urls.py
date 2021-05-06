from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('',views.index),
    path('contact/',views.contact,name='contact'),
    path('blog/',views.document,name='blog'),
    path('project/',views.document,name='project'),  
    path('list/', views.home,name='total'),
    path('aso/', views.view_Aso,name='view_aso'),
    path('cat/', views.view_Cat,name='view_cat'),
    path('item/', views.view_Item,name='view_item'),
    path('product/', views.view_Pro,name='view_pro'),
    path('value/', views.view_Value,name='view_value'),
    path('filter/', views.filter,name='filter'),
    path('compare/', views.compare,name='compare_v2'),
    path('copy/', views.copy_function,name='copy_function'),
    path('login/',auth_views.LoginView.as_view(template_name="pages/login.html"), name="login"),
    path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('signup/',views.signup,name='signup'),
]