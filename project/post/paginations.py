from rest_framework.pagination import PageNumberPagination


class PostPageNumberPagination(PageNumberPagination):
    page_size = 2

    # def get_paginated_response(self, data):
    #     print("@@@@@@@@@@@")
    #     print(data)
    #     return Response({
    #         'count': self.page.paginator.count,
    #         'results': data
    #     })
