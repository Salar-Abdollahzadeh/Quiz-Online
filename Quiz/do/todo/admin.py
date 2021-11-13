from django.contrib import admin
from .models import Category, Task, Author, Book
from django.utils import timezone
from django.utils.translation import ngettext
from django.contrib import messages
# Register your models here.



@admin.action(description="in this action we want update due_at field")
def update_due_at(modeladmin, request, queryset):
    queryset.update(due_at=timezone.now())


# ##### method 2 ######
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at')
    list_editable = ('name', 'due_at', )
    list_display_links = None
    fieldsets = (
        ('identification', {'fields': ('id', 'name')}),
        ('time_section', {'fields': ('created_at', 'due_at')}),
        ('category_section', {'fields': ('cat',)})
    )
    # fields = (('id', 'created_at'), 'description')
    # exclude = ('description',)
    list_display = ('name', 'due_at' )
    list_filter = ('cat__name', 'due_at')
    date_hierarchy = 'due_at'
    actions_on_top = True
    actions_selection_counter = True

    actions = ['update_due_at']

    @admin.action(description="in this action we want update due_at field")
    def update_due_at(self, request, queryset):
        update_number = queryset.update(due_at=timezone.now())
        self.message_user(request=request,
                          message=ngettext("{} task updated ".format(update_number),
                                            "{} tasks updated ".format(update_number),
                                            update_number),
                          level=messages.ERROR)


class TaskInline(admin.StackedInline):
    fields = ('name', 'due_at')
    model = Task
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    #
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     form.base_fields['name'].initial = 'cat_default_name'
    #     return form

    inlines = [TaskInline]

# admin.site.register(Task)
# admin.site.register(Category)


##### method 1 #####
# class TaskAdmin(admin.ModelAdmin):
#     pass

# admin.site.register(Task, TaskAdmin)

class BookAdmin(admin.ModelAdmin):
    pass

###############################
#
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    filter_vertical = ('authors', )
#
#
#
# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):
#     pass