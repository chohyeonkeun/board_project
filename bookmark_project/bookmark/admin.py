from django.contrib import admin

# Register your models here.
# 관리자 페이지에서 관리할 모델을 등록
# 관리자 페이지를 커스터마이징

# 옵션 클래스

from .models import Bookmark
# Register your models here.

class BookmarkOptions(admin.ModelAdmin):
    list_display = ['id', 'site_name', 'url']
    # list_editable = ['site_name', 'url']   # 목록에서 값 변경하는 건 위험할 수 있다.
    # list_filter = ['url']   # 대부분 DateTime 필드가 있을 경우 많이 사용
    search_fields = ['site_name', 'url']  # ForeignKey 필드와 같이 다른 테이블을 참조하는 항목은 사용하지 않는다.
    # raw_id_fields : 선택값 -> 입력값
    # 관리자 페이지에 커스텀 페이지 추가
    # 관리자 페이지에 action 추가
    #


admin.site.register(Bookmark, BookmarkOptions)