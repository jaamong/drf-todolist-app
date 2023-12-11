from django.db import models


# 모델 생성 시마다 유사한 필드를 적용해야할 때 TrackingModel 사용
# 장고 모델 객체가 생성되거나 업데이트 될 때 등 대부분의 항목이 공통적으로 적용됨
# 모델 helper를 생성하여, 모델을 생성할 때 세부 정보를 한 번에 빠르게 추가할 수 있음
class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 자식과 부모의 상속관계는 실제로 없는 것.
        # 부모 모델은 실제로 존재하지 않는 가상의 클래스가 됨
        # 자식 모델은 부모 필드의 속성과 함수를 물려받으며, 실체가 있는 DB 테이블이 됨
        abstract = True

        # set up ordering by created_at descending
        ordering = ('-created_at', )
