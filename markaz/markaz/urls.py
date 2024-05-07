from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('api/v1/auth', include('rest_framework.urls')),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    # admin
    path('admin-manage/',views.ADMIN, name='admin-manage'),
    # guruhlar
    path('add-group/',views.ADD_GROUP, name='add-group'),
    path('manage-group/',views.MANAGE_GROUP, name='manage-group'),
    path('edit-group/<int:id>',views.EDIT_GROUP, name='edit-group'),
    path('delete-group/<int:id>',views.DELETE_GROUP, name='delete-group'),
    path('update-group/',views.UPDATE_GROUP, name='update-group'),
    # kurslar
    path('add-course/',views.ADD_COURSE, name='add-course'),
    path('manage-course/',views.MANAGE_COURSE, name='manage-course'),
    path('edit-course/<int:id>',views.EDIT_COURSE, name='edit-course'),
    path('update-course/',views.UPDATE_COURSE, name='update-course'),
    path('delete-course/<int:id>',views.DELETE_COURSE, name='delete-course'),
    # new
    path('add-new/', views.ADD_NEW, name='add-new'),
    path('manage-new/', views.MANAGE_NEW, name='manage-new'),
    path('edit-new/<int:id>', views.EDIT_NEW, name='edit-new'),
    path('update-new/', views.UPDATE_NEW, name='update-new'),
    path('delete-new/<int:id>', views.DELETE_NEW, name='delete-new'),
    # test tuzish
    path('add-test/', views.ADD_TEST, name='add-test'),
    path('manage-test/', views.MANAGE_TEST, name='manage-test'),
    path('edit-test/<int:id>', views.EDIT_TEST, name='edit-test'),
    # user admin control
    path('add-student/', views.ADD_STUDENT, name='add-student'),
    path('manage-student/', views.MANAGE_STUDENT, name='manage-student'),
    path('edit-student/<int:id>', views.EDIT_STUDENT, name='edit-student'),
    path('test-bor/<int:id>', views.TESTBOR, name='test_bor'),
    path('user-result', views.USERRESULT, name='user_result'),
    path('murojaat', views.MUROJAAT, name='murojaat'),
    path('delete-murojaat/<int:id>', views.DELETEMUROJAAT, name='delete_murojaat'),
    path('delete-result/<int:id>', views.DELETERESULT, name='delete_result'),
    path('sertifikat/<str:username>', views.SERTIFIKAT, name='sertifikat'),
    path('yuklash/<str:username>', views.DOWNLOAD, name='download'),
    path('status/<int:id>', views.STATUS, name='status'),
    path('update-student/', views.UPDATE_STUDENT, name='update-student'),
    path('delete-new/<int:id>', views.DELETE_NEW, name='delete-new'),
    # user interface
    path('base/', views.BASE, name='base'),
    path('test/<int:test_id>/', views.TEST_BOSHLASH, name='test_boshla'),
    path('', views.HOME, name='home'),
    path('contact/', views.CONTACT, name='contact'),
    path('news/', views.NEWS, name='news'),
    path('profile/<str:username>', views.PROFILE, name='user-profile'),
    path('check/<str:username>', views.CHECKPROFILE, name='check-profile'),
    path('edit/<int:id>', views.EDITPROFILE, name='edit_profile'),
    path('update/<int:id>', views.UPDATEPROFILE, name='update_profile'),
    path('courses/', views.COURSE, name='course'),
    path('login/', views.LOGIN, name='login_user'),

    path('register/', views.REGISTER, name='register'),
    path('logout/', views.LOGOUT, name='logout'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
