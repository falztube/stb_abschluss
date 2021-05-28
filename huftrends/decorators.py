from django.http import HttpResponse
from django.shortcuts import redirect


#diese Funktion "unauthenticated_user" ersetzt die user authentication 
# in dem login_view. vor dem login_view wird diese funktion aufgerufen und ausgeführt
#nach der ausführung wird die login_view wieder aufgerufen und ausgeführt (falls)
#wenn der user bereits authentifiziert (eingeloggt) ist, kann er die login seite nicht mehr aufrufen.
#stattdessen wird er zur "home" (was auch immer als home definiert ist) "redrirected"
# ist er nicht authentifiziert gehts zur login seite

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None 
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                 return redirect('/home')
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator

