import './styles.css'
import 'htmx.org'

// Configuración de HTMX
htmx.config.defaultSwapStyle = 'outerHTML'
htmx.config.globalViewTransitions = true
htmx.config.headers['X-CSRFToken'] = document.querySelector('[name=csrfmiddlewaretoken]').value

// Evento para confirmar que HTMX está cargado
document.addEventListener('DOMContentLoaded', function() {
    document.dispatchEvent(new CustomEvent('htmx:loaded', {
        detail: { version: htmx.version }
    }));
});

// Log de versión de HTMX
console.log('HTMX version:', htmx.version)

console.log('Vite + HTMX is running! 🚀') 