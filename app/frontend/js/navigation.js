// Navigation active link handler
function setActiveNavLink() {
  // Get current page URL
  const currentPage = window.location.pathname;
  
  // Get all nav links
  const navLinks = document.querySelectorAll('.navbar-links a');
  
  navLinks.forEach(link => {
    link.classList.remove('active');
    
    // Check if link matches current page
    if (currentPage === '/' && link.getAttribute('href') === '/' ) {
      link.classList.add('active');
    } else if (currentPage.includes('index.html') && link.getAttribute('href') === '/index.html') {
      link.classList.add('active');
    } else if (currentPage.includes('analyzer') && link.getAttribute('href') === '/analyzer.html') {
      link.classList.add('active');
    }
  });
}

// Run when page loads
document.addEventListener('DOMContentLoaded', setActiveNavLink);
window.addEventListener('pageshow', setActiveNavLink);
