from django.urls import path
from .views import (
    FieldList, FieldCreate, FieldUpdate, FieldDelete,
    WellList, WellCreate, WellUpdate, WellDelete,
    DashboardView
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('wells/', WellList.as_view(), name='well'),
    path('fields/', FieldList.as_view(), name='field'),

    path('field_create/', FieldCreate.as_view(), name='field-create'),
    path('field_update/<str:pk>', FieldUpdate.as_view(), name='field-update'),
    path('field_delete/<str:pk>', FieldDelete.as_view(), name='field-delete'),

    path('well_create/', WellCreate.as_view(), name='well-create'),
    path('well_create/<str:id>', WellCreate.as_view(), name='well-create'),
    path('well_update/<str:id>', WellUpdate.as_view(), name='well-update'),
    path('well_delete/<str:pk>', WellDelete.as_view(), name='well-delete'),



]
