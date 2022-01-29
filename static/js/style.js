// В этом файле будут храниться и запускаться функции, которые влияют на стилизацию и анимацию
// Для применения стилей нам надо дождаться загрузки DOM
$(document).ready(function () {

    // @TheSleepyNomad
    // Стилизация четных и нечетных строк
    table_rows = $('#table').children() // Получаем список всех строк из таблицы
    for (let i = 0; i < table_rows.length; i++) {

        // четным устанавливаем один стиль, нечетным другой
        if (i % 2) {

            table_rows[i].classList.add('form-table__table_even');

        } else {

            table_rows[i].classList.add('form-table__table_odd');

        };
    };

    // @TheSleepyNomad
    // Отображение определенного количества строк
    // Так как у нас пока одна таблица, то вешаем на все кнопки
    $('#tableSelect').change(function () {

        // Проверяем есть ли уже скрытые строки
        hide_rows = $('.form-table__table_hide');

        // Если пользователь снова захочет отобразить всю таблицу
        if ($(this).val() == '-') {

            for (let i = 0; i < table_rows.length; i++) {

                table_rows[i].classList.remove('form-table__table_hide');
            };

        };
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

    // @TheSleepyNomad
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
            };
        });
    });



    // @TheSleepyNomad
    // Переход через select
    $('#selectProject').change(function(){
		window.location.href = $('option:selected',this).data('url');
	});

    // @TheSleepyNomad
    // Открытие/закрытие бокового навигационного меню через кнопку меню и поле поиска
    $('#menu-btn, #searchBtn').click(function(){
        $('#sidebar').toggleClass('sidebar_active');
    });

    // Скрипты для pop-up окон

    // @TheSleepyNomad
    // Для вызова pop-up формы уведомлений
    $('#not-pop').click(function(){
        $('#pop-min').toggleClass('pop-mini_open');
    });

    // @TheSleepyNomad
    // Для вызова pop-up формы добавления документа
    $('#add-document, #popup__close_doc').click(function(){
        $('#popup-document').toggleClass('popup_open');
    });

    // @TheSleepyNomad
    // Для вызова pop-up формы добавления раздела
    $('#add-section, #popup__close_sec').click(function(){
        $('#popup-section').toggleClass('popup_open');
    });

    // @TheSleepyNomad
    // Для вызова pop-up формы добавления проекта
    $('#add-project, #popup__close_pro').click(function(){
        $('#popup-project').toggleClass('popup_open');
    });

    // @TheSleepyNomad
    // Для вызова pop-up формы добавления корректировок
    $('#add-remarkdoc, #popup__close_remarkdoc').click(function(){
        $('#popup-remarkdoc').toggleClass('popup_open');
    });

    // @TheSleepyNomad
    // Для вызова pop-up формы добавления корректировок
    $('#secRefAdd, #subSecAdd, #newform-close').click(function(e){
        e.preventDefault()
        $('#newForm').toggleClass('new-form_open');
    });

    // @KokoulinKV
    // Для вызова pop-up формы изменения пароля, email и телефона пользователя
    $('#add-password, #popup__close_password').click(function(){
        $('#popup-password').toggleClass('popup_open');
    });
});