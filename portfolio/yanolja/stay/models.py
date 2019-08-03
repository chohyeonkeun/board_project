from django.db import models

from django.contrib.auth import get_user_model

from multiselectfield import MultiSelectField

from datetime import date, timedelta

class Category(models.Model):
    staying = models.CharField(max_length=50)  # 모텔, 호텔/리조트, 펜션/풀빌라, 게스트하우스



SERVICE_CHOICES = (
    # 호텔
    (1, '주차가능'),
    (2, '레스토랑'),
    (3, '부페'),
    (4, '커피숍'),
    (5, '유료세탁'),
    (6, '24시간데스크'),
    (7, '객실금연'),
    (8, '수화물보관'),
    (9, '연회장'),
    (10, '어메니티'),
    (11, '비즈니스'),
    (12, '피트니스'),
    (13, '와이파이'),
    (14, '조식운영'),
    (15, '야외수영장'),
    (16, '스파/월풀'),
    (17, '야외테라스'),
    (18, '공항셔틀'),
    (19, '바'),
    (20, '수영장'),
    (21, '사우나'),
    (22, '주방'),
    # 모텔
    (23, '파티룸'),
    (24, 'VOD'),
    (25, '노트북대여'),
    (26, '트윈베드'),
    (27, '커플PC'),
    (28, '무인텔'),
    (29, '객실내PC'),
    (30, '무료영화'),
    (31, '동물입실'),
    (32, '안마의자'),
    (33, '거울룸'),
    (34, '글램핑'),
    (35, '복층구조'),
    # 펜션
    (36, '바베큐'),
    (37, '해수욕장인근'),
    (38, '개별바베큐'),
    (39, '상비약'),
    (40, '워터슬라이드'),
    (41, '이벤트가능'),
    (42, '독채객실'),
    (43, '계곡인접'),
    (44, '족구장'),
    (45, '축구장'),
    (46, '기본양념'),
)

class Stay(models.Model):
    # name 앞에 city 이름 붙일 것(ex. '강남', '역삼', '선릉')
    # 나중에 프론트단에서 카테고리(강남/역삼/삼성/논현 클릭 시,
    # name에서 해당 city 쿼리셋하거나
    # location 위치정보를 이용하여 해당 위치의 숙소 쿼리셋 실시시    name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="stays")
    # 숙소 위치
    # map api 이용하여 location 선택 시, 서울특별시 강남구 봉은사로 428 같이 띄워주는 방법 구상
    # 정 안되면, 텍스트 형식으로 진행

    location = models.CharField(max_length=100) # ex) 서울특별시 강남구 봉은사로 428

    # 건물 지어진 날짜
    built_date = models.DateField(auto_now=False)

    # 리모델링된 날짜
    remodeled_date = models.DateField(auto_now=False)

    # 프렌차이즈 여부
    check_franchise = models.BooleanField(default=False)

    # 신축/리모델링 여부(유동적 -> 설정한지 1년 지나면 자동 해제)
    check_new_or_remodeling = models.BooleanField(default=False)

    # 숙소 소개
    introduce = models.TextField()

    # 초특가호텔 (호텔 사장이 당일특가로 가격 40% 이상 할인 시,)
    # ForeignKey로 연결되어 있는 Room 모델에서 초특가호텔 여부 확인

    # 편의시설 및 서비스
    service_kinds = MultiSelectField(choices=SERVICE_CHOICES, null=True, blank=True)

    # 편의시설 및 서비스 설명
    service_introduce = models.TextField(default="")

    # 이용안내
    service_notice = models.TextField()

    # 픽업안내
    pickup_notice = models.TextField(default="")

    # 찾아오시는 길
    directions = models.TextField(default="")


class Image(models.Model):
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE, related_name="images_stay")
    image = models.ImageField(upload_to='room_image/%Y/%m/%d', blank=False)

    def __str__(self):
        return self.stay.name + "image"

# room --> 멀티 이미지 구현 필요
class Room(models.Model):
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE, related_name="rooms")

    name = models.CharField(max_length=50)

    reserved = models.ManyToManyField(get_user_model(), related_name="reserved")
    # 예약 가능 여부 (views에서 결과에 따라 예약가, 현장결제가 분기할 것)
    check_reservation = models.BooleanField(default=True)

    # 대실 이용시간(ex. 3시간)
    hours_available = models.IntegerField(default=0)
    # 숙박 체크인 가능 시간, 체크아웃 시간
    days_checkin = models.IntegerField(default=0)
    days_checkout = models.IntegerField(default=0)

    # 대실 예약가
    price_hours_reserve = models.IntegerField(default=0)
    # 숙박 예약가
    price_days_reserve = models.IntegerField(default=0)


    # 대실 현장결제가
    price_hours_not_reserve = models.IntegerField(default=0)
    # 숙박 현장결제가
    price_days_not_reserve = models.IntegerField(default=0)

    # 페이지에서 가격 표시할 때, 당일특가 입력되어있으면 표시하고, 없으면 일반 가격 표시
    # 당일특가 할인율((price - 당일특가)//price)*100 표기
    sprice_a_few_hours = models.IntegerField(default=0)
    sprice_a_day = models.IntegerField(default=0)


    basic_info = models.TextField(default="")
    reservation_notice = models.TextField(default="")
    cancel_regulation = models.TextField(default="")

class Check_in_out(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name="checks")
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="checks")
    check_in = models.DateField(auto_now=False)
    check_out = models.DateField(auto_now=False)

class Comment(models.Model):
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="comments")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent_comment_id = models.IntegerField(default=0)

    evaluation_items1 = models.IntegerField(default=5) # 평가항목 별 점수 선택
    evaluation_items2 = models.IntegerField(default=5)
    evaluation_items3 = models.IntegerField(default=5)
    evaluation_items4 = models.IntegerField(default=5)