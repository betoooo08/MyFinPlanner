document.addEventListener('DOMContentLoaded', function() {
  // Preset periods functionality
  const presetPeriodSelect = document.getElementById('preset-period');
  const startDateInput = document.getElementById('start-date');
  const endDateInput = document.getElementById('end-date');
  
  presetPeriodSelect.addEventListener('change', function() {
    const selectedValue = this.value;
    const today = new Date();
    let startDate, endDate;
    
    switch(selectedValue) {
      case 'current-quarter':
        // Set dates for current quarter
        startDate = new Date(today.getFullYear(), Math.floor(today.getMonth() / 3) * 3, 1);
        endDate = new Date(startDate.getFullYear(), startDate.getMonth() + 3, 0);
        break;
      case 'previous-quarter':
        // Set dates for previous quarter
        startDate = new Date(today.getFullYear(), Math.floor(today.getMonth() / 3) * 3 - 3, 1);
        endDate = new Date(startDate.getFullYear(), startDate.getMonth() + 3, 0);
        break;
      case 'current-year':
        // Set dates for current year
        startDate = new Date(today.getFullYear(), 0, 1);
        endDate = new Date(today.getFullYear(), 11, 31);
        break;
      case 'previous-year':
        // Set dates for previous year
        startDate = new Date(today.getFullYear() - 1, 0, 1);
        endDate = new Date(today.getFullYear() - 1, 11, 31);
        break;
      case 'last-30-days':
        // Set dates for last 30 days
        endDate = new Date();
        startDate = new Date();
        startDate.setDate(endDate.getDate() - 30);
        break;
      case 'last-90-days':
        // Set dates for last 90 days
        endDate = new Date();
        startDate = new Date();
        startDate.setDate(endDate.getDate() - 90);
        break;
      case 'custom':
        // Do nothing, let user select custom dates
        return;
    }
    
    // Format dates as YYYY-MM-DD for input fields
    startDateInput.value = formatDate(startDate);
    endDateInput.value = formatDate(endDate);
  });
  
  // Format date as YYYY-MM-DD
  function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
  
  // Generate report button functionality
  const generateBtn = document.querySelector('.generate-btn');
  
  generateBtn.addEventListener('click', function() {
    // Get form values
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;
    const reportCategory = document.getElementById('report-category').value;
    const reportFormat = document.getElementById('report-format').value;
    const includeVisualizations = document.getElementById('include-visualizations').value;
    const reportName = document.getElementById('report-name').value;
    const reportDescription = document.getElementById('report-description').value;
    
    // Validate form
    if (!startDate || !endDate || !reportName) {
      alert('Please fill in all required fields');
      return;
    }
    
    // In a real implementation, this would send an AJAX request to generate the report
    // For this demo, we'll just show a success message
    alert(`Report "${reportName}" is being generated. It will appear in your saved reports when complete.`);
  });
  
  // Download and delete report functionality
  const reportActionBtns = document.querySelectorAll('.report-action-btn');
  
  reportActionBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      const action = this.getAttribute('title');
      const reportName = this.closest('tr').querySelector('.report-name').textContent;
      
      if (action === 'Download Report') {
        // In a real implementation, this would trigger a download
        alert(`Downloading report: ${reportName}`);
      } else if (action === 'Delete Report') {
        // In a real implementation, this would delete the report
        if (confirm(`Are you sure you want to delete the report: ${reportName}?`)) {
          this.closest('tr').remove();
        }
      }
    });
  });

  // AI Insight functionality
  const aiInsightForm = document.getElementById('ai-insight-form');
  const aiInsightResult = document.getElementById('ai-insight-result');
  const aiLoading = document.getElementById('ai-loading');
  const aiInsightsPlaceholder = document.querySelector('.ai-insights-placeholder');
  
  if (aiInsightForm) {
    aiInsightForm.addEventListener('submit', function(e) {
      // Si no estamos en modo de desarrollo, prevenir el envío normal del formulario
      // y manejar la solicitud con AJAX
      if (!window.location.hostname.includes('localhost') && !window.location.hostname.includes('127.0.0.1')) {
        e.preventDefault();
        
        // Mostrar el spinner de carga y ocultar otros elementos
        if (aiInsightsPlaceholder) {
          aiInsightsPlaceholder.style.display = 'none';
        }
        if (aiInsightResult) {
          aiInsightResult.classList.remove('active');
        }
        aiLoading.classList.add('active');
        
        // Realizar la solicitud AJAX
        fetch(this.action, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
          },
          body: new URLSearchParams(new FormData(this))
        })
        .then(response => response.text())
        .then(html => {
          // Ocultar el spinner de carga
          aiLoading.classList.remove('active');
          
          // Crear un elemento temporal para analizar la respuesta HTML
          const tempDiv = document.createElement('div');
          tempDiv.innerHTML = html;
          
          // Extraer el insight del HTML
          const newInsight = tempDiv.querySelector('#ai-insight-result');
          
          if (newInsight) {
            // Si ya existe un contenedor de resultado, actualizarlo
            if (aiInsightResult) {
              aiInsightResult.innerHTML = newInsight.innerHTML;
              aiInsightResult.classList.add('active');
            } else {
              // Si no existe, crear uno nuevo
              const insightsContent = document.querySelector('.ai-insights-content');
              insightsContent.appendChild(newInsight);
            }
          }
        })
        .catch(error => {
          console.error('Error:', error);
          aiLoading.classList.remove('active');
          alert('There was an error generating the AI insight. Please try again.');
        });
      }
    });
  }
});
