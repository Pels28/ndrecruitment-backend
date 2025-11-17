# # blogs/admin.py
# from django.contrib import admin
# from .models import Author, Category, Tag, Post
# from django.utils.text import slugify

# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ['user', 'bio']
#     search_fields = ['user__username', 'user__first_name', 'user__last_name']

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug': ('name',)}

# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug': ('name',)}

# # @admin.register(Post)
# # class PostAdmin(admin.ModelAdmin):
# #     list_display = ['title', 'author', 'date', 'draft']
# #     list_filter = ['draft', 'categories', 'date']
# #     search_fields = ['title', 'content']
# #     prepopulated_fields = {'slug': ('title',)}
# #     filter_horizontal = ['categories', 'tags']

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ['title', 'author', 'date', 'draft']
#     list_filter = ['draft', 'categories', 'date']
#     search_fields = ['title', 'content']
#     filter_horizontal = ['categories', 'tags']
    
#     # Remove 'slug' from readonly_fields since it's not in the form anymore
#     readonly_fields = ['created_at', 'updated_at']
    
#     fieldsets = (
#         ('Basic Information', {
#             'fields': ('title', 'description', 'content', 'image')
#             # Note: slug is removed from here
#         }),
#         ('Relations', {
#             'fields': ('author', 'categories', 'tags')
#         }),
#         ('Publishing', {
#             'fields': ('date', 'draft', 'created_at', 'updated_at')
#         }),
#     )
    
#     def save_model(self, request, obj, form, change):
#         if not obj.slug:  # Only generate slug if it doesn't exist
#             obj.slug = slugify(obj.title)
#         super().save_model(request, obj, form, change)

# blogs/admin.py
from django.contrib import admin
from django.utils.text import slugify
from .models import Author, Category, Tag, Post

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']  # Remove slug from list_display
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.slug:
            base_slug = slugify(obj.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            obj.slug = slug
        super().save_model(request, obj, form, change)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']  # Remove slug from list_display
    
    fieldsets = (
        ('Tag Information', {
            'fields': ('name',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.slug:
            base_slug = slugify(obj.name)
            slug = base_slug
            counter = 1
            while Tag.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            obj.slug = slug
        super().save_model(request, obj, form, change)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date', 'draft']  # Slug already removed
    list_filter = ['draft', 'categories', 'date']
    search_fields = ['title', 'content']
    filter_horizontal = ['categories', 'tags']
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'content', 'image')
        }),
        ('Relations', {
            'fields': ('author', 'categories', 'tags')
        }),
        ('Publishing', {
            'fields': ('date', 'draft', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.slug:
            base_slug = slugify(obj.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            obj.slug = slug
        super().save_model(request, obj, form, change)