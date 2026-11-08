/**
 * PRIME CITY PROPERTIES - CORE INTERACTIVITY SCRIPT
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Sticky Navbar shadow update on scroll
  const navbar = document.querySelector('.pc-navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 30) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }

  // 2. Property Detail Gallery Image Switcher
  const mainGalleryImg = document.getElementById('mainGalleryImage');
  const galleryThumbnails = document.querySelectorAll('.pc-gallery-thumb');

  if (mainGalleryImg && galleryThumbnails.length > 0) {
    galleryThumbnails.forEach(thumb => {
      thumb.addEventListener('click', function() {
        galleryThumbnails.forEach(t => t.classList.remove('active'));
        this.classList.add('active');
        const targetSrc = this.getAttribute('data-img-src');
        if (targetSrc) {
          mainGalleryImg.style.opacity = '0.5';
          setTimeout(() => {
            mainGalleryImg.src = targetSrc;
            mainGalleryImg.style.opacity = '1';
          }, 150);
        }
      });
    });
  }

  // 3. Auto-format phone input fields (Nigerian format preference +234...)
  const phoneInputs = document.querySelectorAll('input[name="phone_number"]');
  phoneInputs.forEach(input => {
    input.addEventListener('blur', function() {
      let val = this.value.trim();
      if (val.startsWith('0') && val.length === 11) {
        this.value = '+234 ' + val.substring(1, 4) + ' ' + val.substring(4, 7) + ' ' + val.substring(7);
      }
    });
  });

  // 4. Smooth scroll for internal anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const targetElem = document.querySelector(targetId);
        if (targetElem) {
          e.preventDefault();
          targetElem.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
  });
});
