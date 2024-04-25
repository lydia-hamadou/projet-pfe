const btnOK = document.querySelector('.btnOK');
    btnOK.addEventListener('click', function() {
      const formData = new FormData();
      formData.append('file', document.querySelector('input[name="file"]').files[0]);
      fetch('{{ request.build_absolute_uri }}upload_file', {
        method: 'POST',
        body: formData
      })
      .then(response => response.text())
      .then(data => {
        // Handle the response from the server here
        console.log(data);
      })
      .catch(error => {
        // Handle any errors here
        console.error(error);
      });
    });