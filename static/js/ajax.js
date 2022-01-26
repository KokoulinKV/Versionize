// В этом файле будут все ajax функции
$(document).ready(function () {
    // Ждем, когда DOM страницы загрузиться и начинаем вешать наши функции на объекты

    // Смена активного проекта в личном кабинете пользователя
    $('#activeProjectChge').change(function () {
        console.log()
        $.ajax({
            url: "",
            type: 'POST',
            dataType: 'json',
            data: {
                project_id: $(this).val(),
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
            },
            // если успешно, то
            success: function (response) {
                if (response.status == true) {
                    alert('Вы сменили активный проект')
                    location.reload()
                }
            },
            // если ошибка, то
            error: function (response) {
                // предупредим об ошибке
                console.log('Ошибка')
            }
        });
    });
    $('#commentInput').keydown(function (e){
        // Проверяем что нажат именно Enter, а в значении не пробел и не пустая строка
        if(e.keyCode === 13 && $(this).val() != ' ' && $(this).val() != ''){
            // Сохраняем полученное сообщение и очищаем поле
            commentBody = $(this).val()
            console.log(commentBody);
            $(this).val('') // очищаем поле
            $.ajax({
                url: "",
                type: 'POST',
                dataType: 'json',
                data: {
                    commentBody: commentBody,
                    csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
                },
                // если успешно, то
                success: function (response) {
                    if (response.status == true) {
                        alert('Вы отправили сообщение')
                        location.reload()
                    }
                },
                // если ошибка, то
                error: function (response) {
                    // предупредим об ошибке
                    console.log('Ошибка')
                    console.log(response)
                    
                }
            });
        }
    });
});