document.addEventListener("DOMContentLoaded", () => {
  const textarea = document.getElementById("message");
  const counter = document.getElementById("char-count");
  const examples = document.querySelectorAll("[data-example]");
  if (textarea && counter) {
    const update = () => counter.textContent = `${textarea.value.length.toLocaleString()} / 10,000`;
    textarea.addEventListener("input", update);
    update();
  }
  examples.forEach(button => button.addEventListener("click", () => {
    if (textarea) {
      textarea.value = button.dataset.example || "";
      textarea.dispatchEvent(new Event("input"));
      textarea.focus();
    }
  }));
  const results = document.getElementById("results");
  if (results) results.scrollIntoView({behavior:"smooth", block:"start"});
});
