const registerForm = document.getElementById('register-form');

if (registerForm) {
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const user_name = document.getElementById('user_name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const age = document.getElementById('age').value;

    try {
      const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_name, email, password, age })
      });

      const data = await response.json();

      if (response.ok) {
        alert('註冊成功，請重新登入！');
        window.location.href = 'index.html';  // 註冊成功，導回登入頁
      } else {
        alert(data.error || '註冊失敗');
      }
    } catch (error) {
      alert('連線錯誤，請稍後再試');
    }
  });
}
