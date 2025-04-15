document.addEventListener("DOMContentLoaded", () => {
  // Inicializa los iconos de Lucide si la librería está cargada
  if (window.lucide && typeof window.lucide.createIcons === "function") {
    window.lucide.createIcons();
  } else {
    console.error("Lucide library is not loaded. Please check your CDN link in base.html.");
  }

  // Toggle del menú móvil
  const menuTrigger = document.getElementById("menu-trigger");
  const mobileMenu = document.querySelector(".mobile-menu");

  if (menuTrigger && mobileMenu) {
    menuTrigger.addEventListener("click", () => {
      mobileMenu.classList.toggle("show");
    });

    // Cierra el menú móvil al hacer click fuera
    document.addEventListener("click", (event) => {
      if (
        !mobileMenu.contains(event.target) &&
        !menuTrigger.contains(event.target) &&
        mobileMenu.classList.contains("show")
      ) {
        mobileMenu.classList.remove("show");
      }
    });
  }
});