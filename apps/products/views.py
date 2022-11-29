# Django
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, View, UpdateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
# Apps
from apps.products.models import Product, ProductEntry
from apps.products.forms import ProductForm, ProductEntryCreateForm, ProductEntryUpdateForm, ProductEntryApproveForm
from apps.products.filters import ProductFilter, ProductEntryFilter
# Utils
from utils.users import get_admins, is_searcher
from utils.mixins import Permissionmixin


class ProductListView(LoginRequiredMixin, ListView):
    """ListView"s Products"""
    model = Product
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "products"
        context["filters"] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return ProductFilter(self.request.GET, queryset=queryset).qs


class ProductView(LoginRequiredMixin, View):
    """View to create or update a product"""

    def get(self, request, *args, **kwargs):
        context = {
            "product_form": ProductForm(None),
            "segment": "products"
        }
        return render(request, "products/product_create.html", context)
    
    def post(self, request, *args, **kwargs):
        instance = self.get_product(request.POST["asin"])
        product_form = ProductForm(request.POST, instance=instance)

        if product_form.is_valid():
            # Create or Update product
            product, created = product_form.save()

            if created:
                message = "Created correctly"
            else:
                message = "Updated correctly"
 
            messages.success(request, message)
            context = {
                "product_form": ProductForm(None),
                "segment": "products",
            }            
            return render(request, "products/product_create.html", context)
        else:
            context = {
                "product_form": ProductForm(request.POST),
                "segment": "products",
            }            
            for error, message in product_form.errors.items():
                messages.success(request,  message[0])
            return render(request, "products/product_create.html", context)

    def get_product(self, asin):
        if Product.objects.filter(asin=asin).exists():
            return Product.objects.get(asin=asin)
        return None


class ProductDetailView(LoginRequiredMixin,DetailView):
    """DetailView"s Product"""
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "products"
        return context


class ProductEntryListView(LoginRequiredMixin, ListView):
    """LisView"s Product Entry"""
    model = ProductEntry
    paginate_by = 50
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "products_entries"
        context["filters"] = ProductEntryFilter(
            self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # If the user is searchers only display the products entries
        # registred by.
        if is_searcher(self.request.user):
            queryset = queryset.filter(searcher=self.request.user)
        return ProductEntryFilter(self.request.GET, queryset=queryset).qs


class ProductEntryCreateView(LoginRequiredMixin, View):
    """View to create a Product Entry"""

    def get(self, request, *args, **kwargs):
        context = {
            "product_form": ProductForm(None),
            "product_entry_form": ProductEntryCreateForm(None),
            "segment": "products_entries"
        }
        return render(request, "products/productentry_create.html", context)

    def post(self, request, *args, **kwargs):
        instance = self.get_product(request.POST["asin"])
        product_form = ProductForm(request.POST, instance=instance)
        product_entry_form = ProductEntryCreateForm(request.POST)
        context = {
            "product_form": product_form,
            "product_entry_form": product_entry_form,
            "segment": "products_entries",
        }
        if product_form.is_valid() and product_entry_form.is_valid():
            # Create or Update product
            product, created = product_form.save()

            # Create Product Entry
            product_entry = product_entry_form.save(commit=False)
            product_entry.product = product
            product_entry.searcher = request.user
            product_entry.total_amount = product_entry.quantity * product_entry.buy_amount_per_piece
            product_entry.save()
            messages.success(self.request, "Product Entry Created Correctly")
            context.update({"product_form": ProductForm(None)})
            context.update({"product_entry_form": ProductEntryCreateForm(None)})
        else:
            messages.error(request, "Something was wrong. {} {}".format(product_form.errors, product_entry_form.errors))

        return render(request, "products/productentry_create.html", context=context)

    def get_product(self, asin):
        if Product.objects.filter(asin=asin).exists():
            return Product.objects.get(asin=asin)
        return None


class ProductEntryDetailView(LoginRequiredMixin, UserPassesTestMixin ,DetailView):
    model = ProductEntry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "products"
        context["product_entry"] = self.object
        return context

    def test_func(self):
        user = self.request.user
        product_entry = self.get_object()
        if is_searcher(user) and product_entry.searcher != user:
            return False
        return True


class ProductEntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """UpdateView"s Product Entry"""
    model = ProductEntry
    template_name_suffix = "_detail"
    form_class = ProductEntryUpdateForm
    success_url = "product-entry-detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_entry"] = self.get_object()
        context["edit"] = True
        context["update"] = True
        return context
    
    def form_valid(self, form):
        form.instance.total_amount = form.instance.buy_amount_per_piece * form.instance.quantity 
        messages.success(self.request, "Product entry updated correctly")
        super().form_valid(form)
        return HttpResponseRedirect(reverse(self.get_success_url(), kwargs={"pk": self.kwargs["pk"]}))
    
    def test_func(self):
        user = self.request.user
        product_entry = self.get_object()
        if is_searcher(user) and product_entry.searcher != user:
            return False
        return True


class ProductEntryApproveUpdateView(Permissionmixin, UpdateView):
    """View to Approve a Product Entry"""
    model = ProductEntry
    template_name_suffix = "_detail"
    form_class = ProductEntryApproveForm
    success_url = "product-entry-detail"
    permission_required = "products.can_approve"

    def form_valid(self, form):
        super().form_valid(form)
        product_entry = self.object

        if product_entry.status == "approved":        
            product_entry.orders.create(
                store = product_entry.store,
                link_store = product_entry.link_store,
                buy_amount_per_piece = product_entry.buy_amount_per_piece,
                observations = product_entry.observations,
                quantity = product_entry.quantity,
                total_amount = product_entry.total_amount,
            )
            messages.success(self.request, "Product entry approved")
            messages.success(self.request, "Order created")

        if product_entry.status == "rejected":
            messages.success(self.request, "Product entry rejected")

        if product_entry.status == "pending":
            messages.success(self.request, "Product entry updated")

        return HttpResponseRedirect(reverse(self.get_success_url(), kwargs={"pk": self.kwargs["pk"]}))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_entry"] = self.get_object()
        context["edit"] = True
        context["approve"] = True
        return context

    def get_initial(self):
        return {"status": "approved"}
