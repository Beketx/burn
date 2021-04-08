import hashlib
import os

import requests
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
import datetime as dt
from datetime import datetime
from rest_framework.response import Response


class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator
    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'

class ML(APIView):

    def post(self, request):
        data = request.data


        date = datetime.today().strftime('%Y-%m-%d')
        folder = 'media/' + str(date) + 'ml/'
        myfile = request.FILES['document']
        fileName, fileExtension = os.path.splitext(myfile.name)
        myfile.name = 'passport' + hashlib.md5(fileName.encode('utf-8')).hexdigest() + fileExtension
        url_name = 'media/' + str(date) + '/' + str(myfile.name)
        fs = FileSystemStorage(location=folder)
        fileName = fs.save(myfile.name, myfile)
        payload = {
            'document': url_name
        }
        url = 'http://138.68.184.57:5000/compare-faces/'
        result = requests.post(url, data=payload)
        if result.status_code == 200:
            return Response({"Status": 200})
        else:
            return {"Status": 404}


