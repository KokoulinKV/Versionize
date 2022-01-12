let arrow = document.querySelectorAll('.arrow');
let submenu = document.querySelectorAll('.sub-menu');
let sidebar = document.querySelectorAll('.sidebar-nav');
for (var i = 0; i < arrow.length; i++) {
    arrow[0].addEventListener('click', () => {
        // console.log(submenu[0]);
        submenu[0].classList.toggle('sub-menu_open')
        sidebar[0].classList.toggle('sidebar-nav_close')

    });
}
;


let close_btn = document.querySelectorAll('.sub-menu-top__list-title')
console.log(close_btn);
close_btn[0].addEventListener('click', () => {
    submenu[0].classList.toggle('sub-menu_open')
    sidebar[0].classList.toggle('sidebar-nav_close')
})

// Настройки для последнего списка
// Задачи
let tasks = document.getElementById('tasks')
tasks.addEventListener('click', () => {
    let taks = document.getElementById('task')
    task.classList.toggle('sub-menu-top__sub-list_open')
})
// Документы
let docs = document.getElementById('docs')
docs.addEventListener('click', () => {
    let doc = document.getElementById('doc')
    doc.classList.toggle('sub-menu-top__sub-list_open')
})
// Канцелярия
let chancellery = document.getElementById('chancellery')
chancellery.addEventListener('click', () => {
    let chancery = document.getElementById('chancery')
    chancery.classList.toggle('sub-menu-top__sub-list_open')
})
// Все мои задачи
let mytasks = document.getElementById('my_tasks')
mytasks.addEventListener('click', () => {
    let mytask = document.getElementById('my_task')
    mytask.classList.toggle('sub-menu-top__sub-list_open')
})
// Документы
let mydocs = document.getElementById('my_docs')
mydocs.addEventListener('click', () => {
    let mydoc = document.getElementById('my_doc')
    mydoc.classList.toggle('sub-menu-top__sub-list_open')
})
// Канцелярия
let my_contracts = document.getElementById('my_contracts')
my_contracts.addEventListener('click', () => {
    let my_contract = document.getElementById('my_contract')
    my_contract.classList.toggle('sub-menu-top__sub-list_open')
})



// Комментарии в документе
let hide_btn = document.getElementById('hide')
// let hiden_obj = document.getElementById('workspace-comments__content')
hide_btn.addEventListener('click', () => {
    let hiden_obj = document.getElementById('workspace-comments__content')
    let hiden_ob1 = document.getElementById('notice')
    hiden_obj.classList.toggle('workspace-comments__content_hide')
    hiden_ob1.classList.toggle('notice_hide')
})