from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm
from .models import Category


def category_detail(request: HttpRequest, category_id):
    # Logic to retrieve category details using category_id
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(
                request=request, message='Category updated successfully!', extra_tags='success')
            next_url = request.META.get('HTTP_REFERER', 'home')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('category:category_detail', category_id=category_id)
        else:
            messages.error(
                request=request, message='Failed to update category.', extra_tags='danger')

            print(f"==>*** {form.errors} ***<==")

            return render(request, 'category/category_detail.html', {'form': form, 'category_id': category_id})
    else:
        form = CategoryForm(instance=category)
        context = {
            'form': form,
            'category': category,
        }
        return render(request, 'category/category_detail.html', context)


def category_list(request):
    # Logic to retrieve a list of categories
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})


def category_create(request: HttpRequest):
    # Logic to handle category creation
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request=request, message='Category created successfully!', extra_tags='success')
            return redirect('category:category_list')
        else:
            messages.error(
                request=request, message='Failed to create category.', extra_tags='danger')
    else:
        form = CategoryForm()
    return render(request, 'category/category_create.html', {'form': form})


def category_update(request, category_id):
    # Logic to handle category update
    # For example:
    # category = get_object_or_404(Category, id=category_id)
    # if request.method == 'POST':
    #     form = CategoryForm(request.POST, instance=category)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('category_detail', category_id=category.id)
    # else:
    #     form = CategoryForm(instance=category)
    # return render(request, 'category_form.html', {'form': form})
    pass


def category_delete(request: HttpRequest, category_id):
    # Logic to handle category deletion
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(
        request=request, message='Category deleted successfully!', extra_tags='success')
    return redirect('category:category_list')


def category_search(request):
    # Logic to handle category search
    # For example:
    # query = request.GET.get('q')
    # categories = Category.objects.filter(name__icontains=query)
    # return render(request, 'category_list.html', {'categories': categories})
    pass


def category_filter(request):
    # Logic to handle category filtering
    # For example:
    # filter_criteria = request.GET.get('filter')
    # categories = Category.objects.filter(criteria=filter_criteria)
    # return render(request, 'category_list.html', {'categories': categories})
    pass


def category_sort(request):
    # Logic to handle category sorting
    # For example:
    # sort_by = request.GET.get('sort')
    # categories = Category.objects.all().order_by(sort_by)
    # return render(request, 'category_list.html', {'categories': categories})
    pass


def category_paginate(request):
    # Logic to handle category pagination
    # For example:
    # categories = Category.objects.all()
    # paginator = Paginator(categories, 10)  # Show 10 categories per page
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    # return render(request, 'category_list.html', {'page_obj': page_obj})
    pass


def category_export(request):
    # Logic to handle category export
    # For example:
    # categories = Category.objects.all()
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="categories.csv"'
    # writer = csv.writer(response)
    # writer.writerow(['ID', 'Name', 'Description'])
    # for category in categories:
    #     writer.writerow([category.id, category.name, category.description])
    # return response
    pass


def category_import(request):
    # Logic to handle category import
    # For example:
    # if request.method == 'POST':
    #     file = request.FILES['file']
    #     # Logic to process the uploaded file and import categories
    # return render(request, 'category_import.html')
    pass


def category_bulk_update(request):
    # Logic to handle bulk update of categories
    # For example:
    # if request.method == 'POST':
    #     formset = CategoryFormSet(request.POST)
    #     if formset.is_valid():
    #         formset.save()
    #         return redirect('category_list')
    # else:
    #     formset = CategoryFormSet(queryset=Category.objects.all())
    # return render(request, 'category_bulk_update.html', {'formset': formset})
    pass


def category_bulk_delete(request):
    # Logic to handle bulk deletion of categories
    # For example:
    # if request.method == 'POST':
    #     selected_ids = request.POST.getlist('selected_ids')
    #     Category.objects.filter(id__in=selected_ids).delete()
    #     return redirect('category_list')
    # categories = Category.objects.all()
    # return render(request, 'category_bulk_delete.html', {'categories': categories})
    pass


def category_archive(request):
    # Logic to handle category archiving
    # For example:
    # categories = Category.objects.filter(is_archived=True)
    # return render(request, 'category_archive.html', {'categories': categories})
    pass
