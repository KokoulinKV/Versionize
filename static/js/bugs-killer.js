// В этом файле будут скрипты для исправления багов и ошибок, которые были найдены в процессе разработки
// При добавлении скрипта напишите небольшое описание
$(document).ready(function () {

    // @TheSleepyNomad
    // Устраняет проблему, когда при обновлении страницы в БД дублируются данные
    if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
      };
});