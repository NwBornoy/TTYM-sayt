// Footer va bosh menyu (nav) ichidagi ochiladigan menyular
// (Faoliyat, Markaz, Hujjatlar, Matbuot markazi va h.k.)
// Telefon va planshetda strelkaga bosilganda ochiladi/yopiladi.

document.addEventListener('DOMContentLoaded', function () {

    function setupAccordion(selector, breakpoint) {
        var groups = document.querySelectorAll(selector);

        groups.forEach(function (group) {
            var arrow = group.querySelector('.menu-arrow');

            if (!arrow) {
                return;
            }

            arrow.addEventListener('click', function (e) {
                if (window.innerWidth <= breakpoint) {
                    e.preventDefault();
                    e.stopPropagation();

                    var isOpen = group.classList.contains('open');

                    // Boshqa ochiq menyularni yopib qo'yamiz (bittasi ochiq bo'lsin)
                    groups.forEach(function (other) {
                        other.classList.remove('open');
                    });

                    if (!isOpen) {
                        group.classList.add('open');
                    }
                }
            });
        });
    }

    setupAccordion('.footer-dropdown', 900);
    setupAccordion('.nav-dropdown', 900);
});