document.querySelector('.menu-btn')?.addEventListener('click',()=>document.querySelector('nav').classList.toggle('open'));

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const revealTargets = document.querySelectorAll('.features article, .split > *, .form-section, .factor-note, .submit, .result-cards article, .chart-card, .insight, .dashboard-stats article, .table-wrap, .compare, .about-grid article, .academic');

if (!reduceMotion && revealTargets.length) {
  document.documentElement.classList.add('js-active');
  revealTargets.forEach(element => element.classList.add('reveal'));
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  revealTargets.forEach(element => observer.observe(element));
}

const heroArt = document.querySelector('.hero-art');
if (heroArt && !reduceMotion) {
  let queued = false;
  window.addEventListener('scroll', () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      heroArt.style.setProperty('--hero-shift', `${Math.min(window.scrollY * -0.06, 18)}px`);
      queued = false;
    });
  }, { passive: true });
}
