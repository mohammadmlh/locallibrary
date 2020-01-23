from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse ,reverse_lazy
import datetime

from .forms import RenewBookFrom
from . import  models
# Create your views here.
 
class Index(generic.TemplateView):
   template_name = "catalog/index.html"

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['num_books'] = models.Book.objects.all().count()
      context['num_instances'] = models.BookInstance.objects.all().count()
      context['num_instances_available'] = models.BookInstance.objects.filter(status__exact='a').count()
      context['num_authors'] = models.Author.objects.all().count()

      return context


class BookListView(generic.ListView):
   model = models.Book
   template_name = 'catalog/book_list.html'


class BookDetailView(generic.DetailView):
   model = models.Book
   template_name = 'catalog/book_detail.html'


class AuthorListView(generic.ListView):
   model = models.Author
   template_name = 'catalog/author_list.html'

class AuthorDetailView(generic.DetailView):
    model = models.Author
    template_name = 'catalog/author_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based View listing books on loan to current user
    """
    model = models.BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10


    def get_queryset(self):
        return models.BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')



def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    bookinst = get_object_or_404(models.BookInstance, pk=pk)

    #If this is a POST request then process the Form data
    if request.method == 'POST':

        #Create A Form instance and populate it with datat from the request
        form = RenewBookFrom(request.POST)

        #Check if the form is valid:
        if form.is_valid():
            bookinst.due_back = form.cleaned_data['renewal_date']
            bookinst.save()

            return HttpResponseRedirect(reverse('catalog:my-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookFrom(initial={'renewal_date': proposed_renewal_date,})

    context = {'form':form, 'bookinst':bookinst}
    return render(request, 'catalog/book_renew_librarian.html',context)

class AuthorCreate(generic.CreateView):
    model = models.Author
    fields = '__all__'
    initial = {'date_of_death':'05/01/2020',}

class AuthorUpdate(generic.UpdateView):
    model = models.Author
    fields = {'first_name', 'last_name', 'date_of_birth', 'date_of_death'}

class AuthorDelete(generic.DeleteView):
    model = models.Author
    success_url = reverse_lazy('catalog:authors')





"""
def index(request):
   
   #View function for home page of site
   

   #Generate counts of some of the main objects
   num_books = models.Book.objects.all().count()
   num_instances = models.BookInstance.objects.all().count()
   #Available books (status = 'a')
   num_instances_available = models.BookInstance.objects.all().filter(status__exact='a', ).count()
   num_authors = models.Author.objects.count()
   context = {'num_books':num_books,
               'num_instances':num_instances,
               'num_instances_available':num_instances_available,
               'num_authors':num_authors,}

   return render(request, 'catalog/index.html', context)
"""
