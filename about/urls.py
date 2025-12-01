from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/success/', views.ContactSuccessView.as_view(), name='contact_success'),
    path('team/', views.TeamView.as_view(), name='team'),
    path('team/<slug:slug>/', views.TeamMemberDetailView.as_view(), name='team_member_detail'),
    path('detail/', views.DetailView.as_view(), name='detail'),
]