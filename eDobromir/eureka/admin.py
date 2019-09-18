from django.contrib import admin
from .models import Eureka, EurekaInstruction, EurekaInstructionStep
from guardian.admin import GuardedModelAdmin


class EurekaAdmin(GuardedModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'slug', 'created')
    search_fields = ('title', 'content')
    ordering = ('-created',)
    date_hierarchy = 'created'
admin.site.register(Eureka, EurekaAdmin)


class EurekaInstructionAdmin(GuardedModelAdmin):
    ordering = ('-created',)
    date_hierarchy = 'created'
admin.site.register(EurekaInstruction, EurekaInstructionAdmin)


class EurekaInstructionStepAdmin(GuardedModelAdmin):
    list_display = ('title', 'step_slug', 'created')
    search_fields = ('title', 'step_slug', 'content')
    ordering = ('-created',)
    date_hierarchy = 'created'
admin.site.register(EurekaInstructionStep, EurekaInstructionStepAdmin)