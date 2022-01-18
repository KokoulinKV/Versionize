let popup_doc = document.getElementById('popup-document')
let popup_section = document.getElementById('popup-section')
let popup_project = document.getElementById('popup-project')
let popup_docCloseIcon = document.getElementById('popup__close_doc')
let popup_secCloseIcon = document.getElementById('popup__close_sec')
let popup_proCloseIcon = document.getElementById('popup__close_pro')

popup_doc.addEventListener('click', () => {
    let popUp = document.getElementById('popup-document')
    popUp.classList.toggle('popup_open')
})

popup_docCloseIcon.addEventListener('click', (e) => {
    let popUp = document.getElementById('popup-document')
    popUp.classList.toggle('popup_open')
})

popup_section.addEventListener('click', () => {
    let popUp = document.getElementById('popup-section')
    popUp.classList.toggle('popup_open')
})

popup_secCloseIcon.addEventListener('click', (e) => {
    let popUp = document.getElementById('popup-section')
    popUp.classList.toggle('popup_open')
})

popup_project.addEventListener('click', () => {
    let popUp = document.getElementById('popup-project')
    popUp.classList.toggle('popup_open')
})

popup_proCloseIcon.addEventListener('click', (e) => {
    let popUp = document.getElementById('popup-project')
    popUp.classList.toggle('popup_open')
})



