$(function () {
    $('#search-questionnaire').on('click', function () {
    $.ajax({
        url: '/admin/exam/exam/search_questionnaire/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            $('#search-questionnaire-modal .modal-content').html(data.form);
            $("#search-questionnaire-modal").modal('show');
        }
    });
});

function showQuestionnaire() {
    $("#template-list").addClass('d-none');
    $('#questionnaire-list').removeClass('d-none');
}
function showTemplate() {
    $("#questionnaire-list").addClass('d-none');
    $('#template-list').removeClass('d-none');
}

$('#questionnaire-table ').on('click','.removebutton',function () {
    $(this).parent().parent().remove()
});

})
