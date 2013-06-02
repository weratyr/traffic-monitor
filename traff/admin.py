from django.contrib import admin
from traff.models import Day,DayTime


class TraffAdmin(admin.ModelAdmin):
	fields = ['date']


class TraffTimeAdmin(admin.ModelAdmin):
	fields = ['time', 'traff', 'day']


admin.site.register(Day)
admin.site.register(DayTime, TraffTimeAdmin)
