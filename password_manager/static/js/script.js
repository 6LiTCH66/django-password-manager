window.addEventListener('load', function () {
    var allGs = document.getElementsByTagName('g');
    if (allGs) {
        Array.from(allGs).forEach(element => {
            if (element.parentElement) {

                // console.log(element.parentElement.nextSibling.nextSibling.nextSibling);
                element.parentElement.nextSibling.nextSibling.nextSibling.style.display = "flex"
                element.parentElement.style.display = "none"
            }

        });
    }
})

