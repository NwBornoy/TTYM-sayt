// Footer ichidagi ochiladigan menyular (Faoliyat, Markaz, Hujjatlar, Matbuot markazi)
// Telefon va planshetda strelkaga bosilganda ochiladi/yopiladi — xuddi
// kompyuter variantida sichqoncha olib borilganda ochilgani kabi.

document.addEventListener('DOMContentLoaded', function () {
    var dropdowns = document.querySelectorAll('.footer-dropdown');

    dropdowns.forEach(function (dropdown) {
        var title = dropdown.querySelector('.footer-dropdown-title');
        var arrow = dropdown.querySelector('.menu-arrow');

        if (!title || !arrow) {
            return;
        }

        arrow.addEventListener('click', function (e) {
            // Faqat mobil/planshet enida ishlaydi.
            // Kompyuterda (768px dan katta) sichqoncha bilan hover orqali ochiladi.
            if (window.innerWidth <= 900) {
                e.preventDefault();
                e.stopPropagation();

                var isOpen = dropdown.classList.contains('open');

                // Boshqa ochiq menyularni yopib qo'yamiz (bittasi ochiq bo'lsin)
                dropdowns.forEach(function (other) {
                    other.classList.remove('open');
                });

                if (!isOpen) {
                    dropdown.classList.add('open');
                }
            }
        });
    });
});