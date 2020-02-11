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
        success : callback
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
        var url = $(this).prop('action');
        var formId = $(this).attr("id");
        var data = form2Json(formId);
        console.log(data);
        var method = $(this).prop('method');
        var callback= $(this).data("callback");  // $(this).attr("data-callback");
        send(url, method, data, callback);
		return false;
	}).addClass("ajax-linked");
}


function form2Json(id){
    return JSON.stringify(form2js(id));
}

function json2Form(data, id){
    for(key in data){
        var el = $("#" + id).find("[name='"+ key +"']");
        console.log(el.data("parent"));
        if(el.data("parent")){
            var elChild = el;
            var v = data[key];
            setTimeout(function () {
                elChild.val(v).change();
            },50);
        }else{
            el.val(data[key]).change();//.change() is needed??
        }

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
                var prev_url = url
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
	var html = "";
	for (i=0; i < data.length; i++){
		var templateEl = $(template);
		for( k in data[i]){
			templateEl.find(".__" + k).text(data[i][k]);
		}
		html+= templateEl.html()
	}
	return html;
}