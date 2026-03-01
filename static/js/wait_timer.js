function updateWaitTimers() {
  document.querySelectorAll('[data-checkin]').forEach(el => {
    const checkinTime = new Date(el.dataset.checkin);
    const now = new Date();
    const minutes = Math.floor((now - checkinTime) / 60000);

    el.querySelector('.wait-mins').textContent = minutes;

    el.classList.remove('wait-long', 'wait-medium', 'wait-short');
    if (minutes >= 20)      el.classList.add('wait-long');
    else if (minutes >= 10) el.classList.add('wait-medium');
    else                    el.classList.add('wait-short');
  });
}

updateWaitTimers();
setInterval(updateWaitTimers, 60000);