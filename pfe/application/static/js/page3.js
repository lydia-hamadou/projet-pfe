const chooseFileInput = document.querySelector('.choose-file-button');
const chooseFileLabel = document.querySelector('.choose-file-label');

chooseFileInput.addEventListener('change', () => {
  if (chooseFileInput.files.length > 0) {
    chooseFileLabel.dataset.fileName = chooseFileInput.files[0].name;
    chooseFileLabel.textContent = chooseFileInput.files[0].name;
    chooseFileInput.classList.remove('invalid');
    chooseFileInput.classList.add('valid');
  } else {
    chooseFileLabel.dataset.fileName = '';
    chooseFileLabel.textContent = 'Choisir fichier';
    chooseFileInput.classList.remove('valid');
    chooseFileInput.classList.add('invalid');
  }
});

function testData() {
    // Send a POST request to the test_data view
    $.ajax({
      url: '/test-data/',
      type: 'POST',
      data: $('#file-upload-form').serialize(),
      success: function(response) {
        // Handle successful data test here
        alert('Data test complete.');
      },
      error: function(xhr, status, error) {
        // Handle error here
        alert('Error testing data.');
      }
    });
  }

  function saveData() {
    // Send a POST request to the save_data view
    $.ajax({
      url: '/save-data/',
      type: 'POST',
      data: $('#file-upload-form').serialize(),
      success: function(response) {
        // Handle successful data save here
        alert('Data saved to database.');
      },
      error: function(xhr, status, error) {
        // Handle error here
        alert('Error saving data to database.');
      }
    });
  }