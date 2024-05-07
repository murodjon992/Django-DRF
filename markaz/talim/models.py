from io import BytesIO

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
# Create your models here.
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40,unique=True)
    descr = models.CharField(max_length=500)
    price = models.IntegerField()
    course_img = models.ImageField(upload_to='kurs/',default='media/no.jpg')

    def __str__(self):
        return self.name

class New(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.TimeField(auto_now_add=True)
    new_img = models.ImageField(upload_to='news/',default='media/no.jpg')

    def __str__(self):
        return self.title

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    vaqti = models.CharField(max_length=100)
    created = models.TimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=(timezone.now() + timezone.timedelta(days=61)))
    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    USER = (
        ('1','Boshliq'),
        ('2','Ishchi'),
        ('3','Talaba'),
    )
    user_type = models.CharField(choices=USER,max_length=50,default='1')
    profile_pic = models.ImageField(upload_to='profile_pic')
    test = models.BooleanField(default=False)
    natija = models.BooleanField(default=False)
    status = models.IntegerField(default=1)
    sertifikat = models.BooleanField(default=False)
    course_id = models.ForeignKey(Course,on_delete=models.DO_NOTHING, related_name='courses', null=True, max_length=50, default=None)
    group_id = models.ForeignKey(Group,on_delete=models.DO_NOTHING, related_name='groups', null=True, max_length=50, default=None)

class Test(models.Model):
    category = models.ForeignKey(Course,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    maximum = models.PositiveBigIntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=(timezone.now()+timezone.timedelta(days=3)))
    pass_percentage = models.PositiveBigIntegerField()

    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    a = models.CharField(max_length=100)
    b = models.CharField(max_length=100)
    c = models.CharField(max_length=100)
    d = models.CharField(max_length=100)
    togri_javob = models.CharField(max_length=150,help_text='Nam, A')

    def __str__(self):
        return self.question


class CheckTest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    finded_question = models.PositiveBigIntegerField(default=0)
    user_passed = models.BooleanField(default=False)
    percentage = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.user.username + str(' test javobi')

class CheckQuestion(models.Model):
    checktest = models.ForeignKey(CheckTest,on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    given_answer = models.CharField(max_length=1,help_text='Nam: A ')
    true_answer = models.CharField(max_length=1,help_text='Nam: A ')
    is_true = models.BooleanField(default=False)

@receiver(pre_save,sender=CheckQuestion)
def check_answer(sender,instance,*args,**kwargs):
    if instance.given_answer == instance.true_answer:
        instance.is_true = True



@receiver(post_save,sender=CheckTest)
def check_test(sender,instance,*args,**kwargs):
    checktest = instance
    checktest.finded_question = CheckQuestion.objects.filter(checktest=checktest,is_true=True).count()
    try:
        checktest.percentage = int(checktest.finded_question)*100//CheckQuestion.objects.filter(checktest=checktest).count()
        if checktest.test.pass_percentage <= checktest.percentage:
            checktest.user_passed = True
        checktest.save()
    except:pass

class Testimonial(models.Model):
    body = models.TextField()
    full_name = models.CharField(max_length=100)
    jobs = models.CharField(max_length=50)
    img = models.ImageField(upload_to='testimonial/',default='media/no.jpg')

    def __str__(self):
        return self.full_name

class Murojaat(models.Model):
    body = models.TextField()
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Banner(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    img = models.ImageField(upload_to='banner/',default='media/no.jpg')

    def __str__(self):
        return self.title