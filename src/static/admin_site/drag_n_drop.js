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

            if( fileName )
                label.querySelector( 'span' ).innerHTML = fileName;
            else
                label.innerHTML = labelVal;
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
var template = '\
<div class="card small_form" >\
    <div class="card-content">\
        <div class="row" id="title-{0}">\
            <div class="col s12">\
                <h4 class="form-title black-text">New File #{4}</h4>\
            </div>\
        </div>\
        <div class="section row">\
            <div class="col s12">\
                <h5>File</h5>\
                <div class="row">\
                    <div class="input-field col s12 required" id="id_name_container-{0}">\
                        <input id="id_form-{0}-name" maxlength="100" name="form-{0}-name" autofocus="autofocus" type="text" value="{1}">\
                        <label for="id_form-{0}-name" class="{2}">Name</label>\
                    </div>\
                </div>\
                <div class="row">\
                    <div class="input-field file-field col s12 required" id="id_file_container-{0}">\
                        <div class="btn">\
                            <span>File</span>\
                            <input id="file-{0}" name="form-{0}-file" type="file" onchange="change_file({0});">\
                        </div>\
                        <div class="file-path-wrapper">\
                            <input class="file-path" id="id_form-{0}-file" value="{3}" type="text">\
                        </div>\
                    </div>\
                </div>\
            </div>\
        </div>\
    </div>\
    <div class="card-action">\
        <div class="right-align">\
            <button type="button" onclick="delete_entry({0});" class="waves-effect waves-light btn white-text">Delete</button>\
        </div>\
    </div>\
</div>\
';


var $big_form = $("#post_form");

function rewrite_form(){
    $(".small_form").remove();
    $('#id_form-TOTAL_FORMS').val(totalFiles.length);
    if (totalFiles) {
        $.each( totalFiles, function(i, file) {
            $big_form.append(template.format(i, totalNames[i] !== undefined ? totalNames[i] : "", totalNames[i] !== undefined ? "active" : "", totalFiles[i].name, i+1));
        });
    }
}

function delete_entry(i){
    for(var j = 0; j < totalFiles.length; j++){
        totalNames[j] = $("#id_form-{0}-name".format(j)).val();
    }
    totalFiles.splice(i,1);
    totalNames.splice(i,1);
    rewrite_form();
}

function change_file(i){
    totalFiles[i] = $("#file-{0}".format(i))[0].files[0];
    console.log(totalFiles[i]);
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
            $("#title-{0}".format(i)).after(error_header);
            console.log(obj);
            $.each( obj, function(atr, err) {
                
                $("#id_{0}_container-{1}".format(atr, i)).append(error_msg.format(err));
            });
        }
    });
}

function post(){
    for(var j = 0; j < totalFiles.length; j++){
        totalNames[j] = $("#id_form-{0}-name".format(j)).val();
    }
    var ajaxData = new FormData();
    ajaxData.append( "form-TOTAL_FORMS", $('#id_form-TOTAL_FORMS').val() );
    ajaxData.append( "form-INITIAL_FORMS", $('#id_form-INITIAL_FORMS').val() );
    ajaxData.append( "form-MAX_NUM_FORMS", $('#id_form-MAX_NUM_FORMS').val() );
    ajaxData.append( "csrfmiddlewaretoken", $('input[name=csrfmiddlewaretoken]').val() );
    $.each( totalFiles, function(i, file) {
        ajaxData.append( "form-{0}-file".format(i), file );
        ajaxData.append( "form-{0}-name".format(i), totalNames[i] );
    });
    $.ajax({
            url: "/add_files/",
            type: "POST",
            data: ajaxData,    
            processData: false,
            contentType: false,
            success: (function(e){
                window.location.replace("/admin/post/post/");
            }),
            error: (function(XMLHttpRequest, textStatus, errorThrown) { 
                show_errors(JSON.parse(XMLHttpRequest.responseText));
            }),
    });
}

var totalFiles = [];
var totalNames = [];
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
        
        for(var j = 0; j < totalFiles.length; j++){
            totalNames[j] = $("#id_form-{0}-name".format(j)).val();
        }
        rewrite_form();
    }
    
//     $form.trigger('submit');
  });

}

$form.on('submit', function(e) {
    if ($form.hasClass('is-uploading')) return false;
    
    $form.addClass('is-uploading').removeClass('is-error');
    
    if (isAdvancedUpload) {
        e.preventDefault();

        var ajaxData = new FormData($form.get(0));
        
        if (droppedFiles) {
            $.each( droppedFiles, function(i, file) {
                ajaxData.append( $input.attr('name'), file );
            });
        }
        ajaxData.append("new_files", 1);
        
        $.ajax({
            url: $form.attr('action'),
            type: $form.attr('method'),
            data: ajaxData,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            complete: function() {
              $form.removeClass('is-uploading');
            },
            success: function(data) {
              $form.addClass( data.success == true ? 'is-success' : 'is-error' );
              if (!data.success) $errorMsg.text(data.error);
            },
            error: function() {
              // Log the error, show an alert, whatever works for you
            }
        });
    } else {
        var iframeName  = 'uploadiframe' + new Date().getTime();
        $iframe   = $('<iframe name="' + iframeName + '" style="display: none;"></iframe>');
    
        $('body').append($iframe);
        $form.attr('target', iframeName);
    
        $iframe.one('load', function() {
            var data = JSON.parse($iframe.contents().find('body' ).text());
            $form
                .removeClass('is-uploading')
                .addClass(data.success == true ? 'is-success' : 'is-error')
                .removeAttr('target');
            if (!data.success) $errorMsg.text(data.error);
            $form.removeAttr('target');
            $iframe.remove();
        });
    }
});

$input.on('change', function(e) { // when drag & drop is NOT supported
    droppedFiles = this.files
    console.log(droppedFiles);
});

$form.hover(
       function(){ $('.box__file + label').addClass('accent-color'); },
       function(){ $('.box__file + label').removeClass('accent-color'); }
);