from django.db.models.query import QuerySet
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.contrib.auth.hashers import make_password, check_password

from .models import *
from .crypto import transact
from .config import web3


def index(request):
    return redirect('blog')


def logout(request):
    if not request.session.get('logged_in', False):
        return redirect('index')

    request.session['logged_in'] = False
    del request.session['user_id']

    return redirect('index')
    

def donate(request):
    if not request.POST:
        return HttpResponseForbidden('Only POST method allowed')
    
    from_account = request.POST['fromAccount']
    to_account = request.POST['toAccount']
    value = request.POST['value']
    pk = request.POST['privateKey']

    trx = transact(web3, from_account, to_account, value, pk)

    context = {
        'title': 'Transaction Details' if trx['success'] else 'Transaction Error',
        'status': trx['success'],
        'details': trx['details'],
        'logged_in': request.session.get('logged_in', False)
    }

    return render(
        request=request,
        template_name='main/transactionDetails.html',
        context=context
    )


def write_article(request):
    if not request.session.get('logged_in', False):
        return redirect('index')
    
    if not request.POST:
        return render(
            request=request,
            template_name='main/writeArticle.html',
            context={
                'title': 'Write Article',
                'logged_in': request.session.get('logged_in', False)
            }
        )
    
    title = request.POST['title']
    mins = request.POST['mins']
    content = request.POST['content']

    article = Article(
        title=title,
        slug=slugify(title),
        mins_to_read=int(mins),
        content=content,
        author=User.objects.get(pk=request.session['user_id'])
    )

    article.save()

    return redirect(article.get_absolute_url())

    


def login_form(request):
    if request.session.get('logged_in', False):
        return redirect('index')
    
    if not request.POST:
        return render(
            request=request,
            template_name='main/login.html',
            context={ 'title': 'Login' }
        )
    
    username = request.POST['username']
    password = request.POST['password']

    user = User.objects.filter(username=username).first()

    if user:
        if check_password(password, user.hashed_password):
            request.session['logged_in'] = True
            request.session['user_id'] = user.pk

            return redirect('index')
        
    return render(
        request=request,
        template_name='main/login.html',
        context={ 'title': 'Login', 'loginError': True }
    )


def register_form(request):
    if request.session.get('logged_in', False):
        return redirect('index')

    if not request.POST:
        return render(
            request=request,
            template_name='main/register.html',
            context={ 'title': 'Register' }
        )
    
    name = request.POST['name']
    username = request.POST['username']
    eth_address = request.POST['ethAddress']
    password = request.POST['password1']

    user = User.objects.filter(username=username).first()

    if user:
        return HttpResponseBadRequest(f'User {username} already exist')
    
    user = User(
        name=name,
        username=username,
        eth_address=eth_address,
        hashed_password=make_password(password)
    )

    user.save()

    return redirect('login')
    

class RenderArticle(DetailView):
    model = Article
    template_name = 'main/article.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'article'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['article']
        context['logged_in'] = self.request.session.get('logged_in', False)

        if context['logged_in']:
            user = User.objects.get(pk=self.request.session['user_id'])
            context['user_eth_address'] = user.eth_address

        return context


class RenderBlog(ListView):
    model = Article
    template_name = 'main/blog.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Articles'
        context['logged_in'] = self.request.session.get('logged_in', False)
        return context
    
    def get_queryset(self) -> QuerySet[Article]:
        return Article.objects.all()


def render_user(request, username):
    user = User.objects.filter(username=username).first()

    if not user:
        return HttpResponseBadRequest(f'User {username} not found')
    
    context={
        'title': username,
        'logged_in': request.session.get('logged_in', False),
        'user': user,
        'user_articles': Article.objects.filter(author=user).all()
    }

    if request.session['logged_in']:
        me = User.objects.get(pk=request.session['user_id'])
        context['user_eth_address'] = me.eth_address

    return render(
        request=request,
        template_name='main/user.html',
        context=context
    )


def about(request):
    return render(
        request=request,
        template_name='main/about.html',
        context={
            'title': 'About',
            'logged_in': request.session.get('logged_in', False)
        }
    )


