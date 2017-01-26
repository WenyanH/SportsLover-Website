import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from forms import *
from models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from mimetypes import guess_type
from django.http import HttpResponse, Http404
from datetime import datetime
from django.utils import timezone
from django.db.models import Count
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
import re


def search(request):
    notifications = {}
    groups = Group.objects.filter(member__username__contains=request.user).filter(date_end__lt=timezone.now()).order_by("time").reverse()
    for group in groups:
        if not Notification.objects.filter(reciever=request.user).filter(group=group):
            content = "Please comment and rank on the place " + group.place.name + " you have visited"
            new_notification = Notification(reciever=request.user, content=content, status="incomplete", group=group, types="comment")
            new_notification.save()
        if not Place.objects.filter(visitor__username__contains=request.user).filter(group=group):
            places = Place.objects.filter(group=group)
            for place in places:
                if request.user not in place.visitor.all():
                    place.visitor.add(request.user)
                    place.save()
    if request.user.is_authenticated() is True:
        group_notification = GroupNotification.objects.filter(reciever=request.user)
        friend_notification = FriendNotification.objects.filter(reciever=request.user)
        comment_notification = Notification.objects.filter(reciever=request.user).filter(status="incomplete")
        notifications = group_notification and friend_notification and comment_notification
    context = {
        'user': request.user,
        'notifications':notifications
    }
    return render(request, 'search.html', context)

@login_required
def update_news(request):
    notifications = GroupNotification.objects.filter(reciever=request.user)
    notification = list()
    for item in notifications:
        news = {}
        news['id'] = item.id
        news['context'] = item.content
        news['type']=item.types
        news['class']="group"
        notification.append(news)
    notifications = FriendNotification.objects.filter(reciever=request.user)
    for item in notifications:
        news = {}
        news['id'] = item.id
        news['context'] = item.content
        news['type']=item.types
        news['class']="friend"
        notification.append(news)
    notifications = Notification.objects.filter(reciever=request.user).filter(status="incomplete")
    for item in notifications:
        news = {}
        news['id'] = item.group.id
        news['context'] = item.content
        news['class']=item.types
        notification.append(news)
    response_text = json.dumps(notification, cls=DjangoJSONEncoder)
    return HttpResponse(response_text, content_type='application/json')

def popular_place(request):
    places = list()
    groups = Group.objects.annotate(num_member=Count('member')).filter(num_member__gt=0)
    for group in groups:
        places.append(group.place)
    place_list = list()
    item = {}
    for place in places:
        item[place.id] = len(place.visitor.all())
    item = sorted(item.iteritems(), key=lambda d:d[1], reverse = True)
    if len(item)>10:
        for i in range(0, 10):
            place_list.append(Place.objects.get(id=item[i][0]))
    else:
        for i in range(0, len(item)):
            place_list.append(Place.objects.get(id=item[i][0]))

    context = {'place_list':place_list}
    return render(request, 'popular_place.html', context)

def nearby_places(request):
    geolocator = Nominatim()
    places = Place.objects.all()
    current_location = (request.GET['lat'], request.GET['lng'])
    addresses = []
    for p in places:
        addresses.append(p.address)
    coords = []
    for address in addresses:
        # None object check
        if geolocator.geocode(address):
            location = (geolocator.geocode(address).latitude, geolocator.geocode(address).longitude)
            coords.append(location)
    place_distance = {}
    for i in range(len(coords)):
        place_distance[places[i].id] = vincenty(current_location, coords[i])

    place_distance = sorted(place_distance.iteritems(), key=lambda d: d[1])

    place_list = list()

    if len(place_distance) > 10:
        for i in range(0, 10):
            place_list.append(Place.objects.get(id=place_distance[i][0]))
    else:
        for i in range(0, len(place_distance)):
            place_list.append(Place.objects.get(id=place_distance[i][0]))

    context = {'place_list': place_list}

    return render(request, 'nearby_places.html', context)


def recent_sports(request):
    groups=Group.objects.annotate(num_member=Count('member')).filter(num_member__gt=0).order_by("time").reverse()
    group_list = list()
    if len(groups)>10:
        for i in range(0, 10):
            group_list.append(groups[i])
    else:
        for i in range(0, len(groups)):
            group_list.append(groups[i])
    context = {'group_list':group_list}
    return render(request, 'recent_sports.html', context)

def group(request):
    sportsitem = request.POST.get("item")
    date_begin = request.POST.get("start")
    date_end = request.POST.get("end")
    expense = request.POST.get("money")
    classsport = request.POST.get("classsport")
    itemsport = request.POST.get("itemsport")
    if sportsitem is None and date_begin is None and date_begin is None and date_end is None and expense is None and classsport is None and itemsport is None:
        groups=Group.objects.annotate(num_member=Count('member')).filter(num_member__gt=0)
    elif classsport is None and itemsport is None:
        groups=Group.objects.annotate(num_member=Count('member')).filter(num_member__gt=0)
        if sportsitem != "":
            sportsitem = SportsItem.objects.filter(item=sportsitem)
            groups = groups.filter(sportsitem=sportsitem)
        if date_begin !="":
            start = datetime.strptime(date_begin, "%m/%d/%Y")
            date_begin = start.strftime("%Y-%m-%d %H:%M:%S")
            groups = groups.filter(date_begin__gte=date_begin)
        if date_end != "":
            end = datetime.strptime(date_end+" 23:59:59", "%m/%d/%Y %H:%M:%S")
            date_end = end.strftime("%Y-%m-%d %H:%M:%S")
            groups = groups.filter(date_end__lte=date_end)
        if expense != "":
            if expense == "Free":
                groups = groups.filter(cost__exact=0.00)
            if expense == "Below 10$":
                groups = groups.filter(cost__lte=10.00)
            if expense == "10-20$":
                groups = groups.filter(cost__gte=10).filter(cost__lte=20)
            if expense == "20-50$":
                groups = groups.filter(cost__gte=20).filter(cost__lte=50)
            if expense == "50-100$":
                groups = groups.filter(cost__gte=50).filter(cost__lte=100)
            if expense == ">100$":
                groups = groups.filter(cost__gte=100.00)
    elif classsport is not None or itemsport is not None:
        if itemsport != "" and classsport != "":
            classsport = SportsClass.objects.get(name=classsport)
            itemsport = SportsItem.objects.filter(item=itemsport, label=classsport)
            for item in itemsport:
                sportsitem = item
            groups = Group.objects.annotate(num_member=Count('member')).filter(num_member__gt=0).filter(sportsclass=classsport, sportsitem=sportsitem).order_by("time").reverse()
        if itemsport == "" and classsport != "":
            classsport = SportsClass.objects.get(name=classsport)
            groups = Group.objects.annotate(num_member=Count('member')).filter(num_member__gt=0).filter(sportsclass=classsport).order_by("time").reverse()
    sportsitem = SportsItem.objects.all()
    sportsclass = SportsClass.objects.all()
    notifications = {}
    if request.user.is_authenticated() is True:
        notifications = GroupNotification.objects.filter(reciever=request.user) and FriendNotification.objects.filter(reciever=request.user) and Notification.objects.filter(reciever=request.user)
    latest_time = ""
    items = Group.objects.all().order_by("time").reverse()
    if len(items)!=0:
        latest_time = str(items[0].time)
    context = {
        'user': request.user,
        'groups':groups,
        'notifications':notifications,
        'sportsitem':sportsitem,
        'sportsclass':sportsclass,
        'latest_time':latest_time
    }
    return render(request, 'group.html', context)

def place(request):
    sportsitem = SportsItem.objects.all()
    sportsclass = SportsClass.objects.all()
    places = list()
    groups = Group.objects.annotate(num_member=Count('member')).filter(num_member__gt=0)
    for group in groups:
        places.append(group.place)
    items = list()
    for place in places:
        item = {}
        name = place.name
        item['name']=name
        item['id']=place.id
        groups = Group.objects.filter(place=place)
        for group in groups:
            if item.get('sportsitem') is None:
                item['sportsitem']=""
            item['sportsitem'] = item['sportsitem'] + " "+group.sportsitem.item
        item['cost'] = place.cost
        item['footprint'] = len(place.visitor.all())
        item['rank'] = place.rank
        items.append(item)
    context = {
        'items':items,
        'sportsitem':sportsitem,
        'sportsclass':sportsclass
    }
    return render(request, 'place.html', context)

def place_item(request, id):
    place = get_object_or_404(Place, id=id)
    groups = Group.objects.annotate(num_member=Count('member')).filter(num_member__gt=0).filter(place=place).order_by("time").reverse()
    current_groups = list()
    if len(groups)>3:
        for i in range(0, 3):
            group = {}
            group['id']=groups[i].id
            group['subject']=groups[i].subject
            group['owner'] = groups[i].owner
            group['time'] = groups[i].time
            group['sportsitem']=groups[i].sportsitem.item
            if groups[i].date_end >= timezone.now():
                group['status'] = 'In Progress'
            else:
                group['status'] = 'Past'
            current_groups.append(group)
    else:
        for i in range(0, len(groups)):
            group = {}
            group['id']=groups[i].id
            group['subject']=groups[i].subject
            group['owner'] = groups[i].owner
            group['time'] = groups[i].time
            group['sportsitem']=groups[i].sportsitem.item
            if groups[i].date_end >= timezone.now():
                group['status'] = 'In Progress'
            else:
                group['status'] = 'Past'
            current_groups.append(group)

    footprint = len(place.visitor.all())
    comments = Comment.objects.filter(place=place)
    info = Info.objects.all()
    place_image = PlaceImage.objects.filter(place=place)
    context = {
        'place':place, 
        'footprint':footprint,
        'current_groups': current_groups,
        'comments':comments,
        'info':info,
        'place_image':place_image
    }
    return render(request, 'place_item.html', context)
    
def signout(request):
    logout(request)
    return redirect(reverse('login'))

@login_required
def delete_notification_decline_group(request, id):
    item_to_delete = get_object_or_404(GroupNotification, reciever=request.user, id=id)
    item_to_delete.delete()
    return redirect(reverse('group'))

@login_required
def delete_notification_accept_group(request, id):
    update_group = GroupNotification.objects.get(id=id).group
    member = GroupNotification.objects.get(id=id).sender
    item_to_delete = get_object_or_404(GroupNotification, reciever=request.user, id=id)
    item_to_delete.delete()
    new_sender = request.user
    new_reciever = member
    content = new_sender.username +" has accepted your group request for group: " + update_group.subject 
    new_notification = GroupNotification(reciever=new_reciever,sender=new_sender,content=content, group=update_group, types="response")
    new_notification.save()
    if member not in update_group.member.all():
        update_group.member.add(member)
        update_group.save()
    return redirect(reverse('group'))

@login_required
def delete_news_decline_group(request, id):
    item_to_delete = get_object_or_404(FriendNotification, reciever=request.user, id=id)
    item_to_delete.delete()
    return redirect(reverse('group'))

@login_required
def delete_news_accept_group(request, id):
    sender = FriendNotification.objects.get(id=id).sender
    reciever = FriendNotification.objects.get(id=id).reciever
    new_friend = Friend.objects.get(user=reciever)
    another_new_friend = Friend.objects.get(user=sender)
    item_to_delete = get_object_or_404(FriendNotification, reciever=request.user, id=id)
    item_to_delete.delete()
    new_sender = request.user
    new_reciever = sender
    content = new_sender.username +" has accepted your friend request."
    new_notification = FriendNotification(reciever=new_reciever,sender=new_sender,content=content,types="response")
    new_notification.save()
    if sender not in new_friend.friend.all():
        new_friend.friend.add(sender)
        new_friend.save()
    if reciever not in another_new_friend.friend.all():
        another_new_friend.friend.add(reciever);
        another_new_friend.save()
    return redirect(reverse('group'))

@login_required
def delete_notification_decline_profile(request, id):
    item_to_delete = get_object_or_404(GroupNotification, reciever=request.user, id=id)
    item_to_delete.delete()
    return redirect(reverse('myprofile'))

@login_required
def delete_notification_accept_profile(request, id):
    update_group = GroupNotification.objects.get(id=id).group
    member = GroupNotification.objects.get(id=id).sender
    item_to_delete = get_object_or_404(GroupNotification, reciever=request.user, id=id)
    item_to_delete.delete()
    new_sender = request.user
    new_reciever = member
    content = new_sender.username +" has accepted your group request for group: " + update_group.subject 
    new_notification = GroupNotification(reciever=new_reciever,sender=new_sender,content=content,group=update_group, types="response")
    new_notification.save()
    if member not in update_group.member.all():
        update_group.member.add(member)
        update_group.save()
    return redirect(reverse('myprofile'))

@login_required
def delete_news_decline_profile(request, id):
    item_to_delete = get_object_or_404(FriendNotification, reciever=request.user, id=id)
    item_to_delete.delete()
    return redirect(reverse('myprofile'))

@login_required
def delete_news_accept_profile(request, id):
    sender = FriendNotification.objects.get(id=id).sender
    reciever = FriendNotification.objects.get(id=id).reciever
    new_friend = Friend.objects.get(user=reciever)
    another_new_friend = Friend.objects.get(user=sender)
    item_to_delete = get_object_or_404(FriendNotification, reciever=request.user, id=id)
    item_to_delete.delete()
    new_sender = request.user
    new_reciever = sender
    content = new_sender.username +" has accepted your friend request."
    new_notification = FriendNotification(reciever=new_reciever,sender=new_sender,content=content,types="response")
    new_notification.save()
    if sender not in new_friend.friend.all():
        new_friend.friend.add(sender)
        new_friend.save()
    if reciever not in another_new_friend.friend.all():
        another_new_friend.friend.add(reciever);
        another_new_friend.save()
    return redirect(reverse('myprofile'))

@login_required
def delete_notification_decline_search(request, id):
    item_to_delete = get_object_or_404(GroupNotification, reciever=request.user, id=id)
    item_to_delete.delete()
    return redirect(reverse('search'))

@login_required
def delete_notification_accept_search(request, id):
    update_group = GroupNotification.objects.get(id=id).group
    member = GroupNotification.objects.get(id=id).sender
    item_to_delete = get_object_or_404(GroupNotification, reciever=request.user, id=id)
    item_to_delete.delete()
    new_sender = request.user
    new_reciever = member
    content = new_sender.username +" has accepted your group request for group: " + update_group.subject 
    new_notification = GroupNotification(reciever=new_reciever,sender=new_sender,content=content, group=update_group, types="response")
    new_notification.save()
    if member not in update_group.member.all():
        update_group.member.add(member)
        update_group.save()
    return redirect(reverse('search'))

@login_required
def delete_news_decline_search(request, id):
    item_to_delete = get_object_or_404(FriendNotification, reciever=request.user, id=id)
    item_to_delete.delete()
    return redirect(reverse('search'))

@login_required
def delete_news_accept_search(request, id):
    sender = FriendNotification.objects.get(id=id).sender
    reciever = FriendNotification.objects.get(id=id).reciever
    new_friend = Friend.objects.get(user=reciever)
    another_new_friend = Friend.objects.get(user=sender)
    item_to_delete = get_object_or_404(FriendNotification, reciever=request.user, id=id)
    item_to_delete.delete()
    new_sender = request.user
    new_reciever = sender
    content = new_sender.username +" has accepted your friend request."
    new_notification = FriendNotification(reciever=new_reciever,sender=new_sender,content=content,types="response")
    new_notification.save()
    if sender not in new_friend.friend.all():
        new_friend.friend.add(sender)
        new_friend.save()
    if reciever not in another_new_friend.friend.all():
        another_new_friend.friend.add(reciever);
        another_new_friend.save()
    return redirect(reverse('search'))

@login_required
def friend_request(request):
    if request.method == 'GET':
        return render(request, 'friend_request.html')
    reciever_name = request.POST.get('reciever')
    reciever = User.objects.get(username=reciever_name)
    content = request.POST.get('notification')
    sender = request.user
    if not FriendNotification.objects.filter(reciever=reciever, sender=sender, content=content, types="request"):
        new_notification = FriendNotification(reciever=reciever, sender=sender, content=content, types="request")
        new_notification.save()
        response={"send":"never"}
    else:
        response={"send":"already"}
    response_data = json.dumps(response, cls=DjangoJSONEncoder)
    return HttpResponse(response_data, content_type='application/json')

@login_required
def group_request(request):
    if request.method == 'GET':
        return render(request, 'group_request.html')
    reciever_name = request.POST.get('reciever')
    reciever = User.objects.get(username=reciever_name)
    content = request.POST.get('notification')
    sender = request.user
    group_id = request.POST.get('groupid')
    group = Group.objects.get(id=group_id)
    if not request.user in group.member.all():
        if len(group.member.all())==group.size:
            context = {'status':'full'}
            return render(request, 'group_exist.html', context)
        else:
            if not GroupNotification.objects.filter(reciever=reciever, sender=sender, content=content, group=group, types="request"):
                new_notification = GroupNotification(reciever=reciever, sender=sender, content=content, group=group,types="request")
                new_notification.save()
                return render(request, 'group_request.html')
            else:
                context = {'status':'nofull', 'group':group, 'user':request.user}
                return render(request, 'group_exist.html', context)
    if request.user in group.member.all():
        context = {'group':group, 'user':request.user}
        return render(request, 'group_exist.html', context)

def group_detail(request, id):
    group = get_object_or_404(Group, id=id)
    if not group:
        raise Http404
    if group.date_begin < timezone.now():
        status = "past"
    else:
        status = "in"
    context = {'group':group, 'user':request.user, 'status':status}
    return render(request, 'group_detail.html', context)

@login_required
def update_group_info(request, id):
    group = get_object_or_404(Group, id=id)
    if not group:
        raise Http404
    context = {'group':group}
    return render(request, 'update_group_info.html', context)

@login_required
def profile(request, username):
    user =  get_object_or_404(User, username=username)
    info = Info.objects.get(user=user)
    groups = Group.objects.annotate(num_member=Count('member')).filter(num_member__gt=0).filter(owner=user).order_by("time").reverse()
    current_time = datetime.now()
    current_groups = Group.objects.filter(date_end__gte=current_time, member__username__contains=user).order_by("time").reverse()
    past_groups = Group.objects.filter(date_end__lt=current_time, member__username__contains=user)
    notifications = {}
    if request.user.is_authenticated() is True:
        notifications = GroupNotification.objects.filter(reciever=request.user) and FriendNotification.objects.filter(reciever=request.user)
    context = {
        'user': user,
        'info': info,
        'groups':groups,
        'current_groups':current_groups,
        'past_groups':past_groups,
        'notifications':notifications
    }
    return render(request, 'profile.html', context)

@login_required
def myprofile(request):
    info = Info.objects.get(user=request.user)
    groups = Group.objects.annotate(num_member=Count('member')).filter(num_member__gt=0).filter(owner=request.user).order_by("time").reverse()
    current_time = datetime.now()
    current_groups = Group.objects.filter(date_end__gte=current_time, member__username__contains=request.user).order_by("time").reverse()
    past_groups = Group.objects.filter(date_end__lt=current_time, member__username__contains=request.user)
    notifications = {}
    if request.user.is_authenticated() is True:
        notifications = GroupNotification.objects.filter(reciever=request.user) and FriendNotification.objects.filter(reciever=request.user)
    context = {
        'user': request.user,
        'info': info,
        'groups':groups,
        'current_groups':current_groups,
        'past_groups':past_groups,
        'notifications':notifications
    }
    return render(request, 'profile.html', context)

@login_required
def add_group(request):
    if request.method == "GET":
        context = {'form': GroupForm()}
        return render(request, 'create_group.html', context)
    form = GroupForm(request.POST)
    if not form.is_valid():
        context = {'form': form}
        return render(request, 'create_group.html', context)
    data = form.cleaned_data
    subject = data['subject']
    sportsitem = data['sportsitem']
    sportsclass = data['sportsclass']
    place = data['place']
    address = data['address']
    cost = data['cost']
    size = data['size']
    date_begin = data['date_begin']
    date_end = data['date_end']
    introduction = data['introduction']
    if not Place.objects.filter(name__exact=place, address__exact=address):
        new_place = Place(name=data['place'], address=data['address'])
        new_place.save()
    if not SportsClass.objects.filter(name__exact=sportsclass):
        new_sportsclass = SportsClass(name=sportsclass)
        new_sportsclass.save()
    sports_class = SportsClass.objects.get(name=sportsclass)
    new_sportsitem = SportsItem(item=sportsitem)
    new_sportsitem.save()
    new_sportsitem.label.add(sports_class)
    new_sportsitem.save()
    new_group = Group(
        owner=request.user, 
        subject=subject,
        sportsitem=new_sportsitem,
        sportsclass=sports_class,
        place=Place.objects.get(name=place, address=address),
        address=address,
        cost=cost,
        size=size,
        date_begin=date_begin,
        date_end=date_end,
        introduction=introduction
    )
    new_group.save()
    if request.user not in new_group.member.all():
        new_group.member.add(request.user)
        new_group.save()
    return render(request, 'create_confirmation.html')

@login_required
def create_group(request):
    context = {'form':GroupForm()}
    return render(request, 'create_group.html', context)

@login_required
def quit_group(request, id):
    group_to_quit = get_object_or_404(Group, id=id)
    group_to_quit.member.remove(request.user)
    if request.user == group_to_quit.owner:
        for person in group_to_quit.member.all():
            content = "Sorry, the group owner has dismissed the group: " + group_to_quit.subject
            new_notification = Notification(reciever=person, content=content, status="incomplete", group=group_to_quit, types="delete")
            new_notification.save()
            for member in group_to_quit.member.all():
                group_to_quit.member.remove(member)
    return redirect(reverse('myprofile'))

@login_required
def delete_confirm(request, id):
    group = get_object_or_404(Group, id=id)
    notification = get_object_or_404(Notification, reciever=request.user, group=group, types="delete")
    notification.status = "complete"
    notification.save()
    return redirect(reverse('myprofile'))

@login_required
def create_confirmation(request):
    return render(request, 'create_confirmation.html')

@login_required
def update_confirmation(request, id):
    group = get_object_or_404(Group, id=id)
    if request.method == "POST":
        cost = request.POST.get('cost')
        size = request.POST.get('size').split(' ')[0]
        date_begin = request.POST.get('start_time')
        date_end = request.POST.get('end_time')
        cost = float(re.search(r'\d+\.*\d*', cost).group())
        group.cost = cost
        group.size = int(size)
        if date_begin !="":
            start = datetime.strptime(date_begin, "%Y/%m/%d %H:%M")
            date_begin = start.strftime("%Y-%m-%d %H:%M:%S")
        if date_end != "":
            end = datetime.strptime(date_end, "%Y/%m/%d %H:%M")
            date_end = end.strftime("%Y-%m-%d %H:%M:%S")
        group.date_begin = date_begin
        group.date_end = date_end
        group.save()
    return render(request, 'update_confirmation.html')

@login_required
def password(request):
    context = {}
    form = PasswordForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'password.html', context)
    new_password = request.POST.get('password1')
    update_user = User.objects.get(username=request.user)
    update_user.set_password(new_password)
    update_user.save()
    return redirect('login')

@login_required
def setting(request):
    info = Info.objects.get(user=request.user)
    form = InfoForm(initial={
        'first_name': info.first_name, 
        'last_name': info.last_name, 
        'age': info.age,
        'bio': info.bio,
        'image': info.image
    })
    if request.POST != {}:
        form = InfoForm(request.POST, request.FILES)
    context = {'form': form}
    if not form.is_valid():
        return render(request, 'setting.html', context)
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    age = request.POST.get('age')
    bio = request.POST.get('bio')
    image = request.FILES.get('image')
    update_info = Info.objects.get(user=request.user)
    if image != None:
        update_info.image = image
    update_info.first_name = first_name
    update_info.last_name = last_name
    update_info.age = age
    update_info.bio = bio
    update_info.save()
    return redirect('myprofile')

def registration(request):
    context = {}

    if request.method == 'GET':
        context['form'] = UserForm()
        return render(request, 'signup.html', context)

    form = UserForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'signup.html', context)

    data = form.cleaned_data

    new_user = User.objects.create_user(username=data['username'], email=data['email'],
                                        password=data['password1'],
                                        first_name=data['first_name'],
                                        last_name=data['last_name'])
    new_user.save()
    new_user = authenticate(username=data['username'], password=data['password1'])
    login(request, new_user)
    new_info = Info(
        first_name=data['first_name'], last_name=data['last_name'], user=request.user
    )
    new_info.save()
    new_friend = Friend(user=request.user)
    new_friend.save()
    return redirect(reverse('search'))

def get_photo(request, id):
    info = get_object_or_404(Info, id=id)
    if not info.image:
        raise Http404
    content_type = guess_type(info.image.name)
    return HttpResponse(info.image, content_type=content_type)

def get_place_photo(request, id):
    placeimage = get_object_or_404(PlaceImage, id=id)
    if not placeimage.image:
        raise Http404
    content_type = guess_type(placeimage.image.name)
    return HttpResponse(placeimage.image, content_type=content_type)

@login_required
def manage_group(request):
    group_list = Group.objects.annotate(num_member=Count('member')).filter(num_member__gt=0).filter(owner=request.user).filter(date_begin__gt=timezone.now()).order_by("time").reverse()
    context = {'group_list':group_list}
    return render(request, 'manage_group.html', context)

@login_required
def get_groups(request):
    user = request.user
    groups = Group.objects.filter(member__username__contains=user).order_by("time").reverse()
    group_dict = {}
    group_dict['group'] = list()
    group_dict['group_subject'] = list()
    for item in groups:
        group_dict['group'].append(item.id)
        group_dict['group_subject'].append(item.subject)
    response_data = json.dumps(group_dict, cls=DjangoJSONEncoder)
    return HttpResponse(response_data, content_type='application/json')

@login_required
def get_friends(request):
    user = request.user
    if Friend.objects.filter(user=request.user):
        friend = Friend.objects.get(user=request.user)
    else:
        friend={}
    friends_dict = {}
    friends_dict['friend'] = list()
    friends = friend.friend.all()
    for item in friends:
        friends_dict['friend'].append(item.username)
    friends_dict['user'] = request.user.username
    response_data = json.dumps(friends_dict, cls=DjangoJSONEncoder)
    return HttpResponse(response_data, content_type='application/json')

@login_required
@ensure_csrf_cookie
def post_chat(request, id):
    return render(request, 'chatroom.html', {'id': id})

@login_required
def friend_chat(request, roomname):
    member_a=roomname.split("_")[0]
    member_b=roomname.split("_")[1]
    return render(request, 'friendroom.html', {'roomname':roomname, 'member_a':member_a, 'member_b':member_b})

@ensure_csrf_cookie
def add_chat(request):
    if not 'chat' in request.POST or not request.POST['chat']:
        raise Http404
    else:
        group_id = request.POST['group_id']
        new_chat = Chat(content=request.POST['chat'], sender=request.user, group=group_id)
        new_chat.save()

    return HttpResponse("")  # Empty response on success.


@ensure_csrf_cookie
# Returns all recent additions in the database, as JSON
def get_chats(request, time="1970-01-01T00:00+00:00"):
    max_time = Chat.get_max_time()
    group_id = request.POST['group_id']
    chats = Chat.get_chats(time, group_id=group_id)
    group = Group.objects.get(id=group_id)
    members = group.member.all()
    friends = Friend.objects.get(user=request.user).friend.all()
    context = {"max_time": max_time, "chats": chats, "user":request.user.username, "members":members,"friends":friends}
    return render(request, 'chats.json', context, content_type='application/json')

@ensure_csrf_cookie
# Returns all recent additions in the database, as JSON
def get_friend_chats(request, time="1970-01-01T00:00+00:00"):
    max_time = Chat.get_max_time()
    roomname = request.POST['roomname']
    chats = Chat.get_chats(time, group_id=roomname)
    context = {"max_time": max_time, "chats": chats, "user":request.user.username}
    return render(request, 'chats.json', context, content_type='application/json')

@ensure_csrf_cookie
# Returns all recent changes to the database, as JSON
def get_changes(request, time="1970-01-01T00:00+00:00"):
    max_time = Chat.get_max_time()
    group_id = request.POST['group_id']
    chats = Chat.get_changes(time, group_id=group_id)
    group = Group.objects.get(id=group_id)
    members = group.member.all()
    friends = Friend.objects.get(user=request.user).friend.all()
    context = {"max_time": max_time, "chats": chats, "user":request.user.username, "members":members, "friends":friends}
    return render(request, 'chats.json', context, content_type='application/json')


@ensure_csrf_cookie
# Returns all recent changes to the database, as JSON
def get_friend_changes(request, time="1970-01-01T00:00+00:00"):
    max_time = Chat.get_max_time()
    group_id = request.POST['roomname']
    chats = Chat.get_changes(time, group_id=group_id)
    context = {"max_time": max_time, "chats": chats, "user":request.user.username}
    return render(request, 'chats.json', context, content_type='application/json')

@ensure_csrf_cookie
def add_friend_chat(request):
    if not 'chat' in request.POST or not request.POST['chat']:
        raise Http404
    else:
        group_id = request.POST['roomname']
        new_chat = Chat(content=request.POST['chat'], sender=request.user, group=group_id)
        new_chat.save()
    return HttpResponse("")  # Empty response on success.


def update_groups(request):
    groups = {}
    latest_time = request.POST.get('latest_time')
    groups['groups']=list()
    items = Group.objects.annotate(num_member=Count('member')).filter(num_member__gt=0).filter(time__gt=latest_time).order_by("time").reverse()
    for item in items:
        group = {}
        time = str(item.time).split(' ')
        used_time = time[0] + " " + time[1].split('.')[0]
        group['id'] = item.id
        group['subject'] = item.subject
        group['owner'] = item.owner.username
        group['time'] = used_time
        group['place'] = item.place.name
        group['sportsitem'] = item.sportsitem.item
        group['size'] = item.size
        group['cost'] = item.cost
        group['date_begin']=item.date_begin
        groups['groups'].append(group)
    groups['latest_time'] = str(Group.objects.order_by('-pk')[0].time);
    response_text = json.dumps(groups, cls=DjangoJSONEncoder)
    return HttpResponse(response_text, content_type='application/json')

@login_required
def add_comment(request, id):
    group = get_object_or_404(Group, id=id)
    place = group.place
    if request.method == "POST":
        comment = request.POST.get('comment')
        rank = request.POST.get('rank')
        cost = request.POST.get('cost')

        rank = int(rank)
        new_rank = Rank(place=place,rank=rank)
        new_rank.save()
        ranks = Rank.objects.filter(place=place)
        update_rank = 0.0
        for item in ranks:
            update_rank = update_rank + item.rank
        update_rank = update_rank / len(ranks)
        place.rank = update_rank
        place.save()

        new_cost = Cost(place=place, cost=cost)
        new_cost.save()
        costs = Cost.objects.filter(place=place)
        update_cost = 0.0
        for item in costs:
            update_cost = update_cost + float(item.cost)
        update_cost = update_cost / len(costs)
        place.cost = update_cost
        place.save()

        new_comment = Comment(place=place, author=request.user, text=comment)
        new_comment.save()

        for filename, image in request.FILES.iteritems():
            if image != None:
                new_image = PlaceImage(place=place, image=image)
                new_image.save()

        notification = get_object_or_404(Notification, reciever=request.user, group=group, types="comment")
        notification.status = "complete"
        notification.save()
        return redirect('place_item', id=place.id)
    else:
        context={'place':place}
        return render(request, 'add_comment.html', context)


def charge(request):
    context = {}
    return render(request, "generatePaymentLink.html", context)


def get_places(request):
    groups = Group.objects.filter(date_end__gt=timezone.now())
    return_dict = {'address': list(), 'subject': list(), 'cost': list(), 'size': list(), 'date_begin': list(),
                   'date_end': list(), 'owner': list(), 'id':list()}
    for g in groups:
        return_dict['subject'].append(g.subject)
        return_dict['cost'].append(g.cost)
        return_dict['size'].append(g.size)
        return_dict['address'].append(g.address)
        return_dict['date_begin'].append(g.date_begin.date())
        return_dict['date_end'].append(g.date_end.date())
        return_dict['owner'].append(g.owner.username)
        return_dict['id'].append(g.id)
    response_data = json.dumps(return_dict, cls=DjangoJSONEncoder)
    return HttpResponse(response_data, content_type='application/json')

