from rest_framework.serializers import ModelSerializer
from talim.models import New,Test,Course,Group,Question,Testimonial,Banner,CustomUser

class NewSerializer(ModelSerializer):
    class Meta:
        model = New
        fields = '__all__'

class TestSerializer(ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class TestimonialSerializer(ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class BannerSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'