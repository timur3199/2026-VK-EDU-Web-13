'use strict';

document.addEventListener('DOMContentLoaded', () => {

  /* ════════════════════════════════════════
     1. Like / Dislike widgets
     ════════════════════════════════════════ */
  document.querySelectorAll('.like-widget').forEach(widget => {
    const likeBtn    = widget.querySelector('[data-action="like"]');
    const dislikeBtn = widget.querySelector('[data-action="dislike"]');
    const countEl    = widget.querySelector('.like-count');
    if (!likeBtn || !countEl) return;

    let count = parseInt(countEl.textContent, 10);
    let state = widget.dataset.state || 'none';

    function render() {
      likeBtn.classList.toggle('liked', state === 'liked');
      if (dislikeBtn)
        dislikeBtn.classList.toggle('disliked', state === 'disliked');
      countEl.textContent = count;
    }

    likeBtn.addEventListener('click', () => {
      if (state === 'liked')    { count--; state = 'none'; }
      else { if (state === 'disliked') count++; count++; state = 'liked'; }
      render();
    });

    if (dislikeBtn) {
      dislikeBtn.addEventListener('click', () => {
        if (state === 'disliked') { count++; state = 'none'; }
        else { if (state === 'liked') count--; count--; state = 'disliked'; }
        render();
      });
    }
  });

  /* ════════════════════════════════════════
     2. Correct answer toggle
     ════════════════════════════════════════ */
  document.querySelectorAll('.correct-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const wasActive = btn.classList.contains('active');
      document.querySelectorAll('.correct-btn').forEach(b => {
        b.classList.remove('active');
        b.closest('.answer-card')?.classList.remove('correct');
        b.innerHTML = iconCheck(false) + ' Правильный';
      });
      if (!wasActive) {
        btn.classList.add('active');
        btn.closest('.answer-card')?.classList.add('correct');
        btn.innerHTML = iconCheck(true) + ' Правильный \u2713';
      }
    });
  });

  function iconCheck(filled) {
    if (filled) return '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M20.707 5.293a1 1 0 010 1.414l-11 11a1 1 0 01-1.414 0l-5-5a1 1 0 011.414-1.414L9 15.586l10.293-10.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>';
    return '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>';
  }

  /* ════════════════════════════════════════
     3. Avatar preview
     ════════════════════════════════════════ */
  const avatarInput   = document.getElementById('avatarInput');
  const avatarPreview = document.getElementById('avatarPreview');
  if (avatarInput && avatarPreview) {
    avatarInput.addEventListener('change', e => {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = ev => {
        avatarPreview.src = ev.target.result;
        avatarPreview.style.display = 'block';
        const ph = document.querySelector('.avatar-preview-placeholder');
        if (ph) ph.style.display = 'none';
      };
      reader.readAsDataURL(file);
    });
  }

  /* ════════════════════════════════════════
     4. Tags input (ask page)
     ════════════════════════════════════════ */
  const tagsInput = document.getElementById('tagsInput');
  if (tagsInput) {
    tagsInput.addEventListener('keydown', e => {
      if (e.key !== 'Enter' && e.key !== ',') return;
      e.preventDefault();
      const val = tagsInput.value.trim().replace(/,+$/, '');
      if (!val) return;
      const container = document.getElementById('tagsList');
      if (!container) return;
      if (container.querySelectorAll('.tag-item').length >= 5) {
        showFieldError(tagsInput, 'Максимум 5 тегов');
        return;
      }
      clearFieldError(tagsInput);
      const tag = document.createElement('span');
      tag.className = 'tag-item badge me-1 mb-1';
      tag.style.cssText = 'background:var(--bg-body);border:1.5px solid var(--border);color:var(--text-primary);font-weight:500;font-size:.8rem;padding:4px 10px;border-radius:20px;cursor:pointer;';
      tag.textContent = val;
      tag.title = 'Нажмите для удаления';
      tag.addEventListener('click', () => tag.remove());
      container.appendChild(tag);
      tagsInput.value = '';
    });
  }

  /* ════════════════════════════════════════
     5. Form validation
     ════════════════════════════════════════ */

  function showFieldError(input, message) {
    input.classList.add('is-invalid');
    input.classList.remove('is-valid');
    const fb = input.parentElement.querySelector('.invalid-feedback');
    if (fb && message) fb.textContent = message;
  }

  function clearFieldError(input) {
    input.classList.remove('is-invalid');
    input.classList.remove('is-valid');
  }

  function markValid(input) {
    input.classList.remove('is-invalid');
    input.classList.add('is-valid');
  }

  function validateField(input) {
    const val = input.value.trim();
    const id  = input.id;

    if (id === 'questionTitle') {
      if (val.length < 15) { showFieldError(input, 'Заголовок должен содержать от 15 до 200 символов.'); return false; }
      markValid(input); return true;
    }
    if (id === 'questionBody') {
      if (val.length < 20) { showFieldError(input, 'Описание должно содержать минимум 20 символов.'); return false; }
      markValid(input); return true;
    }
    if (id === 'answerText') {
      if (val.length < 20) { showFieldError(input, 'Ответ должен содержать минимум 20 символов.'); return false; }
      markValid(input); return true;
    }
    if (id === 'loginUsername') {
      if (!val) { showFieldError(input, 'Введите имя пользователя.'); return false; }
      markValid(input); return true;
    }
    if (id === 'loginPassword') {
      if (!val) { showFieldError(input, 'Введите пароль.'); return false; }
      markValid(input); return true;
    }
    if (id === 'signupUsername' || id === 'profileUsername') {
      if (!/^[a-zA-Z0-9_]{3,50}$/.test(val)) {
        showFieldError(input, 'Только латинские буквы, цифры и _ (3–50 символов).'); return false;
      }
      markValid(input); return true;
    }
    if (id === 'signupEmail' || id === 'profileEmail') {
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) {
        showFieldError(input, 'Введите корректный email-адрес.'); return false;
      }
      markValid(input); return true;
    }
    if (id === 'signupPassword' || id === 'newPassword') {
      if (val && val.length < 8) { showFieldError(input, 'Пароль должен содержать минимум 8 символов.'); return false; }
      if (val) markValid(input); else clearFieldError(input);
      return true;
    }
    if (id === 'signupPasswordConfirm' || id === 'confirmPassword') {
      const pwdId  = id === 'signupPasswordConfirm' ? 'signupPassword' : 'newPassword';
      const pwdVal = document.getElementById(pwdId)?.value || '';
      if (val !== pwdVal) { showFieldError(input, 'Пароли не совпадают.'); return false; }
      if (val) markValid(input); else clearFieldError(input);
      return true;
    }
    return true;
  }

  /* Realtime: validate after first blur */
  const validatableIds = [
    'questionTitle','questionBody','answerText',
    'loginUsername','loginPassword',
    'signupUsername','signupEmail','signupPassword','signupPasswordConfirm',
    'profileUsername','profileEmail','newPassword','confirmPassword',
  ];

  validatableIds.forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    let touched = false;
    el.addEventListener('blur',  () => { touched = true; validateField(el); });
    el.addEventListener('input', () => { if (touched) validateField(el); });
  });

  /* Submit handlers */
  attachSubmit('#loginUsername', ['loginUsername','loginPassword'], () => {
    const banner = document.getElementById('loginError');
    if (banner) banner.style.display = 'block';
  });

  attachSubmit('#questionTitle', ['questionTitle','questionBody']);
  attachSubmit('#signupUsername', ['signupUsername','signupEmail','signupPassword','signupPasswordConfirm']);
  attachSubmit('#profileUsername', ['profileUsername','profileEmail','newPassword','confirmPassword']);

  function attachSubmit(anchorId, fieldIds, onInvalid) {
    const anchor = document.getElementById(anchorId.replace('#',''));
    if (!anchor) return;
    const form = anchor.closest('form');
    if (!form) return;
    form.addEventListener('submit', e => {
      e.preventDefault();
      const els = fieldIds.map(id => document.getElementById(id)).filter(Boolean);
      els.forEach(el => { el._touched = true; });
      const allOk = els.map(validateField).every(Boolean);
      if (!allOk && onInvalid) onInvalid();
    });
  }

});
