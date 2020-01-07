from django.urls import path, include
from .views import DashboardView, KPIDetailView, Ibyakozwe, District_chartView, Sector_chartView, CreateFamily, \
    change_status, AddKpi, load_cells, load_village,export,simple_upload

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('kpi/<int:pk>', KPIDetailView.as_view(), name='kpi-detail'),
    path('ibyakozwe/<int:pk>', Ibyakozwe.as_view(), name='ibyakozwe'),
    path('ibisigaye/<int:pk>', Ibyakozwe.as_view(), name='ibisigaye'),
    path('ibyakozwe_sector/<int:pk>', Ibyakozwe.as_view(), name='ibyakozwe_sector'),
    path('ibisigaye_sector/<int:pk>', Ibyakozwe.as_view(), name='ibisigaye_sector'),
    path('kpi/charts/<int:pk>', District_chartView.as_view(), name='kpi_charts'),
    path('sector_chart/charts/<int:pk>', Sector_chartView.as_view(), name='sector_charts'),
    path('add_family', CreateFamily.as_view(), name='family'),
    path('add_kpi', AddKpi.as_view(), name='add_kpi'),
    path('status/<int:fam_id>', change_status, name='status'),
    path('export/',export, name='export'),
    path('import/',simple_upload, name='import'),

    path('ajax/load-cells/', load_cells, name='ajax_load_cells'),
    path('ajax/load-villages/', load_village, name='ajax_load_villages'),
]