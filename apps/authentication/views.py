from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from apps.authentication.forms import LoginForm, SignUpForm, PasswordResetFormCustom, SetPasswordFormCustom
from apps.authentication.models import User
from apps.authentication.filters import UserFilter


# ================ View's Login ================
class LoginView(auth_views.LoginView):
    """View to Login using AuthViews"""
    template_name = "authentication/login.html"
    redirect_authenticated_user = True
    form_class = LoginForm

    def form_invalid(self, form):
        """Function to send error messages"""
        for message in form.error_messages:
            messages.error(self.request, form.error_messages[message])
        return super().form_invalid(form)


class LogoutView(auth_views.LogoutView):
    """View to Logout"""
    pass

class SignUpView(LoginRequiredMixin, CreateView):
    """View to register a user"""
    template_name = "authentication/signup.html"
    success_url = reverse_lazy("signup")
    form_class = SignUpForm

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        # Save the user and make random password
        self.object = form.save(commit=False)
        password = User.objects.make_random_password()
        self.object.set_password(password)
        self.object.save()

        # Send Email with credentials
        message = "A user was created in Keepa System. Your credentials are Email: {} | Password: {}".format(self.object.email, password)
        send_mail("Keepa System | User Created", message, "send@test.com", [self.object.email], fail_silently=False)

        # Send front messages of success
        messages.success(self.request, "User correctly created.")
        messages.success(self.request, "Email send to the new user.")

        return super().form_valid(form)


class UserListView(LoginRequiredMixin, ListView):
    """ListView to list users"""
    model = User
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "authentication"
        context["filters"] = UserFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return UserFilter(self.request.GET, queryset=queryset).qs


class UserDetailView(LoginRequiredMixin,DetailView):
    """DetailView"s User"""
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "authentication"
        return context



# ================ View's Password Reset ================
class PasswordResetView(auth_views.PasswordResetView):
    """View to send mail to change the password"""
    template_name = "accounts/password_reset_form.html"
    form_class = PasswordResetFormCustom


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """ View to show a success message for the above """
    template_name = "accounts/password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """ View to checks the link the user clicked and prompts for a new password """
    template_name = "accounts/password_reset_confirm.html"
    form_class = SetPasswordFormCustom

    def form_invalid(self, form):
        for message in form.error_messages:
            messages.error(self.request, form.error_messages[message])
        return super().form_invalid(form)


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """ View to show a success message for the above """
    template_name = "accounts/password_reset_complete.html"


# =================== Views Error's Manage ===================
class Error400TemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home/page-400.html"


class Error403TemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home/page-403.html"


class Error404TemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home/page-404.html"


class Error500TemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home/page-500.html"

    @classmethod
    def as_error_view(cls):
        v = cls.as_view()
        def view(request):
            r = v(request)
            r.render()
            return r
        return view


# def register_user(request):
#     msg = None
#     success = False

#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             raw_password = form.cleaned_data.get("password1")
#             user = authenticate(username=username, password=raw_password)

#             msg = 'User created - please <a href="/login">login</a>.'
#             success = True

#             # return redirect("/login/")

#         else:
#             msg = 'Form is not valid'
#     else:
#         form = SignUpForm()

#     return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
