from django.shortcuts import render
from .models import Link
from .forms import AddLinkForm
# Create your views here.
from django.views.generic import DeleteView
from django.urls import reverse_lazy
import traceback


def home_view(request):
  no_discounted = 0
  error = None

  form = AddLinkForm(request.POST or None)

  if request.method =="POST":
    try:
      if form.is_valid():
        form.save()
    except AttributeError:
      error = "Ops.. Couldn't get the name and proce"
    except:
      error = "Ops.. Something went wrong"

  form = AddLinkForm()
  qs = Link.objects.all()
  item_no = qs.count()
  discount_list = []
  
  if item_no > 0:
    for item in qs:
      if item.old_price > item.current_price:
        discount_list.append(item)
      no_discounted = len(discount_list)

  context = {
    'qs': qs,
    'item_no': item_no,
    'no_discounted': no_discounted,
    'form':form,
    'error':error
  }
  
  return render(request, 'links/main.html', context)  


class LinkDeleteView(DeleteView):
  try:
    model = Link
    template_name = 'links/confirm_del.html'
    success_url =reverse_lazy('home')
  except BaseException as e:
    # traceback.print_exc()
    print(e)