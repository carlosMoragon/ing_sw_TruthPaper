    // JavaScript para get and show the real date
    var fechaActual = new Date();
    var dia = fechaActual.getDate();
    var mes = fechaActual.getMonth() + 1; // months in js go from 0 to 11
    var anio = fechaActual.getFullYear();

    // Format "dd/mm/yyyy"
    var fechaFormateada = dia + '/' + mes + '/' + anio;

    // Mostrar la fecha en el elemento con id "fecha"
    // Show the date un the element w/ id "currentDate"
    document.getElementById('currentDate').textContent = fechaFormateada;