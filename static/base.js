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