from storages.backends.s3boto3 import S3Boto3Storage
class MediaStorage(S3Boto3Storage):
    location = 'media'
    bucket_name = 'images.wpsshool.site'
    custom_domain = 'images.wpsshool.site'
    file_overwrite = False

# S3 > images.wpsshool.site 버킷에 media라는 폴더로 미디어 파일 생성