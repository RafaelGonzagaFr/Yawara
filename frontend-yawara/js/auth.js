const API_URL = 'http://localhost:8000'; // Ajuste conforme necessário

document.getElementById('login-form').addEventListener('submit', async function (e) {
  e.preventDefault();

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  try {
    // Login e obtenção do token
    const resposta = await fetch(`${API_URL}/auth/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    if (!resposta.ok) {
      const errorText = await resposta.json();
      document.getElementById('error-message').textContent = errorText.detail;
      document.getElementById('error-message').style.display = 'block';
      return;
    }

    const data = await resposta.json();
    const token = data.access_token;
    localStorage.setItem('access_token', token);

    // Verifica tipo de usuário
    const tipoResposta = await fetch(`${API_URL}/usuarios/userType`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json'
      }
    });

    if (!tipoResposta.ok) {
      throw new Error("Erro ao verificar tipo de usuário");
    }

    const tipoData = await tipoResposta.json();
    const tipo = tipoData.tipo;

    console.log("Tipo de usuário:", tipo); // Debug

    // Redirecionamento baseado no tipo
    if (tipo === 'cliente') {
      window.location.href = 'home.html';
    } else {
      window.location.href = 'index.html';
    }

  } catch (err) {
    console.error('Erro no login:', err);
    document.getElementById('error-message').textContent = 'Erro inesperado.';
    document.getElementById('error-message').style.display = 'block';
  }
});
