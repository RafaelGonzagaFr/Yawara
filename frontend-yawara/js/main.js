const API_URL = 'http://localhost:8000';
const token = localStorage.getItem('access_token');
if (!token) window.location.href = 'login.html';


const userType = fetch(`${API_URL}/usuarios/userType`, {
  method: 'GET',
  headers: { Authorization: `Bearer ${token}` }
});
if (userType == "cliente") {
  window.location.href = 'home.html';
}

function logout() {
  localStorage.removeItem('access_token');
  window.location.href = 'login.html';
}