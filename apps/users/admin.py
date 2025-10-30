""" ================= Admin Panel for User Management ================= """
from django.contrib import admin
from django.utils.html import format_html
from apps.users.models import User, Profile, Address, ContactDetail


""" ========== Inline Models (Appear Inside User Admin) ========== """
class ContactDetailInline(admin.TabularInline):
    model = ContactDetail
    extra = 1
    fields = ('phone_number', 'alt_phone_number', 'email', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    show_change_link = True


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    fields = ('full_name', 'street_address', 'city', 'state', 'country', 'postal_code', 'is_default_shipping')
    readonly_fields = ('created_at', 'updated_at')
    show_change_link = True


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0
    fields = ('gender', 'date_of_birth', 'profile_image', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    show_change_link = True


""" ========== User Admin ========== """
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline, AddressInline, ContactDetailInline]

    list_display = ('email', 'full_name', 'phone_number', 'is_active', 'is_staff', 'joined_on', 'colored_status')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')
    list_per_page = 20

    fieldsets = (
        ("Basic Info", {"fields": ("email", "full_name", "phone_number", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    """ === Custom Admin Display === """
    @admin.display(description="Joined")
    def joined_on(self, obj):
        return obj.date_joined.strftime("%b %d, %Y")

    @admin.display(description="Status")
    def colored_status(self, obj):
        color = "green" if obj.is_active else "red"
        return format_html(f'<b style="color:{color};">{obj.is_active}</b>')

    """ === Custom Admin Actions === """
    @admin.action(description="Activate selected users")
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Deactivate selected users")
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)

    actions = ['activate_users', 'deactivate_users']


""" ========== Profile Admin ========== """
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'date_of_birth', 'is_active', 'created_at')
    list_filter = ('gender', 'is_active', 'created_at')
    search_fields = ('user__email',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


""" ========== Address Admin ========== """
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'city', 'country', 'postal_code', 'is_default_shipping', 'created_at')
    list_filter = ('country', 'is_default_shipping', 'is_active')
    search_fields = ('user__email', 'city', 'postal_code')
    ordering = ('-created_at',)


""" ========== Contact Detail Admin ========== """
@admin.register(ContactDetail)
class ContactDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'alt_phone_number', 'email', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('user__email', 'phone_number')
    ordering = ('-created_at',)
