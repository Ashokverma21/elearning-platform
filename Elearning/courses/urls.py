from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('all/', views.all_courses, name='all_courses'),

    # Course Detail
    path('course/<int:id>/', views.course_detail, name='course_detail'),

    # Checkout + Razorpay
    path('course/<int:id>/checkout/', views.checkout, name='checkout'),
    path('course/<int:id>/checkout/success/', views.payment_success, name='checkout_success'),
    path("payment-success/<int:id>/", views.payment_success, name="payment_success"),

    # My Courses
    path('my-courses/', views.my_courses, name='my_courses'),

    # Player
    path("course/<int:id>/learn/", views.course_player, name="course_player"),
    path("course/<int:id>/learn/<int:lesson_id>/", views.course_player_lesson, name="course_player_lesson"),
    path("course/<int:course_id>/learn/<int:lesson_id>/complete/", views.mark_complete, name="mark_complete"),

    # ⭐ Notes Page URL
    path("course/<int:id>/notes/", views.notes_page, name="notes_page"),
]
