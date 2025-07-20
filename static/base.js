// login sidebar
const loginBtn = document.getElementById('loginBtn');
const loginSidebar = document.getElementById('loginSidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');
const closeSidebar = document.getElementById('closeSidebar');

loginBtn.addEventListener('click', () => {
  loginSidebar.classList.add('show');
  sidebarOverlay.classList.add('show');
});

closeSidebar.addEventListener('click', () => {
  loginSidebar.classList.remove('show');
  sidebarOverlay.classList.remove('show');
});

sidebarOverlay.addEventListener('click', () => {
  loginSidebar.classList.remove('show');
  sidebarOverlay.classList.remove('show');
});

// auto closing flash alerts after 5 seconds
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    });
  }, 5000);
});