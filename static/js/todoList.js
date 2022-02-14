// * - Ответственный
// ? - Что делает/За что отвечает
// В этом файле будут хранится настройки стилей и отправки данных для виджета с задачами
$(document).ready(function () {

    let clickCount = 1;
    let elCopy = $('#forCopy').clone(true);
    


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
        $('#to-do-list').prepend('')
        if (clickCount === 2) {
            if (!$('#task_name').val() && !$('#task_description').val()) {
                $('#task_name').toggleClass('form__input_warn')
                $('#task_description').toggleClass('form__input_warn')
                $('#task_name')[0].placeholder = 'Обязательное поле!';
                $('#task_description')[0].placeholder = 'Обязательное поле!'
            } else {
                $.ajax({
                    url: "",
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        formName: 'ToDoList',
                        csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
                        task_name: $('#task_name').val(),
                        task_description: $('#task_description').val(),
                        task_importance: $('#task_importance').val(),
                    },
                    // если успешно, то
                    success: function (response) {
                        console.log(response.status);
                        if (response.status === true) {
                            elCopy.find('.to-do-list__title').text($('#task_name').val())
                            elCopy.find('.to-do-list__text').text($('#task_description').val())
                            $('#task_name').val('')
                            $('#task_description').val('')
                            $('.to-do-list-form').toggleClass('to-do-list-form_open');
                            $('#todoCancel').toggleClass('gear-btn_hide');
                            clickCount = 1;
                            $('.to-do-list').prepend(elCopy)

                        }

                    },
                    // если ошибка, то
                    error: function (response) {
                        // предупредим об ошибке
                        console.log('Ошибка')
                    }
                });
            };
        };
        if (clickCount === 1) {
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