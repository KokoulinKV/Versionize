// * - Ответственный
// ? - Что делает/За что отвечает
// В этом файле будут хранится настройки стилей и отправки данных для виджета с задачами
$(document).ready(function () {

    let clickCount = 1;


    // * @TheSleepyNomad
    // ? Перечеркивание задачи, если чекбокс заполнен(checked)
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

    $('#todoAdd').on('click', function (e) {
        if(clickCount == 2){
            console.log('Я не должен работаь');
            data = $('#todoForm').serialize();
            console.log(data);
        };
        if(clickCount == 1){
            $('.to-do-list-form').toggleClass('to-do-list-form_open');
            $('#todoCancel').toggleClass('gear-btn_hide');
            console.log(clickCount);
            clickCount++;
        };
        
    });

    $('#todoCancel').on('click', function (e) {
        $('.to-do-list-form').toggleClass('to-do-list-form_open');
        $('#todoCancel').toggleClass('gear-btn_hide');
        clickCount = 1;
    });

    
});