// function showSidebar(){
//     const sidebar = document.querySelector('.menu')
//         sidebar.style.display = 'flex' 
//     }


// function hideSidebar(){
//         const sidebar= document.querySelector('.menu')
//         sidebar.style.display = 'none'
        
//     }


document.addEventListener("DOMContentLoaded", function() {
  let availableKeywords = [
      'Web Developer',
      'Cleaner',
      'Designer',
      'Front-End Developer',
      'Python Programmer'
  ];

  const resultsBox = document.querySelector(".result-box");
  const inputBox = document.querySelector(".search-input");

  inputBox.addEventListener("keyup", function() {
      let result = [];
      let input = inputBox.value.trim().toLowerCase();
      if (input.length) {
          result = availableKeywords.filter(keyword => keyword.toLowerCase().includes(input));
      }
      console.log(result)
      display(result);
  });

  function display(result) {
      const content = result.map(list => "<li>" + list + "</li>").join('');
      resultsBox.innerHTML = "<ul>" + content + "</ul>";
  }
});
    
// Initialize Swiper



// document.addEventListener('DOMContentLoaded', function() {
//     const filterSelects = document.querySelectorAll('.filter-select');
//     const chosenCards = document.querySelector('.filter-chosen');

//     filterSelects.forEach(function(filterSelect) {
//         filterSelect.addEventListener('change', function() {
//             const selectedOption = this.options[this.selectedIndex];
//             const selectedOptionText = selectedOption.textContent;
//             const selectedOptionValue = selectedOption.value;

//             if (selectedOptionValue) {
//                 const chosenCard = document.createElement('div');
//                 chosenCard.classList.add('chosen-card');
//                 chosenCard.textContent = selectedOptionText;

//                 const closeIcon = document.createElement('i');
//                 closeIcon.classList.add('fas', 'fa-times-circle');
//                 chosenCard.appendChild(closeIcon);

//                 closeIcon.addEventListener('click', function() {
//                     chosenCard.remove();
//                     filterSelect.selectedIndex = 0;
//                 });

//                 chosenCards.appendChild(chosenCard);
//             }
//         });
//     });
// });

const filterSelects = document.querySelectorAll('.filter-select');
const chosenCards = document.querySelector('.filter-chosen');

filterSelects.forEach(filterSelect => {
  filterSelect.addEventListener('change', () => {
    const selectedOptions = Array.from(filterSelect.options)
      .filter(option => option.selected && option.value !== "")
      .map(option => option.textContent);

    if (selectedOptions.length > 0) {
      const newChosenCard = document.createElement('div');
      newChosenCard.classList.add('chosen-card');
      newChosenCard.textContent = selectedOptions.join(', ');

      const closeIcon = document.createElement('i');
      closeIcon.classList.add('fas', 'fa-times-circle');
      newChosenCard.appendChild(closeIcon);

      closeIcon.addEventListener('click', () => {
        newChosenCard.remove();
        filterSelect.selectedIndex = 0;  // Reset the select dropdown
      });

      chosenCards.appendChild(newChosenCard);
    }
  });
});

