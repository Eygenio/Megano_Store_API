# from app.basket.models import Basket
# from app.catalog.models import Product
#
#
# def get_basket_items(request):
#     if request.user.is_authenticated:
#         return list(
#             Basket.objects
#             .filter(user=request.user)
#             .select_related("product", "product__category")
#             .prefetch_related("product__images", "product__tags")
#         )
#     session_basket = request.session.get("basket", {})
#     if not session_basket:
#         return []
#
#     products = Product.objects.filter(id__in=session_basket.keys()).select_related("category").prefetch_related("images", "tags")
#
#     items = []
#     for product in products:
#         count = session_basket[str(product.id)]["count"]
#         product.count_in_basket = count
#         items.append(product)
#
#     return items
