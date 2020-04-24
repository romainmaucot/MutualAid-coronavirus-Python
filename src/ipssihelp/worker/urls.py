from django.urls import path, re_path
from . import views

app_name = 'worker'

urlpatterns = [
    path('', views.home, name='home'),
    path('demand', views.demand, name='demand'),
    path('supply', views.supply, name='supply'),
    path('detail/<slug:slug>/', views.detail, name='detail'),
    path('profil/<slug:slug>/', views.profil, name='profil'),
    path('account/signup/', views.signup, name='signup'),
    path('account/signin/', views.signin, name='signin'),
    path('account/update/<slug:slug>/', views.update_profil, name='update_profil'),
    path("logout", views.logout, name="logout"),
    re_path(r'conversation/(?P<id>[\w-]+)/$', views.conversation, name='conversation'),
]

