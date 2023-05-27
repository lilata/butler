from django.conf import settings
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models


class ShortenerRedirectView(APIView):
    def get(self, request, alias=None):
        if not alias:
            return Response(
                {"error": "404 Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            surl = models.ShortenedURL.objects.get(alias=alias)
        except models.ShortenedURL.DoesNotExist:
            return Response(
                {"error": "404 Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
        return redirect(surl.url)


class ShortenerView(APIView):
    def post(self, request):
        url = request.data.get("url", request.query_params.get("url"))
        if not url:
            return Response({"error": "Bad url."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            resp_url = (
                settings.SHORTENER_PREFIX_URL + models.ShortenedURL.add_url(url).alias
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"url": resp_url})
