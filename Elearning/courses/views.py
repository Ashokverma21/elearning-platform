from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course, Lesson, EnrolledCourse ,LessonProgress,Discussion,Reply


# HOME
@login_required(login_url='/users/login/')
def home(request):
    return render(request, "courses/home.html", {'courses': Course.objects.all()})


# ALL COURSES
def all_courses(request):
    return render(request, "courses/all_courses.html", {'courses': Course.objects.all()})


# COURSE DETAILS
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)

    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = EnrolledCourse.objects.filter(user=request.user, course=course).exists()

    return render(request, "courses/course_detail.html", {
        'course': course,
        'is_enrolled': is_enrolled
    })



# CHECKOUT (Payment Page)
import razorpay
from django.conf import settings

@login_required(login_url='/users/login/')
def checkout(request, id):
    course = get_object_or_404(Course, id=id)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order = client.order.create({'amount': course.price * 100, 'currency': 'INR', 'payment_capture': '1'})

    return render(request, "courses/checkout.html", {
        'course': course,
        'order_id': order['id'],
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'amount': course.price * 100
    })


# AFTER PAYMENT SUCCESS
@login_required(login_url='/users/login/')
def payment_success(request, id):
    course = get_object_or_404(Course, id=id)

    EnrolledCourse.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'amount': course.price}
    )

    return redirect('my_courses')


# MY COURSES
@login_required(login_url='/users/login/')
def my_courses(request):
    return render(request, "courses/my_courses.html", {
        'enrollments': request.user.enrollments.select_related('course')
    })


# PLAYER FIRST VIDEO
@login_required(login_url='/users/login/')
def course_player(request, id):
    course = get_object_or_404(Course, id=id)

    # Check enrollment
    if not EnrolledCourse.objects.filter(user=request.user, course=course).exists():
        return redirect("checkout", id=course.id)

    lessons = course.course_lessons.all()

    # 🛑 FIX: If no lessons found, show message
    if not lessons.exists():
        messages.error(request, "No lessons uploaded yet. Please contact admin.")
        return redirect("course_detail", id=course.id)

    current_lesson = lessons.first()
    next_lesson = lessons.filter(id__gt=current_lesson.id).first()
    prev_lesson = None

    return render(request, "courses/player.html", {
        "course": course,
        "lessons": lessons,
        "current_lesson": current_lesson,
        "next_lesson": next_lesson,
        "prev_lesson": prev_lesson,
    })

# NEXT VIDEO PLAY
@login_required(login_url='/users/login/')
def course_player_lesson(request, id, lesson_id):
    course = get_object_or_404(Course, id=id)
    lessons = course.course_lessons.all()
    current_lesson = get_object_or_404(lessons, id=lesson_id)

    # check enrollment
    if not EnrolledCourse.objects.filter(user=request.user, course=course).exists():
        return redirect("checkout", id=course.id)

    # fetch discussion chat
    discussions = Discussion.objects.filter(lesson=current_lesson).order_by('-created_at')

    if request.method == "POST" and "ask_question" in request.POST:
        question = request.POST.get("question")
        if question.strip():
            Discussion.objects.create(
                course=course,
                lesson=current_lesson,
                user=request.user,
                question=question
            )
            messages.success(request, "Question posted successfully!")
            return redirect("course_player_lesson", id, lesson_id)

    if request.method == "POST" and "add_reply" in request.POST:
        reply = request.POST.get("reply")
        discussion_id = request.POST.get("discussion_id")
        d = Discussion.objects.get(id=discussion_id)
        Reply.objects.create(discussion=d, user=request.user, answer=reply)
        messages.success(request, "Reply added!")
        return redirect("course_player_lesson", id, lesson_id)

    completed_lessons = []  # if using progress tracking

    return render(request, "courses/player.html", {
        "course": course,
        "lessons": lessons,
        "current_lesson": current_lesson,
        "discussions": discussions,
    })
    
# STREAMING VIDEO
from django.http import StreamingHttpResponse, Http404
from wsgiref.util import FileWrapper
import os

def stream_video(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(file_path):
        raise Http404
    response = StreamingHttpResponse(FileWrapper(open(file_path, 'rb')), content_type='video/mp4')
    response['Accept-Ranges'] = 'bytes'
    return response

#Lesson Progess 
@login_required
def mark_complete(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    LessonProgress.objects.update_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'completed': True}
    )

    messages.success(request, "Lesson marked as completed!")
    return redirect("course_player_lesson", id=course_id, lesson_id=lesson_id)



@login_required(login_url='/users/login/')
def notes_page(request, id):
    course = get_object_or_404(Course, id=id)

    # check if user enrolled
    if not EnrolledCourse.objects.filter(user=request.user, course=course).exists():
        messages.error(request, "You must purchase this course to access notes.")
        return redirect('checkout', id=course.id)

    return render(request, "courses/notes.html", {'course': course})