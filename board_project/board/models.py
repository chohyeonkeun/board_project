from django.db import models

# Create your models here.

class Board(models.Model):
   pass

class Category(models.Model):
   name = models.CharField(max_length=20)
   slug = models.SlugField(max_length=30, db_index=True, unique=True,
                           allow_unicode=True,blank=True)
   # Board를 구현 안했기 때문에 unique 사용 / allow_unicode : 한글 사용 가능하도록 설정
   description = models.CharField(max_length=200, blank=True)
   meta_description = models.CharField(max_length=200, blank=True)
   # meta_description : 검색엔진에 제공해주는 description

   class Meta:
       # DB에 기본적으로 설정될 정렬 값
       ordering = ['slug']

   def __str__(self):
       return self.name


# User 모델을 커스텀할 경우를 위해 get_user_model 사용
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

class Document(models.Model):
   category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='documents')
   author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                              related_name='documents')
   # on_delete=models.SET_NULL : Category 지워진다고 삭제되지 않음
   title = models.CharField(max_length=100)
   slug = models.SlugField(max_length=120, db_index=True, unique= True,
                           allow_unicode=True, blank=True)
   # db_index=True : DB에 인덱싱 가능
   text = models.TextField()
   # upload_to : 동적으로 경로 설정 가능
   image = models.ImageField(upload_to='board_images/%Y/%m/%d')
   created = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now=True)

   def __str__(self):
       return self.title

   def save(self, *args, **kwargs):
       self.slug = slugify(self.title, allow_unicode=True)
       super(Document, self).save(*args, **kwargs)

   def get_absolute_url(self):
       return reverse('board:detail', args=[self.id])

class Comment(models.Model):
   # Todo : 댓글 남기기를 위해서 Form
   # Todo : 뷰는
   document = models.ForeignKey(Document, on_delete=models.CASCADE,related_name='comments')
   author = models.ForeignKey(get_user_model(),on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
   text = models.TextField()
   created = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now=True)
   like = models.IntegerField(default=0) # ManyToMany
   dislike = models.IntegerField(default=0)

   def __str__(self):
       return (self.author.username if self.author else "무명") + "의 댓글"

   class Meta:
       ordering = ['-id']