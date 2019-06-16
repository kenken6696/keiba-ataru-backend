from django.urls import path
from .views import MemoList

urlpatterns = [
    path('', MemoList.as_view()),
]