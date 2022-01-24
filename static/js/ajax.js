// В этом файле будут все ajax функции
$(document).ready(function () {
    // Ждем, когда DOM страницы загрузиться и начинаем вешать наши функции на объекты
    $('#activeProjectChge').change(function () {
        console.log()
        $.ajax({
            url: "",
            type: 'POST',
            dataType: 'json',
            data: {
                select: $(this).val(),
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
            },
            // если успешно, то
            success: function (response) {
                console.log('Успешно')
            },
            // если ошибка, то
            error: function (response) {
                // предупредим об ошибке
                console.log('Ошибка')
                console.log(response);
            }
        });
    });
});