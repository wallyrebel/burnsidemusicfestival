// Burnside Music Fest — minimal enhancements

(function () {
  // Year stamp
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Mobile menu
  const btn = document.querySelector('.nav__menu');
  const menu = document.getElementById('mobile-menu');
  if (btn && menu) {
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      menu.hidden = open;
    });
    menu.querySelectorAll('a').forEach((a) =>
      a.addEventListener('click', () => {
        btn.setAttribute('aria-expanded', 'false');
        menu.hidden = true;
      })
    );
  }

  // Countdown to 2026-06-06 12:00 Central
  const target = new Date('2026-06-06T12:00:00-05:00').getTime();
  const cd = document.getElementById('countdown');
  if (cd) {
    const dEl = cd.querySelector('[data-days]');
    const hEl = cd.querySelector('[data-hours]');
    const mEl = cd.querySelector('[data-minutes]');
    const sEl = cd.querySelector('[data-seconds]');

    const tick = () => {
      const diff = target - Date.now();
      if (diff <= 0) {
        dEl.textContent = hEl.textContent = mEl.textContent = sEl.textContent = '00';
        cd.setAttribute('aria-label', 'The festival is live!');
        return;
      }
      const d = Math.floor(diff / 86400000);
      const h = Math.floor((diff % 86400000) / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      const s = Math.floor((diff % 60000) / 1000);
      dEl.textContent = String(d).padStart(2, '0');
      hEl.textContent = String(h).padStart(2, '0');
      mEl.textContent = String(m).padStart(2, '0');
      sEl.textContent = String(s).padStart(2, '0');
    };
    tick();
    setInterval(tick, 1000);
  }

  // Reveal on scroll (subtle)
  const io = 'IntersectionObserver' in window
    ? new IntersectionObserver(
        (entries) => {
          entries.forEach((e) => {
            if (e.isIntersecting) {
              e.target.classList.add('is-visible');
              io.unobserve(e.target);
            }
          });
        },
        { threshold: 0.12 }
      )
    : null;

  if (io) {
    document.querySelectorAll('.artist, .tile, .legacy__art, .legacy__copy').forEach((el) => {
      el.classList.add('reveal');
      io.observe(el);
    });
  }
})();
