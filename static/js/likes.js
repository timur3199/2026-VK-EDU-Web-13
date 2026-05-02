document.addEventListener('DOMContentLoaded', function () {

  function csrfFetch(url, data) {
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': CSRF_TOKEN,
      },
      body: new URLSearchParams(data),
    }).then(function (res) {
      if (res.status === 403) return res.json().then(function(d) { throw new Error(d.error || 'Доступ запрещён.'); });
      if (!res.ok) throw new Error('Ошибка сервера: ' + res.status);
      return res.json();
    });
  }

  // ── Like widgets ────────────────────────────────────────────────────────────
  document.querySelectorAll('.like-widget').forEach(function (widget) {
    var btn = widget.querySelector('.like-up');
    if (!btn) return;

    btn.addEventListener('click', function () {
      if (!IS_AUTH) {
        window.location.href = LOGIN_URL;
        return;
      }

      var type = widget.dataset.type;   // 'question' or 'answer'
      var id   = widget.dataset.id;
      var url  = type === 'question'
        ? '/question/' + id + '/like/'
        : '/answer/' + id + '/like/';

      csrfFetch(url, {})
        .then(function (data) {
          widget.querySelector('.like-count').textContent = data.likes_count;
          btn.classList.toggle('active', data.liked);
          btn.title = data.liked ? 'Убрать лайк' : 'Лайк';
        })
        .catch(function (err) {
          alert(err.message);
        });
    });
  });

  // ── Mark correct ────────────────────────────────────────────────────────────
  document.querySelectorAll('.correct-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (!IS_AUTH) {
        window.location.href = LOGIN_URL;
        return;
      }

      var answerId = btn.dataset.answerId;

      csrfFetch('/answer/' + answerId + '/correct/', {})
        .then(function (data) {
          // Reset all answer cards
          document.querySelectorAll('.answer-card').forEach(function (card) {
            card.classList.remove('correct');
          });
          document.querySelectorAll('.correct-badge').forEach(function (badge) {
            badge.classList.add('d-none');
          });
          document.querySelectorAll('.correct-btn').forEach(function (b) {
            b.classList.remove('active');
            b.textContent = '✓ Отметить как правильный';
            b.title = 'Отметить как правильный';
          });

          if (data.is_correct) {
            var card = document.getElementById('answer-' + data.answer_id);
            if (card) card.classList.add('correct');

            var badge = document.getElementById('badge-' + data.answer_id);
            if (badge) badge.classList.remove('d-none');

            btn.classList.add('active');
            btn.textContent = '✓ Правильный ответ';
            btn.title = 'Снять отметку';
          }
        })
        .catch(function (err) {
          alert(err.message);
        });
    });
  });

});
