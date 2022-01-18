let popup_doc = document.getElementById('add-document')
let popup_section = document.getElementById('add-section')
let popup_project = document.getElementById('add-project')
let popup_docCloseIcon = document.getElementById('popup__close_doc')
let popup_secCloseIcon = document.getElementById('popup__close_sec')
let popup_proCloseIcon = document.getElementById('popup__close_pro')

const docum = document.getElementById('popup-document')
const sect = document.getElementById('popup-section')
const project = document.getElementById('popup-project')

popup_doc.addEventListener('click', (e) => {

    docum.classList.toggle('popup_open')
})

popup_docCloseIcon.addEventListener('click', (e) => {
    docum.classList.toggle('popup_open')
})

popup_section.addEventListener('click', (e) => {
    sect.classList.toggle('popup_open')
})

popup_secCloseIcon.addEventListener('click', (e) => {
    sect.classList.toggle('popup_open')
})

popup_project.addEventListener('click', (e) => {
    project.classList.toggle('popup_open')
})

popup_proCloseIcon.addEventListener('click', (e) => {
    project.classList.toggle('popup_open')
})



