let popup_section = document.getElementById('add-section')
let popup_secCloseIcon = document.getElementById('popup__close_sec')


const sect = document.getElementById('popup-section')

popup_section.addEventListener('click', (e) => {
    sect.classList.toggle('popup_open')
})

popup_secCloseIcon.addEventListener('click', (e) => {
    sect.classList.toggle('popup_open')
})



let newForm_close = document.getElementById('newform-close')
let newForm_add = document.getElementById('secRefAdd')
let submitSec = document.getElementById('subSecAdd')
const newForm = document.getElementById('newForm')


newForm_add.addEventListener('click', (e) => {
    newForm.classList.toggle('new-form_open')
})
submitSec.addEventListener('click', (e) => {
    // отключаем обновление страницы
    e.preventDefault()
    newForm.classList.toggle('new-form_open')
})
newForm_close.addEventListener('click', (e) => {
    newForm.classList.toggle('new-form_open')
})



