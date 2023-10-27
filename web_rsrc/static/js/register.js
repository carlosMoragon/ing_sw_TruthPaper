function showRegister(userType) {
    var usuario = document.getElementById('common_user');
    var periodista = document.getElementById('journalist');
    var empresa = document.getElementById('company');
 
     // Muestra el formulario correspondiente al tipo de usuario seleccionado
     if (userType === 'common_user') {
         usuario.style.display = 'block';
         periodista.style.display="none";
         empresa.style.display="none";
     } else if (userType === 'journalist') {
         usuario.style.display = 'none';
         periodista.style.display = 'block';
         empresa.style.display="none";
     } else if (userType=== 'company') {
         usuario.style.display = 'none';
         periodista.style.display="none";
         empresa.style.display = 'block';
     }
 }