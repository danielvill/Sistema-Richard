    
// Obtener la fecha actual de la persona 
let today = new Date();
let dd = String(today.getDate()).padStart(2, '0');
let mm = String(today.getMonth() + 1).padStart(2, '0'); //Enero es 0!
let yyyy = today.getFullYear();

today = yyyy + '-' + mm + '-' + dd;
document.getElementById("fecha").setAttribute("min", today);
document.getElementById("fecha").setAttribute("max", today);

document.getElementById('hora').addEventListener('change', function() {
var hora = this.value;
var horarioLaboral = ['08:00', '12:00', '14:00', '18:00'];

if (horarioLaboral.includes(hora)) {
    console.log('Hora laborable');
} else {
    alert('Esa no es una hora laborable solo se acepta este formato de hora 08:00,12:00,14:00,18:00' );
    this.value = '';  // Borra el valor del campo de entrada
}
});
