document.addEventListener('DOMContentLoaded', function () {
    // Hacer una solicitud al servidor para obtener los resultados
    fetch('/obtener_resultados')  // Ajusta la ruta según tu configuración del servidor
        .then(response => response.json())
        .then(data => {
            // Manipula los datos recibidos y muestra los resultados en la página
            mostrarResultados(data);
        })
        .catch(error => console.error('Error al obtener resultados:', error));
});

function mostrarResultados(resultados) {
    // Obtén el contenedor de resultados
    var resultadosContainer = document.getElementById('predicciones-container');

    // Itera sobre los resultados y crea elementos HTML para mostrar la información
    resultados.forEach(function (equipo) {
        var equipoDiv = document.createElement('div');
        equipoDiv.innerHTML = `
            <h2>${equipo.Team}</h2>
            <p>Win Rate: ${equipo.WinRate}%</p>
            <p>GDM: ${equipo.GDM}</p>
            <p>Predicción de Victorias: ${equipo.WinsPred === 1 ? 'Sí' : 'No'}</p>
            <p>Verificación: ${equipo.Check === '✔' ? 'Correcto' : 'Incorrecto'}</p>
            <hr>
        `;
        resultadosContainer.appendChild(equipoDiv);
    });
}
