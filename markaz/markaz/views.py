from django.shortcuts import render,redirect,get_object_or_404,HttpResponse,reverse
from talim.models import Course,Group,New,CustomUser,Test,Question,CheckTest,CheckQuestion,Banner,Murojaat,Testimonial
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import FileResponse
from django.utils.translation import gettext as _

from django.utils.dateformat import DateFormat
from .decorators import unauthenticated_user,admin_only
import qrcode
from PIL import Image,ImageDraw,ImageFont


def BASE(request):
    return render(request, 'index.html')

def HOME(request):
    course = Course.objects.all()
    banner = Banner.objects.all().order_by('-id')[:1]
    testimonial = Testimonial.objects.all()
    return render(request, 'main.html',{'course':course,'banner':banner,'testimonial':testimonial})

def CONTACT(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        Murojaat.objects.create(body=message, name=name, phone=phone)
        messages.success(request,_(f'Xabaringiz qabul qilindi tez orada {phone} raqamiga bog`lanamiz'))
        return redirect('contact')

    return render(request, 'contact.html')

def NEWS(request):
    news = New.objects.all()
    return render(request, 'news.html',{'news':news})
@login_required(login_url='/login')
def PROFILE(request,username):
    user = CustomUser.objects.get(username=username)
    test = Test.objects.all()
    try:
        chek_test = CheckTest.objects.get(user=user)
    except CheckTest.DoesNotExist:
        chek_test = None

    return render(request,'profile.html',{'user':user,'test':test,'chek_test':chek_test})

@unauthenticated_user
def CHECKPROFILE(request,username):
    if username != 'admin':
        user = CustomUser.objects.get(username=username)
        return render(request,'check-profile.html',{'user':user})
    else:
        return redirect(to=reverse('admin:index'))

@login_required(login_url='/login')
def TEST_BOSHLASH(request,test_id):
    test = get_object_or_404(Test,id=test_id)
    savol = Question.objects.filter(test=test).order_by('?')
    if request.method == 'POST':
        checktest = CheckTest.objects.create(user=request.user,test=test)
        for question in savol:
            given_answer = request.POST[str(question.id)]
            CheckQuestion.objects.create(checktest=checktest,question=question,given_answer=given_answer,true_answer=question.togri_javob)
        checktest.save()
        user = request.user
        user.natija = True
        user.save()
        return redirect('user-profile',username=user.username)


    context = {'savol':savol,'test':test}
    return render(request, 'test.html',context)


def EDITPROFILE(request,id):
    user = CustomUser.objects.get(id=id)
    return render(request,'edit-profile.html',{'user':user})

def UPDATEPROFILE(request,id):
    if request.method == 'POST':
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        email = request.POST['email']

        user = CustomUser.objects.get(id=id)
        user.last_name = last_name
        user.first_name = first_name
        user.email = email
        try:
            if request.FILES['profile_pic']:
                user.profile_pic = request.FILES['profile_pic']
        except:
            pass

        user.save()
        messages.success(request, f'{first_name} malumotlaringiz muvaffaqqiyatli yangilandi')
        return redirect('user-profile',user.username)
def COURSE(request):
    course = Course.objects.all()
    return render(request, 'course.html',{'course':course})

@unauthenticated_user
def LOGIN(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                messages.success(request, f'Xush kelibsiz {username}')
                return redirect('admin-manage')
            else:
                messages.success(request, f'Xush kelibsiz {username}')
                return redirect('home')

        else:
            messages.error(request, 'Login yoki Parol xato')
            return redirect('login_user')
    return render(request, 'login.html')

@unauthenticated_user
def REGISTER(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']


        return redirect('login_user')
    return render(request, 'register.html')

def LOGOUT(request):
    logout(request)
    return redirect('login_user')

@login_required(login_url='/login')
@admin_only
def ADMIN(request):
    talabalar = CustomUser.objects.all().count
    return render(request,'master/main.html',{'talabalar':talabalar})
# ======================================== GURUHLAR =====================================
@login_required(login_url='/login')
@admin_only
def ADD_GROUP(request):

    if request.method == 'POST':
        name = request.POST['group_name']
        time = request.POST['group_time']

        group = Group(
            title = name,
            vaqti = time
        )
        group.save()
        return redirect('manage-group')
    return render(request,'master/add-group.html')
@login_required(login_url='/login')
@admin_only
def MANAGE_GROUP(request):
    group = Group.objects.all()
    return render(request,'master/manage-group.html',{'group':group})
@login_required(login_url='/login')
@admin_only
def EDIT_GROUP(request,id):
    group = Group.objects.get(id=id)
    return render(request,'master/edit-group.html',{'group':group})
@login_required(login_url='/login')
@admin_only
def UPDATE_GROUP(request):
    if request.method == 'POST':
        id = request.POST['id']
        title = request.POST['group_name']
        vaqti = request.POST['group_time']
        end_date = request.POST['end_time']

        group = Group.objects.get(id=id)
        group.title = title
        group.vaqti = vaqti
        group.end_date = end_date
        group.save()
        messages.success(request,'Guruh yangilandi')
        return redirect('manage-group')
    else:
        messages.error(request,'Qandaydir xatolik bor qayta urinib ko`rin')
        return redirect('edit-group')

    return render(request,'master/manage-group.html')
@login_required(login_url='/login')
@admin_only
def DELETE_GROUP(request,id):
    group = Group.objects.get(id=id)
    group.delete()
    messages.error(request,'Guruh muvaffaqqiyatli o`chirildi')

    return redirect('manage-group')

# ======================================== GURUHLAR YAKUNI=====================================
# ======================================== KURSLAR ============================================
@login_required(login_url='/login')
@admin_only
def ADD_COURSE(request):

    if request.method == 'POST':
        name = request.POST['course_name']
        descp = request.POST['course_descp']
        price = request.POST['course_price']
        pic = request.FILES['course_pic']

        course = Course(
            name = name,
            descr = descp,
            price = price,
            course_img = pic
        )
        course.save()
        messages.success(request, 'Kurs muvaffaqqiyatli qo`shildi')
        return redirect('manage-course')
    return render(request,'master/add-course.html')

@login_required(login_url='/login')
@admin_only
def MANAGE_COURSE(request):
    course = Course.objects.all()
    return render(request,'master/manage-course.html',{'course':course})

@login_required(login_url='/login')
@admin_only
def EDIT_COURSE(request,id):
    course = Course.objects.get(id=id)
    return render(request,'master/edit-course.html',{'course':course})

@login_required(login_url='/login')
@admin_only
def UPDATE_COURSE(request):
    if request.method == 'POST':
        id = request.POST['id']
        name = request.POST['course_name']
        descr = request.POST['course_descp']
        price = request.POST['course_price']
        pic = request.FILES['course_pic']

        course = Course.objects.get(id=id)
        course.name = name
        course.descr = descr
        course.price = price
        course.course_img = pic
        course.save()
        messages.success(request,'Kurs yangilandi')
        return redirect('manage-course')
    else:
        messages.error(request,'Qandaydir xatolik bor qayta urinib ko`rin')
        return redirect('edit-group')

    return render(request,'master/manage-group.html')


@login_required(login_url='login')
@admin_only
def DELETE_COURSE(request,id):
    course = Course.objects.get(id=id)
    course.delete()
    messages.error(request,'Kurs muvaffaqqiyatli o`chirildi')
    return redirect('manage-course')

# ======================================== KURSLAR YAKUNI==========================================
# ======================================== YANGILIKLAR ============================================
@login_required(login_url='/login')
@admin_only
def ADD_NEW(request):

    if request.method == 'POST':
        name = request.POST['new_name']
        body = request.POST['new_body']
        img = request.FILES['new_img']

        new = New(
            title = name,
            body = body,
            new_img = img
        )
        new.save()
        messages.success(request, 'Yangilik muvaffaqqiyatli qo`shildi')
        return redirect('manage-new')
    return render(request,'master/add-new.html')

@login_required(login_url='/login')
@admin_only
def MANAGE_NEW(request):
    new = New.objects.all()
    return render(request,'master/manage-new.html',{'new':new})

@login_required(login_url='/login')
@admin_only
def EDIT_NEW(request,id):
    new = New.objects.get(id=id)
    return render(request,'master/edit-new.html',{'new':new})

@login_required(login_url='/login')
@admin_only
def UPDATE_NEW(request):
    if request.method == 'POST':
        id = request.POST['id']
        name = request.POST['new_name']
        body = request.POST['new_body']
        img = request.FILES['new_img']

        new = New.objects.get(id=id)
        new.name = name
        new.body = body
        new.new_img = img
        new.save()
        messages.success(request,'Yangilik yangilandi')
        return redirect('manage-new')
    else:
        messages.error(request,'Qandaydir xatolik bor qayta urinib ko`rin')
        return redirect('edit-new')
@login_required(login_url='/login')
@admin_only
def DELETE_NEW(request,id):
    new = New.objects.get(id=id)
    new.delete()
    messages.error(request,'Yangilik muvaffaqqiyatli o`chirildi')

    return redirect('manage-new')

# ======================================== YANGILIKLAR YAKUNI==========================================
# ======================================== STUDENT=====================================================
@login_required(login_url='/login')
@admin_only
def ADD_STUDENT(request):
    course = Course.objects.all()
    guruh = Group.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        email = request.POST['email']
        course_id = request.POST['course']
        group_id = request.POST['group']
        img = request.FILES['student_pic']
        password = request.POST['password']


        courses = Course.objects.get(id = course_id)
        groups = Group.objects.get(id = group_id)
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request,'kechirasiz bunday nom allaqachon band')
            return redirect('add-student')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request,'kechirasiz bunday email allaqachon royxatdan otgan')
            return redirect('add-student')
        else:
            user = CustomUser(
                username = username,
                last_name = last_name,
                first_name = first_name,
                email = email,
                profile_pic = img,
                user_type = '3',
                course_id = courses,
                group_id = groups
            )
        user.set_password(password)
        user.save()
        messages.success(request, 'O`quvchi muvaffaqqiyatli qo`shildi')
        return redirect('manage-student')
    return render(request,'master/add-student.html',{'course':course,'guruh':guruh})

@login_required(login_url='/login')
@admin_only
def MANAGE_STUDENT(request):
    student = CustomUser.objects.all()
    return render(request,'master/manage-student.html',{'student':student})

@login_required(login_url='/login')
@admin_only
def EDIT_STUDENT(request,id):
    student = CustomUser.objects.get(id=id)
    course = Course.objects.all()
    guruh = Group.objects.all()
    return render(request,'master/edit-student.html',{'student':student,'course':course,'guruh':guruh })

@login_required(login_url='/login')
@admin_only
def UPDATE_STUDENT(request):
    course = Course.objects.all()
    guruh = Group.objects.all()

    if request.method == 'POST':
        id = request.POST['id']
        username = request.POST['username']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        email = request.POST['email']
        course_id = request.POST['course']
        group_id = request.POST['group']

        courses = Course.objects.get(id = course_id)
        groups = Group.objects.get(id = group_id)

        user = CustomUser.objects.get(id=id)


        user.username = username
        user.last_name = last_name
        user.first_name = first_name
        user.email = email
        user.course_id = courses
        user.group_id = groups
        try:
            if request.FILES['student_pic']:
                user.profile_pic = request.FILES['student_pic']

        except:
            pass
        if request.POST['password'] != '':
            user.set_password(request.POST['password'])
        user.save()
        messages.success(request, 'O`quvchi malumotlari muvaffaqqiyatli yangilandi')
        return redirect('manage-student')
    return render(request,'master/add-student.html',{'course':course,'guruh':guruh})

def TESTBOR(request,id):
    user_id = CustomUser.objects.get(id = id)
    if user_id.test == False:
        user_id.test = True
        messages.success(request, f'{user_id}ga test yuborildi')
    else:
        user_id.test = False
        messages.error(request, f'{user_id}ga test olib tashlandi')
    user_id.save()
    return redirect('manage-student')

def STATUS(request,id):
    user_id = CustomUser.objects.get(id = id)

    if user_id.status == 1:
        user_id.status = 2
        user_id.test = False
        messages.error(request, f'{user_id} ketdi')
    elif user_id.status == 2:
        user_id.status = 0
        messages.success(request, f'{user_id} bitirdi')
    else:
        user_id.status = 1
        messages.info(request, f'{user_id} o`qiyapti')
    user_id.save()
    return redirect('manage-student')
# =====================================TEST TUZISH============================================
@login_required(login_url='/login')
@admin_only
def ADD_TEST(request):
    test = Test.objects.all()
    if request.method == 'POST':

        test_id = request.POST['test_id']
        test_savol = request.POST['test_savol']
        a = request.POST['a']
        b = request.POST['b']
        c = request.POST['c']
        d = request.POST['d']
        true_answer = request.POST['true_answer']

        test_id  = Test.objects.get(id=test_id)

        testlar = Question(
            test = test_id,
            question = test_savol,
            a = a,
            b = b,
            c = c,
            d = d,
            togri_javob = true_answer
        )
        testlar.save()
        messages.success(request, 'Yangi test muvaffaqqiyatli qo`shildi')
        return redirect('manage-test')

    return render(request,'master/testtuzish.html',{'test':test})


@login_required(login_url='/login')
@admin_only
def MANAGE_TEST(request):
    test = Question.objects.all()
    return render(request,'master/manage-test.html',{'test':test})

@login_required(login_url='/login')
@admin_only
def EDIT_TEST(request,id):
    test = Test.objects.all()
    savol = Question.objects.get(id=id)
    return render(request,'master/edit-test.html',{'savol':savol,'test':test})

def USERRESULT(request):
    test = CheckTest.objects.all()
    return render(request,'master/user-result.html',{'test':test})

def SERTIFIKAT(request,username):

    user = CustomUser.objects.get(username=username)
    if user.sertifikat == False:
        id = user.id
        ismi = user.first_name
        famililya = user.last_name
        full = f'{ismi} {famililya}'
        kurs = user.course_id.name
        sana = user.group_id.end_date
        oldin = f'https://it-planet.uz/check/{username}'
        qr = qrcode.make(oldin)
        img = Image.open('sertifikat.jpg')
        img.paste(qr, (1500, 1850))
        eni = 3508
        dt = DateFormat(sana)
        sana = dt.format('d.m.Y')

        d = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', 200)
        font2 = ImageFont.truetype('arial.ttf', 130)
        font_id = ImageFont.truetype('arial.ttf', 130)
        font_sane = ImageFont.truetype('arial.ttf', 110)




        d.text((300,1050),text=f'{ismi} {famililya}', align='C',font=font,fill=(15,25,47))
        d.text((150,1450),text=f'{kurs}',font=font2,fill=(125,99,166))
        d.text((3120,1920),text=f'{id}',font=font_id,fill=(125,99,166))
        d.text((2720,2120),text=f'{sana}',font=font_sane,fill=(125,99,166))

        user.sertifikat = True
        user.save()
        rasm = img.save(f'media/sertifikat/{username}.pdf')
        return render(request, 'master/sertifikat.html')
    else:
        messages.error(request, f'{username}ga sertifikat yuborilgan')
        return redirect('user_result')

def DOWNLOAD(request, username):
    file = f'media/sertifikat/{username}.pdf'
    fileopen = open(file, 'rb')
    return FileResponse(fileopen,content_type='application/pdf')
def DELETERESULT(request,id):
    result = CheckTest.objects.get(id=id)
    result.delete()
    messages.error(request, 'Natija muvaffaqqiyatli o`chirildi')
    return redirect('user_result')

def MUROJAAT(request):
    murojaat = Murojaat.objects.all()
    return render(request,'master/murojaat.html',{'murojaat':murojaat})
def DELETEMUROJAAT(request,id):
    murojaat = Murojaat.objects.get(id=id)
    murojaat.delete()
    messages.success(request,'Murojaat muvaffaqqiyatli o`chirildi')
    return redirect('murojaat')