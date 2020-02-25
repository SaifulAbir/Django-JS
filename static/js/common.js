function get(url, callback) {
    if(!callback) callback = () => {};
    if(typeof(callback) !== "function") callback = window[callback];
    $.ajax({
        type : 'get',
        url : url,
        success : callback
    });
}

function del(url, callback) {
    var csrf = getCsrfToken();
    $.ajax({
        url : url,
        beforeSend : function(xhr) {
            if(csrf) xhr.setRequestHeader(csrf.header, csrf.token);
        },
        type : 'DELETE',
        cache : false,
        complete : callback
    });
    return false;
}


function send(url, method, data, callback) {
    var csrf = getCsrfToken();
    if(!callback) callback = () => {};
    if(typeof(callback) !== "function") callback = window[callback];
    $.ajax({
        beforeSend : function(xhr) {
            if(csrf) xhr.setRequestHeader(csrf.header, csrf.token);
        },
        type : method,
        contentType : 'application/json',
        url : url,
        data : data,
        async: true,        // Cross-domain requests and dataType: "jsonp" requests do not support synchronous operation
        cache: false,       // This will force requested pages not to be cached by the browser
        processData: false, // To avoid making query String instead of JSON
        complete : callback,
    });
}


function getCsrfToken(){
    //  The html would contain somthing like below"
    //  <meta name="_csrf_header" content="X-CSRF-TOKEN"/>
    //  <meta name="X-CSRF-TOKEN" content="44f02902-3ac0-4d5a-86e2-da3d17430c26"/>
    var header = $("meta[name='_csrf_header']").attr("content");
    var token = $("meta[name='_csrf']").attr("content");
    if (header && token){
        return {
            header: header,
            token: token
        }
    }
}


function post(url, data, callback){
    send(url, "POST", data, callback);
}


function put(url, data, callback){
    send(url, "PUT", data, callback);
}


function initAjaxForms() {
    $("form.ajax:not(.ajax-linked)").on('submit', function(event) {
        event.preventDefault();
        if ($(this).valid()){
            var url = $(this).prop('action');
            var formId = $(this).attr("id");
            var data = form2Json(formId);
            var method = $(this).attr('method');
            var callback= $(this).data("callback");  // $(this).attr("data-callback");
            send(url, method, data, callback);
        }
        return false;
    }).addClass("ajax-linked");
}


function form2Json(id){
    return JSON.stringify(form2js(id));
}

function json2Form(data, id){
    for(key in data){
        // var el = $("#" + id).find("[name='"+ key +"']");
        var el = $("#" + id).find("[id='"+ key +"']");
        console.log(el.data("parent"));
        if(el.data("parent")){
            var elChild = el;
            var v = data[key];
            setTimeout(function () {
                elChild.val(v).change();
            },3000);
        }else{
            el.val(data[key]).change();
        }

    }
}

function json2Div(data, container){
    for(key in data) {
        // var el = $("#" + id).find("[name='"+ key +"']");
        var el = $(container).find("[id='" + key + "']");
        console.log(el)
        el.html(data[key]);
    }
}

function initAjaxSelects(container){
    if(!container) container = "body";
    $(container).find('select[data-src]').each(function() {
        var select = $(this);
        var parentSelector = $(this).attr("data-parent");
        var url = select.attr('data-src');
        if (parentSelector){
            var parent = $(parentSelector);
            parent.on("change", function(){
                var prev_url = url;
                var final_url = prev_url+ "/" + parent.val();
                populateSelect(select, final_url);
            });
        } else {
            populateSelect(select, url);
        }
    });
}

function populateSelect(select, url){
    select.find('option').remove();
    select.append('<option>' + select.attr('data-placeholder') + '</option>');
    $.ajax({
        url: url,
        success: function(options) {
            options.map(function(item) {
                var option = $('<option>');
                option
                    .val( item[select.attr('data-value')])
                    .text( item[select.attr('data-text')]);
                select.append(option);
            });
        }
    });
}

function makeListHtml(data, template){
    var wrapper = $("<div>");
    for (i=0; i < data.length; i++){
        var templateEl = $(template);
        for( k in data[i]){
            var el = templateEl.find(".__" + k);
            el.each(function (_, item) {
                if($(item).hasClass("dynamic-link")){
                    var href = $(item).attr("href") + data[i][k];
                    $(item).attr("href", href);
                } else {
                    $(item).html(data[i][k]);
                }
            });

        }
        wrapper.append(templateEl)
    }
    return wrapper.html();
}

function showSuccess(title, msg) {
    Swal.fire({
        icon: 'success',
        title: title,
        text: msg
    })
}

function showError(title, msg) {
    Swal.fire({
        icon: 'error',
        title: title,
        text: msg
    })
}

function showQuestion(title, msg, yesCallback, noCallback) {
    Swal.fire({
        title: title,
        text: msg,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes'
    }).then((result) => {
        console.log(result.value)
        if (result.value && typeof (yesCallback) ==='function') {
            yesCallback();
        } else if(result.dismiss=='cancel' && typeof(noCallback) ==='function'){
            noCallback();
        }
    })
}

$.validator.addMethod(
    "regex",
    function(value, element, regexp) {
        var re = new RegExp(regexp);
        return this.optional(element) || re.test(value);
    },
    "Please check your input."
);

function makePagination(totalRecord, pageSize, url, startingIndex){
    var paginationStringStart = '<nav class="navigation pagination"><div class="nav-links"><button disabled class="prev page-numbers cursor-pointer cursor-pointer" data-value="prev"><i class="fas fa-angle-left"></i></button>';
    startingIndex = parseInt(startingIndex);
    var numberOfPaginationIndex = totalRecord/pageSize;
    numberOfPaginationIndex = Math.ceil(numberOfPaginationIndex);
    var primaryNumberOfPaginationIndex = numberOfPaginationIndex;
    var paginationIndexString = '';
    if (numberOfPaginationIndex > 10){
        numberOfPaginationIndex=10;
    }

    var paginationPadding = startingIndex-6
    if (startingIndex<7){
        startingIndex=1;
    }else {
        startingIndex=startingIndex-5;
        numberOfPaginationIndex = numberOfPaginationIndex+paginationPadding;
        if (numberOfPaginationIndex > primaryNumberOfPaginationIndex){
            numberOfPaginationIndex = primaryNumberOfPaginationIndex;
            //startingIndex = startingIndex-paginationPadding;
            console.log('paginationPadding '+paginationPadding);
            console.log('startingindex '+startingIndex);
            var paddingStartingIndex =10-(primaryNumberOfPaginationIndex-startingIndex);
            console.log(paddingStartingIndex);
            startingIndex = startingIndex-paddingStartingIndex;
        }
    }

    for (startingIndex; startingIndex <= numberOfPaginationIndex; startingIndex++){
        if (startingIndex==1 || startingIndex==numberOfPaginationIndex){
            var str ="<a class='page-numbers' href='javascript:void(0);' data-pazesize='"+ pageSize +"' data-value='"+ startingIndex +"' data-url='"+ url +"/?page=" + startingIndex + "&page_size="+ pageSize +"'>"+startingIndex+"</a>";
        }else {
            var str ="<a class='page-numbers' href='javascript:void(0);' data-pazesize='"+ pageSize +"' data-value='"+ startingIndex +"' data-url='"+ url +"/?page=" + startingIndex + "&page_size="+ pageSize +"'>"+startingIndex+"</a>";
        }
        paginationIndexString += str;

    }

    var a = '<a class="page-numbers" href="#">1</a><a class="page-numbers" href="#">3</a>' +
        ' <a class="page-numbers" href="#">4</a>';

    var paginationStringEnd = '<a class="next page-numbers" data-value="next" href="javascript:void(0);"><i class="fas fa-angle-right"></i></a></div></nav>';
    var paginationString = paginationStringStart + paginationIndexString + paginationStringEnd;
    $('.pagination-list').html(paginationString);
}
