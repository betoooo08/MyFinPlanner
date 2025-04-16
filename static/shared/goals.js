document.addEventListener('DOMContentLoaded', function () {
  // Seleccionar todos los botones de contribución
  const buttons = document.querySelectorAll('.add-contribution-btn');

  buttons.forEach(button => {
    button.addEventListener('click', function () {
      const goalId = this.dataset.goalId; // Obtener el ID de la meta
      const amount = prompt('Enter contribution amount:'); // Pedir al usuario el monto

      // Validar el monto ingresado
      if (amount && !isNaN(amount) && parseFloat(amount) > 0) {
        // Enviar la solicitud POST al servidor
        fetch(`/finances/goals/${goalId}/add-contribution/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
          },
          body: JSON.stringify({ amount }),
        })
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            if (data.success) {
              // Actualizar dinámicamente la barra de progreso y los valores
              const card = button.closest('.card');
              const progressBar = card.querySelector('.progress-bar');
              const savedText = card.querySelector('p:nth-of-type(1)');
              const percentageText = card.querySelector('p:nth-of-type(3)');

              // Actualizar los valores en la interfaz
              savedText.textContent = `Saved: $${data.new_amount} | Remaining: $${data.remaining}`;
              progressBar.style.width = `${data.percentage}%`;
              percentageText.textContent = `${data.percentage}% Complete`;

              // Deshabilitar el botón si la meta está completa
              if (data.percentage >= 100) {
                button.disabled = true;
                button.textContent = 'Goal Completed';
              }

              alert('Contribution added successfully!');
            } else {
              // Mostrar el mensaje de error devuelto por el servidor
              alert(`Error: ${data.error}`);
            }
          })
          .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while adding the contribution.');
          });
      } else {
        alert('Please enter a valid amount.');
      }
    });
  });
});