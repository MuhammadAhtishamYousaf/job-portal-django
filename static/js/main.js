document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('[data-nav-toggle]');
  const drawer = document.querySelector('[data-nav-drawer]');
  const authModal = document.querySelector('[data-auth-modal]');
  const authTriggers = document.querySelectorAll('[data-auth-trigger]');
  const authButtons = document.querySelectorAll('[data-auth-select]');
  const authCloseButtons = document.querySelectorAll('[data-auth-close]');

  if (toggle && drawer) {
    toggle.addEventListener('click', () => {
      const open = drawer.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }

  const authRoutes = {
    register: {
      candidate: '/candidate_registration/',
      employer: '/employer_registration/',
    },
    login: {
      candidate: '/candidate_login/',
      employer: '/employer_login/',
    },
  };

  let authMode = 'register';

  const openAuthModal = (mode) => {
    authMode = mode || 'register';
    if (authModal) {
      authModal.hidden = false;
    }
  };

  const closeAuthModal = () => {
    if (authModal) {
      authModal.hidden = true;
    }
  };

  authTriggers.forEach((trigger) => {
    trigger.addEventListener('click', (event) => {
      event.preventDefault();
      openAuthModal(trigger.dataset.authTrigger);
    });
  });

  authButtons.forEach((button) => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      const role = button.dataset.authSelect;
      const target = authRoutes[authMode]?.[role];
      if (target) {
        window.location.href = target;
      }
    });
  });

  authCloseButtons.forEach((button) => {
    button.addEventListener('click', closeAuthModal);
  });

  if (authModal) {
    authModal.addEventListener('click', (event) => {
      if (event.target === authModal) {
        closeAuthModal();
      }
    });
  }
});

