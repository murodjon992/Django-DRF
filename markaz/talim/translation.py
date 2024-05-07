from .models import Course,New,Testimonial,Banner
from modeltranslation.translator import TranslationOptions,register

@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('name', 'descr')


@register(New)
class NewTranslationOptions(TranslationOptions):
    fields = ('title', 'body')

@register(Testimonial)
class TestimonialTranslationOptions(TranslationOptions):
    fields = ('jobs', 'body')

@register(Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ('title', 'body')