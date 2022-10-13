window.addEventListener('load', function () {
    $('.upload-btn').on('click', function () {
        $('.upload-input').trigger('click');
    });

    $(document).ready(function () {
        $("#exampleModal6").modal('show'); // success message modal
        $("#exampleModal7").modal('show'); // error message modal

        $('.modal-backdrop').remove();
        if ($('#exampleModal7').hasClass('show') || $('#exampleModal6').hasClass('show')) {
            $("body").removeAttr("class")
            $("body").removeAttr("style")
        }

    });


    setTimeout(() => {
        $(document).ready(function () {
            $("#exampleModal6").modal('hide');
            $("#exampleModal7").modal('hide');
        });
    }, 3000)



    var allGs = document.getElementsByTagName('g');
    if (allGs) {
        Array.from(allGs).forEach(element => {
            if (element.parentElement) {

                // console.log(element.parentElement);
                element.parentElement.nextSibling.nextSibling.nextSibling.style.display = "flex"
                element.parentElement.style.display = "none"
            }

        });
    }

    const exampleModal = document.getElementById('exampleModal2'); // show, update, delete modal
    // if exampleModal добавить проверку
    exampleModal.addEventListener('show.mdb.modal', (e) => {
        exampleModal.querySelector(".error-message").style.visibility = "hidden"

        // Button that triggered the modal
        const button = e.relatedTarget;

        // Extract info from data-mdb-* attributes
        const password_id = button.getAttribute('data-mdb-pass_id'); // getting password id

        const password_login = button.getAttribute('data-mdb-pass_login'); // getting password login
        let password_title = button.getAttribute('data-mdb-pass_title'); // getting password title
        const password_icon = button.getAttribute('data-mdb-pass_icon'); // getting password icon
        const password_website = button.getAttribute('data-mdb-website'); // getting password website

        users_login = exampleModal.querySelectorAll('#user_login')

        users_login.forEach(
            function (login) {
                login.value = password_login
            }
        )

        // exampleModal.querySelector("#user_login").value = password_login // setting login to login input
        exampleModal.querySelector("#user_title").value = password_title
        exampleModal.querySelector("#user_website").value = password_website


        if (password_title.length > 18) {
            password_title = password_title.substring(0, 18) + "..."
        }

        exampleModal.querySelector("#exampleModalLabel").textContent = password_title.substring(0, 21)

        exampleModal.querySelector("#exampleModalLabel")
            .insertAdjacentHTML('afterbegin',
                `<div class="icon-container me-2" style="display: none;">
            <div class="iconImage">
                ${password_title.charAt(0)}
            </div>
        </div>`
            )

        exampleModal.querySelector("#exampleModalLabel")
            .insertAdjacentHTML('afterbegin', `<i class="fa-brands fa-${password_icon} fa-2xl text-light me-2" style="color: #4547e2;"></i>`)




        setTimeout(() => {
            $('#exampleModalLabel').ready(function () {

                var allGs_modal = exampleModal.getElementsByTagName('g');

                if (allGs_modal) {
                    Array.from(allGs_modal).forEach(element => {
                        if (element.parentElement) {

                            // console.log(element.parentElement.nextSibling.nextSibling);
                            element.parentElement.nextSibling.nextSibling.style.display = "flex"
                            element.parentElement.style.display = "none"
                        }

                    });
                }
            });
        }, 1000)

        exampleModal.querySelector('#password_id').value = password_id // setting hidden input to password's id

        exampleModal.querySelector('#user_password').value = "*********" // if modal form is opend clear 'Password' input
        exampleModal.querySelector('#user_password').type = 'password' // and set password type back
        exampleModal.querySelector('#user_master_password').value = "" // clear Master password input from previous password

        document.querySelector("#yes-btn").href = password_id + "/delete" // setting url for current password to delete
        document.querySelector("#myForm1").action = password_id + "/update/" // setting action for form to update password



    })

})



$(document).ready(function () {
    $("#myForm").submit(function (event) {
        event.preventDefault();
        $.ajax({
            url: "/show/",
            type: "POST",
            data: $('#myForm').serialize(),
            success: function (data) {
                // console.log(data)
                $("#user_password").get(0).type = 'text';
                $("#user_password").val(data["password"]);
                $("#user_master_password").val("");
                $(".error-message").css("visibility", "hidden");

            },
            error: function (error) {
                error_message = error["responseText"]
                $(".error-message").html(error_message)
                $(".error-message").css("visibility", "visible");
                $("#user_master_password").val("");
            }

        });
    });
});





