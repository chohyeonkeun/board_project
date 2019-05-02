from .views import *

from django.urls import path

app_name = 'photo'

urlpatterns = [
    path('slist/', PhotoSaveList.as_view(), name='slist'),
    path('saved/<int:photo_id>', PhotoSaved.as_view(), name='saved'),
    path('like/<int:photo_id>/', PhotoLike.as_view(), name='like'),
    path('', PhotoList.as_view(), name='index'),
    path('create/', PhotoCreate.as_view(), name='create'),
    path('update/<int:pk>/', PhotoUpdate.as_view(), name='update'),
    path('detail/<int:pk>/', PhotoDetail.as_view(), name='detail'),
    path('delete/<int:pk>/', PhotoDelete.as_view(), name='delete'),
]