from django.contrib import admin
from .models import Tag, Project, Skill, Experience, Education, Certificate, Issuer,Message,Profile,Category

from django import forms
from django.contrib import admin


admin.site.register(Tag)
admin.site.register(Issuer)
admin.site.register(Profile)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'live_link')
    search_fields = ('title', 'description')
    list_filter = ('tags',)

# And do the same for the other models
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'order')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'order')


# @admin.register(Certificate)
# class CertificateAdmin(admin.ModelAdmin):
#     list_display = ('title', 'issuer', 'issue_date', 'order')
#     search_fields = ('title', 'issuer')



class CertificateAdminForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = "__all__"
        widgets = {
            "issuers": admin.widgets.FilteredSelectMultiple("Issuers", is_stacked=False),
        }

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    form = CertificateAdminForm
    list_display = ("title", "get_issuers", "issue_date", "order")
    search_fields = ("title", "issuers__name")

    def get_issuers(self, obj):
        return ", ".join([issuer.name for issuer in obj.issuers.all()])
    get_issuers.short_description = "Issuers"






@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    readonly_fields = ('name', 'email', 'message', 'created_at')
