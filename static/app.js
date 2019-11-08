window.translations = []

/* add extend method to arrays */
Array.prototype.extend = function (other_array) {
    other_array.forEach(function(v) {this.push(v)}, this);
}

$.ajax({
    url: "translations",
    type: "GET",
    success: function (data, status)
    {
        //console.log(data)
        if ( data.length != 0 ){
        window.translations.extend(data)
        sortTranslationByLength()

        var str = renderTranslations();
        $("#translations").html(str);
        }
        
    },
    error: function (xhr, desc, err)
    {


    }
}); 

function sortTranslationByLength(){
    window.translations.sort(function(a, b) {
        return b.source_text.length - a.source_text.length;
    });
}

function renderTranslations(){
    var str = "";
    window.translations.forEach(function(element) {
            //str += "<p>Source text: " + element.source_text + ". Target text: " + element.target_text + ". Status: " + element.status + "</p><br><hr>";
            if (element.status == null){
                var status_text = 'requested';
                var status_class = 'danger';
            }
            else if (element.status == "new") {
                var status_text = "pending";
                var status_class = 'info';
            }
            else if (element.status == "completed") {
                var status_text = "translated";
                var status_class = 'success';
            }
            str +=  '<div class="panel panel-' + status_class + '"> \
                    <div class="panel-heading">Created time: ' + element.created_time + '</div> \
                    <div class="panel-body"> \
                    <ul class="list-group remove-margin-bottom"> \
                    <li class="list-group-item"><b>Source text:</b> <p class="vertical-spacing-5px-top">' + element.source_text + ' </p></li> \
                    <li class="list-group-item"><b>Translated text:</b> <p class="vertical-spacing-5px-top"> ' + element.target_text + '</p> </li> \
                    <li class="list-group-item"><b>Status:</b> ' + status_text+ '</li>\
                    </ul> \
                    </div> \
                    </div>'
        })
    return str
}

$(document).on("submit", "form", function(event)
{
    event.preventDefault();        
    $.ajax({
        url: "translation",
        type: "POST",
        dataType: "JSON",
        data: new FormData(this),
        processData: false,
        contentType: false,
        success: function (data, status)
        {
            $('#translation_text').val("");
            //console.log(data)
            window.translations.push(data)
            sortTranslationByLength()

            var str = renderTranslations();
            $("#translations").html(str);
            
        },
        error: function (xhr, desc, err)
        {


        }
    });        
});

var socket = io();
socket.on('connect', function() {
    socket.emit('message', {data: 'I\'m connected!'});
});

socket.on('response', function(msg) {
    //console.log(msg)
    var id = msg.id
    var index = window.translations.findIndex(element => element.id === id)
    if (index !== -1) {
        window.translations[index] = msg;
    }

    sortTranslationByLength();

    var str = renderTranslations();

    $("#translations").html(str);
    
});