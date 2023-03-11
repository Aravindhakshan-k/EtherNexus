from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView
from .models import UserModel, WebpageModel, ContentModel, LikeModel, CommentModel
from django.db.models.query import QuerySet
from django.contrib import messages
from django.http import HttpResponse
import logging

logger = logging.getLogger('django')


class SerialMixin:
    def serialization_obj(self,obj):
        list=[]
        try:
            if type(obj) in [QuerySet,list]:
                for o in obj:
                    d={}
                    for attr in o.__dict__:
                        d[attr] = getattr(o,attr)      # str(o.__getattribute__(attr))
                    list.append(d)
            else:
                d={}
                for attr in obj.__dict__:
                    d[attr] = getattr(obj,attr)
                list.append(d)
            return list
        except:
            return list

class UserRegisterView(CreateView):
    template_name = 'register.html'
    fields = ['name','dob','email','password']
    model = UserModel
    success_url = '/login'

    def post(self, request, *args, **kwargs):
        Email = request.POST['email']
        if UserModel.objects.filter(email=Email):
            messages.error(request, 'Email already Registered !!!')
            return self.get(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

class UserLoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('uid'):
            del request.session['uid']
        return super().get(request, *args, **kwargs)
    
    def post(self,request, *args, **kwargs):
        Email = request.POST['email']
        Password = request.POST['password']
        user = UserModel.objects.filter(email=Email).first()
        if user:
            if user.password != Password:
                messages.error(request, "Incorrect Password")
                return self.get(request, *args, **kwargs)
        if user:
            request.session['uid']=user.user_id
            return redirect(reverse('profile'))
        return redirect(reverse('error'))

class UserProfileView(SerialMixin, TemplateView):
    template_name = 'user.html'

    def get(self, request, *args, **kwargs):
        u_id = request.session.get('uid')
        try:
            user = UserModel.objects.filter(user_id=u_id)
            if not user:
                return redirect(reverse('login'))
        except:
            return redirect(reverse('error'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        u_id = self.request.session.get('uid')
        user = UserModel.objects.filter(user_id=u_id).first()
        user_data = self.serialization_obj(user)

        # likes = LikeModel.objects.filter(content__user=user, is_liked=True).count()
        # comments = CommentModel.objects.filter(content__user=user).count()

        for u in user_data:
            context = {
                'user' : u,
                # 'likes' : likes,
                # 'comments' : comments
            }
            kwargs.update(context)
        return kwargs

class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.session.get('uid'):
            del request.session['uid']
            messages.success(request, "User Successfully Logged Out")
        return redirect(reverse('login'))

class WebpageCreateView(CreateView):
    template_name = 'create_webpage.html'
    fields = '__all__'
    model = WebpageModel
    success_url = '/webpages'

    def post(self, request, *args, **kwargs):
        try:
            uid = request.session.get('uid')
            user = UserModel.objects.get(user_id=uid)
            request.POST = request.POST.copy()
            request.POST['author'] = user.user_id
            return super().post(request, *args, **kwargs)
        except Exception as e:
            print("Error",e)

class WebpageListView(ListView):
    template_name = 'webpages.html'
    model = WebpageModel
    context_object_name = 'web'

    def get(self, request, *args, **kwargs):
        u_id = request.session.get('uid')
        try:
            user = UserModel.objects.filter(user_id=u_id)
            if not user:
                return redirect(reverse('login'))
        except:
            return redirect(reverse('error'))
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        user = UserModel.objects.filter(user_id=self.request.session.get('uid')).first()
        web = WebpageModel.objects.filter(author=user)
        context = {
            'web':web
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

       
class ContentCreateView(CreateView):
    template_name = 'create_content.html'
    fields = "__all__"
    model = ContentModel
    logger.info('Url Attend')

    def get_success_url(self):
        return reverse(
            'content',
            kwargs={
                'web_id': self.kwargs.get('web_id',0)
            }
        )

    def get(self, request, *args, **kwargs):
        logger.info('inside content create get')
        user = UserModel.objects.filter(user_id=self.request.session.get('uid')).first()
        try:
            if not user:
                return HttpResponse('User Not Found')
        except Exception as e:
            print(e)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.kwargs = kwargs
            logger.info('inside post content create')
            web = WebpageModel.objects.get(id=kwargs.get('web_id',0))
            request.POST = request.POST.copy()
            request.POST['website'] = web.id
            post_ret = super().post(request, *args, **kwargs)
            return post_ret
        except Exception as e:
            print("Error",e)
        return self.get(request, *args, **kwargs)
    

class ContentView(ListView):
    logger.info('content view hit')
    template_name = 'content_view.html'
    model = ContentModel
    context_object_name = 'contents'
    
    def get(self, request, *args, **kwargs):
        u_id = request.session.get('uid')
        try:
            user = UserModel.objects.filter(user_id=u_id)
            if not user:
                return redirect(reverse('login'))
        except:
            return redirect(reverse('error'))
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        print(kwargs)
        print(self.kwargs)
        web = WebpageModel.objects.filter(id=self.kwargs.get('web_id',0)).first()
        print(web)
        contents = ContentModel.objects.filter(website=web)
        print(contents)
        context = {
            'contents':contents
        }
        print(context)
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        if 'like' in request.POST:
            content_id = request.POST['like']
            lm = LikeModel.objects.filter(content__id=content_id).first()
            if not lm:
                LikeModel.objects.create(content=ContentModel.objects.get(id=content_id), is_liked=True)
            else:
                l = LikeModel.objects.get(content__id=content_id)
                if l.is_liked:
                    l.is_liked = False
                else:
                    l.is_liked = True
                l.save()
        elif 'comment' in request.POST:
            content_id = request.POST['content_id']
            CommentModel.objects.create(content=ContentModel.objects.get(id=content_id),
                                        name = request.POST['name'],
                                        comment = request.POST['comment'])

        return super().get(request, *args, **kwargs)
    

class ContentUpdateView(UpdateView):
    template_name = 'content_update.html'
    model = ContentModel
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('content', args=(self.object.website.id,))
    
    

class ContentDeleteView(DeleteView):
    template_name = 'content_delete.html'
    model = ContentModel
    
    def get_success_url(self):
        return reverse_lazy('content', args=(self.object.website.id,))
