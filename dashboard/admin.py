from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import District, Sector, KPI, Department, Umuryango, Cell, Village

admin.site.register(District)
admin.site.register(Sector)
admin.site.register(KPI)
admin.site.register(Department)
admin.site.register(Umuryango)
admin.site.register(Village)
admin.site.register(Cell)
# admin.site.register(Umuryang)


############################# importing and exporting data in admin panel ######################################
# @admin. register(Umuryango)
# class UmuryangoAdmin(ImportExportModelAdmin):
#     pass
