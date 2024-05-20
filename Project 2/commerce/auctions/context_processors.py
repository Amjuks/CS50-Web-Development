from .models import Category
from .forms import CommentForm

def categories(request):
    return {'categories': Category.objects.all()}

def comment_form(request):
    return {'comment_form': CommentForm()}