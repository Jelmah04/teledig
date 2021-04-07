from web.models import *
from django.contrib import admin

# Register your models here.

class AirtimeHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'transaction_id', 'network', 'mobile_number', 'amount', 'status', 'date')
    list_display_links = ('user', 'transaction_id', 'network', 'mobile_number', 'amount', 'status', 'date')
    list_filter = ('id', 'user', 'transaction_id', 'network', 'mobile_number', 'amount', 'status', 'date')
    list_per_page = 20
    search_fields = ('user', 'transaction_id', 'network', 'mobile_number', 'amount', 'status', 'date')

class DataHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'transaction_id', 'network', 'plan', 'mobile_number', 'amount', 'status', 'date')
    list_display_links = ('user', 'transaction_id', 'network', 'plan', 'mobile_number', 'amount', 'status', 'date')
    list_filter = ('id', 'user', 'transaction_id', 'network', 'plan', 'mobile_number', 'amount', 'status', 'date')
    list_per_page = 20
    search_fields = ('user', 'transaction_id', 'network', 'plan', 'mobile_number', 'amount', 'status', 'date')



admin.site.register(AirtimeHistory, AirtimeHistoryAdmin)
admin.site.register(DataHistory, DataHistoryAdmin)


admin.site.register(User)
admin.site.register(UserWallet)
admin.site.register(Contactinfo)
admin.site.register(UserSettings)
admin.site.register(PayHistory)
admin.site.register(AlertVerify)
admin.site.register(UserPassToken)
admin.site.register(Notification)
admin.site.register(UserNotification)
admin.site.register(ManualFunding)