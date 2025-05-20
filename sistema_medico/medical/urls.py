from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('consultas/', views.consulta_list, name='consulta_list'),
    path('consulta/<int:pk>/', views.consulta_detail, name='consulta_detail'),
    path('consulta/new/', views.consulta_new, name='consulta_new'),
    path('consulta/<int:pk>/edit/', views.consulta_edit, name='consulta_edit'),
    path('consulta/<int:pk>/delete/', views.consulta_delete, name='consulta_delete'),
    path('consulta/<int:consulta_id>/receta/add/', views.receta_add, name='receta_add'),
]
