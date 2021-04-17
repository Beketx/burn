from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ClientContactDev(APIView):
    """
    {
    dev_id:123
    }
    """
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        data = request.data
        user = request.user
        print(user.id)
        return Response("one")