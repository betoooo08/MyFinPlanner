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

  // Toggle de tema
  const themeToggle = document.getElementById("theme-toggle");
  const darkIcon = document.querySelector(".dark-icon");
  const lightIcon = document.querySelector(".light-icon");
  const html = document.documentElement;

  if (themeToggle && darkIcon && lightIcon) {
    const savedTheme = localStorage.getItem("theme") || "light";

    if (savedTheme === "dark") {
      html.classList.add("dark");
      darkIcon.classList.remove("hidden");
      lightIcon.classList.add("hidden");
    }

    themeToggle.addEventListener("click", () => {
      const isDark = html.classList.toggle("dark");
      if (isDark) {
        darkIcon.classList.remove("hidden");
        lightIcon.classList.add("hidden");
        localStorage.setItem("theme", "dark");
      } else {
        darkIcon.classList.add("hidden");
        lightIcon.classList.remove("hidden");
        localStorage.setItem("theme", "light");
      }
    });
  }
});