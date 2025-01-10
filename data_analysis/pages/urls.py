from django.urls import path
from .views import upload_file, data_overview, visualize_data, update_visualization
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_file, name='upload_file'),
    path('overview/', data_overview, name='data_overview'),
    path('visualize/', visualize_data, name='visualize_data'),
    path('update_visualization/', update_visualization, name='update_visualization'),
]
