var $ = django.jQuery;
$( document ).ready(function() {
    $('#id_topic').attr("data-text","name");
    $('#id_topic').attr("data-value","name");
    $('#id_topic').attr("data-src","http://127.0.0.1:8000/api/topic_populate");
    $('#id_topic').attr("data-parent","#id_subject");


});