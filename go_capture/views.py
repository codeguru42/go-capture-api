from django.http import HttpResponse


def capture(request):
    html = "<html><body>Hello, World!</body></html>"
    return HttpResponse(html)
