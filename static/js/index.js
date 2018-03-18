var droppedFiles = false;
var fileName = '';
var $dropzone = $('.dropzone');
var $button = $('.upload-btn');
var uploading = false;
var $syncing = $('.syncing');
var $done = $('.done');
var $bar = $('.bar');
var timeOut;

function check_extension(filename)
{
    ext = filename.split('.').pop();
    allowed_ext = ['doc','docx','pdf','html']
    if(allowed_ext.indexOf(ext) !== -1)
    {
      return true;
    }
    else
    {
        return false;
    }
}

$button.bind('click', function() {
	startUpload();
});

$("input:file").change(function (){
	fileName = $(this)[0].files[0].name;
	$('.filename').html(fileName);
	$('.dropzone .upload').hide();
	console.log("filename",fileName);
});

function startUpload() {
	if (!uploading && fileName != '' ) {
		uploading = true;
        if(!check_extension(fileName))
        {
            alert('File Format Not Allowed !!');
        }
        else
        {
            $button.html('Uploading...');
		    $dropzone.fadeOut();
            var newFromData = new FormData($('#file_form')[0]);
            $.ajax({
                url: '/upload',
                type: "POST",
                data:  newFromData,
                processData: false,
                async: false,
                cache: false,
               contentType: false,
               mimeType: 'multipart/form-data',
                success: function (result) {
                    $syncing.addClass('active');
                    $done.addClass('active');
                    $bar.addClass('active');
                    timeoutID = window.setTimeout(showDone,1000);
                     setTimeout(function(){
                          window.location.href = window.location.href;
                     },5000)
                }
            });
        }
	}
}

function showDone() {
	$button.html('Done');
}

