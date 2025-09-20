from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Product, NetworkLink


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date')
    search_fields = ('name', 'model')


@admin.register(NetworkLink)
class NetworkLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'city', 'display_supplier_link', 'debt')
    list_filter = ('city',)
    search_fields = ('name', 'city', 'country')
    actions = ['clear_debt']

    def display_supplier_link(self, obj):
        if obj.supplier:
            link = reverse("admin:network_networklink_change", args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', link, obj.supplier.name)
        return "Нет поставщика"

    display_supplier_link.short_description = "Поставщик"

    @admin.action(description="Очистить задолженность перед поставщиком")
    def clear_debt(self, request, queryset):
        updated_count = queryset.update(debt=0)
        self.message_user(request, f"Задолженность была очищена для {updated_count} объектов.")
