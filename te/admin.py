from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from te.models import Account, User, Profile, Tree, PlantedTree

@admin.action(description="Activate selected accounts")
def activate_accounts(modeladmin, request, queryset):
    queryset.update(active=True)

@admin.action(description="Deactivate selected accounts")
def deactivate_accounts(modeladmin, request, queryset):
    queryset.update(active=False)

class AccountCustom(admin.ModelAdmin):
    list_display = ('name', 'created', 'active')
    list_filter = ('active',)
    actions = [activate_accounts, deactivate_accounts]
    filter_horizontal = ('users',)
    search_fields = ('name',)

class UserCustom(UserAdmin):
    list_display = ('username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('date_joined', 'user_accounts', 'profile_information'),}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    search_fields = ('username',)
    readonly_fields = ('date_joined', 'user_accounts', 'profile_information')
    ordering = None
    
    def profile_information(self, obj):
        profile = Profile.objects.filter(user=obj).first()
        if profile.about:
            return profile.about
        return "You don't have an about section yet."

    def user_accounts(self, obj):
        accounts = Account.objects.filter(users=obj, active=True)
        if accounts.exists():
            return ", ".join(account.name for account in accounts)
        return "No active linked accounts"
    
    profile_information.short_description = "About"
    user_accounts.short_description = "Active accounts"

class ProfileCustom(admin.ModelAdmin):
    list_display = ('user', 'joined', 'about')
    search_fields = ('user__username',)
    readonly_fields = ('user',)

    def has_add_permission(self, request, obj=None):
        return False

class PlantedTreeCustom(admin.ModelAdmin):
    list_display = ( 'tree', 'age', 'user', 'account', 'location')
    search_fields = ('tree__name', 'user__username', 'account__name')

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
class PlantedTreeInline(admin.TabularInline):
    model = PlantedTree
    fields = ['user', 'age', 'account', 'planted_at', 'location']
    readonly_fields = ['user', 'age', 'account', 'planted_at', 'location']
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

class TreeCustom(admin.ModelAdmin):
    list_display = ('name', 'scientific_name')
    search_fields = ('name',)
    inlines = [PlantedTreeInline]   

admin.site.register(Account, AccountCustom)
admin.site.register(User, UserCustom)
admin.site.register(Profile, ProfileCustom)
admin.site.register(PlantedTree, PlantedTreeCustom)
admin.site.register(Tree, TreeCustom)
admin.site.unregister(Group)
