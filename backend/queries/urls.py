from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_queries, name='list_queries'),
    path('run/<int:query_number>/', views.run_query, name='run_query'),
]
