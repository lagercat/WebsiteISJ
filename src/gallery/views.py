from django.shortcuts import render, get_object_or_404, redirect
from models import Gallery
from django.http.response import HttpResponseForbidden, HttpResponse
from gallery.models import GalleryPhoto
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.html import escape
import json
import os
from view_permission.utility import clean_file


# Create your views here.

def gallery(request):
    image = Gallery.objects.all()
    return render(request, 'gallery/gallery.html', {
        'gallery': image,
    })


@staff_member_required
def remove_gallery_photo(request):
    if request.method == "POST":
        photo = get_object_or_404(GalleryPhoto, id=request.POST["id"])
        photo.delete()
        return HttpResponse()
    else:
        return HttpResponseForbidden()


@staff_member_required
def add_gallery(request):
    if request.method == "POST":
        obj = None
        json_dict = {}
        if(request.POST["name"] == ""):
            json_dict["name"] = "This field is required."
            
        file = None
        if request.FILES.get("file"):
            file = request.FILES["file"]
        
        if not file:
            json_dict["file"] = "This field is required. Please select a file."
            
        elif clean_file(file, image=True) != "":
            json_dict["file"] = clean_file(file, image=True)
            
        for i in range(0, int(request.POST["nr"])):
            file = None
            if request.FILES.get("form-" + str(i) + "-file"):
                file = request.FILES["form-" + str(i) + "-file"]
              
            error = clean_file(file, image=True)
            if error != "":
                json_dict[i] = error
            
        if json_dict != {}:
            response = HttpResponse(json.dumps(json_dict), 
                content_type='application/json')
            response.status_code = 400
            return response

        if (request.POST["change"] == "1"):
            obj = get_object_or_404(Gallery, id=request.POST["id"])
            obj.name = escape(request.POST["name"])
            if request.FILES.get("file"):
                obj.file = request.FILES["file"]
            obj.save()

            for i in range(0, int(request.POST["delete_nr"])):
                print request.POST["delete-" + str(i) + "-id"]
                id = int(request.POST["delete-" + str(i) + "-id"])
                photo = GalleryPhoto.objects.get(pk=id)
                photo.delete()
        else:
            obj = Gallery(name=escape(request.POST["name"]),
                          file=request.FILES["file"], author=request.user)
            obj.save()

        for i in range(0, int(request.POST["nr"])):
            id = None
            if request.POST.get("form-" + str(i) + "-id"):
                id = request.POST["form-" + str(i) + "-id"]

            file = None
            if request.FILES.get("form-" + str(i) + "-file"):
                file = request.FILES["form-" + str(i) + "-file"]

            name = request.POST["form-" + str(i) + "-name"]
            if not id: 
                photo = GalleryPhoto(gallery=obj, name=name, file=file, author=request.user, location="gallery/" + obj.slug)
                photo.save()
            else:
                photo = GalleryPhoto.objects.get(pk=id)
                photo.name = name
                photo.save()
        return redirect("/admin/gallery/gallery/")

    else:
        return HttpResponseForbidden()


def gallery_img(request, slug):
    instance = Gallery.objects.get(slug=slug)
    photos = GalleryPhoto.objects.filter(gallery=instance).extra(
        select={'order': 'CAST(name AS INTEGER)'}
    ).order_by('order')
    return render(request, 'gallery/imagini.html', {
        'photos': photos,
    })
