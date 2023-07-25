from rest_framework import filters

from essences.models import Favorite


class TagsFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        print('>>>', queryset.exists())
        tags = dict(request.query_params).get('tags')
        return queryset.filter(tags__slug__in=tags)


class FavoritedFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        is_favorited = request.query_params.get('is_favorited')
        print('>>> is_favorited:', repr(is_favorited))
        if is_favorited is None:
            return queryset
        if is_favorited == '1':
            print('>>> is_favorited:', is_favorited)
            recipes_id = Favorite.objects.filter(
                siteuser=request.user).values('recipe__id')
            print('>>> recipes_id:', recipes_id)
            queryset.filter(id__in=recipes_id)
            print('>>> queryset:', queryset)
#            return queryset.filter(id__in=request.user.favorites.values())
            return queryset
        else:
            return queryset


