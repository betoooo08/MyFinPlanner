document.addEventListener("DOMContentLoaded", () => {
    // Manejo de pestañas
    const tabs = document.querySelectorAll(".tab");
    const tabContents = document.querySelectorAll("[data-tab-content]");

    tabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            const target = tab.dataset.tab;

            // Desactivar todas las pestañas
            tabs.forEach((t) => t.classList.remove("active"));
            tabContents.forEach((content) => content.classList.remove("active"));

            // Activar la pestaña seleccionada
            tab.classList.add("active");
            document.querySelector(`[data-tab-content="${target}"]`)?.classList.add("active");
        });
    });

    // Inicializar tooltips
    const tooltips = document.querySelectorAll("[data-tooltip]");
    tooltips.forEach((tooltip) => {
        tooltip.addEventListener("mouseenter", () => {
            const tooltipText = tooltip.dataset.tooltip;
            const tooltipEl = document.createElement("div");
            tooltipEl.className = "tooltip";
            tooltipEl.textContent = tooltipText;
            document.body.appendChild(tooltipEl);

            const rect = tooltip.getBoundingClientRect();
            tooltipEl.style.top = `${rect.top - tooltipEl.offsetHeight - 10}px`;
            tooltipEl.style.left = `${rect.left + (rect.width / 2) - tooltipEl.offsetWidth / 2}px`;
            tooltipEl.style.opacity = "1";
        });

        tooltip.addEventListener("mouseleave", () => {
            const tooltipEl = document.querySelector(".tooltip");
            if (tooltipEl) {
                tooltipEl.remove();
            }
        });
    });
});