from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Article, Category, Comment
from django.contrib.auth.models import User
from django.db.models import Q

def home(request):
    articles = Article.objects.all().order_by('-created_date')[:5]
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'articles': articles,
        'categories': categories
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Login yoki parol xato!')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu username allaqachon mavjud!')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            return redirect('home')
    
    return render(request, 'register.html')

# ✅ profile funksiyasi - LOGINSIZ (login_required O'CHIRILDI)
def profile(request):
    # Agar user login qilgan bo'lsa, uning maqolalarini ko'rsatadi
    # Agar login qilmagan bo'lsa, barcha maqolalarni ko'rsatadi
    if request.user.is_authenticated:
        user_articles = Article.objects.filter(author=request.user)
    else:
        user_articles = Article.objects.none()  # Login qilmagan bo'lsa bo'sh ro'yxat
        messages.info(request, 'Profilni ko\'rish uchun iltimos, kirish qiling yoki ro\'yxatdan o\'ting!')
    
    return render(request, 'profile.html', {
        'user_articles': user_articles
    })

def about(request):
    return render(request, 'about.html')

def pages(request):
    # Barcha maqolalarni olish
    articles = Article.objects.all()
    
    # Qidiruv so'rovi
    query = request.GET.get('search', '')
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    # Kategoriya filtri
    category_id = request.GET.get('category', '')
    if category_id and category_id.isdigit():
        articles = articles.filter(category_id=category_id)
    
    # Tartiblash
    sort = request.GET.get('sort', '-created_date')
    if sort == 'title_asc':
        articles = articles.order_by('title')
    elif sort == 'title_desc':
        articles = articles.order_by('-title')
    elif sort == 'popular':
        articles = articles.order_by('-comments_count')
    else:
        articles = articles.order_by('-created_date')
    
    # Kategoriyalarni olish
    categories = Category.objects.all()
    
    context = {
        'articles': articles,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'selected_sort': sort,
    }
    
    return render(request, 'pages.html', context)

def contact(request):
    return render(request, 'contact.html')

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all()
    
    # Comment qo'shish (istalgan user qo'sha oladi, lekin login qilgan bo'lishi kerak)
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_text = request.POST.get('comment')
            if comment_text:
                Comment.objects.create(
                    article=article,
                    user=request.user,
                    text=comment_text
                )
                article.comments_count += 1
                article.save()
                messages.success(request, 'Izoh qo\'shildi!')
            else:
                messages.error(request, 'Izoh matni bo\'sh bo\'lishi mumkin emas!')
        else:
            messages.error(request, 'Izoh qoldirish uchun iltimos, kirish qiling!')
        return redirect('article_detail', pk=article.pk)
    
    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments
    })

def books_view(request):
    # Kitoblar kategoriyasidagi maqolalarni olish
    books_articles = Article.objects.none() # hech bo'lmaganda bo'sh
    try:
        books_category = Category.objects.get(name='Books')
        books_articles = Article.objects.filter(category=books_category).order_by('-created_date')
    except Category.DoesNotExist:
        # Kategoriya mavjud emas, hech narsa qilma, shunchaki bo'sh o'tib ket
        pass 
    return render(request, 'books.html', {
        'articles': books_articles
    })