from rest_framework import generics
from .models import Memo
from .serializer import MemoSerializer

# Create your views here.
class MemoList(generics.ListAPIView):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer