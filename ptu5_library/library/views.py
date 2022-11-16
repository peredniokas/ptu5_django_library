from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from . models import Genre, Author, Book, BookInstance

# Create your views here.

def index(request):
    # return HttpResponse("Sveiki atvyke!")
    book_count = Book.objects.count()
    book_instance_count = BookInstance.objects.count()
    book_instance_available_count = BookInstance.objects.filter(status='a').count()
    author_count = Author.objects.count()
    visits_count = request.session.get('visits_count', 1)
    request.session['visits_count'] = visits_count + 1
    
    context = {
        'book_count': book_count,
        'book_instance_count': book_instance_count,
        'book_instance_available_count': book_instance_available_count,
        'author_count': author_count,
        'genre_count': Genre.objects.count(),
        'visits_count': visits_count,
    }

    return render(request, 'library/index.html', context)


def authors(request):
    paginator = Paginator(Author.objects.all(), 5)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    return render(request, 'library/authors.html', {'authors': paged_authors })

def author(request, author_id):
    return render(request, 'library/author.html', {'author': get_object_or_404(Author, id=author_id)})


class BookListView(ListView):
    model = Book
    paginate_by = 5
    template_name = 'library/book_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(summary__icontains=search))
        genre_id = self.request.GET.get('genre_id')
        if genre_id:
            queryset = queryset.filter(genre__id=genre_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['books_count'] = Book.objects.count()
        context['books_count'] = self.get_queryset().count()
        genre_id = self.request.GET.get('genre_id')
        context['genres'] = Genre.objects.all()
        if genre_id:
            context['genre'] = get_object_or_404(Genre, id=genre_id)
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'


class UserBookListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'library/user_book_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(reader=self.request.user).order_by('due_back')
        return queryset