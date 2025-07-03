from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('label/<uuid:session_id>/', views.label_view, name='label'),
    path('save-label/', views.save_label, name='save_label'),
    path('download/<uuid:session_id>/', views.download_zips, name='download_zips'),
    path('sessions/', views.session_list, name='session_list'),
    path('relabel/<uuid:session_id>/', views.relabel_view, name='relabel'),
    path('delete/<uuid:session_id>/', views.delete_session, name='delete_session'),




]
