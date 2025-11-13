
from django.urls import path
from search import views
app_name='search'

urlpatterns = [
        path('',views.Searchview.as_view(),name='searchitem')
]
