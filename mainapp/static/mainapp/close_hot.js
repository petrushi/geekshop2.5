window.onload = () => {
    console.log('loads')
    let closeButton = document.querySelector('.close-button')
    console.log(closeButton)
    closeButton.onclick = () => {
        document.querySelector('.hot-card').style.display = 'none'
    }
}