from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
# create your views here.
def index(r):
    return render(r, 'learning_logs/index.html')
@login_required
def topics(r):
    topics = Topic.objects.filter(owner=r.user).order_by('date_added')
    context = {'topics': topics}
    return render(r, 'learning_logs/topics.html', context)
@login_required
def topic(r, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if r.user == "admin":
        pass
    elif topic.owner != r.user:
        raise Http404 
    entries = topic.entry_set.order_by('-date_added') 
    context = {'topic': topic, 'entries': entries} 
    return render(r, 'learning_logs/topic.html', context)
@login_required
def new_topic(r):
    if r.method == "GET":
        form = TopicForm()
    elif r.method == "POST":
        form = TopicForm(data=r.post)
        if form.is_valid():
            new_topic = form.save(commit=false) 
            new_topic.owner = r.user 
            new_topic.save() 
            print("success")
            return redirect("learning_logs:topics")
    else:
        raise http404("wrong request method")
    context = {"form": form}
    return render(r, "learning_logs/new_topic.html", context)
@login_required
def new_entry(r, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if r.user == "admin":
        pass
    elif topic.owner != r.user:
        raise Http404  
    if r.method == "GET":
        form = EntryForm()
    elif r.method == "POST":
        form = EntryForm(data=r.post)
        new_entry.topic = topic
        new_entry.save()
        return redirect("learning_logs:topic", topic_id=topic_id)
    else:
        raise Http404("wrong request method")
    context = {"topic":topic, "form":form}
    return render(r, "learning_logs/new_entry.html", context)
@login_required
def edit_entry(r, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if r.user == "admin":
        pass
    elif topic.owner != r.user:
        raise Http404 
    if r.method == "GET":
        form = EntryForm(instance=entry)
    elif r.method == "POST":
        form = EntryForm(instance=entry, data=r.POST)
        new_entry.topic = topic
        new_entry.save()
        return redirect("learning_logs:topic", topic_id=topic.id)
    else:
        raise Http404("Wrong Request Method")
    context = {"entry":entry, "topic":topic, "form":form}
    return render(r, "learning_logs/edit_entry.html", context)
