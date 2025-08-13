/**
 * Feature to export schedule to image
 */

// Configuration to high quality image
const EXPORT_CONFIG = {
    backgroundColor: "#EBF2FA",
    scale: 2,
    useCORS: true,
    allowTaint: false,
    removeContainer: true,
    scrollX: 0,
    scrollY: 0,
    onclone: function(clonedDoc) {
        const clonedContainer = clonedDoc.getElementById("schedule-container");
        if (clonedContainer) {
            clonedContainer.style.transform = "scale(1)";
            clonedContainer.style.transformOrigin = "top left";
        }
    }
};

/**
 * Export schedule to image
 */
function exportScheduleAsImage() {
    const button = document.getElementById("export-btn");
    const loading = document.getElementById("loading");
    const scheduleOnly = document.getElementById("schedule-only");

    if(!scheduleOnly) {
        showErrorMessage("No se encontró el contenedor del horario");
        return;
    }

    button.style.display = "none";
    loading.style.display = "block";

    const config = {
        ...EXPORT_CONFIG,
        width: scheduleOnly.scrollWidth,
        height: scheduleOnly.scrollHeight
    };

    html2canvas(scheduleOnly, config)
        .then(function(canvas) {
            const link = document.createElement("a");
            const date = new Date().toISOString().split("T")[0];
            link.download = `horario-${date}.png`;
            link.href = canvas.toDataURL("image/png", 1.0);

            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            resetButtonState(button, loading);
            showSuccessMessage("Imagen descargada exitosamente");
        })
        .catch(function(error) {
            console.error("Error al generar la imagen:", error);
            resetButtonState(button, loading);
            showErrorMessage("Error al generar la imagen. Inténtalo de nuevo");
        });
}

/**
 * Restore button original state
 */
function resetButtonState(button, loading) {
    loading.style.display = "none";
    button.style.display = "inline-flex";
}

/**
 * Show success message
 */
function showSuccessMessage(message) {
    showMessage(message, "success");
}


/**
 * Show error message
 */
function showErrorMessage(message) {
    showMessage(message, "error");
}

/**
 * Show temporary message
 */
function showMessage(text, type) {
    const message = document.createElement("div");
    message.className = `${type}-message`;

    const icon = type === "success"
        ? "<i class='fa-solid fa-check'></i>"
        : "<i class='fa-solid fa-exclamation-triangle'></i>";

    message.innerHTML = `${icon} ${text}`;
    document.body.appendChild(message);

    setTimeout(() => {
        if (document.body.contains(message)) {
            document.body.removeChild(message);
        }
    }, 3000);
}

/**
 * Initialize export feature
 */
function initializeExport() {
    if (typeof html2canvas === "undefined") {
        console.error("html2canvas no está cargado");
        return;
    }
    
    const exportBtn = document.getElementById("export-btn");
    if (exportBtn) {
        exportBtn.addEventListener("click", exportScheduleAsImage);
    }
}

/**
 * Initialize when DOM is ready
 */
document.addEventListener("DOMContentLoaded", initializeExport);