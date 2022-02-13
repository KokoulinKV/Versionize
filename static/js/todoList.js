$(document).ready(function () {
    $('.to-do-list__check-widget').on('click', function (e) {
        let todoTitle = $(this).parent().parent().find('.to-do-list__title');
        let todoText = $(this).parent().parent().find('.to-do-list__text');

        if ($(this).is(':checked')) {
            todoTitle.css('text-decoration', 'line-through');
            todoText.css('text-decoration', 'line-through');
        } else {
            todoTitle.css('text-decoration', 'none');
            todoText.css('text-decoration', 'none');
        }
    });
});