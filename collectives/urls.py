from django.urls import path
from . import views

app_name = 'collectives'

urlpatterns = [
    path('', views.CollectiveListView.as_view(), name='collective_list'),
    path('<int:pk>/', views.CollectiveDetailView.as_view(), name='collective_detail'),
    path('register/', views.CollectiveRegistrationView.as_view(), name='collective_register'),
    path('registration/success/', views.CollectiveRegistrationSuccessView.as_view(), name='registration_success'),
    path('<int:pk>/add-review/', views.AddReviewView.as_view(), name='add_review'),
]