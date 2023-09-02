from django.shortcuts import redirect

def auth_middleware(get_response):

    def middleware(request):
        if not request.user.id:
            return redirect("/login")
        response = get_response(request)
        return response


    return middleware