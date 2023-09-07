from recipes.models import Favorite, Shoppingcart
from rest_framework import filters


class AuthorFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        author = request.query_params.get('author')
        if author is None:
            return queryset
        return queryset.filter(author__id=author)


class FavoritedFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        is_favorited = request.query_params.get('is_favorited')
        if is_favorited is None:
            return queryset
        if is_favorited == '1':
            recipes_id = Favorite.objects.filter(
                siteuser=request.user).values('recipe__id')
            if not recipes_id:
                return queryset.none()
            else:
                return queryset.filter(id__in=recipes_id)
        else:
            return queryset


class ShoppingCartFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        in_shopcart = request.query_params.get('is_in_shopping_cart')
        if in_shopcart is None:
            return queryset
        if in_shopcart == '1':
            recipes_id = Shoppingcart.objects.filter(
                siteuser=request.user).values('recipe__id')
            if not recipes_id:
                return queryset.none()
            else:
                return queryset.filter(id__in=recipes_id)
        else:
            return queryset


class TagsFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        params_tags = dict(request.query_params).get('tags')
        if params_tags is None:
            return queryset
        q = queryset.filter(tags__slug__in=params_tags)
        return q.union(q)
