from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.http import HttpResponseRedirect

class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.user_type == "owner":
                if modulename == "owner.views":
                    pass
                elif modulename == 'shop.views' or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("owner:ownerDashboard"))
            elif user.user_type == "customer":
                if modulename == "com.views":
                    pass
                elif modulename == 'shop.views' or modulename == "django.views.static" or  modulename == "django.contrib.auth.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("customer:dashboard"))
        else:
            if modulename == 'shop.views' or modulename == "django.contrib.auth.views" or modulename == "django.views.static":
                pass
            else:
                return HttpResponseRedirect(reverse("shop:login"))


            
    