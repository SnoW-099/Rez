// Script para la web de Rez Bot

document.addEventListener('DOMContentLoaded', function() {
    // Agregar funcionalidad a los enlaces de navegación
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                window.scrollTo({
                    top: targetSection.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Función para actualizar el ranking (simulado)
    function actualizarRanking() {
        console.log('Actualizando ranking...');
        // Aquí iría la lógica para obtener datos del servidor
    }
    
    // Simular carga de datos cuando se hace clic en la sección de ranking
    const rankingLink = document.querySelector('a[href="#ranking"]');
    if (rankingLink) {
        rankingLink.addEventListener('click', function() {
            setTimeout(actualizarRanking, 500);
        });
    }
    
    // Mostrar notificación cuando se carga la página
    mostrarNotificacion('Panel web de Rez Bot cargado correctamente', 'info');
});

// Función para mostrar notificaciones
function mostrarNotificacion(mensaje, tipo) {
    // Crear elemento de notificación
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion ${tipo}`;
    notificacion.textContent = mensaje;
    notificacion.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        background-color: #3498db;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 1000;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    `;
    
    // Ajustar color según tipo
    switch(tipo) {
        case 'success':
            notificacion.style.backgroundColor = '#2ecc71';
            break;
        case 'error':
            notificacion.style.backgroundColor = '#e74c3c';
            break;
        case 'warning':
            notificacion.style.backgroundColor = '#f39c12';
            break;
        default:
            notificacion.style.backgroundColor = '#3498db';
    }
    
    document.body.appendChild(notificacion);
    
    // Animar entrada
    setTimeout(() => {
        notificacion.style.opacity = '1';
        notificacion.style.transform = 'translateX(0)';
    }, 10);
    
    // Remover después de cierto tiempo
    setTimeout(() => {
        notificacion.style.opacity = '0';
        notificacion.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notificacion.parentNode) {
                notificacion.parentNode.removeChild(notificacion);
            }
        }, 300);
    }, 3000);
}