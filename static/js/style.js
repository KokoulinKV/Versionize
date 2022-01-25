// В этом файле будут храниться и запускаться функции, которые влияют только на стиль
// Для применения стилей нам надо дождаться загрузки DOM
$(document).ready(function () {

    // Стилизация пока всех таблиц. В зависимости от количества их строк
    // console.log($('#table'));
    table_rows = $('#table').children() // Получаем список всех строк из таблицы
    for (let i = 0; i < table_rows.length; i++) {

        // четным устанавливаем один стиль, нечетным другой
        if (i % 2) {

            table_rows[i].classList.add('form-table__table_even');

        } else {

            table_rows[i].classList.add('form-table__table_odd');

        };
    };

    // Так как у нас пока одна таблица, то вешаем на все кнопки
    $('#tableSelect').change(function () {

        // Проверяем есть ли уже скрытые строки
        hide_rows = $('.form-table__table_hide')

        // Если пользователь снова захочет отобразить всю таблицу
        if ($(this).val() == '-') {

            for (let i = 0; i < table_rows.length; i++) {

                table_rows[i].classList.remove('form-table__table_hide');
            };

        }
        if (hide_rows.length == 0) {

            // Если таблица полность отображена, то скрываем до нужного количества
            for (let i = 0; i < table_rows.length; i++) {

                if (i >= $(this).val()) {
                    table_rows[i].classList.add('form-table__table_hide');
                };
            };
        } else {

            // Если строки есть, то сначала удаляем модификатор для скрытия и накладываем новый
            for (let i = 0; i < table_rows.length; i++) {

                table_rows[i].classList.remove('form-table__table_hide');
            };

            // И снова добавляем класс и скрываем лишние строки
            for (let i = 0; i < table_rows.length; i++) {
                if (i >= $(this).val()) {
                    table_rows[i].classList.add('form-table__table_hide');
                };
            };
        };
    });


    // Поиск по таблице
    // Получаем поле для ввода текса
    $('#tableSearch').keyup(function () { // функция запускаеться каждый раз, когда будет отждата клавиша
        _this = this;

        $.each($('#table tr'), function () { 
            // проверяем совпадения по строкам таблицы
            if($(this).text().toLowerCase().indexOf($(_this).val().toLowerCase()) === -1){
                // скрывает строки которые не содержат поисковую фразу
                $(this).hide();
            } else {
                // показываем нужные
                $(this).show();
            }
        });
    });
});