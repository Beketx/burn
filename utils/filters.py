# import operator
# from functools import reduce
#
# from django.db.models import Q
# from django_filters import rest_framework as filters
# from dry_rest_permissions.generics import DRYPermissionFiltersBase
#
# from developer import models
#
# class DeveloperFilterBackend(DRYPermissionFiltersBase):
#     def filter_list_queryset(self, request, queryset, view):
#         if request.user.is_joined:
#             return queryset
#
#         return queryset.filter(Q(role=request.user.role))
#
# def filter_developer(queryset, name, value):
#     lookups = ['title__icontains']
#     or_queries = []
#     search_terms = value.split()
#
#     for search_term in search_terms:
#         or_queries += [Q(**{lookup: search_term}) for lookup in lookups]
#
#     return queryset.filter(reduce(operator.or_, or_queries))
#
# class DeveloperFilter(filters.FilterSet):
#     title = filters.CharFilter(method=filter_developer)
#
#     class Meta:
#         model = models.Developer
#         fields = [
#             'stacks_id'
#         ]

from django_filters import rest_framework as filters

from developer.models import DeveloperService, Developer


class PriceFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='dev_service__price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='dev_service__price', lookup_expr='lte')


    class Meta:
        model = Developer
        fields = ('dev_service__price', )