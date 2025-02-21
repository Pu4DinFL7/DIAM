from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from PIL import Image as PILImage

from .models import Image, Rats, LikedGames, BookmarkImage
from .models import Comment
from django.contrib import messages


def teste(request):
    latest_image_list = Image.objects.order_by('-views')[:10]
    most_liked_list = Image.objects.order_by('-likes')[:10]
    recently_added_list = Image.objects.order_by('-pub_date')[:10]
    context ={'latest_image_list' : latest_image_list, 'most_liked_list': most_liked_list, 'recently_added_list': recently_added_list}
    return render(request, 'teste.html', context)

def show_all_games(request):
    latest_image_list = Image.objects.order_by('name')
    context = {'latest_image_list': latest_image_list}
    return render(request, 'show_all_games.html', context)

def image_detail(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    new_liked_game = LikedGames()
    commentList = Comment.objects.filter(image_id = image_id).order_by('-comment_data')[:10]
    liked=False
    bookmarked = False
    new_bookmark_images = BookmarkImage()
    if request.user.is_authenticated:
        rats = get_object_or_404(Rats, user_id=request.user.rats.user_id)

        liked = LikedGames.objects.filter(user=rats, image=image).exists()
        bookmarked = BookmarkImage.objects.filter(user=rats, image=image).exists()
        if request.method == 'POST' and 'remove' in request.POST:
            image.delete()
            messages.success(request, 'Game removed successfully!')
            return redirect('games_hub_app:teste')
        if request.method == 'POST' and 'bookmark' in request.POST and not BookmarkImage.objects.filter(user=rats, image=image).exists():
            image.bookmark = True
            image.save()
            new_bookmark_images.user = rats
            new_bookmark_images.image = image
            new_bookmark_images.save()
            return HttpResponseRedirect(reverse('games_hub_app:image_detail', args=[image_id]))
        if request.method == 'POST' and 'bookmark' in request.POST and BookmarkImage.objects.filter(user=rats,
                                                                                                    image=image).exists():
            image.bookmark = False
            image.save()
            new_bookmark_images2 = BookmarkImage.objects.get(user=rats, image=image)
            new_bookmark_images2.delete()
            return HttpResponseRedirect(reverse('games_hub_app:image_detail', args=[image_id]))
        if request.method == 'POST' and 'like' in request.POST and  not LikedGames.objects.filter(user=rats, image=image).exists():
            image.likes+=1
            image.save()
            new_liked_game.user = rats
            new_liked_game.image = image
            new_liked_game.save()
            url = reverse('games_hub_app:image_detail', args=[image_id])
            image.views -= 1
            image.save()
            return HttpResponseRedirect(url)
        if request.method == 'POST' and 'like' in request.POST and  LikedGames.objects.filter(user=rats, image=image).exists():
            image.likes -=1
            image.save()
            new_liked_game2 = LikedGames.objects.get(user=rats,image=image)
            new_liked_game2.delete()
            url = reverse('games_hub_app:image_detail', args=[image_id])
            image.views -= 1
            image.save()
            return HttpResponseRedirect(url)

        image.views += 1
        image.save()
    else:

        if request.method == 'POST' and 'bookmark' in request.POST:
            messages.info(request, 'You need to login to favourite a game!')
            return HttpResponseRedirect(reverse('games_hub_app:loginview'))

        if request.method == 'POST' and 'like' in request.POST:
            messages.info(request, 'You need to login to like a game!')
            return HttpResponseRedirect(reverse('games_hub_app:loginview', ))
        else:
            image.views += 1
            image.save()
    return render(request, 'imageDetail.html', { 'image': image, 'commentList': commentList, 'liked': liked, 'bookmarked': bookmarked})



def new_comment(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    if request.user.is_authenticated:
        try:
            request.POST.get('new_comment')
        except IOError:
            messages.success(request, 'Your comment!')
            return redirect('games_hub_app:image_detail', image_id=image_id)

        if request.method == 'POST' and request.POST.get('new_comment') != '':
            new_comment = Comment()
            new_comment.comment_text = request.POST['new_comment']
            new_comment.comment_data = datetime.now()
            new_comment.image = image
            new_comment.user = request.user.rats
            new_comment.rating = request.POST['rate']
            new_comment.save()
            messages.success(request, 'Your comment has been successfully submitted!')
            return redirect('games_hub_app:image_detail', image_id=image_id)

    else:
        messages.info(request, 'You need to login to comment a game!')
        return HttpResponseRedirect(reverse('games_hub_app:loginview', ))
    return render(request, 'new_comment.html', {'image': image})


def new_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not username or not password or not email:

            return HttpResponse('Campos não preenchidos')
        else:
            u = User.objects.create_user(username, email, password)
            a = Rats(user=u)
            a.save()

            messages.success(request, 'Your account has been successfully created!')

            return redirect('games_hub_app:teste')

    else:
        # If the request method is not POST, return the form template
        return render(request, 'new_account.html')
    return render(request, 'new_account.html', )

def loginview(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username,password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('games_hub_app:teste',))
    # direccionar para página de sucesso
    return render(request, 'login.html',)

@login_required
def favourite_games(request):
    favourite_games_list_id = BookmarkImage.objects.filter(user = request.user.rats.id )
    image_ids = [bookmark.image_id for bookmark in favourite_games_list_id]
    image_list = Image.objects.filter(id__in=image_ids)
    context = {'image_list': image_list}
    return render(request, 'favourite_games.html', context)


@login_required
def perfil(request):
    try:
        rat = Rats.objects.get(user=request.user)
    except Rats.DoesNotExist:
        context = {'user': request.user,}
        return render(request, 'perfil.html', context)

    context = {'user': request.user, 'rat': rat}
    return render(request, 'perfil.html', context)

@login_required
def upload(request):
    if request.method == 'POST' and request.FILES.get('myfile') and request.FILES['myfile'] and request.POST['rat_id'] :
        myfile = request.FILES['myfile']

        try:
            image_file = PILImage.open(myfile)

        except IOError:
            messages.error(request, "Invalid image format.")
            return HttpResponseRedirect(reverse('games_hub_app:perfil'))

        width, height = image_file.size
        valid_formats = ('JPEG', 'JPG', 'PNG', 'jpeg', 'jpg', 'png')
        image_extension = myfile.name.split('.')[-1]
        print(image_extension)

        if image_extension not in valid_formats:
            print(image_extension)
            messages.error(request, "Image must be a PNG, JPEG or JPG.")
            return HttpResponseRedirect(reverse('games_hub_app:perfil'))


        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = '/pics/' + filename
        rat_id = request.POST['rat_id']
        rat = Rats.objects.get(id=rat_id)
        rat.perfil_image = uploaded_file_url
        rat.save()
        user = User.objects.get(username='Samurai')
        messages.success(request, 'Your profile image has been successfully changed!')
        return HttpResponseRedirect(reverse('games_hub_app:perfil', ))
    rat = Rats.objects.get(user=request.user)
    context = {'user': request.user, 'rat': rat}
    return render(request,'perfil.html',context)

@login_required
def logout_view(request):

    logout(request)
    return HttpResponseRedirect(reverse('games_hub_app:teste', ))

def erase_comment(request, comment_id, image_id):
    deletedComment = Comment.objects.get(id=comment_id)
    deletedComment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return HttpResponseRedirect(reverse('games_hub_app:image_detail', args=[image_id]))


def add_game(request):
    if request.user.is_superuser:
        if (request.method == 'POST' and request.FILES.get('myfile') and request.FILES['myfile'] ):
            print('Olaaaaaaaaaaaa')


            myfile = request.FILES['myfile']

            try:
             image_file = PILImage.open(myfile)

            except IOError:
                messages.error(request, "Invalid image format.")
                return HttpResponseRedirect(reverse('games_hub_app:add_game'))


            width, height = image_file.size
            valid_formats = ('JPEG', 'JPG', 'PNG', 'jpeg', 'jpg', 'png')
            image_extension = myfile.name.split('.')[-1]
            print(image_extension)

            if image_extension not in valid_formats:
                print(image_extension)
                messages.error(request, "Image must be a PNG, JPEG or JPG.")
                return HttpResponseRedirect(reverse('games_hub_app:add_game'))


            if image_file.width >= 245 and image_file.height >= 587:
                add_game = Image()
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = '/pics/' + filename
                add_game.image = uploaded_file_url
                add_game.name = request.POST['name']
                add_game.description = request.POST['description']
                add_game.likes = 0
                add_game.bookmark =0
                add_game.views = 0
                add_game.pub_date = datetime.now()
                add_game.save()
                messages.success(request, 'Your game was added successfully!')
                return HttpResponseRedirect(reverse('games_hub_app:teste'))
            else:

                messages.error(request, 'Image dimensions must be greater than 245x587.')
                return HttpResponseRedirect(reverse('games_hub_app:add_game'))
        else:
            return render(request, 'add_game.html')
    else:
        return HttpResponseRedirect(reverse('games_hub_app:loginview'))