from django.shortcuts import render, redirect

def error_404(request, exception):
    data = {}
    data['error'] = "404 Page Not Found"
    return render(request, 'templates/pacApp/404.html', data)


def error_500(request):
    data = {}
    data['error'] = "500 Internal Server Error"
    return render(request, 'templates/pacApp/404.html', data)