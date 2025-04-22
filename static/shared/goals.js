document.addEventListener('DOMContentLoaded', function() {
  // — AI Insight AJAX (no recarga completa) —
  const insightBtn       = document.getElementById('generate-insight-btn');
  const insightContainer = document.getElementById('ai-insight-container');
  if (insightBtn) {
    insightBtn.addEventListener('click', function() {
      fetch(this.dataset.url)
        .then(response => response.text())
        .then(html => {
          // Inyectamos solo el bloque .ai-insight-container
          const tempDiv    = document.createElement('div');
          tempDiv.innerHTML = html;
          const aiBlock     = tempDiv.querySelector('.ai-insight-container');
          if (aiBlock) {
            insightContainer.innerHTML = '';
            insightContainer.appendChild(aiBlock);
          }
        })
        .catch(err => {
          console.error('Error fetching AI insight:', err);
        });
    });
  }

  // — Filtrado de metas según estado —
  const goalFilters = document.querySelectorAll('input[name="goal-filter"]');
  const goalCards   = document.querySelectorAll('.goal-card');
  goalFilters.forEach(filter => {
    filter.addEventListener('change', function() {
      const v = this.value;
      goalCards.forEach(card => {
        if (v === 'all') {
          card.style.display = 'block';
          return;
        }
        const fill   = card.querySelector('.progress-fill');
        let status   = 'behind-schedule';
        if (fill.classList.contains('needs-attention')) status = 'needs-attention';
        if (fill.classList.contains('on-track'))        status = 'on-track';
        card.style.display = (status === v ? 'block' : 'none');
      });
    });
  });

  // — Modal “Add Contribution” —
  const modal             = document.getElementById('contributionModal');
  const closeModalBtn     = document.getElementById('closeModal');
  const contributionForm  = document.getElementById('contributionForm');
  const contributionError = document.getElementById('contributionError');
  const goalIdInput       = document.getElementById('goalId');

  document.querySelectorAll('.add-contribution-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      goalIdInput.value = btn.dataset.goalId;
      modal.classList.add('active');
    });
  });

  closeModalBtn.addEventListener('click', () => {
    modal.classList.remove('active');
    contributionForm.reset();
    contributionError.textContent = '';
  });
  window.addEventListener('click', e => {
    if (e.target === modal) closeModalBtn.click();
  });

  contributionForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const id     = goalIdInput.value;
    const amount = parseFloat(document.getElementById('contributionAmount').value);

    fetch(`/finances/goals/${id}/add-contribution/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ amount })
    })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        const card = document.querySelector(`.goal-card[data-goal-id="${id}"]`);
        const fill = card.querySelector('.progress-fill');

        card.querySelector('.goal-amount-saved').textContent = `$${data.new_amount.toFixed(2)} saved`;
        card.querySelector('.goal-amount-to-go').textContent = `$${data.remaining.toFixed(2)} to go`;

        fill.style.width = `${data.percentage}%`;
        fill.classList.remove('on-track','needs-attention','behind-schedule');
        if (data.percentage <= 33)      fill.classList.add('behind-schedule');
        else if (data.percentage <= 66) fill.classList.add('needs-attention');
        else                            fill.classList.add('on-track');

        closeModalBtn.click();
        alert('Contribution added successfully!');
      } else {
        contributionError.textContent = data.error;
      }
    })
    .catch(() => {
      contributionError.textContent = 'An error occurred. Please try again.';
    });
  });

  // — Modal “View Contributions” —
  const listModal           = document.getElementById('contributionsListModal');
  const closeListModalBtn   = document.getElementById('closeContributionsListModal');
  const contributionsList    = document.getElementById('contributionsList');

  document.querySelectorAll('.view-contributions-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.goalId;
      listModal.classList.add('active');
      fetch(`/finances/goals/${id}/contributions/`)
        .then(r => r.json())
        .then(data => {
          if (data.success && data.contributions.length > 0) {
            contributionsList.innerHTML = data.contributions
              .map(c => `
                <div class="flex justify-between items-center border-b pb-2">
                  <span>$${c.amount.toFixed(2)}</span>
                  <span class="text-sm text-gray-500">
                    ${new Date(c.date).toLocaleDateString()}
                  </span>
                </div>
              `).join('');
          } else {
            contributionsList.innerHTML =
              '<p class="text-center py-4 text-gray-500">No contributions yet.</p>';
          }
        })
        .catch(() => {
          contributionsList.innerHTML =
            '<p class="text-center py-4 text-red-500">Error loading contributions.</p>';
        });
    });
  });

  closeListModalBtn.addEventListener('click', () => {
    listModal.classList.remove('active');
  });
  window.addEventListener('click', e => {
    if (e.target === listModal) closeListModalBtn.click();
  });

  // — Helper para CSRF —
  function getCookie(name) {
    const cookies = document.cookie.split(';').map(c => c.trim());
    for (let c of cookies) {
      if (c.startsWith(name + '=')) {
        return decodeURIComponent(c.split('=')[1]);
      }
    }
    return null;
  }
});