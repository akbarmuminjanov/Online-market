from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.http import Http404
from django.contrib import messages

class AdminRequiredMixin(AccessMixin):
    redirect_url = "sell_product"
    """Bu mixin foydalanuvchi ekanligini tekshiradi"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and ( request.user.is_superuser or request.user.is_staff ):
            return super().dispatch(request, *args, **kwargs)
            
        messages.error(request, "Ushbu sahifa uchun ruxsatingiz yo'q")
        return redirect(self.redirect_url)
        # raise Http404("this page is not available for you")