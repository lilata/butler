from ipware import get_client_ip
from rest_framework.response import Response
from rest_framework.views import APIView


class PingView(APIView):
    def get(self, request):
        ip, is_ip_routable = get_client_ip(request)
        return Response(
            {"pinged_from": ip, "is_ip_routable": is_ip_routable, "path": request.path}
        )

    def post(self, request):
        return self.get(request)
