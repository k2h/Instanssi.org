# -*- coding: utf-8 -*-

from django.http import Http404,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from Instanssi.admin_base.misc.custom_render import admin_render
from Instanssi.ext_programme.models import ProgrammeEvent
from Instanssi.admin_programme.forms import ProgrammeEventForm

@login_required(login_url='/manage/auth/login/')
def index(request, sel_event_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http404
    
    # Create form
    if request.method == "POST":
        # Check rights
        if not request.user.has_perm('ext_programme.add_programmeevent'):
            raise Http404
        
        # Handle form
        form = ProgrammeEventForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.event_id = int(sel_event_id)
            data.save()
            return HttpResponseRedirect("/manage/"+sel_event_id+"/programme/")
    else:
        form = ProgrammeEventForm()
    
    # Filter programme events by selected event
    pevs = ProgrammeEvent.objects.filter(event_id=int(sel_event_id))
    
    # Render response
    return admin_render(request, "admin_programme/index.html", {
        'pevs': pevs,
        'selected_event_id': int(sel_event_id),
        'eventform': form,
    })

@login_required(login_url='/manage/auth/login/')
def edit(request, sel_event_id, pev_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http404
    
    # Check rights
    if not request.user.has_perm('ext_programme.change_programmeevent'):
        raise Http404
    
    # Get event
    pev = get_object_or_404(ProgrammeEvent, pk=pev_id)
    
    # Create form
    if request.method == "POST":
        form = ProgrammeEventForm(request.POST, request.FILES, instance=pev)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/manage/"+sel_event_id+"/programme/")
    else:
        form = ProgrammeEventForm(instance=pev)
    
    # Render response
    return admin_render(request, "admin_programme/edit.html", {
        'eventform': form,
        'event': pev,
        'selected_event_id': int(sel_event_id),
    })

@login_required(login_url='/manage/auth/login/')
def delete(request, sel_event_id, pev_id):
    # Make sure the user is staff.
    if not request.user.is_staff:
        raise Http404
    
    # Check rights
    if not request.user.has_perm('ext_programme.delete_programmeevent'):
        raise Http404
    
    # Delete event
    try:
        ProgrammeEvent.objects.get(id=pev_id).delete()
    except:
        raise Http404
    
    # Render response
    return HttpResponseRedirect("/manage/"+sel_event_id+"/programme/")

