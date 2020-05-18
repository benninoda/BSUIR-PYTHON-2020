from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import HomeView, SignUpView, CheckInView, RentView, RulesView, SignUpLodgerView, SignUpPersonnelView, \
    ProfileDetailView, ContactsView, SignInView, loginRequiredView, LodgersView, WorkPersonnelView, ActivateUserView, \
    login_required_works_view, MessageToDormitoryView, login_required_verification_send, WorkPersonnelUpdateView, \
    EggView, WorkEntryDeleteView

urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', SignUpView.as_view(), name='register_page'),
    path('register/lodger/', SignUpLodgerView.as_view(), name='register_lodger_page'),
    path('register/staff/', SignUpPersonnelView.as_view(), name='register_staff_page'),
    path('<slug:name>/profile-<int:pk>/', ProfileDetailView.as_view(), name='profile_page'),
    path('actionUrl/', login_required_verification_send, name='actionUrl'),
    path('<slug:name>/profile<int:pk>/lodgers', LodgersView.as_view(), name='lodgers_page'),
    path('<slug:name>/profile<int:pk>/works', WorkPersonnelView.as_view(), name='works_page_hi'),
    path('<slug:name>/profile<int:pk>/works/update<int:num>', WorkPersonnelUpdateView.as_view(), name='update_works'),
    path('works/delete<int:pk>', WorkEntryDeleteView.as_view(), name='delete_works'),
    path('verificated/<str:uid>/<str:token>', ActivateUserView.as_view(), name='verificated_page'),
    path('mdamdamda/', loginRequiredView, name='mdamdamda'),
    path('redirect/works', login_required_works_view, name='redirect_works_page'),
    path('egg/', EggView.as_view(), name='egg'),
    path('contacts/', ContactsView.as_view(), name='contacts_page'),
    path('contacts/message', MessageToDormitoryView.as_view(), name='message_to_dormitory_page'),
    path('check_in/', CheckInView.as_view(), name='checkin_page'),
    path('rent/', RentView.as_view(), name='rent_page'),
    path('rules/', RulesView.as_view(), name='rules_page'),

    # path('lodgers/', LodgerListView.as_view(), name='lodger_list_page'),
]
