import os
from base64 import b64decode
from mimetypes import guess_type

from django.conf import settings
from django.http import StreamingHttpResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers


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


class CommentsView(APIView):
    def get(self, request):
        data = request.query_params
        b64key = data.get("b64key")
        if not b64key:
            key = data.get("key")
            if not key:
                return Response(
                    {"error": "bad key"}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            key = str(b64decode(b64key), "utf-8")
        page = int(data.get("page", 1))
        page_size = int(data.get("page_size", 10))
        return Response({"comments": models.Comment.comments(key, page, page_size)})

    def post(self, request):
        data = serializers.CommentSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response({"detail": "inserted"})


class ProtectedFileView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        data = serializers.ProtectedFileSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        protected_file = data.save()
        return Response(
            {
                "detail": "uploaded",
                "filename": os.path.basename(protected_file.file.name),
            }
        )

    def get(self, request):
        filename = request.query_params.get("filename")
        code = request.query_params.get("code")
        file_obj = models.ProtectedFile.get_file(filename, code)
        if file_obj is not None:
            response = StreamingHttpResponse(
                file_obj.file.chunks(), guess_type(filename)[0]
            )
            response["Content-Disposition"] = f"attachment; filename={filename}"
            return response
        return Response({"error": "404 Not Found"}, status=status.HTTP_404_NOT_FOUND)
