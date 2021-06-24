import hashlib
import json
import os
import requests
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
import datetime as dt
from datetime import datetime
from rest_framework.response import Response

from developer.models import DeveloperImages
from utils.serializers import DevAvatarsSerializer


class ML(APIView):

    parser_classes = (MultiPartParser, )

    def post(self, request):
        print(request)
        try:
            data = request.data
            date = datetime.today().strftime('%Y-%m-%d')
            folder = 'media/' + str(date) + 'ml/'
            x = request.FILES
            myfile = x['document']
            fileName, fileExtension = os.path.splitext(myfile.name)
            myfile.name = 'passport' + hashlib.md5(fileName.encode('utf-8')).hexdigest() + fileExtension
            url_name = 'media/' + str(date) + '/' + str(myfile.name)
            fs = FileSystemStorage(location=folder)
            fileName = fs.save(myfile.name, myfile)
            y = DeveloperImages.objects.all()[:1].get()
            payload = {
                'document': y.image
            }
            url = 'http://138.68.184.57/compare-faces'
            result = requests.post(url, files=payload)
            if result.status_code == 200:
                for i in result:
                    x = str(i)
                    y = x.split(" ")
                print(json.dumps(y[0]))
                return Response(y)
            else:
                return Response({"Status": 404})
        except Exception as e:
            return Response(str(e))

class MLViewSet(viewsets.ModelViewSet):
    queryset = DeveloperImages.objects.all()
    serializer_class = DevAvatarsSerializer
    parser_classes = (MultiPartParser, )

