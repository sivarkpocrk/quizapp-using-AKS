from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Health endpoints — exempted from CSRF as these are typically accessed anonymously
@csrf_exempt
def health_check(request):
    return HttpResponse("OK", status=200)

@csrf_exempt
def readiness_check(request):
    return JsonResponse({"status": "ready"}, status=200)

@csrf_exempt
def liveness_check(request):
    return JsonResponse({"status": "alive"}, status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('questions/', include('questions.urls')),
    path('analytics/', include('analytics.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),

    # Health probe endpoints
    path('health', health_check),
    path('health/', health_check),
    path('healthz/readiness', readiness_check),
    path('healthz/liveness', liveness_check),
]
