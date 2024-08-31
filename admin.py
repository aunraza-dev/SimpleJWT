from django.contrib import admin
from .models import *

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('pricingModel', 'subscription', 'price', 'description', 'button_text')
    search_fields = ('pricingModel', 'subscription', 'description')

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'plan')
    search_fields = ('title',)
    list_filter = ('plan',)

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display= ('fullName', 'email', 'message')

@admin.register(BuyPackage)
class BuyPackageAdmin(admin.ModelAdmin):
    list_display = ('email', 'message')
    