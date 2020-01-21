from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date
# Create your models here.


class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction)
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g Science Fiction)")

    def __str__(self):
        """
        String for representing the model object (in Admin site etc.)
        """
        return self.name

class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """

    title =  models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summaty = models.TextField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number </a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    
    def __str__(self):
        """
        String for representing the Model object
        """
        return self.title
    
    def get_absolute_url(self):
        """
        Return the url to access a paticular book instance
        """
        return reverse('catalog:book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Creates a String for the Genre. this is required to display genre in Admin
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this paticular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
            ('m', 'Maintenance'),
            ('o', 'On loan'),
            ('a', 'Available'),
            ('r', 'Reserved'), 
            )
    
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text="Book availability")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id,self.book.title)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

class Author(models.Model):
    """
    Model representing an Author
    """
    first_name = models.CharField(max_length=100) 
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Returns the url to access a paticular author instance
        """
        return reverse('catalog:author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the model object
        """
        return '(%s, %s)' % (self.last_name, self.first_name)
