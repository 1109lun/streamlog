document.addEventListener("DOMContentLoaded", () => {
    const username = localStorage.getItem("user_name");
    console.log("登入者是：", username);
  
    const loginSection = document.getElementById('login-section');
    const navbarSection = document.getElementById('navbar-section');
    const contentSection = document.getElementById('content-section');
    const currentUser = document.getElementById('current-user');
  
    if (username) {
      loginSection.classList.add('d-none');
      navbarSection.classList.remove('d-none');
      contentSection.classList.remove('d-none');
      currentUser.textContent = `您好，${username}`;
    } else {
      loginSection.classList.remove('d-none');
      navbarSection.classList.add('d-none');
      contentSection.classList.add('d-none');
    }
  
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
  
        try {
          const response = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
          });
  
          const data = await response.json();
  
          if (response.ok) {
            localStorage.setItem('user_name', data.user_name);
            window.location.reload();
          } else {
            alert(data.error || '登入失敗');
          }
        } catch (error) {
          alert('連線錯誤，請稍後再試');
        }
      });
    }
  
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
      logoutButton.addEventListener('click', () => {
        localStorage.removeItem('username');
        window.location.reload();
      });
    }
  });
  