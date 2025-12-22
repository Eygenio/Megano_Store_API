from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer

class CategoriesListAPIView(APIView):
    def get(self, request):
        queryset = (
            Category.objects
            .filter(parent__isnull=True)
            .select_related("image")
            .prefetch_related("subcategories__image")
        )

        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)



# def perform_create(self, serializer):
#     user = self.request.user
#     serializer.save(
#         user=user,
#         author=user.fullname,
#         email=user.email
#     )