document.addEventListener("DOMContentLoaded", function() {
  const availableKeywords = [
    'Web Developer',
    'Cleaner',
    'Designer',
    'Front-End Developer',
    'Python Programmer'
  ];

  const resultsBox = document.querySelector(".result-box");
  const inputBox = document.querySelector(".search-input");

  if (inputBox && resultsBox) {
    inputBox.addEventListener("keyup", function() {
      const input = inputBox.value.trim().toLowerCase();
      const result = input.length
        ? availableKeywords.filter(keyword => keyword.toLowerCase().includes(input))
        : [];

      resultsBox.innerHTML = result.length
        ? `<ul>${result.map(item => `<li>${item}</li>`).join('')}</ul>`
        : '';
    });
  }

  const filterSelects = document.querySelectorAll('.filter-select');
  const chosenCards = document.querySelector('.filter-chosen');

  if (chosenCards && filterSelects.length) {
    filterSelects.forEach(filterSelect => {
      filterSelect.addEventListener('change', () => {
        const selectedText = filterSelect.options[filterSelect.selectedIndex].textContent;

        if (filterSelect.value) {
          const chosenCard = document.createElement('div');
          chosenCard.classList.add('chosen-card');
          chosenCard.textContent = selectedText;

          const closeIcon = document.createElement('i');
          closeIcon.classList.add('fas', 'fa-times-circle');
          chosenCard.appendChild(closeIcon);

          closeIcon.addEventListener('click', () => {
            chosenCard.remove();
            filterSelect.selectedIndex = 0;
          });

          chosenCards.appendChild(chosenCard);
        }
      });
    });
  }
});
