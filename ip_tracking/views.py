from django.http import JsonResponse
from ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='10/m', method='POST', block=True)
@ratelimit(key='ip', rate='5/m', method='POST', block=True, group='anon')
def login_view(request):
    if request.method == "POST":
        return JsonResponse({"status": "success", "msg": "Login logic placeholder"})
    return JsonResponse({"detail": "Only POST allowed"}, status=405)
