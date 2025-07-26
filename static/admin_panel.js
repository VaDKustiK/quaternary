function loadIframe(url) {
  document.getElementById('adminIframe').src = url;
}

document.querySelectorAll(".clickable-row").forEach(row => {
    row.addEventListener("click", () => {
      window.location = row.dataset.href;
    });
});