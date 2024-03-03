from django.contrib import admin
from .models import Company, registered_companies, placed_students, job_profile

# Register your models here.
admin.site.register(Company)
admin.site.register(registered_companies)
admin.site.register(placed_students)
admin.site.register(job_profile)
