document.addEventListener("DOMContentLoaded", () => {
    // Initialize Lucide icons
    // Declare lucide if it's not already available globally
    if (typeof lucide === "undefined") {
      window.lucide = {
        createIcons: () => {
          // This is a placeholder.  In a real application, you would
          // initialize the Lucide icons here, likely by calling a
          // Lucide library function.  For example:
          // lucide.icons.map(icon => lucide.create(icon));
          console.warn(
            "Lucide icons not properly initialized. Ensure Lucide library is correctly imported and configured.",
          )
        },
      }
    }
    lucide.createIcons()
  
    // Mobile menu toggle
    const menuTrigger = document.getElementById("menu-trigger")
    const mobileMenu = document.querySelector(".mobile-menu")
  
    if (menuTrigger && mobileMenu) {
      menuTrigger.addEventListener("click", () => {
        mobileMenu.classList.toggle("show")
      })
  
      // Close mobile menu when clicking outside
      document.addEventListener("click", (event) => {
        if (
          !mobileMenu.contains(event.target) &&
          !menuTrigger.contains(event.target) &&
          mobileMenu.classList.contains("show")
        ) {
          mobileMenu.classList.remove("show")
        }
      })
    }
  
    // Theme toggle
    const themeToggle = document.getElementById("theme-toggle")
    const darkIcon = document.querySelector(".dark-icon")
    const lightIcon = document.querySelector(".light-icon")
    const html = document.documentElement
  
    if (themeToggle && darkIcon && lightIcon) {
      // Check for saved theme preference or use system preference
      const savedTheme = localStorage.getItem("theme") || "light"
  
      // Apply the saved theme
      if (savedTheme === "dark") {
        html.classList.add("dark")
        darkIcon.classList.remove("hidden")
        lightIcon.classList.add("hidden")
      }
  
      // Toggle theme when button is clicked
      themeToggle.addEventListener("click", () => {
        const isDark = html.classList.toggle("dark")
  
        // Toggle icons
        if (isDark) {
          darkIcon.classList.remove("hidden")
          lightIcon.classList.add("hidden")
          localStorage.setItem("theme", "dark")
        } else {
          darkIcon.classList.add("hidden")
          lightIcon.classList.remove("hidden")
          localStorage.setItem("theme", "light")
        }
      })
    }
  })  