from django.contrib import admin

# Register your models here.
from .models import Question, Choice, Profile, Product, emp


# admin.site.register(Question)
# admin.site.register(Choice)






class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question_text']}), ('Date Information', {
        'fields': ['pub_date'], 'classes': ['collapse']}), ]
    inlines = [ChoiceInLine]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Profile)

from .models import newsletter

admin.site.register(newsletter)

@admin.register(Product)
class ProdutAdmin(admin.ModelAdmin):
    list_display = ['id','name','barcode','batch_number']



from .models import QRCode

admin.site.register(QRCode)

from .models import QRCode


from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


@admin.register(emp)
class PcAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['name','address','location']

    class Meta:
        model = emp
        fields =  ['name','address','location']