# learning_logs/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm,  EntryForm
from django.http import Http404
from django.utils.html import mark_safe

def index(request):
    """
    The home page for Learning Log.

    Parameters:
        - request: HttpRequest object

    Returns:
        - HttpResponse
    """
    return render(request, 'learning_logs/index.html')

@login_required
def topic(request, topic_id):
    """
    Show a single topic and all its entries.

    Parameters:
        - request: HttpRequest object
        - topic_id: ID of the topic to be displayed


    Returns:
        - HttpResponse
    """
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
       raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def topics(request):
    """
    Show all topics.

    Parameters:
        - request: HttpRequest object

    Returns:
        - HttpResponse
    """
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def new_topic(request):
    """
    Add a new topic.

    Parameters:
        - request: HttpRequest object

    Returns:
        - HttpResponse
    """
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user  
            new_topic.save()
            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """
    Add a new entry for a particular topic.

    Parameters:
        - request: HttpRequest object
        - topic_id: int, ID of the topic for which a new entry is added

    Returns:
        - HttpResponse
    """
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """
    Edit an existing entry.

    Parameters:
        - request: HttpRequest object
        - entry_id: int, ID of the entry to be edited

    Returns:
        - HttpResponse
    """
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            # Mark the content as safe before saving it
            entry = form.save(commit=False)
            entry.text = mark_safe(entry.text)
            entry.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
        else:
            print("Form errors:", form.errors)
    else:
        form = EntryForm(instance=entry)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


def delete_topic(request, topic_id):
    """Delete a topic."""
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')

    context = {'topic': topic}
    return render(request, 'learning_logs/delete_topic.html', context)