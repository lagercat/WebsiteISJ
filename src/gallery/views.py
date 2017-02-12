from django.shortcuts import render, get_object_or_404, redirect
from models import Gallery
from django.http.response import HttpResponseForbidden, HttpResponse
from gallery.models import GalleryPhoto
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.html import escape
import json


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
        print request.POST
        if(request.POST["name"] == ""):
            response = HttpResponse(json.dumps({"error" : "This field is required."}), 
                content_type='application/json')
            response.status_code = 400
            return response
        
        if(request.POST["change"] == "1"):
            obj = get_object_or_404(Gallery, id=request.POST["id"])
            obj.name = escape(request.POST["name"])
            obj.save()
            
            for i in range(0, int(request.POST["delete_nr"])):
                id = request.POST["delete-" + str(i) + "-id"]
                print id
                photo = GalleryPhoto.objects.get(pk=id)
                photo.delete()
        else:
            obj = Gallery(name=escape(request.POST["name"]))
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
                photo = GalleryPhoto(gallery=obj, name=name, file=file, author=request.user, location="gallery/" + str(obj.id))
                photo.save()
            else:
                photo = GalleryPhoto.objects.get(pk=id)
                photo.name = name
                photo.save()
        return redirect("/admin/gallery/gallery/")
          
    else:
        return HttpResponseForbidden()