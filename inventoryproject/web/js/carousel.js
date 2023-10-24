document.addEventListener('DOMContentLoaded', () => {
    const elementosCarousel = document.querySelectorAll('.carousel');
    M.Carousel.init(elementosCarousel, {
        duration: 150,
        dist: -120,
        shift: 5,
        padding: 5,
        numVisible: 3,
        indicators: true
    });
});