from django.contrib import admin
from django.urls.resolvers import URLPattern
from .models import Sdrate, bstat, Fdrate, Ratings, RatingAgencies
from django.shortcuts import render
from django.urls import path
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
# Register your models here.

@admin.register(Sdrate)
class AdminSdrates(admin.ModelAdmin):
    list_display = ['id','bank_name', 'date', 'bcode','rateid','bref','effdate','r1','s1','r2','s2','r3','s3','r4','s4','r5','s5','r6','s6',
    'r7','s7','r8','s8','r9','s9','r10','s10','r11','s11','r12','s12','r13','s13','r14','s14','r15','s15','floatrate']
    exclude = ('bcode','bref','id', 'rateid','effdate',)


@admin.register(bstat)
class Adminbstat(admin.ModelAdmin):
    list_display = ['id', 'name', 'bref', 'bcode', 'type', 'display_name', 'founded_yr', 'hqcity', 'hqstate', 'active', 'sd_url', "fd_url"]

# @admin.register(Fdrate)

@admin.register(Ratings)
class AdminRatings(admin.ModelAdmin):
    list_display = ['bref', 'updatedate', 'Agency', 'Rating', 'Outlook']    



@admin.register(RatingAgencies)
class AdminRatingAgencies(admin.ModelAdmin):
    list_display = ['Agency', 'parent', 'DisplayPriority']
class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()
class AdminFdrates(admin.ModelAdmin):
    list_display=['bref','order', 'effstartdate','specialrate', 'effenddate', 'tenorstart', 'tenorend', 'startincl', 'endincl', 'baserate', 'seniorextra', 'superextra']

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path("upload-csv/", self.upload_csv),]
        return new_urls+urls
    
    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES['csv_upload']
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for data in csv_data:
                fields = data.split(",")
                print(data)
                created = Fdrate.objects.create(
                    # id = fields[0], it will be autoupdated
                    bcode = fields[0],
                    bref = fields[1],
                    effdate = fields[2],
                    effenddate = fields[3],
                    special_rate = fields[4],
                    tenorstart = fields[5],
                    tenorend = fields[6],
                    startincl = fields[7],
                    endincl = fields[8],
                    baserate = fields[9],
                    seniorextra = fields[10],
                    superextra = fields[11],
                    order = fields[12],
                )
            
            messages.success(request, "CSV Data Imported Successfully")
            return HttpResponseRedirect("./admin/")
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)
    
admin.site.register(Fdrate, AdminFdrates)