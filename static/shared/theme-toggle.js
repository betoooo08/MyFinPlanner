document.addEventListener("DOMContentLoaded", () => {
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
      darkIcon.classList.toggle("hidden", !isDark);
      lightIcon.classList.toggle("hidden", isDark);
      localStorage.setItem("theme", isDark ? "dark" : "light");
    });
  }
});