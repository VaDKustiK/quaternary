function loadIframe(url) {
  document.getElementById('adminIframe').src = url;
}

document.querySelectorAll(".clickable-row").forEach(row => {
    row.addEventListener("click", () => {
      window.location = row.dataset.href;
    });
});

document.getElementById("issueSearch").addEventListener("keyup", function() {
  let filter = this.value.toLowerCase();
  let items = document.querySelectorAll("#issuesList a");
  items.forEach(function(item) {
    let text = item.textContent.toLowerCase();
    item.style.display = text.includes(filter) ? "" : "none";
  });
});