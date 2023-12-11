from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Category
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EditItemForm

# Create your views here.

# searching / browsing
def items(request):
    query = request.GET.get('query','')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)
    
    # filter out the categories
    if category_id:
        items = items.filter(category_id = category_id)
        
    # if the query text contained in name or description of the product then it gets filtered out
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html',{
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })

# detail view
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    # related_item = Item.objects.all()
    related_item = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(request, 'item/details.html', {
        'item':item,
        'related_item':related_item,
    })

# creating a new item
@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid:
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()


    return render(request, 'item/form.html',{
        'form': form,
        'title': 'New item',
    })


# editing existing item information
@login_required
def edit(request,pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid:
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)


    return render(request, 'item/form.html',{
        'form': form,
        'title': 'Edit item',
    })

# deleting an item
@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    return redirect('dashboard:index')