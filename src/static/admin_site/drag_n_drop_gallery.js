'use strict';

;( function ( document, window, index )
{
    $('html').removeClass("no-js");
    $('html').addClass("js");
    var inputs = document.querySelectorAll( '.box__file' );
    Array.prototype.forEach.call( inputs, function( input )
    {
        var label    = input.nextElementSibling,
            labelVal = label.innerHTML;

        input.addEventListener( 'change', function( e )
        {
            var fileName = '';
            if( this.files && this.files.length > 1 )
                fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
            else
                fileName = e.target.value.split( '\\' ).pop();

        });

        // Firefox bug fix
        input.addEventListener( 'focus', function(){ input.classList.add( 'has-focus' ); });
        input.addEventListener( 'blur', function(){ input.classList.remove( 'has-focus' ); });
    });
}( document, window, 0 ));


$('.column-height-match').matchHeight();
var isAdvancedUpload = function() {
  var div = document.createElement('div');
  return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
}();

var $form = $('.box');
var $input = $form.find('input[type="file"]');

if (isAdvancedUpload) {
  $form.addClass('has-advanced-upload');   
}

if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

function $_GET(parameterName) {
    var result = null,
        tmp = [];
    location.search
    .substr(1)
        .split("&")
        .forEach(function (item) {
        tmp = item.split("=");
        if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
    });
    return result;
}

var template = '\
<div class="card gallery_photo" >\
    <div class="card-content">\
        <input name="index" type="hidden" value="{1}">\
        <input name="id" type="hidden" value="{2}">\
        <image id="src_photo_{1}">\
    </div>\
    <a class="btn-floating waves-effect waves-light z-depth-2 delete" onclick="delete_entry({1})">\
        <i class="material-icons">delete</i>\
    </a>\
</div>\
';


var $big_form = $("#post_form");

function rewrite_form(){
    $(".gallery_photo").remove();
    if (totalFiles) {
        $.each( totalFiles, function(i, file) {
            $("#gallery").append(template.format("", i, totalIds[i]));
            if(typeof file === "string"){
                $('#src_photo_{0}'.format(i)).attr('src', "/media/" + file);
                return;
            }
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#src_photo_{0}'.format(i)).attr('src', e.target.result);
                
            };
            reader.readAsDataURL(file);
        });
    }

    $('#gallery').sortable({
        items: ".gallery_photo",
        update: function( event, ui ) {
            setTimeout(reindex, 200);
        }
    });
}

function reindex(){
    var newTotalFiles = [];
    var newTotalIds  = [];
    $.each($(".gallery_photo"), function(i, el){
        var oi = parseInt($(el).find("input").val());
        newTotalFiles[i] = totalFiles[oi];
        newTotalIds[i] = totalIds[oi];
    });
    
    totalFiles = newTotalFiles;
    totalIds = newTotalIds;
    rewrite_form();
}

var deleteIds = [];
var deleteFiles = [];

function delete_entry(i){
    if(totalIds[i] !== undefined){
        deleteIds.push(totalIds[i]);
        deleteFiles.push(totalFiles[i]);
        totalIds.splice(i,1);
    }
    totalFiles.splice(i,1);
    rewrite_form();
}

function restore_deleted(){
    for(var i = 0; i < deleteIds.length; i++){
        totalIds[i + totalIds.length] = deleteIds[i];
        totalFiles[i + totalFiles.length] = deleteFiles[i];
    }
    deleteIds= [];
    deleteFiles= [];
    rewrite_form();
}


var error_header = '\
<div class="row errors">\
    <div class="col s12">\
        <small class="errornote">\
            Please correct the errors below.\
            <br/><br/>\
        </small>\
    </div>\
</div>\
';

var error_msg = '\
<div class="errors">\
    <small class="errornote">\
        {0}\
    </small>\
</div>\
';

function show_errors(errors){
    console.log(errors);
    $(".errors").remove();
    $.each( errors["errors"], function(i, obj) {
        if(!$.isEmptyObject(obj)){
            $(".form-title").after(error_header);
            $.each( obj, function(atr, err) {
                
                $("#id_{0}_container-{1}".format(atr, i)).append(error_msg.format(err));
            });
        }
    });
}

function post(){
    var ajaxData = new FormData();
    ajaxData.append( "name", $('#id_name').val() );
    ajaxData.append( "file", $('input[name=file]')[0].files[0]);
    ajaxData.append( "nr", totalFiles.length );
    ajaxData.append( "delete_nr", deleteIds.length );
    ajaxData.append( "csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val() );
    ajaxData.append( "change", $('input[name=change]').val() );
    if($('input[name=change]').val() == "1")
        ajaxData.append( "id", id );
    
    $.each( deleteIds, function(i, id) {
        ajaxData.append( "delete-{0}-id".format(i), totalIds[i] );
    });        

    $.each( totalFiles, function(i, file) {
        ajaxData.append( "form-{0}-file".format(i), file );
        ajaxData.append( "form-{0}-name".format(i), i );
        if(totalIds[i])
            ajaxData.append( "form-{0}-id".format(i), totalIds[i] );
    });
    $.ajax({
            url: "/add_gallery/",
            type: "POST",
            data: ajaxData,    
            processData: false,
            contentType: false,
            success: (function(e){
                window.location.replace("/admin/gallery/gallery/");
            }),
            error: (function(XMLHttpRequest, textStatus, errorThrown) { 
                show_errors(JSON.parse(XMLHttpRequest.responseText));
            }),
    });
}

var id = null;

var totalFiles = [];
var totalIds = [];

$(window).on("load", function(){
    if($("#id_id")){
        id = $("#id_id").val();
        totalIds = $("#id_gallery_photos").val().split(" ");
        totalFiles = $("#id_gallery_photos_urls").val().split(" ");
        console.log(totalIds);
        $(".row #id_gallery_photos_container").parent().remove();
        $(".row #id_gallery_photos_urls_container").parent().remove();
        $(".row #id_id_container").parent().remove();
        rewrite_form();
    }
});
var droppedFiles = false;

if (isAdvancedUpload) {


  $form.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
  })
  .on('dragover dragenter', function() {
    $form.addClass('is-dragover');
    $('.box__file + label').addClass('accent-color');
  })
  .on('dragleave dragend drop', function() {
    $form.removeClass('is-dragover');
    $('.box__file + label').removeClass('accent-color');
  })
  .on('drop', function(e) {
    droppedFiles = e.originalEvent.dataTransfer.files;
    if (droppedFiles) {
        $.each( droppedFiles, function(i, file) {
            totalFiles.push(file);
        });
        
        rewrite_form();
    }
    
//     $form.trigger('submit');
  });

}

$input.on('change', function(e) { // when drag & drop is NOT supported
    droppedFiles = this.files;
    if (droppedFiles) {
        $.each( droppedFiles, function(i, file) {
            totalFiles.push(file);
        });
        
        rewrite_form();
    }
});

$form.hover(
       function(){ $('.box__file + label').addClass('accent-color'); },
       function(){ $('.box__file + label').removeClass('accent-color'); }
);




