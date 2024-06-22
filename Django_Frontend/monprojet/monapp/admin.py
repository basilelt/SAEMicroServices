from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Client)
admin.site.register(Staff)
admin.site.register(StaffType)
admin.site.register(Group)
admin.site.register(ClientGroups)
admin.site.register(StaffGroups)
admin.site.register(Permission)
admin.site.register(ClientPermissions)
admin.site.register(StaffPermissions)
admin.site.register(Flight)
admin.site.register(Plane)
admin.site.register(Booking)
admin.site.register(BookingType)
admin.site.register(Working)
admin.site.register(Airport)
admin.site.register(Track)
