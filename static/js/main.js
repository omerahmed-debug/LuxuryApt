/* =============================================
   NOOR RESIDENCE — Main JavaScript
   ============================================= */

document.addEventListener("DOMContentLoaded", () => {
  lucide.createIcons();

  initNavbar();
  initMobileMenu();
  initScrollReveal();
  initFloorPlanFilters();
  initGallery();
  initLightbox();
  initTourForm();
  initSmoothScroll();
});

/* ============ NAVBAR ============ */
function initNavbar() {
  const navbar = document.getElementById("navbar");
  const onScroll = () => {
    navbar.classList.toggle("scrolled", window.scrollY > 60);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
}

/* ============ MOBILE MENU ============ */
function initMobileMenu() {
  const btn = document.getElementById("mobile-menu-btn");
  const menu = document.getElementById("mobile-menu");
  if (!btn || !menu) return;

  btn.addEventListener("click", () => {
    menu.classList.toggle("hidden");
    const icon = btn.querySelector("i");
    icon.setAttribute("data-lucide", menu.classList.contains("hidden") ? "menu" : "x");
    lucide.createIcons();
  });

  // Close on link click
  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      menu.classList.add("hidden");
      const icon = btn.querySelector("i");
      icon.setAttribute("data-lucide", "menu");
      lucide.createIcons();
    });
  });
}

/* ============ SCROLL REVEAL ============ */
function initScrollReveal() {
  const targets = document.querySelectorAll(".reveal-up, .reveal-left, .reveal-right");
  if (!targets.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  targets.forEach((el) => {
    // Skip hero content (uses CSS animation)
    if (el.closest(".hero-content")) return;
    observer.observe(el);
  });
}

/* ============ FLOOR PLAN FILTERS ============ */
function initFloorPlanFilters() {
  const filters = document.querySelectorAll(".fp-filter");
  const cards = document.querySelectorAll(".fp-card");
  if (!filters.length) return;

  filters.forEach((btn) => {
    btn.addEventListener("click", () => {
      filters.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      const filter = btn.dataset.filter;

      cards.forEach((card) => {
        const beds = card.dataset.beds;
        const show = filter === "all" || beds === filter;
        card.classList.toggle("hidden", !show);

        if (show) {
          // Re-trigger reveal animation
          card.classList.remove("visible");
          setTimeout(() => card.classList.add("visible"), 50);
        }
      });

      // Fetch from API for dynamic availability
      if (filter !== "all") {
        fetchAvailability(filter);
      }
    });
  });
}

function fetchAvailability(beds) {
  fetch(`/api/availability?beds=${beds}`)
    .then((r) => r.json())
    .then((data) => {
      // Update availability badges dynamically
      data.forEach((unit) => {
        const card = document.querySelector(`.fp-card[data-beds="${unit.beds}"]`);
        if (!card) return;
        const badge = card.querySelector(".fp-availability");
        if (!badge) return;
        if (unit.available === 0) {
          badge.textContent = "Waitlist";
          badge.style.color = "#ef4444";
        } else if (unit.available <= 2) {
          badge.textContent = `${unit.available} Left`;
          badge.style.color = "#f59e0b";
          badge.classList.add("scarce");
        } else {
          badge.textContent = `${unit.available} Available`;
          badge.style.color = "#6db87e";
        }
      });
    })
    .catch(() => {});
}

/* ============ GALLERY SLIDER ============ */
let galIndex = 0;
let galDragStart = null;
let galDragDelta = 0;
let galleryData = [];

function initGallery() {
  const track = document.getElementById("gallery-track");
  const prevBtn = document.getElementById("gal-prev");
  const nextBtn = document.getElementById("gal-next");
  const counter = document.getElementById("gal-counter");
  const slides = document.querySelectorAll(".gallery-slide");

  if (!track || !slides.length) return;

  galleryData = window.GALLERY_DATA || [];
  const total = slides.length;

  function updateGallery(animate = true) {
    const slideWidth = slides[0].offsetWidth + 20; // gap
    if (!animate) track.style.transition = "none";
    else track.style.transition = "";
    track.style.transform = `translateX(-${galIndex * slideWidth}px)`;
    if (counter) counter.textContent = `${galIndex + 1} / ${total}`;
  }

  prevBtn?.addEventListener("click", () => {
    galIndex = (galIndex - 1 + total) % total;
    updateGallery();
  });
  nextBtn?.addEventListener("click", () => {
    galIndex = (galIndex + 1) % total;
    updateGallery();
  });

  // Click to open lightbox
  slides.forEach((slide, i) => {
    slide.addEventListener("click", () => {
      if (Math.abs(galDragDelta) < 5) openLightbox(i);
    });
  });

  // Drag to scroll
  track.addEventListener("mousedown", (e) => {
    galDragStart = e.clientX;
    galDragDelta = 0;
  });
  track.addEventListener("mousemove", (e) => {
    if (galDragStart === null) return;
    galDragDelta = e.clientX - galDragStart;
  });
  track.addEventListener("mouseup", () => {
    if (galDragStart === null) return;
    if (galDragDelta < -60) {
      galIndex = Math.min(galIndex + 1, total - 1);
    } else if (galDragDelta > 60) {
      galIndex = Math.max(galIndex - 1, 0);
    }
    updateGallery();
    galDragStart = null;
  });

  // Touch
  let touchStartX = 0;
  track.addEventListener("touchstart", (e) => { touchStartX = e.touches[0].clientX; }, { passive: true });
  track.addEventListener("touchend", (e) => {
    const delta = e.changedTouches[0].clientX - touchStartX;
    if (delta < -60) galIndex = Math.min(galIndex + 1, total - 1);
    else if (delta > 60) galIndex = Math.max(galIndex - 1, 0);
    updateGallery();
  });

  // Keyboard arrows
  document.addEventListener("keydown", (e) => {
    if (document.getElementById("lightbox")?.classList.contains("hidden")) {
      if (e.key === "ArrowRight") { galIndex = (galIndex + 1) % total; updateGallery(); }
      if (e.key === "ArrowLeft") { galIndex = (galIndex - 1 + total) % total; updateGallery(); }
    }
  });

  window.addEventListener("resize", () => updateGallery(false));
  updateGallery(false);
}

/* ============ LIGHTBOX ============ */
let lbIndex = 0;

function initLightbox() {
  const lb = document.getElementById("lightbox");
  const lbImg = document.getElementById("lb-img");
  const lbCaption = document.getElementById("lb-caption");
  const lbClose = document.getElementById("lb-close");
  const lbPrev = document.getElementById("lb-prev");
  const lbNext = document.getElementById("lb-next");
  if (!lb) return;

  function showLightbox(i) {
    if (!galleryData.length) return;
    lbIndex = (i + galleryData.length) % galleryData.length;
    lbImg.src = galleryData[lbIndex].url;
    lbCaption.textContent = galleryData[lbIndex].caption;
    lb.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  }

  window.openLightbox = showLightbox;

  lbClose?.addEventListener("click", () => {
    lb.classList.add("hidden");
    document.body.style.overflow = "";
  });
  lbPrev?.addEventListener("click", () => showLightbox(lbIndex - 1));
  lbNext?.addEventListener("click", () => showLightbox(lbIndex + 1));

  lb.addEventListener("click", (e) => {
    if (e.target === lb) {
      lb.classList.add("hidden");
      document.body.style.overflow = "";
    }
  });

  document.addEventListener("keydown", (e) => {
    if (!lb.classList.contains("hidden")) {
      if (e.key === "Escape") { lb.classList.add("hidden"); document.body.style.overflow = ""; }
      if (e.key === "ArrowRight") showLightbox(lbIndex + 1);
      if (e.key === "ArrowLeft") showLightbox(lbIndex - 1);
    }
  });
}

/* ============ TOUR FORM ============ */
function initTourForm() {
  const form = document.getElementById("tour-form");
  const success = document.getElementById("form-success");
  const submitBtn = document.getElementById("form-submit");
  const btnText = document.getElementById("btn-text");
  if (!form) return;

  // Set min date to today
  const dateInput = form.querySelector('input[type="date"]');
  if (dateInput) {
    const today = new Date().toISOString().split("T")[0];
    dateInput.min = today;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (submitBtn) {
      submitBtn.disabled = true;
      if (btnText) btnText.textContent = "Sending…";
    }

    const formData = Object.fromEntries(new FormData(form).entries());

    try {
      const res = await fetch("/api/tour", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();

      if (data.success) {
        form.style.display = "none";
        success.classList.remove("hidden");
        const msgEl = document.getElementById("success-msg");
        if (msgEl) msgEl.textContent = data.message;
      } else {
        alert(data.message || "Something went wrong. Please try again.");
        submitBtn.disabled = false;
        if (btnText) btnText.textContent = "Schedule My Tour";
      }
    } catch {
      alert("Network error. Please try again.");
      if (submitBtn) {
        submitBtn.disabled = false;
        if (btnText) btnText.textContent = "Schedule My Tour";
      }
    }
  });
}

/* ============ SMOOTH SCROLL ============ */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", (e) => {
      const target = document.querySelector(anchor.getAttribute("href"));
      if (!target) return;
      e.preventDefault();
      const offset = 80;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: "smooth" });
    });
  });
}
