from .views import PhotoList, PhotoCreate, PhotoUpdate, PhotoDetail, PhotoDelete

from django.urls import path

app_name = 'photo'

urlpatterns = [
    path('', PhotoList.as_view(), name='index'),
    path('create/', PhotoCreate.as_view(), name='create'),
    path('update/<int:pk>/', PhotoUpdate.as_view(), name='update'),
    path('detail/<int:pk>/', PhotoDetail.as_view(), name='detail'),
    path('delete/<int:pk>/', PhotoDelete.as_view(), name='delete'),
]