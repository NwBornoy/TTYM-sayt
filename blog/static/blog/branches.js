/* =========================================================
   QASHQADARYO FILIALLARI
========================================================= */

const branches = {

    "qarshi-shahar": {
        name: "Qarshi shahar filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Qarshi shahri",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/qarshi-shahar.jpg"
    },

    "qarshi-tumani": {
        name: "Qarshi tumani filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Qarshi tumani",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/qarshi-tumani.jpg"
    },

    "shahrisabz-shahar": {
        name: "Shahrisabz shahar filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Shahrisabz shahri",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/shahrisabz-shahar.jpg"
    },

    "shahrisabz-tumani": {
        name: "Shahrisabz tumani filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Shahrisabz tumani",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/shahrisabz-tumani.jpg"
    },

    "kitob": {
        name: "Kitob tumani filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Kitob tumani",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/kitob.jpg"
    },

    "chiroqchi": {
        name: "Chiroqchi tumani filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Chiroqchi tumani",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/chiroqchi.jpg"
    },

    "yakkabog": {
        name: "Yakkabog‘ tumani filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Yakkabog‘ tumani",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/yakkabog.jpg"
    },

    "qamashi": {
        name: "Qamashi tumani filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Qamashi tumani",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/qamashi.jpg"
    },

    "guzor": {
        name: "G‘uzor tumani filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "G‘uzor tumani",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/guzor.jpg"
    },

    "dehqonobod": {
        name: "Dehqonobod tumani filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Dehqonobod tumani",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/dehqonobod.jpg"
    },

    "nishon": {
        name: "Nishon tumani filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Nishon tumani",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/nishon.jpg"
    },

    "kasbi": {
        name: "Kasbi tumani filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Kasbi tumani",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/kasbi.jpg"
    },

    "koson": {
        name: "Koson tumani filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Koson tumani",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/koson.jpg"
    },

    "muborak": {
        name: "Muborak tumani filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Muborak tumani",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/muborak.jpg"
    },

    "mirishkor": {
        name: "Mirishkor tumani filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Mirishkor tumani",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/mirishkor.jpg"
    },

    "kokdala": {
        name: "Ko‘kdala tumani filiali",
        director: "Rahbar: __________",
        phone: "Telefon: __________",
        address: "Ko‘kdala tumani",
        email: "example@gmail.com",
        telegram: "https://t.me/example",
        instagram: "https://instagram.com/example",
        image: "/static/blog/images/directors/kokdala.jpg"
    }

};


/* =========================================================
   GLOBAL O'ZGARUVCHILAR
========================================================= */

let branchIds = Object.keys(branches);

let currentBranchIndex = -1;

let mapTooltip = null;


/* =========================================================
   XARITA HUDUDINI TOZALASH
========================================================= */

function clearMapHighlight() {

    const mapContainer =
        document.getElementById("qashqadaryo-map");

    if (!mapContainer) {
        return;
    }

    const allAreas =
        mapContainer.querySelectorAll("svg [id]");

    allAreas.forEach(function (area) {

        if (!branches[area.id]) {
            return;
        }

        area.classList.remove("branch-active-area");

        area.style.fill = "";
        area.style.stroke = "";
        area.style.strokeWidth = "";
        area.style.strokeOpacity = "";
        area.style.opacity = "1";

    });

}


/* =========================================================
   TANLANGAN HUDUDNI YORITISH
========================================================= */

function highlightBranchArea(branchId) {

    const mapContainer =
        document.getElementById("qashqadaryo-map");

    if (!mapContainer) {
        return;
    }


    /* Avval hamma hududni tozalaymiz */

    clearMapHighlight();


    /* Tanlangan hududni topamiz */

    const activeArea =
        mapContainer.querySelector(
            `svg [id="${branchId}"]`
        );

    if (!activeArea) {
        return;
    }


    /* =====================================================
       TANLANGAN HUDUD RANGI
    ===================================================== */

    activeArea.style.fill = "#8FE388";

    activeArea.style.stroke = "#16803A";

    activeArea.style.strokeWidth = "2.5";

    activeArea.style.strokeOpacity = "1";

    activeArea.style.opacity = "1";


    activeArea.classList.add(
        "branch-active-area"
    );

}


/* =========================================================
   TOOLTIP YARATISH
========================================================= */

function createMapTooltip() {

    if (mapTooltip) {
        return;
    }


    mapTooltip =
        document.createElement("div");

    mapTooltip.className =
        "map-tooltip";


    document.body.appendChild(
        mapTooltip
    );

}


/* =========================================================
   TOOLTIPNI KO'RSATISH
========================================================= */

function showMapTooltip(
    branchName,
    event
) {

    if (!mapTooltip) {
        return;
    }


    mapTooltip.textContent =
        branchName;


    mapTooltip.classList.add(
        "show"
    );


    moveMapTooltip(event);

}


/* =========================================================
   TOOLTIPNI HARAKATLANTIRISH
========================================================= */

function moveMapTooltip(event) {

    if (!mapTooltip) {
        return;
    }


    const offsetX = 16;

    const offsetY = -42;


    let left =
        event.clientX + offsetX;

    let top =
        event.clientY + offsetY;


    /*
     * Ekranning o'ng tomonidan
     * chiqib ketmasin.
     */

    const tooltipWidth =
        mapTooltip.offsetWidth;

    const tooltipHeight =
        mapTooltip.offsetHeight;


    if (
        left + tooltipWidth >
        window.innerWidth - 10
    ) {

        left =
            event.clientX -
            tooltipWidth -
            16;

    }


    /*
     * Ekranning yuqorisidan
     * chiqib ketmasin.
     */

    if (top < 10) {

        top =
            event.clientY + 20;

    }


    mapTooltip.style.left =
        left + "px";

    mapTooltip.style.top =
        top + "px";

}


/* =========================================================
   TOOLTIPNI YOPISH
========================================================= */

function hideMapTooltip() {

    if (!mapTooltip) {
        return;
    }

    mapTooltip.classList.remove(
        "show"
    );

}


/* =========================================================
   FILIAL KARTASINI CHIQARISH
========================================================= */

function showBranch(branchId) {

    const branchInfo =
        document.getElementById(
            "branch-info"
        );


    if (!branchInfo) {
        return;
    }


    const branch =
        branches[branchId];


    if (!branch) {
        return;
    }


    /*
     * Joriy filial indeksini saqlaymiz.
     */

    currentBranchIndex =
        branchIds.indexOf(
            branchId
        );


    /*
     * Xaritadagi hududni yoritamiz.
     */

    highlightBranchArea(
        branchId
    );


    /*
     * Tooltipni yopamiz.
     */

    hideMapTooltip();


    /* =====================================================
       RAHBAR KARTASI
    ===================================================== */

    branchInfo.innerHTML = `

        <!-- RAHBAR RASMI -->

        <div class="branch-info-icon">

            <img
                src="${branch.image}"
                alt="${branch.name}"

                onerror="
                    this.style.display='none';
                    this.parentElement.classList.add('no-image');
                "
            >

            <div class="fallback-icon">
                🚑
            </div>

        </div>


        <!-- FILIAL NOMI -->

        <h3 class="branch-title">
            ${branch.name}
        </h3>


        <!-- RAHBAR -->

        <div class="branch-info-line">

            <span>
                👨‍⚕️
            </span>

            <span>
                ${branch.director}
            </span>

        </div>


        <!-- TELEFON -->

        <div class="branch-info-line">

            <span>
                📞
            </span>

            <span>
                ${branch.phone}
            </span>

        </div>


        <!-- MANZIL -->

        <div class="branch-info-line">

            <span>
                📍
            </span>

            <span>
                ${branch.address}
            </span>

        </div>


        <!-- EMAIL -->

        <div
            class="branch-info-line"
            id="branch-email"
        >

            <span>
                📧
            </span>

            <span>
                Email:
            </span>

            <a
                href="mailto:${branch.email}"
            >
                ${branch.email}
            </a>

        </div>


        <!-- IJTIMOIY TARMOQLAR -->

        <div class="branch-socials">


            <!-- GMAIL -->

            <a
                href="mailto:${branch.email}"
                class="branch-social"
                title="Gmail"
            >

                <svg
                    viewBox="0 0 256 193"
                    aria-hidden="true"
                >

                    <path
                        fill="#4285F4"
                        d="M58.182 192.05V93.14L27.507 65.077 0 49.504v125.091c0 9.658 7.825 17.455 17.455 17.455h40.727Z"
                    />

                    <path
                        fill="#34A853"
                        d="M197.818 192.05h40.727c9.659 0 17.455-7.826 17.455-17.455V49.505l-31.156 17.837-27.026 25.798v98.91Z"
                    />

                    <path
                        fill="#EA4335"
                        d="m58.182 93.14-4.174-38.647 4.174-36.989L128 69.868l69.818-52.364 4.67 34.992-4.67 40.644L128 145.504z"
                    />

                    <path
                        fill="#FBBC04"
                        d="M197.818 17.504V93.14L256 49.504V26.231c0-21.585-24.64-33.89-41.89-20.945l-16.292 12.218Z"
                    />

                    <path
                        fill="#C5221F"
                        d="m0 49.504 26.759 20.07L58.182 93.14V17.504L41.89 5.286C24.61-7.66 0 4.646 0 26.23v23.273Z"
                    />

                </svg>

            </a>


            <!-- TELEGRAM -->

            <a
                href="${branch.telegram}"
                target="_blank"
                rel="noopener noreferrer"
                class="branch-social"
                title="Telegram"
            >

                <svg
                    viewBox="0 0 240 240"
                    aria-hidden="true"
                >

                    <circle
                        cx="120"
                        cy="120"
                        r="120"
                        fill="#229ED9"
                    />

                    <path
                        fill="#ffffff"
                        d="M184.7 70.3 159.4 190c-1.9 8.5-6.9 10.6-14 6.6l-38.6-28.5-18.6 17.9c-2.1 2.1-3.8 3.8-7.8 3.8l2.8-39.3 71.5-64.6c3.1-2.8-.7-4.4-4.8-1.6L61.5 141.8 24.2 130.1c-8.1-2.5-8.3-8.1 1.7-12L171.7 60.6c6.8-2.5 12.8 1.6 13 9.7Z"
                    />

                </svg>

            </a>


            <!-- INSTAGRAM -->

            <a
                href="${branch.instagram}"
                target="_blank"
                rel="noopener noreferrer"
                class="branch-social"
                title="Instagram"
            >

                <svg
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                >

                    <path
                        fill="#E4405F"
                        d="M12 0C8.74 0 8.333.015 7.053.072 5.775.132 4.905.333 4.14.63c-.789.306-1.459.717-2.126 1.384S.935 3.35.63 4.14C.333 4.905.131 5.775.072 7.053.012 8.333 0 8.74 0 12s.015 3.667.072 4.947c.06 1.277.261 2.148.558 2.913.306.788.717 1.459 1.384 2.126.667.666 1.336 1.079 2.126 1.384.766.296 1.636.499 2.913.558C8.333 23.988 8.74 24 12 24s3.667-.015 4.947-.072c1.277-.059 2.148-.262 2.913-.558.788-.306 1.459-.718 2.126-1.384.666-.667 1.079-1.335 1.384-2.126.296-.765.499-1.636.558-2.913.06-1.28.072-1.687.072-4.947s-.015-3.667-.072-4.947c-.059-1.277-.262-2.149-.558-2.913-.306-.789-.718-1.459-1.384-2.126C21.319 1.347 20.651.935 19.86.63c-.765-.297-1.636-.499-2.913-.558C15.667.012 15.26 0 12 0zm0 2.16c3.203 0 3.585.016 4.85.071 1.17.055 1.805.249 2.227.415.562.217.96.477 1.382.896.419.42.679.819.896 1.381.164.422.36 1.057.413 2.227.057 1.266.07 1.646.07 4.85s-.015 3.585-.074 4.85c-.061 1.17-.256 1.805-.421 2.227-.224.562-.479.96-.899 1.382-.419.419-.824.679-1.38.896-.42.164-1.065.36-2.235.413-1.274.057-1.649.07-4.859.07-3.211 0-3.586-.015-4.859-.074-1.171-.061-1.816-.256-2.236-.421-.569-.224-.96-.479-1.379-.899-.421-.419-.69-.824-.9-1.38-.165-.42-.359-1.065-.42-2.235-.045-1.26-.061-1.649-.061-4.844 0-3.196.016-3.586.061-4.861.061-1.17.255-1.814.42-2.234.21-.57.479-.96.9-1.381.419-.419.81-.689 1.379-.898.42-.166 1.051-.361 2.221-.421 1.275-.045 1.65-.06 4.859-.06l.045.03zM12 5.838c-3.405 0-6.162 2.76-6.162 6.162 0 3.405 2.76 6.162 6.162 6.162 3.405 0 6.162-2.76 6.162-6.162 0-3.405-2.76-6.162-6.162-6.162zm0 10.162a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm7.846-10.405a1.44 1.44 0 1 1-2.88 0 1.44 1.44 0 0 1 2.88 0z"
                    />

                </svg>

            </a>

        </div>


        <!-- OLDINGI / KEYINGI TUGMALAR -->

        <div class="branch-navigation">

            <button
                type="button"
                class="branch-nav-btn branch-prev"
                id="branch-prev"
                title="Oldingi filial"
            >
                ‹
            </button>


            <button
                type="button"
                class="branch-nav-btn branch-next"
                id="branch-next"
                title="Keyingi filial"
            >
                ›
            </button>

        </div>


        <!-- YORDAMCHI YOZUV -->

        <p class="branch-info-help">
            Xarita ustidagi hududlardan birini bosing.
        </p>

    `;

}


/* =========================================================
   OLDINGI FILIAL
========================================================= */

function previousBranch() {

    if (branchIds.length === 0) {
        return;
    }


    if (currentBranchIndex === -1) {

        currentBranchIndex =
            branchIds.length - 1;

    } else {

        currentBranchIndex--;

        if (currentBranchIndex < 0) {

            currentBranchIndex =
                branchIds.length - 1;

        }

    }


    showBranch(
        branchIds[currentBranchIndex]
    );

}


/* =========================================================
   KEYINGI FILIAL
========================================================= */

function nextBranch() {

    if (branchIds.length === 0) {
        return;
    }


    if (currentBranchIndex === -1) {

        currentBranchIndex = 0;

    } else {

        currentBranchIndex++;

        if (
            currentBranchIndex >=
            branchIds.length
        ) {

            currentBranchIndex = 0;

        }

    }


    showBranch(
        branchIds[currentBranchIndex]
    );

}


/* =========================================================
   DOM YUKLANGANDA
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const mapContainer =
            document.getElementById(
                "qashqadaryo-map"
            );


        const branchInfo =
            document.getElementById(
                "branch-info"
            );


        if (!mapContainer || !branchInfo) {

            console.error(
                "qashqadaryo-map yoki branch-info topilmadi."
            );

            return;

        }


        /*
         * Tooltipni faqat DOM tayyor
         * bo'lgandan keyin yaratamiz.
         */

        createMapTooltip();


        /* =================================================
           SVG XARITANI YUKLASH
        ================================================= */

        fetch(
            "/static/blog/qashqadaryo.svg"
        )

        .then(function (response) {

            if (!response.ok) {

                throw new Error(
                    "SVG yuklanmadi: " +
                    response.status
                );

            }

            return response.text();

        })


        .then(function (svgText) {

            mapContainer.innerHTML =
                svgText;


            /* =================================================
               SVG HUDUDLARI
            ================================================= */

            const areas =
                mapContainer.querySelectorAll(
                    "svg [id]"
                );


            /*
             * Faqat branches ichidagi
             * hududlarni olamiz.
             */

            branchIds =
                Array.from(areas)

                    .map(
                        function (area) {
                            return area.id;
                        }
                    )

                    .filter(
                        function (id) {
                            return branches[id];
                        }
                    );


            /* =================================================
               HUDUDLARGA EVENT BERISH
            ================================================= */

            areas.forEach(
                function (area) {

                    const branch =
                        branches[area.id];


                    /*
                     * Agar bu hudud branches
                     * ichida bo'lmasa, o'tkazib yuboramiz.
                     */

                    if (!branch) {
                        return;
                    }


                    /* =========================================
                       SICHQONCHA HUDUD USTIGA KELGANDA
                    ========================================= */

                    area.addEventListener(
                        "mouseenter",
                        function (event) {

                            this.style.cursor =
                                "pointer";


                            /*
                             * Tanlangan hudud bo'lmasa,
                             * hover paytida och yashil qilamiz.
                             */

                            if (
                                !this.classList.contains(
                                    "branch-active-area"
                                )
                            ) {

                                this.style.fill =
                                    "#B8E6B5";

                                this.style.stroke =
                                    "#16803A";

                                this.style.strokeWidth =
                                    "2";

                                this.style.strokeOpacity =
                                    "1";

                                this.style.opacity =
                                    "1";

                            }


                            /*
                             * Tooltip.
                             */

                            showMapTooltip(
                                branch.name,
                                event
                            );

                        }
                    );


                    /* =========================================
                       SICHQONCHA HUDUD ICHIDA YURGANDA
                    ========================================= */

                    area.addEventListener(
                        "mousemove",
                        function (event) {

                            moveMapTooltip(
                                event
                            );

                        }
                    );


                    /* =========================================
                       SICHQONCHA HUDUDDAN CHIQGANDA
                    ========================================= */

                    area.addEventListener(
                        "mouseleave",
                        function () {

                            /*
                             * Agar hudud tanlanmagan bo'lsa,
                             * oddiy holatga qaytaramiz.
                             */

                            if (
                                !this.classList.contains(
                                    "branch-active-area"
                                )
                            ) {

                                this.style.fill = "";

                                this.style.stroke = "";

                                this.style.strokeWidth = "";

                                this.style.strokeOpacity = "";

                                this.style.opacity =
                                    "1";

                            }


                            hideMapTooltip();

                        }
                    );


                    /* =========================================
                       HUDUD BOSILGANDA
                    ========================================= */

                    area.addEventListener(
                        "click",
                        function () {

                            showBranch(
                                this.id
                            );

                        }
                    );

                }
            );


            /* =================================================
               OLDINGI / KEYINGI TUGMALAR
            ================================================= */

            branchInfo.addEventListener(
                "click",
                function (event) {

                    const button =
                        event.target.closest(
                            ".branch-nav-btn"
                        );


                    if (!button) {
                        return;
                    }


                    /* OLDINGI */

                    if (
                        button.id ===
                        "branch-prev"
                    ) {

                        previousBranch();

                    }


                    /* KEYINGI */

                    if (
                        button.id ===
                        "branch-next"
                    ) {

                        nextBranch();

                    }

                }
            );

        })


        .catch(
            function (error) {

                console.error(
                    "Qashqadaryo SVG yuklanmadi:",
                    error
                );

            }
        );

    }
);
/* ==========================================================
   XATO HAQIDA XABAR BERISH — Ctrl+Enter
   ========================================================== */

   (function () {
    "use strict";

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function showToast(message, isError) {
        const toast = document.createElement("div");
        toast.textContent = message;
        toast.style.cssText = [
            "position:fixed",
            "left:50%",
            "bottom:40px",
            "transform:translateX(-50%)",
            "background:#d71920",
            "color:#ffffff",
            "padding:18px 34px",
            "border-radius:10px",
            "font-size:19px",
            "font-weight:700",
            "max-width:90%",
            "text-align:center",
            "z-index:999999",
            "box-shadow:0 10px 30px rgba(0,0,0,0.35)",
            "opacity:0",
            "transition:opacity 0.25s ease"
        ].join(";");

        document.body.appendChild(toast);
        requestAnimationFrame(function () {
            toast.style.opacity = "1";
        });

        setTimeout(function () {
            toast.style.opacity = "0";
            setTimeout(function () {
                toast.remove();
            }, 300);
        }, 2500);
    }

    function sendReport(selectedText) {
        const csrftoken = getCookie("csrftoken");

        fetch("/report-error/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                selected_text: selectedText,
                page_url: window.location.href
            })
        })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error("Server xatosi");
                }
                return response.json();
            })
            .then(function (data) {
                if (data.ok) {
                    showToast("Xabaringiz uchun rahmat! Ma'muriyatga yuborildi.", false);
                    window.getSelection().removeAllRanges();
                } else {
                    showToast("Xabar yuborilmadi, qayta urinib ko'ring.", true);
                }
            })
            .catch(function () {
                showToast("Xabar yuborilmadi, internetni tekshiring.", true);
            });
    }

    document.addEventListener("keydown", function (event) {
        const isCtrlEnter = (event.ctrlKey || event.metaKey) && event.key === "Enter";

        if (!isCtrlEnter) {
            return;
        }

        const selection = window.getSelection();
        const selectedText = selection ? selection.toString().trim() : "";

        if (!selectedText) {
            return;
        }

        event.preventDefault();
        sendReport(selectedText);
    });
})();