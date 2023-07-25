from rest_framework import filters

from essences.models import Favorite


class TagsFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        tags = dict(request.query_params).get('tags')
        if tags is None:
            return queryset.none()
        return queryset.filter(tags__slug__in=tags)


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


