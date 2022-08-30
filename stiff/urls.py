from django.urls import path
from .views import (
    StiffTemplateLevelCreate, StiffTemplateLevelList, StiffTemplateList, StiffTemplateCreate, StiffTemplateUpdate, StiffTemplateDelete,
    StiffTemplateLevelList, StiffTemplateLevelCreate, StiffTemplateLevelUpdate, StiffTemplateLevelDelete,
    StiffTemplateLevelIonList, StiffTemplateLevelIonCreate, StiffTemplateLevelIonDelete,
    radarchartLoad, radarchartFilter, stiffcharttLoad
)


urlpatterns = [
    path('stifftemplate/', StiffTemplateList.as_view(), name='stifftemplate'),
    #path('stifftemplate/<str:pk>', StiffTemplateLevelList.as_view(),name='stifftemplate-view'),
    path('stifftemplate-create/', StiffTemplateCreate.as_view(),
         name='stifftemplate-create'),
    path('stifftemplate-update/<str:pk>',
         StiffTemplateUpdate.as_view(), name='stifftemplate-update'),
    path('stifftemplate-delete/<str:pk>',
         StiffTemplateDelete.as_view(), name='stifftemplate-delete'),

    path('stifftemplatelevel/<str:pk>',
         StiffTemplateLevelList.as_view(), name='stifftemplatelevel'),
    #path('stifftemplatelevel/<str:pk>', views.stifftemplateLoad, name='stifftemplatelevel-view'),
    path('stifftemplatelevel-create/<str:pk>',
         StiffTemplateLevelCreate.as_view(), name='stifftemplatelevel-create'),
    path('stifftemplatelevel-update/<str:pk>',
         StiffTemplateLevelUpdate.as_view(), name='stifftemplatelevel-update'),
    path('stifftemplatelevel-delete/<str:pk>',
         StiffTemplateLevelDelete.as_view(), name='stifftemplatelevel-delete'),

    path('stifftemplatelevelion/<str:pk>',
         StiffTemplateLevelIonList.as_view(), name='stifftemplatelevelion'),
    #path('stifftemplatelevel/<str:pk>', views.stifftemplateLoad, name='stifftemplatelevel-view'),
    path('stifftemplatelevelion-create/<str:pk>',
         StiffTemplateLevelIonCreate.as_view(), name='stifftemplatelevelion-create'),
    path('stifftemplatelevelion-delete/<str:pk>',
         StiffTemplateLevelIonDelete.as_view(), name='stifftemplatelevelion-delete'),

    path('radarchart/<str:pk>', radarchartLoad, name="radarchart"),
    path('radarchart-filter/', radarchartFilter, name="radarchart-filter"),

    path('stiffchart/<str:pk>', stiffcharttLoad, name="stiffchart"),
]
