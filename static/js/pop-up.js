let popupBtn = document.querySelectorAll('.popupBtn')
let body = document.querySelectorAll('body')
let lockPadding = document.querySelectorAll('.lock-padding')

let unlock = true

const timeout = 500;

if (popupBtn.length > 0) {
    for (let i = 0; i < popupBtn.length; i++) {
        let popupLink = popupBtn[i];
        popupLink.addEventListener('click', (e) => {
            let popUp = document.getElementById('popup')
            popUp.classList.toggle('popup_open')
            e.preventDefault();
        })
    }
}
let popupCloseIcon = document.getElementById('popup__close')
popupCloseIcon.addEventListener('click', (e) => {
    let popUp = document.getElementById('popup')
    popUp.classList.toggle('popup_open')
    e.preventDefault();
})