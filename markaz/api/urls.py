from django.urls import path
from .views import NewCreateAPIView,NewDetailAPIView,TestCreateAPIView,TestDetailAPIView,CourseCreateAPIView,CourseDetailAPIView,GroupCreateAPIView,GroupDetailAPIView,QuestionCreateAPIView,QuestionDetailAPIView,TestimonialDetailAPIView,TestimonialCreateAPIView,BannerCreateAPIView,BannerDetailAPIView,CustomUserCreateAPIView,CustomUserDetailAPIView


app_name = 'api'

urlpatterns = [
    path('news/', NewCreateAPIView.as_view(), name='addapi-new'),
    path('news/<int:pk>', NewDetailAPIView.as_view(), name='detailapi-new'),
    path('test/', TestCreateAPIView.as_view(), name='addapi-test'),
    path('test/<int:pk>', TestDetailAPIView.as_view(), name='detailapi-test'),
    path('course/', CourseCreateAPIView.as_view(), name='addapi-course'),
    path('course/<int:pk>', CourseDetailAPIView.as_view(), name='detailapi-course'),
    path('group/', GroupCreateAPIView.as_view(), name='addapi-group'),
    path('group/<int:pk>', GroupDetailAPIView.as_view(), name='detailapi-group'),
    path('question/', QuestionCreateAPIView.as_view(), name='addapi-question'),
    path('question/<int:pk>', QuestionDetailAPIView.as_view(), name='detailapi-question'),
    path('testimonial/', TestimonialCreateAPIView.as_view(), name='addapi-testimonial'),
    path('testimonial/<int:pk>', TestimonialDetailAPIView.as_view(), name='detailapi-testimonial'),
    path('banner/', BannerCreateAPIView.as_view(), name='addapi-banner'),
    path('banner/<int:pk>', BannerDetailAPIView.as_view(), name='detailapi-banner'),
    path('user/', CustomUserCreateAPIView.as_view(), name='addapi-user'),
    path('user/<int:pk>', CustomUserDetailAPIView.as_view(), name='detailapi-user'),
]