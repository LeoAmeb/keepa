from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.authentication.models import User
from apps.clients.models import Budget, Client
from apps.clients.forms import ClientForm, BudgetForm
from apps.clients.filters import ClientFilter


class ClientListView(LoginRequiredMixin, ListView):
    """View to List all the clients"""
    model = Client
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "clients"
        context["filters"] = ClientFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return ClientFilter(self.request.GET, queryset=queryset).qs


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = "clients"
        return context


class ClientView(View):
    """View to create a client"""
    form_class = ClientForm
    success_url = reverse_lazy('clients')
    fail_url = reverse_lazy('clients-add')
    tamplate_name = 'clients/client_create.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.tamplate_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.create_objects(form, request.user)
            messages.success(self.request, "User correctly created.")
            messages.success(self.request, "Budget correctly created.")
            messages.success(self.request, "Email send to the new user.")
            context = self.get_context_data()
            return redirect(to=self.success_url, kwargs={'context': context})
        else:
            context = self.get_context_data()
            context.update({'client_form': self.form_class(request.POST)})
            for error, message in form.errors.items():
                messages.error(self.request, "{}".format(message[0]))
            return render(request, self.tamplate_name, context)

    def get_context_data(self,*args, **kwargs):
        context = dict()
        context["client_form"] = self.form_class(data=None)
        context["segment"] = "clients"
        return context        

    def create_objects(self, form, user_created):
        """Method to create objects of a client"""
        # Generate random password
        password = User.objects.make_random_password()
        
        # Create User
        user = User.objects.create(
            email=form.cleaned_data.get('email'),
            username=form.cleaned_data.get('username'),
            first_name=form.cleaned_data.get('first_name'),
            last_name=form.cleaned_data.get('last_name')
        )
        # Set Password to the user
        user.set_password(password)
        user.save()

        # Create a Client
        client = Client.objects.create(user=user, created_by=user_created)

        # Create the budget
        client.budgets.create(
            total_amount=form.cleaned_data.get('budget'),
            amount=form.cleaned_data.get('budget'),
            created_by=user_created
        )

        # Send Email with credentials
        message = "A user was created in Keepa System. Your credentials are Email: {} | Password: {}".format(client.user.email, password)
        send_mail("Keepa System | User Created", message, "send@test.com", [client.user.email], fail_silently=False)

        return client


class ClientBudgetCreateView(CreateView):
    """View to create budget's client"""
    model = Budget
    form_class = BudgetForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.total_amount = form.cleaned_data.get('amount')
        messages.success(self.request, "Budget created correctly.")
        return super().form_valid(form)

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        kwargs.update({'client_id': self.get_client().id })
        return kwargs

    def get_initial(self):
        client = self.get_client()
        return {'client': client}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = self.get_initial()
        context["client"] =  data["client"]
        context["segment"] = "clients"
        return context
    
    def get_client(self):
        return get_object_or_404(Client,  pk=self.kwargs.get('pk'))
    
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return '/clients/{}'.format(self.get_client().id)
