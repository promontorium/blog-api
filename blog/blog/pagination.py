from rest_framework import pagination


class MaxLimitOffsetPagination(pagination.LimitOffsetPagination):
    max_limit = pagination.LimitOffsetPagination.default_limit
