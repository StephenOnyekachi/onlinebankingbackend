from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Users)
admin.site.register(Transactions)
admin.site.register(OTP)

admin.site.register(Currency)
admin.site.register(Account_type)
admin.site.register(Bank)
admin.site.register(Gender)