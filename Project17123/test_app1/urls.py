from django.urls import path
from test_app1.views import UserRegisterView, UserLoginView, \
UserProfileView, TemplateView, LogoutView, WebpageCreateView, WebpageListView, ContentCreateView, \
    ContentView, ContentUpdateView, ContentDeleteView
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('error/', TemplateView.as_view(template_name='error.html'), name='error'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('new_webpages/', WebpageCreateView.as_view(), name='new_webpages'),
    path('webpages/', WebpageListView.as_view(), name='webpages'),
    path('create_content/<int:web_id>/', ContentCreateView.as_view(), name='create_content'),
    path('content/<int:web_id>/', ContentView.as_view(), name='content'),
    path('content_update/<int:pk>/', ContentUpdateView.as_view(), name='update'),
    path('content_delete/<int:pk>/', ContentDeleteView.as_view(), name='delete'),
]
