from rest_framework import filters


class IsPostComment(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(post=view.kwargs.get("post_id"))
