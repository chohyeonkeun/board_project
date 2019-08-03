from django.urls import path
from .views import document_list, document_create, document_delete, document_detail, \
    document_update, comment_create, comment_update, comment_delete
from .views import get_data_ajax

app_name = 'board'

urlpatterns = [
    path('', document_list, name='list'),
    path('create/', document_create, name='create'),
    path('update/<int:document_id>', document_update, name='update'),
    path('delete/<int:document_id>', document_delete, name='delete'),
    path('detail/<int:document_id>', document_detail, name='detail'),
    path('comment/create/<int:document_id>', comment_create, name='comment_create'),
    path('comment/update/<int:comment_id>', comment_update, name='comment_update'),
    path('comment/delete/<int:comment_id>', comment_delete, name='comment_delete'),
    path('ajax/get_data/', get_data_ajax, name='get_data_ajax'),
    # 클래스형뷰에서는 pk로 받아서 <int:pk>로 설정해준다.
]