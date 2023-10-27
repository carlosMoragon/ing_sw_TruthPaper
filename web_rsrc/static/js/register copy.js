// Esta función se encarga de alternar la visibilidad del formulario y los botones
function toggleForm(buttonId, formId) {
    var button = document.getElementById(buttonId);
    var form = document.getElementById(formId);

    // Verifica si el formulario está visible o no
    var isVisible = form.style.display !== 'none';

    // Oculta todos los formularios
    var formularios = document.getElementsByClassName('register_user');
    for (var i = 0; i < formularios.length; i++) {
        formularios[i].style.display = 'none';
    }

    // Alterna la visibilidad del formulario actual
    form.style.display = isVisible ? 'none' : 'block';

    // Ajusta el tamaño y la apariencia del botón
    if (isVisible) {
        button.style.width = '200px';
        button.style.height = '300px';
        button.style.transform = 'none';
    } else {
        button.style.width = '100%';
        button.style.height = 'auto';
        button.style.transform = 'scale(1.2)';
    }
}

// Esta función resetea la apariencia de los botones y oculta todos los formularios
function resetButtons() {
    var buttons = document.getElementsByTagName('button');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].style.width = '200px';
        buttons[i].style.height = '300px';
        buttons[i].style.transform = 'none';
    }

    var formularios = document.getElementsByClassName('register_user');
    for (var i = 0; i < formularios.length; i++) {
        formularios[i].style.display = 'none';
    }
}
