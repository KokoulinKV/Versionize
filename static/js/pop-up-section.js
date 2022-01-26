let popup_doc = document.getElementById('add-document')
let popup_remarkdoc = document.getElementById('add-remarkdoc')
let popup_docCloseIcon = document.getElementById('popup__close_doc')
let popup_remarkdocCloseIcon = document.getElementById('popup__close_remarkdoc')


const docum = document.getElementById('popup-document')
const remarkdoc = document.getElementById('popup-remarkdoc')

popup_doc.addEventListener('click', (e) => {

    docum.classList.toggle('popup_open')
})

popup_docCloseIcon.addEventListener('click', (e) => {
    docum.classList.toggle('popup_open')
})


popup_remarkdoc.addEventListener('click', (e) => {

    remarkdoc.classList.toggle('popup_open')
})

popup_remarkdocCloseIcon.addEventListener('click', (e) => {
    remarkdoc.classList.toggle('popup_open')
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



