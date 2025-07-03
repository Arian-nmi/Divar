document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('register-form');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      const first_name = document.getElementById('first_name').value;
      const last_name = document.getElementById('last_name').value;

      try {
        const response = await fetch('http://localhost:8000/api/users/signup/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password, first_name, last_name }),
          mode: 'cors'
        });

        const message = document.getElementById('message');
        const data = await response.json();

        if (response.ok) {
          message.textContent = ' ثبت‌نام با موفقیت انجام شد!';
          message.style.color = 'green';
        } else {
          message.textContent = ' خطا: ' + JSON.stringify(data);
          message.style.color = 'red';
        }
      } catch (err) {
        console.error('Fetch error:', err);
        alert(' ارتباط با سرور برقرار نشد.');
      }
    });
  }
});
