from django.urls import path
from .views import (
    AnalysisList, AnalysisCreate, AnalysisUpdate, AnalysisDelete,
    SamplePointList, SamplePointCreate, SamplePointUpdate, SamplePointDelete,
    TestList, TestCreate, TestUpdate, TestView, TestDelete,
    MetaDataList, MetaDataCreate, MetaDataUpdate, MetaDataDelete
)
from . import views

urlpatterns = [
    path('analysis/', AnalysisList.as_view(), name='analysis'),
    path('analysis-create/', AnalysisCreate.as_view(), name='analysis-create'),
    path('analysis-update/<str:id>',
         AnalysisUpdate.as_view(), name='analysis-update'),
    path('analysis-delete/<str:id>',
         AnalysisDelete.as_view(), name='analysis-delete'),

    path('samplepoint/', SamplePointList.as_view(), name='samplepoint'),
    path('samplepoint-create/', SamplePointCreate.as_view(),
         name='samplepoint-create'),
    path('samplepoint-update/<str:pk>',
         SamplePointUpdate.as_view(), name='samplepoint-update'),
    path('samplepoint-delete/<str:pk>',
         SamplePointDelete.as_view(), name='samplepoint-delete'),


    path('test/', TestList.as_view(), name='test'),
    path('testview/<str:pk>', TestView.as_view(), name='test-view'),
    path('test-create/', TestCreate.as_view(), name='test-create'),
    path('test-update/<str:pk>', TestUpdate.as_view(), name='test-update'),
    path('test-delete/<str:pk>', TestDelete.as_view(), name='test-delete'),

    path('metadata/', MetaDataList.as_view(), name='metadata'),
    path('metadata-create/', MetaDataCreate.as_view(), name='metadata-create'),
    path('metadata-update/<str:pk>',
         MetaDataUpdate.as_view(), name='metadata-update'),
    path('metadata-delete/<str:pk>',
         MetaDataDelete.as_view(), name='metadata-delete'),

]
