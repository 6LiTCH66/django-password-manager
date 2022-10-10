var janelaPopUp = new Object();
janelaPopUp.abre = function (id, classes, titulo, corpo, functionCancelar, functionEnviar, textoCancelar, textoEnviar) {
    var cancelar = (textoCancelar !== undefined) ? textoCancelar : 'Cancel';
    var enviar = (textoEnviar !== undefined) ? textoEnviar : 'Send';
    classes += ' ';
    var classArray = classes.split(' ');
    classes = '';
    classesFundo = '';
    var classBot = '';
    $.each(classArray, function (index, value) {
        switch (value) {
            case 'alert': classBot += ' alert '; break;
            case 'blue': classesFundo += this + ' ';
            case 'green': classesFundo += this + ' ';
            case 'red': classesFundo += this + ' ';
            case 'white': classesFundo += this + ' ';
            case 'orange': classesFundo += this + ' ';
            case 'purple': classesFundo += this + ' ';
            default: classes += this + ' '; break;
        }
    });
    var popFundo = '<div id="popFundo_' + id + '" class="popUpFundo ' + classesFundo + '"></div>'
    var janela = '<div id="' + id + '" class="popUp ' + classes + '"><h1>' + titulo + "</h1><div><span>" + corpo + "</span></div><button class='puCancelar " + classBot + "' id='" + id + "_cancelar' data-parent=" + id + ">" + cancelar + "</button><button class='puEnviar " + classBot + "' data-parent=" + id + " id='" + id + "_enviar'>" + enviar + "</button></div>";
    $("window, body").css('overflow', 'hidden');

    $("body").append(popFundo);
    $("body").append(janela);
    $("body").append(popFundo);
    //alert(janela);
    $("#popFundo_" + id).fadeIn("fast");
    $("#" + id).addClass("popUpEntrada");

    $("#" + id + '_cancelar').on("click", function () {
        if ((functionCancelar !== undefined) && (functionCancelar !== '')) {
            functionCancelar();

        } else {
            janelaPopUp.fecha(id);
        }
    });
    $("#" + id + '_enviar').on("click", function () {
        if ((functionEnviar !== undefined) && (functionEnviar !== '')) {
            functionEnviar();
        } else {
            janelaPopUp.fecha(id);
        }
    });

};
janelaPopUp.fecha = function (id) {
    if (id !== undefined) {
        $("#" + id).removeClass("popUpEntrada").addClass("popUpSaida");

        $("#popFundo_" + id).fadeOut(1000, function () {
            $("#popFundo_" + id).remove();
            $("#" + $(this).attr("id") + ", #" + id).remove();
            if (!($(".popUp")[0])) {
                $("window, body").css('overflow', 'auto');
            }
        });


    }
    else {
        $(".popUp").removeClass("popUpEntrada").addClass("popUpSaida");

        $(".popUpFundo").fadeOut(1000, function () {
            $(".popUpFundo").remove();
            $(".popUp").remove();
            $("window, body").css('overflow', 'auto');
        });


    }
}
$("button").on("click", function () {
    var myText = $("#myText").val();
    janelaPopUp.abre("asdf", $("#size").val() + " " + $(this).html() + ' ' + $("#mode").val(), $("#title").val(), myText)
});
janelaPopUp.abre("example", 'p red', 'Example', 'chosse a configuration and click the color!');
setTimeout(function () { janelaPopUp.fecha('example'); }, 2000);
window.addEventListener('load', function () {


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

    const exampleModal = document.getElementById('exampleModal2');

    exampleModal.addEventListener('show.mdb.modal', (e) => {

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





