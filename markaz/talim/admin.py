from django.contrib import admin
from .models import Course,New,CustomUser,Group,Test,Question,CheckQuestion,CheckTest,Banner,Testimonial,Murojaat

class QuestionInline(admin.TabularInline):
    model = Question

class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline,]
    list_display = ['title']


admin.site.register(Course)
admin.site.register(CustomUser)
admin.site.register(New)
admin.site.register(Banner)
admin.site.register(Murojaat)
admin.site.register(Testimonial)
admin.site.register(Group)
admin.site.register(Question)
admin.site.register(CheckQuestion)
admin.site.register(CheckTest)
admin.site.register(Test,TestAdmin)

