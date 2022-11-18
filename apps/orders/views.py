# Django
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, View, UpdateView, CreateView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import formset_factory
from django.views.generic.detail import SingleObjectMixin

# Apps
from apps.orders.models import Order
from apps.orders.filters import OrderFilter
from apps.orders.forms import PurchaseForm
from apps.clients.models import Budget, Client, Purchase


class OrderListView(LoginRequiredMixin, ListView):
    """ListView"s Orders"""
    model = Order
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "orders"
        context["filters"] = OrderFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return OrderFilter(self.request.GET, queryset=queryset).qs


class OrderDetailView(LoginRequiredMixin,DetailView):
    """DetailView"s Orders"""
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "orders"
        context["order"] = self.get_object()
        context["budgets"] = self.get_budgets()
        return context

    def get_budgets(self):
        order = self.get_object()
        return order.purchases.all()


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    """View to make purchase to a client"""
    model = Purchase
    form_class = PurchaseForm
    template_name = "orders/order_purchase_form.html"

    def get_absolute_url(self):
        return reverse("orders:order-detail", kwargs={"pk":self.kwargs.get('pk')})

    def get_order(self):
        return get_object_or_404(Order, pk=self.kwargs.get('pk'))

    def get_initial(self):
        order = self.get_order()
        return {'order': order}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = self.get_initial()
        context["order"] =  data["order"]
        context["segment"] = "clients"
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        client = form.cleaned_data.get("client")
        budget = client.budgets.last()
        purchase = form.save(commit=False)
        purchase.budget = budget
        self.object = purchase.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse("order-detail", kwargs={"pk": self.kwargs.get('pk')})


class DeletePurchaseView(LoginRequiredMixin, DeleteView):
    # specify the model you want to use
    model = Order
    success_url = "order-detail"
    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        budget = get_object_or_404(Purchase, pk=self.kwargs.get('pk_purchase'))
        budget.delete()
        messages.success(request, "Assigment correctly deleted")
        return HttpResponseRedirect(reverse("order-detail", kwargs={"pk": self.object.pk}))


class BoughtPurchaseView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        budget = get_object_or_404(Purchase, pk=self.kwargs.get('pk_purchase'))
        budget.confirm = True
        budget.save()
        messages.success(request, "Assigments correctly created")
        return HttpResponseRedirect(reverse("order-detail", kwargs={"pk": order.pk}))
