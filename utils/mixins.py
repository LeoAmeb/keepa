from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class Permissionmixin(LoginRequiredMixin, PermissionRequiredMixin):
    pass
