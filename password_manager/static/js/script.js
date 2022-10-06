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

// if (document.querySelector("#down-btn")) {
//     // console.log(document.querySelector("#down-btn"));
//     document.addEventListener("click", function (event) {

//         const workContainer = event.target.closest('.svg-inline--fa');
//         if (workContainer !== null) {
//             const div = document.querySelector("#down-btn");
//             if (document.querySelector("#down-btn").classList.contains('fa-chevron-down')) {

//                 div.classList.remove('fa-chevron-down');
//                 div.classList.add("fa-chevron-up")
//             } else {
//                 div.classList.remove('fa-chevron-up');
//                 div.classList.add("fa-chevron-down")
//             }
//         }
//     });
// }





