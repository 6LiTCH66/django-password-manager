window.addEventListener('load', function () {

    const profileModal = document.getElementById('profileModal'); // modal from profile
    if (profileModal) {
        profileModal.addEventListener('show.mdb.modal', (e) => {
            const button = e.relatedTarget;
            const password_id = button.getAttribute('data-mdb-profile-password-id');
            document.querySelector("#yes-btn").href = password_id + "/delete"
        })
    }


    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.profile-pic').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }


    $('.upload-btn').on('click', function () {
        $('#id_image').trigger('click');
        $('#id_image').change(function () {
            readURL(this)
        });
    });


    $(document).ready(function () {
        $("#successModal").modal('show'); // success message modal
        $("#errorModal").modal('show'); // error message modal

        $('.modal-backdrop').remove();
        if ($('#errorModal').hasClass('show') || $('#successModal').hasClass('show')) {
            $("body").removeAttr("class")
            $("body").removeAttr("style")
        }

    });


    setTimeout(() => {
        $(document).ready(function () {
            $("#successModal").modal('hide');
            $("#errorModal").modal('hide');
        });
    }, 3000)


    var allGs = document.getElementsByTagName('g');
    if (allGs) {
        Array.from(allGs).forEach(element => {
            if (element.parentElement) {

                if (element.parentElement.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling) {
                    element.parentElement.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.style.display = "flex"
                    element.parentElement.style.display = "none"
                    element.parentElement.nextSibling.nextSibling.nextSibling.style.display = "none"

                } else if (element.parentElement.nextSibling.nextSibling.nextSibling) {
                    element.parentElement.nextSibling.nextSibling.nextSibling.style.display = "flex"
                    element.parentElement.style.display = "none"
                }


            }

        });
    }

    const editModal = document.getElementById('editModal'); // show, update, delete modal
    if (editModal) {


        editModal.addEventListener('show.mdb.modal', (e) => {
            editModal.querySelector(".error-message").style.visibility = "hidden"

            const button = e.relatedTarget;

            const password_id = button.getAttribute('data-mdb-pass_id'); // getting password id

            const password_login = button.getAttribute('data-mdb-pass_login'); // getting password login
            let password_title = button.getAttribute('data-mdb-pass_title'); // getting password title
            const password_icon = button.getAttribute('data-mdb-pass_icon'); // getting password icon
            const password_website = button.getAttribute('data-mdb-website'); // getting password website

            users_login = editModal.querySelectorAll('#user_login')

            users_login.forEach(
                function (login) {
                    login.value = password_login
                }
            )

            editModal.querySelector("#user_title").value = password_title
            editModal.querySelector("#user_website").value = password_website


            if (password_title.length > 18) {
                password_title = password_title.substring(0, 18) + "..."
            }

            editModal.querySelector("#editModalLabel").textContent = password_title.substring(0, 21)

            editModal.querySelector("#editModalLabel")
                .insertAdjacentHTML('afterbegin',
                    `<div class="icon-container me-2" style="display: none;">
            <div class="iconImage">
                ${password_title.charAt(0)}
            </div>
        </div>`
                )

            editModal.querySelector("#editModalLabel")
                .insertAdjacentHTML('afterbegin', `<i class="fa-brands fa-${password_icon} fa-2xl text-light me-2" style="color: #4547e2;"></i>`)


            setTimeout(() => {
                $('#editModalLabel').ready(function () {

                    var allGs_modal = editModal.getElementsByTagName('g');

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


            editModal.querySelector('#password_id').value = password_id // setting hidden input to password's id

            editModal.querySelector('#user_password').value = "*********" // if modal form is opened clear 'Password' input
            editModal.querySelector('#user_password').type = 'password' // and set password type back
            editModal.querySelector('#user_master_password').value = "" // clear Master password input from previous password

            document.querySelector("#yes-btn").href = password_id + "/delete" // setting url for current password to delete
            document.querySelector("#myForm1").action = password_id + "/update/" // setting action for form to update password


        })
    }


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





