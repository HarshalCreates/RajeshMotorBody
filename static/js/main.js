// Lightbox Gallery for Model Detail Page
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the custom lightbox
    initLightbox();

    // Initialize image upload preview
    initImageUploadPreview();

    // Initialize AOS animations
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            once: true
        });
    }
});

// Function to preview uploaded images
function initImageUploadPreview() {
    const imageInput = document.querySelector('input[type="file"][name="image"]');
    const previewContainer = document.getElementById('image-preview-container');

    if (!imageInput || !previewContainer) return;

    imageInput.addEventListener('change', function() {
        previewContainer.innerHTML = '';

        if (this.files && this.files[0]) {
            const file = this.files[0];
            const reader = new FileReader();

            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.classList.add('img-fluid', 'rounded', 'mt-2');
                img.style.maxHeight = '200px';

                const caption = document.createElement('p');
                caption.classList.add('text-muted', 'mb-0', 'mt-1');
                caption.textContent = file.name;

                previewContainer.appendChild(img);
                previewContainer.appendChild(caption);
            };

            reader.readAsDataURL(file);
        }
    });
}

function initLightbox() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    const lightbox = document.getElementById('lightbox');

    if (!lightbox || galleryItems.length === 0) return;

    const lightboxImage = lightbox.querySelector('.lightbox-image');
    const lightboxCaption = lightbox.querySelector('.lightbox-caption');
    const lightboxClose = lightbox.querySelector('.lightbox-close');
    const lightboxPrev = lightbox.querySelector('.lightbox-prev');
    const lightboxNext = lightbox.querySelector('.lightbox-next');

    let currentIndex = 0;
    const images = Array.from(document.querySelectorAll('.gallery-img'));

    // Open lightbox when clicking on gallery item
    galleryItems.forEach((item, index) => {
        item.addEventListener('click', function() {
            const img = item.querySelector('img');
            openLightbox(img.src, img.getAttribute('data-caption'), index);
        });
    });

    // Close lightbox
    lightboxClose.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });

    // Navigate through images
    lightboxPrev.addEventListener('click', function() {
        navigate(-1);
    });

    lightboxNext.addEventListener('click', function() {
        navigate(1);
    });

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (lightbox.style.display === 'block') {
            if (e.key === 'Escape') {
                closeLightbox();
            } else if (e.key === 'ArrowLeft') {
                navigate(-1);
            } else if (e.key === 'ArrowRight') {
                navigate(1);
            }
        }
    });

    function openLightbox(src, caption, index) {
        lightboxImage.src = src;
        lightboxCaption.textContent = caption || '';
        currentIndex = index;
        lightbox.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        lightbox.style.display = 'none';
        document.body.style.overflow = '';
    }

    function navigate(direction) {
        currentIndex = (currentIndex + direction + images.length) % images.length;
        const newImg = images[currentIndex];
        lightboxImage.src = newImg.src;
        lightboxCaption.textContent = newImg.getAttribute('data-caption') || '';
    }
}