import logging

from django.db import connection
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def health(request):
    """Liveness plus a real database round trip. 200 when both answer, 503 otherwise."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        logger.exception("health check: database unreachable")
        return Response({"status": "error", "db": "error"}, status=503)
    return Response({"status": "ok", "db": "ok"})
