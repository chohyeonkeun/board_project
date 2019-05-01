from django.db import models

# Create your models here.
# 모델의 형태 - 클래스

class Bookmark(models.Model):
    site_name = models.CharField(max_length=50)
    url = models.URLField()  # character type 으로 입력받는다
    contents = models.TextField(blank=True)
    # 작성자 -> 로그인한 유저 정보를 찾아서 추가
    # 작성자가 로그인한 유저인지 알 수 없음
    # -> 모델 저장 직전에 직접 코드로 처리

    # 작성일 -> 서버 시간을 읽어서 timestamp값을 만들어 추가
    # 자동 옵션 auto_now, auto_now_add
    created = models.DateTimeField(auto_now_add=True)
    # auto_now_add : 처음 저장 될때의 시간을 자동으로 처리 --> 갱신을 할때마다 저장해줌

    # DB에 적용 : makemigrations, migrate
    # python3 manage.py makemigrations bookmark
    # python3 manage.py migrate bookmark 0001

    # 관리자 페이지 목록에 표시될 내용
    # 확인 메시지에 출력되는 내용을 만들기 위해
    def __str__(self):
        return "Site name : " + self.site_name + " (URL : " + self.url +")"

    # 모델 클래스가 수정됐다고 해서 항상 migrate 해야 하는 것은 아니다.
    # DB에 변경 사항이 반영되어야 할 항목들만 migrate를 한다.

    # 메타 클래스는 옵션 클래스 - 내가 상속을 받았는데, 속성값에 변경이 필요하다면
    class Meta:
        # 정렬 : 필드이름 -> 필드값 오름차순, -필드이름 -> 필드값 내림차순
        ordering = ['-id']
    # class Meta --> DB에 저장 필요