// Generate bubbles dynamically
const container = document.querySelector(".bubble-container");

for (let i = 0; i < 15; i++) {
  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  
  // Random size
  const size = Math.random() * 12 + 8;
  bubble.style.width = `${size}px`;
  bubble.style.height = `${size}px`;
  
  // Random horizontal position
  bubble.style.left = `${Math.random() * 100}%`;
  
  // Random animation duration
  bubble.style.animationDuration = `${4 + Math.random() * 3}s`;
  
  container.appendChild(bubble);
}


// suji popup

 function togglePopup() {
      const popup = document.getElementById("myPopup");
      popup.style.display = (popup.style.display === "flex") ? "none" : "flex";
    }

    // Close popup if clicked outside
    document.addEventListener("click", function(event) {
      const popup = document.getElementById("myPopup");
      const icon = document.querySelector(".nav-icon");
      if (popup && !popup.contains(event.target) && !icon.contains(event.target)) {
        popup.style.display = "none";
      }
    });