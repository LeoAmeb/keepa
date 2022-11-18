from apps.authentication.models import User


def get_admins():
    return User.objects.filter(is_staff=True).values_list('pk', flat=True)

def is_searcher(user):
    return user.groups.filter(name="searcher").exists()