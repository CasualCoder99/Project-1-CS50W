from django.shortcuts import render,redirect

import random
from . import util
from .forms import EntryCreationForm, EditEntryForm
from django.contrib import messages

def index(request):
	if(request.method=="POST"):
		return search(request)
	else:
		return render(request, "encyclopedia/index.html", {
		 "entries": util.list_entries()
		    })

from markdown2 import Markdown

def title_view(request,title):
	if(request.method=="POST"):
		return search(request)
	content=util.get_entry(title)
	#print(content.split())
	if(content is None):
		return render(request,'encyclopedia/404.html')
	else:
		markdowner=Markdown()
		html_content=markdowner.convert(content)
		return render(request,'encyclopedia/title.html',{'content':html_content,
															'title':title})

def edit_entry(request,title):
	if(title not in util.list_entries()):
		messages.warning(f"The entry you want to edit doesn't exist!")
		return redirect('/')
	else:
		entry=util.get_entry(title)
		if(request.method=="POST"):
			form=EditEntryForm(request.POST)
			if(form.is_valid()):
				util.save_entry(form.cleaned_data['title'].capitalize(),form.cleaned_data['entry'])
				return redirect(f'/wiki/{title}')
		initial_dict={'title':title,'entry':entry}
		form=EditEntryForm(request.POST or None, initial=initial_dict)
		return render(request,'encyclopedia/new_post.html',{'form':form})

def search(request):
	title=str(request.POST["q"]).lower()
	content=util.get_entry(title)
	if(content):
		return redirect(f"/wiki/{title.capitalize()}")
	else:
		results=[]
		for query in util.list_entries():
			query=query.lower()
			if(query.find(title)!=-1):
				results.append(query.capitalize())
		#print(results)
		return render(request,"encyclopedia/search_results.html",{"results":results})

def new_post(request):
	if(request.method=='POST'):
		form=EntryCreationForm(request.POST)
		if(form.is_valid() and form.cleaned_data['title'].capitalize() not in util.list_entries()):
			util.save_entry(form.cleaned_data['title'].capitalize(),form.cleaned_data['entry'])
			return redirect(f"/wiki/{form.cleaned_data['title']}")
		else:
			#print(form.cleaned_data['title'].capitalize() in util.list_entries())
			if(form.cleaned_data['title'].capitalize() in util.list_entries()):
				messages.warning(request,f'This title already exists!')
				return render(request,'encyclopedia/new_post.html',{'form':form})
		return render(request,'encyclopedia/new_post.html',{'form':form})
	form=EntryCreationForm()
	return render(request,'encyclopedia/new_post.html',{'form':form})

def get_random(request):
	a=util.list_entries()
	i=random.randint(0,len(a)-1)
	title=a[i]
	return redirect(f'/wiki/{title}')