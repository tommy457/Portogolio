function readURL(input) {
    if (input.files && input.files[0]) {
       var reader = new FileReader();
       reader.onload = function (e) {
          // Get the parent div of the input field
          var parentDiv = input.closest('.project-image');

          // Get the corresponding output element within the same parent div
          var outputElement = parentDiv.querySelector('img');

          // Set the src attribute of the output element
          outputElement.setAttribute("src", e.target.result);
       };

       reader.readAsDataURL(input.files[0]);
    }
 }
 document.addEventListener('DOMContentLoaded', function () {
    var skillsList = document.getElementById('skillsList');
    var dropdownButton = document.getElementById('techSkillsDropdown');
    var dropdownMenu = document.getElementById('techSkillsDropdownMenu');

    // Function to update the skills list
    function updateSkillsList() {
       var selectedSkills = Array.from(dropdownMenu.querySelectorAll('.skillCheckbox:checked'))
          .map(function (checkbox) {
             return checkbox.value;
          });

       // Remove skills not selected anymore
       Array.from(skillsList.querySelectorAll('li')).forEach(function (li) {
          var skill = li.textContent.trim();
          if (!selectedSkills.includes(skill)) {
             li.remove();
          }
       });

       // Append selected skills to the original list
       selectedSkills.forEach(function (skill) {
          if (!skillsListContains(skill)) {
             var li = document.createElement('li');
             li.textContent = skill;
             skillsList.appendChild(li);
          }
       });
    }

    // Function to check if a skill is in the original list
    function skillsListContains(skill) {
       var existingSkills = Array.from(skillsList.querySelectorAll('li'))
          .map(function (li) {
             return li.textContent.trim();
          });

       return existingSkills.includes(skill);
    }

    // Add change event listener to checkboxes for handling selection
    var skillCheckboxes = dropdownMenu.querySelectorAll('.skillCheckbox');
    skillCheckboxes.forEach(function (checkbox) {
       checkbox.addEventListener('change', function () {
          updateSkillsList();
       });

       // Mark checkboxes as checked if the skill is already in the original list
       if (skillsListContains(checkbox.value)) {
          checkbox.checked = true;
       }
    });

    // Add click event listener to dropdown items for handling selection
    var dropdownItems = dropdownMenu.querySelectorAll('.dropdown-item');
    dropdownItems.forEach(function (item) {
       item.addEventListener('click', function () {
          var checkbox = item.querySelector('.skillCheckbox');
          checkbox.checked = !checkbox.checked;
          updateSkillsList();
       });
    });

    // Add click event listener to dropdown button
    dropdownButton.addEventListener('click', function (event) {
       event.stopPropagation();
       event.preventDefault();
       dropdownMenu.style.display = 'block';
    });

    // Add click event listener to document to close dropdown if clicked outside
    document.addEventListener('click', function (event) {
       if (!event.target.matches('.dropdown-toggle') && !event.target.closest('.dropdown-menu')) {
          dropdownMenu.style.display = 'none';
       }
    });
 });
 document.addEventListener("DOMContentLoaded", function () {
    let slideshows = document.getElementsByClassName("slideshow-container");

    for (let i = 0; i < slideshows.length; i++) {
       createSlideshow(i);
    }

    function createSlideshow(index) {
       let slideIndex = 0;
       showSlides(index, slideIndex);

       function plusSlides(n) {
          showSlides(index, slideIndex + n);
       }

       function showSlides(index, n) {
          let slides = slideshows[index].getElementsByClassName('mySlides');

          for (let i = 0; i < slides.length; i++) {
             slides[i].style.display = 'none';
          }

          slideIndex = (n + slides.length) % slides.length;
          slides[slideIndex].style.display = 'block';
       }

       // Set up event listeners for next and previous buttons
       let nextBtn = slideshows[index].getElementsByClassName("next")[0];
       let prevBtn = slideshows[index].getElementsByClassName("prev")[0];

       nextBtn.addEventListener("click", function () {
          plusSlides(1);
       });

       prevBtn.addEventListener("click", function () {
          plusSlides(-1);
       });
    }
 });
 if (window.history.replaceState) {
   // Modify the current URL to remove query parameters
   var newurl = window.location.protocol + "//" + window.location.host + window.location.pathname;
   window.history.replaceState({path:newurl}, '', newurl);
}