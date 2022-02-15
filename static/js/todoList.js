// * - Ответственный
// ? - Что делает/За что отвечает
// В этом файле будут хранится настройки стилей и отправки данных для виджета с задачами
$(document).ready(function () {

    let clickCount = 1; // Отслеживает количество кликов пользователем по кнопке

    // * @TheSleepyNomad
    // ? Перечеркивание задачи, если чекбокс заполнен(checked)
    $('.to-do-list__check-widget').on('click', function (e) {
        let title = $(this).parent().parent().find('.to-do-list__title');
        let text = $(this).parent().parent().find('.to-do-list__text');

        if ($(this).is(':checked')) {
            title.css('text-decoration', 'line-through');
            text.css('text-decoration', 'line-through');
        } else {
            title.css('text-decoration', 'none');
            text.css('text-decoration', 'none');
        }
    });

    // * @TheSleepyNomad
    // ? Открытие формы/добавление задачи/отправка данных на сервер
    // В данный момент тут выполняется основаная логика работы сервиса
    $('#todoAdd').on('click', function (e) {
        // При втором нажатии на кнопку происходит добавление записи и отправка на сервер
        if (clickCount === 2) {
            // Простая валидация на заполнение
            // ToDo Написать отдельную функцию, для валидации и отслеживания действий пользователя
            if (!$('#task_name').val() || !$('#task_description').val()) {
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
                        formName: 'ToDoList', // Обязательный параметр. Отвечает за определение формы в IndexView
                        csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
                        task_name: $('#task_name').val(),
                        task_description: $('#task_description').val(),
                        task_importance: $('#task_importance').val(),
                    },
                    success: function (response) {
                        // Если запись добавлена без ошибок, то сервер вернет нам true, а так же id новой записи в таблице
                        if (response.status === true) {
                            let taskTemplate = $('#forCopy').clone(true); // В DOM есть скрытый элемент, который является шаблоном для новых задач
                            let taskTemplateIndicator = taskTemplate.find('to-do-list__task-indicator')
                            if ($('#task_importance').val() == 2){
                                taskTemplate.find('.to-do-list__task-indicator').addClass('to-do-list__task-indicator_casual')
                            }
                            if ($('#task_importance').val() == 3){
                                taskTemplate.find('.to-do-list__task-indicator').addClass('to-do-list__task-indicator_wait')
                            }
                            if ($('#task_importance').val() == 4){
                                taskTemplate.find('.to-do-list__task-indicator').addClass('to-do-list__task-indicator_hot')
                            }
                            taskTemplate.removeClass('to-do-list__item_hidden')
                            taskTemplate[0].id = 'task' + response.task_id // Добавляем новый id для элемента. Это нужно для того, чтобы пользователь мог сразу удалить элемент
                            taskTemplate.find('.to-do-list__title').text($('#task_name').val())
                            taskTemplate.find('.to-do-list__text').text($('#task_description').val())
                            // Очищаем поля формы
                            $('#task_name').val('')
                            $('#task_description').val('')
                            // Закрываем форму для добавления
                            // ? Может оставить пользователю возможность добавления новой задачи?
                            $('.to-do-list-form').toggleClass('to-do-list-form_open');
                            $('#todoCancel').toggleClass('gear-btn_hide');
                            // Обнуляем счетчик кликов
                            clickCount = 1;
                            // Добавляем новую задачу в самый вверх ссписка
                            $('.to-do-list').prepend(taskTemplate)

                        }

                    },
                    error: function (response) {
                        console.log('Ошибка')
                    }
                });
            };
        };
        // При первом происходит открытие формы
        if (clickCount === 1) {
            // $('.to-do-list-form').toggleClass('to-do-list-form_open');
            $('.to-do-list-form').slideDown(0.5, function () {
                $(this).toggleClass('to-do-list-form_open');
            });
            $('#todoCancel').toggleClass('gear-btn_hide');
            clickCount++;
        };

    });

    // * @TheSleepyNomad
    // ? Закрывает форму добавления задачи
    $('#todoCancel').on('click', function (e) {
        // Скрываем форму добавления задачи
        $('.to-do-list-form').slideUp('slow', function () {
            $(this).toggleClass('to-do-list-form_open');
        });
        // Удаляем/добавляем класс, который отвечает за показ/сокрытие кнопки Отмена
        $('#todoCancel').toggleClass('gear-btn_hide');
        clickCount = 1; // Счетчик кликов приводим к изначальному значению. Это нужно для того, чтобы пользователь смог снова открыть форму через кнопку Добавить
    });

    // * @TheSleepyNomad
    // ? Удаляет элемент из контейнера и базы данных
    $('.sqr-btn_trash').on('click', function (e) {
        let task = $(this).parent().parent().parent() // Получаем ссылку на элемент, где нажали кнопку
        let id = task[0].id.slice(4); // Каждый элемент имеет id - task[норме ид из бд]. Получаем id задачи в БД

        // Отправляем запрос на сервер для удаления
        $.ajax({
            url: "",
            type: 'POST',
            dataType: 'json',
            data: {
                formName: 'ToDoList', // Обязательный параметр. Отвечает за определение формы в IndexView
                action: 'delete', // Обязательный параметр. Отвечает за определение задачи в IndexView
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
                id: id,
            },
            // Если при попытке удаления объекта из БД не будет ошибки, то удаляем его у пользователя
            success: function (response) {
                // Если удаление прошло успешно, то скрываем эдемент и после удаляем
                if (response.status === true) {
                    $(task).slideUp('0.3s', function () {
                        $(this).remove();
                    })
                }

            },
            // если ошибка, то
            error: function (response) {
                // предупредим об ошибке
                console.log('Ошибка')
            }
        });
    })
});