document.addEventListener("DOMContentLoaded", () => {
  // Initialize tooltips if Bootstrap is present
  if (typeof bootstrap !== "undefined") {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll(\x27[data-bs-toggle="tooltip"]\x27));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
  }
});
