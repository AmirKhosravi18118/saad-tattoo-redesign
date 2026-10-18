/* SAAD Booking Widget — ویجت رزرو مشترک (تقویم → ساعت → اطلاعات → تأیید)
   استفاده: <div data-booking-widget data-service="arm-design"></div>
   اگر data-service نباشد، از ?s= خوانده می‌شود. در لایو: جایگزینی با ویجت Wix Bookings. */
(function () {
  const SERVICES = {
    "arm-design":         {de:"Arm Design", en:"Arm Design", fa:"طرح دست"},
    "bein-design":        {de:"Bein Design", en:"Leg Design", fa:"طرح پا"},
    "ruecken-design":     {de:"Rücken Design", en:"Back Design", fa:"طرح پشت"},
    "brust-design":       {de:"Brust Design", en:"Chest Design", fa:"طرح سینه"},
    "hals-nacken-design": {de:"Hals & Nacken", en:"Neck & Nape", fa:"گردن و پشت‌گردن"}
  };
  const TIMES = ["10:00","11:30","13:00","14:30","16:00","17:30"];

  function t(key, fallback) {
    try {
      const lang = document.documentElement.lang || "de";
      const dict = window.I18N && window.I18N[lang];
      return (dict && dict[key]) || fallback;
    } catch (e) { return fallback; }
  }

  function init(root) {
    let slug = root.getAttribute("data-service");
    if (!slug) slug = new URLSearchParams(location.search).get("s") || "arm-design";
    const svc = SERVICES[slug] || SERVICES["arm-design"];
    const lang = document.documentElement.lang || "de";
    root.className = "bk-embed";
    root.innerHTML = `
      <p class="bk-service">${svc[lang] || svc.de} · SAAD Tattoo Wiesbaden</p>
      <div class="bk-bar"><i id="bk-progress" style="width:33%"></i></div>
      <div class="bk-step on" data-step="date">
        <p class="eyebrow" style="justify-content:center;margin-bottom:0"><span data-i18n="bk_s1">1 · Datum</span></p>
        <div class="bk-grid" data-days></div>
      </div>
      <div class="bk-step" data-step="time">
        <p class="eyebrow" style="justify-content:center;margin-bottom:0"><span data-i18n="bk_s2">2 · Uhrzeit</span></p>
        <div class="bk-times" data-times></div>
      </div>
      <div class="bk-step" data-step="data">
        <p class="eyebrow" style="justify-content:center;margin-bottom:0"><span data-i18n="bk_s3">3 · Deine Daten</span></p>
        <form class="bk-form">
          <input type="text" data-i18n-ph="bk_name" aria-label="Name">
          <input type="tel" data-i18n-ph="bk_phone" aria-label="Telefon">
          <input class="full" type="email" required data-i18n-ph="k_email" aria-label="E-Mail">
          <div class="full btn-row"><button class="btn btn-solid" type="submit" data-i18n="bk_confirm">Termin anfragen</button></div>
        </form>
        <p class="bk-pick" style="display:none;text-align:center;color:var(--gold);font-size:13px;margin-top:12px" data-i18n="bk_pick">Bitte Datum und Uhrzeit wählen.</p>
      </div>
      <div class="bk-step" data-step="ok" style="text-align:center">
        <p style="font-family:var(--font-head);color:var(--gold);font-size:22px" data-i18n="bk_success">Anfrage gesendet!</p>
        <p style="color:var(--dim);font-size:13px;margin-top:12px" data-i18n="bk_note">Demo – echte Auswahl erfolgt live über Wix Bookings.</p>
      </div>
      <div class="bk-contact btn-row" style="margin-top:32px;justify-content:center;display:flex">
        <a class="btn btn-ghost" href="https://api.whatsapp.com/send/?phone=%2B4917622067475&text&app_absent=0" target="_blank" rel="noopener">WhatsApp</a>
        <a class="btn btn-ghost" href="tel:+4917622067475">0176 22067475</a>
      </div>`;

    let pickedDate = null, pickedTime = null;
    const q = sel => root.querySelector(sel);
    const qa = sel => root.querySelectorAll(sel);
    function show(step) {
      qa(".bk-step").forEach(el => el.classList.toggle("on", el.dataset.step === step));
      q("#bk-progress").style.width = { date:"33%", time:"66%", data:"90%", ok:"100%" }[step];
    }
    const daysEl = q("[data-days]");
    const today = new Date();
    const fmtDay = new Intl.DateTimeFormat(undefined, { weekday:"short" });
    const fmtNum = new Intl.DateTimeFormat(undefined, { day:"numeric", month:"short" });
    for (let i = 1; i <= 14; i++) {
      const d = new Date(today); d.setDate(today.getDate() + i);
      const b = document.createElement("button");
      b.type = "button"; b.className = "bk-day";
      b.innerHTML = `<small>${fmtDay.format(d)}</small>${fmtNum.format(d)}`;
      if (d.getDay() === 0) b.disabled = true;
      b.addEventListener("click", () => {
        qa(".bk-day").forEach(x => x.classList.remove("sel"));
        b.classList.add("sel"); pickedDate = d;
        show("time"); renderTimes();
      });
      daysEl.appendChild(b);
    }
    function renderTimes() {
      const t = q("[data-times]"); t.innerHTML = "";
      TIMES.forEach(time => {
        const b = document.createElement("button");
        b.type = "button"; b.className = "bk-time"; b.textContent = time;
        b.addEventListener("click", () => {
          qa(".bk-time").forEach(x => x.classList.remove("sel"));
          b.classList.add("sel"); pickedTime = time;
          show("data");
        });
        t.appendChild(b);
      });
    }
    // بازترجمه فوری ویجت با زبان فعال (ترتیب بارگذاری را خنثی می‌کند)
    if (window.setLang) { try { window.setLang(document.documentElement.lang || localStorage.getItem("saad_lang") || "de"); } catch (e) {} }
    q(".bk-form").addEventListener("submit", e => {
      e.preventDefault();
      if (!pickedDate || !pickedTime) { q(".bk-pick").style.display = "block"; return; }
      const btn = q('.bk-form button[type="submit"]');
      const fd = new FormData(e.target);
      const payload = {
        type: "booking",
        service: slug,
        date: pickedDate.toISOString().slice(0, 10),
        time: pickedTime,
        name: fd.get("bk_name") || fd.get(0) || fd.entries().next().value[1] || "",
        email: q('.bk-form input[type="email"]').value,
        phone: [...e.target.querySelectorAll("input[type='tel']")].map(i => i.value)[0] || ""
      };
      // نام/ایمیل/تلفن از ورودی‌های ترتیبی (ویجت input بدون name دارد)
      const ins = [...e.target.querySelectorAll("input")];
      payload.name = ins[0] ? ins[0].value : "";
      payload.phone = ins[1] ? ins[1].value : "";
      payload.email = ins[2] ? ins[2].value : "";
      if (btn) { btn.disabled = true; btn.dataset.old = btn.textContent; }
      fetch("/api/wix", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
        .then(r => r.json())
        .then(d => { if (d.ok || d.booking) show("ok"); else { btn.disabled = false; btn.textContent = d.error || "Error — try again"; } })
        .catch(() => { btn.disabled = false; btn.textContent = "Network error — try again"; });
    });
  }

  function boot() { document.querySelectorAll("[data-booking-widget]").forEach(init); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
