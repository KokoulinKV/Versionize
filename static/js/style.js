// В этом файле будут храниться и запускаться функции, которые влияют только на стиль
// Для применения стилей нам надо дождаться загрузки DOM
$(document).ready(function () {

    // Стилизация пока всех таблиц. В зависимости от количества их строк
    console.log($('#table'));
    table_rows = $('#table').children() // Получаем список всех строк из таблицы
    for (let i = 0; i < table_rows.length; i++) {
        // четным присваиваем один стиль, нечетным другой
        if (i % 2) {
            table_rows[i].classList.add('form-table__table_even');
        } else {
            table_rows[i].classList.add('form-table__table_odd');
        }
    }
    console.log(table_rows);
});