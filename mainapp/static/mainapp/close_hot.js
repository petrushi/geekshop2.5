window.onload = () => {
    let closeButton = document.querySelector('.close-button')
    closeButton.onclick = () => {
        document.querySelector('.hot-card').style.display = 'none'
    }
}