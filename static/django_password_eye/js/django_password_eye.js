var djangoPasswordEyeElements = djangoPasswordEyeElements || undefined;
if(typeof djangoPasswordEyeElements === 'undefined') {
  djangoPasswordEyeElements = [];

  function djangoPasswordEyeClickHandler(event) {
    event.preventDefault();
    for (let i = 0; i < djangoPasswordEyeElements.length; i++) {
      const iElement = djangoPasswordEyeElements[i].querySelector('i');
      const input = djangoPasswordEyeElements[i].querySelector('input');
      if (input.type === 'text') {
        input.type = 'password';
        iElement.classList.add('fa-eye-slash');
        iElement.classList.remove('fa-eye');
      } else if (input.type === 'password') {
        input.type = 'text';
        iElement.classList.remove('fa-eye-slash');
        iElement.classList.add('fa-eye');
      }
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    djangoPasswordEyeElements = document.getElementsByClassName('django_password_eye');
    for (let i = 0; i < djangoPasswordEyeElements.length; i++) {
      djangoPasswordEyeElements[i]
          .querySelector('.input-group-addon')
          .addEventListener('click', djangoPasswordEyeClickHandler);
    }
  });
}