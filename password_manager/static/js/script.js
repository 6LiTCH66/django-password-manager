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

    const exampleModal = document.getElementById('exampleModal2');
    exampleModal.addEventListener('show.mdb.modal', (e) => {
        // Button that triggered the modal
        const button = e.relatedTarget;
        // Extract info from data-mdb-* attributes
        const password_id = button.getAttribute('data-mdb-whatever'); // getting password id

        exampleModal.querySelector('#password_id').value = password_id

    })

    // if ($('#exampleModal2').hasClass('show')) {
    //     console.log("open")
    // }
    // else {
    //     console.log("closed")
    //     $("#user_password").get(0).type = 'password';
    //     $("#user_password").val("**********");
    // }
})


// const modal1 = document.getElementById('exampleModal2');
// modal1.addEventListener('hidden.bs.modal', function (event) {
//     console.log("show.bs.modal event 1")
// });



$(document).ready(function () {
    $("#myForm").submit(function (event) {
        event.preventDefault();
        $.ajax({
            url: "/show/",
            type: "POST",
            data: $('#myForm').serialize(),
            success: function (data) {
                console.log(data)
                $("#user_password").get(0).type = 'text';
                $("#user_password").val(data["key2"]);

            }


        });
    });
});




