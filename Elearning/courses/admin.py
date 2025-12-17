from django.contrib import admin
from .models import Course, EnrolledCourse, Lesson


# COURSE ADMIN
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'instructor', 'language', 'lessons')
    list_filter = ('language', 'instructor')
    search_fields = ('title', 'instructor')

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'price', 'language', 'duration', 'lessons')
        }),
        ('Media Files', {
            'fields': ('thumbnail', 'video', 'notes','notes_thumbnail',),
        }),
        ('Instructor Details', {
            'fields': ('instructor', 'instructor_image'),
        }),
    )

admin.site.register(Course, CourseAdmin)


# ENROLLED COURSE ADMIN
class EnrolledCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'amount')
    list_filter = ('course', 'user')
    search_fields = ('user__username', 'course__title')

admin.site.register(EnrolledCourse, EnrolledCourseAdmin)


# LESSON ADMIN
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')

    fieldsets = (
        ('Lesson Info', {
            'fields': ('course', 'title', 'duration')
        }),
        ('Video Upload', {
            'fields': ('video',)
        }),
    )

admin.site.register(Lesson, LessonAdmin)
