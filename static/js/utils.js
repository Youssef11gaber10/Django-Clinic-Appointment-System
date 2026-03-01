function switchTab(name, btn) {
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
    document.getElementById('tab-' + name).classList.add('active');
    btn.classList.add('active');
  }

  function openModal(id, name, apptId) {
    if (id === 'noShowModal') {
      document.getElementById('noshow-name').textContent = name;
      document.getElementById('noShowForm').action = `/dashboard/appointment/${apptId}/no-show/`;
    }
    if (id === 'declineModal') {
      document.getElementById('decline-name').textContent = name;
      document.getElementById('declineForm').action = `/dashboard/appointment/${apptId}/decline/`;
    }
    document.getElementById(id).classList.add('open');
  }

  function closeModal(id) {
    document.getElementById(id).classList.remove('open');
  }

  document.querySelectorAll('.modal-overlay').forEach(o => {
    o.addEventListener('click', e => { if (e.target === o) o.classList.remove('open'); });
  });

  function showToast(msg, icon) {
    const t = document.getElementById('toast');
    t.textContent = (icon || '✅') + '  ' + msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3000);
  }