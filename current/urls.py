from django.urls import include, path

from current import views

app_name = 'current'

urlpatterns = [
    path('index/', views.index, name='index')
]