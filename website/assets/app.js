/* Gemeinsames Skript für alle Seiten. Alle Inhalte stehen bereits im HTML –
   das Skript ergänzt nur Komfort: Tagesansicht der Gottesdienste, „nächster
   Gottesdienst“, Bürostatus, Suche, Filter, Menü, Hell/Dunkel, Formulare. */
(() => {
"use strict";
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const DATA = window.PFARREI || { churches: [], services: [], search: [] };
const C = Object.fromEntries(DATA.churches.map(c => [c.id, c]));
const params = new URLSearchParams(location.search);

const DAYS = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];
const DS = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"];
const MON = ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sept.", "Okt.", "Nov.", "Dez."];
const KIND = { mass: ["Hl. Messe", ""], fam: ["Familie & Kinder", "fam"], prayer: ["Andacht & Gebet", "prayer"], school: ["Schule", "school"] };

const today0 = () => { const d = new Date(); d.setHours(0, 0, 0, 0); return d; };
const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
const isLast = dt => addDays(dt, 7).getMonth() !== dt.getMonth();
const nth = dt => Math.ceil(dt.getDate() / 7);
const dayLabel = (d, i) => i === 0 ? "Heute" : i === 1 ? "Morgen" : DAYS[d.getDay()];
const fmtH = h => `${String(Math.floor(h)).padStart(2, "0")}:${String(Math.round((h % 1) * 60)).padStart(2, "0")}`;

function servicesOn(dt) {
  const wd = dt.getDay(), mo = dt.getMonth() + 1;
  return DATA.services.filter(s => s.d.includes(wd)
      && (!s.n || s.n.some(n => n === "last" ? isLast(dt) : n === nth(dt)))
      && (!s.m || s.m.includes(mo)))
    .map(s => ({ ...s, time: s.tw && (mo >= 10 || mo <= 3) ? s.tw : s.t }))
    .sort((a, b) => a.time.localeCompare(b.time));
}

/* ---------- Menü, Suche im Kopf, Theme ---------- */
const menuBtn = $("#menuBtn"), drawer = $("#drawer"), searchBtn = $("#searchBtn"), panel = $("#searchpanel");
menuBtn && menuBtn.addEventListener("click", () => {
  const o = drawer.classList.toggle("open"); menuBtn.setAttribute("aria-expanded", String(o));
  if (o && panel) { panel.classList.remove("open"); searchBtn.setAttribute("aria-expanded", "false"); }
});
searchBtn && searchBtn.addEventListener("click", () => {
  const o = panel.classList.toggle("open"); searchBtn.setAttribute("aria-expanded", String(o));
  if (o) { drawer.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); $("input", panel).focus(); }
});
const root = document.documentElement;
$("#themeBtn") && $("#themeBtn").addEventListener("click", () => {
  const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = dark ? "light" : "dark";
  try { localStorage.setItem("theme", root.dataset.theme); } catch (_) {}
});
$$("[data-print]").forEach(b => b.addEventListener("click", () => window.print()));

/* ---------- Suche ---------- */
const norm = s => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
function findHits(v) {
  const words = norm(v.trim()).split(/\s+/).filter(Boolean);
  if (!words.length) return [];
  return DATA.search.map(([t, h, k]) => {
    const title = norm(t), hay = title + " " + norm(k); let sc = 0;
    for (const w of words) { if (title.includes(w)) sc += 3; else if (hay.includes(w)) sc += 1; else return null; }
    return { t, h, sc };
  }).filter(Boolean).sort((a, b) => b.sc - a.sc);
}
$$("form[data-search]").forEach(form => {
  const q = $("input", form), res = $(".results", form); let sel = -1;
  const render = () => {
    const v = q.value.trim(); if (!v) { res.hidden = true; return; }
    const hits = findHits(v).slice(0, 6); sel = -1;
    res.innerHTML = hits.length ? hits.map(x => `<a href="${x.h}" role="option">${esc(x.t)}<small>→</small></a>`).join("")
      : `<a href="kontakt.html" role="option">Nichts gefunden – frag das Pastoralbüro<small>→</small></a>`;
    res.hidden = false;
  };
  q.addEventListener("input", render);
  q.addEventListener("keydown", e => {
    const items = $$("a", res);
    if (e.key === "Escape") { res.hidden = true; return; }
    if (res.hidden || !items.length) return;
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault(); sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + items.length) % items.length;
      items.forEach((a, i) => a.setAttribute("aria-selected", String(i === sel)));
    }
  });
  form.addEventListener("submit", e => {
    const items = $$("a", res);
    if (!res.hidden && items.length) { e.preventDefault(); location.href = (items[sel] || items[0]).getAttribute("href"); }
  });
  document.addEventListener("click", e => { if (!form.contains(e.target)) res.hidden = true; });
});
const all = $("#searchAll");
if (all) {
  const v = params.get("q") || "";
  const inp = $("#q3"); if (inp) inp.value = v;
  const hits = findHits(v);
  all.innerHTML = v ? (hits.length ? `<p>${hits.length} Treffer für „${esc(v)}“:</p><div class="tiles">` +
      hits.map(x => `<a href="${x.h}"><b>${esc(x.t)}</b><span class="go">Öffnen →</span></a>`).join("") + "</div>"
    : `<div class="empty">Nichts gefunden für „${esc(v)}“. Ruf gern im Pastoralbüro an: 02267 88187-0.</div>`) : "";
}

/* ---------- Nächster Gottesdienst (Startseite) ---------- */
function renderNext() {
  if (!$("#nextTitle")) return;
  const now = new Date(), base = today0();
  for (let i = 0; i < 8; i++) {
    const d = addDays(base, i);
    for (const s of servicesOn(d)) {
      if (s.k === "school" || s.title === "Beichtgelegenheit") continue;
      const [h, m] = s.time.split(":").map(Number);
      if (new Date(d.getFullYear(), d.getMonth(), d.getDate(), h, m) > now) {
        const c = C[s.c];
        $("#nextTitle").textContent = `${i < 2 ? dayLabel(d, i) : DAYS[d.getDay()] + ", " + d.getDate() + ". " + MON[d.getMonth()]}, ${s.time} Uhr`;
        $("#nextSub").innerHTML = `${esc(s.title)} · ${esc(c.name)}, ${esc(c.place)} · <a href="gottesdienste.html">alle Termine</a>`;
        return;
      }
    }
  }
}

/* ---------- Gottesdienst-Finder ---------- */
const state = { day: 0, kind: params.get("art") || "all", place: params.get("ort") || "" };
function renderServices() {
  const list = $("#svcList"); if (!list) return;
  const d = addDays(today0(), state.day);
  const items = servicesOn(d).filter(s => (state.kind === "all" || s.k === state.kind) && (!state.place || s.c === state.place));
  $$("#days button").forEach(b => b.setAttribute("aria-pressed", String(+b.dataset.i === state.day)));
  $$("#kindFilters [data-kind]").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.kind === state.kind)));
  list.innerHTML = items.length ? items.map(s => {
    const c = C[s.c], [kl, kc] = KIND[s.k];
    return `<div class="svc"><time>${s.time}</time><div><div class="t">${esc(s.title)}</div>
      <div class="w">${esc(c.name)} · ${esc(c.place)}${c.addr ? " · " + esc(c.addr) : ""}</div>
      <span class="tag ${kc}">${kl}</span>${s.note ? `<span class="tag school">${esc(s.note)}</span>` : ""}</div></div>`;
  }).join("") : `<div class="empty">Keine regelmäßigen Gottesdienste mit dieser Auswahl am ${DAYS[d.getDay()]}. Probier einen anderen Tag oder „Alle Orte“.</div>`;
}
function initFinder() {
  const days = $("#days"); if (!days) return;
  const base = today0();
  days.innerHTML = Array.from({ length: 7 }, (_, i) => {
    const d = addDays(base, i);
    return `<button type="button" data-i="${i}" aria-pressed="false"><b>${i < 2 ? dayLabel(d, i) : DS[d.getDay()]}</b><small>${d.getDate()}. ${MON[d.getMonth()]}</small></button>`;
  }).join("");
  if (state.place) {
    $("#placeSel").value = state.place;
    for (let i = 0; i < 7; i++) if (servicesOn(addDays(base, i)).some(s => s.c === state.place)) { state.day = i; break; }
  }
  days.addEventListener("click", e => { const b = e.target.closest("button"); if (b) { state.day = +b.dataset.i; renderServices(); } });
  $$("#kindFilters [data-kind]").forEach(b => b.addEventListener("click", () => { state.kind = b.dataset.kind; renderServices(); }));
  $("#placeSel").addEventListener("change", e => { state.place = e.target.value; renderServices(); });
  renderServices();
}

/* ---------- Gruppen-Filter ---------- */
const gf = $("#groupFilters");
gf && gf.addEventListener("click", e => {
  const b = e.target.closest("[data-g]"); if (!b) return;
  $$("[data-g]", gf).forEach(x => x.setAttribute("aria-pressed", String(x === b)));
  $$("#groups [data-groups]").forEach(g => { g.hidden = b.dataset.g !== "all" && !g.dataset.groups.split(" ").includes(b.dataset.g); });
});

/* ---------- Pastoralbüro: Status ---------- */
const HOURS = { 1: [[8.5, 15.5]], 2: [[8.5, 15.5]], 3: [[8.5, 12.5]], 4: [[8.5, 15.5]], 5: [[8.5, 15.5]], 6: [], 0: [] };
const closedDay = d => d.getMonth() === 11 && (d.getDate() === 24 || d.getDate() === 31);
function officeStatus() {
  const now = new Date(), h = now.getHours() + now.getMinutes() / 60;
  const slot = !closedDay(now) && HOURS[now.getDay()].find(([a, b]) => h >= a && h < b);
  if (slot) return { open: true, text: `Jetzt geöffnet bis ${fmtH(slot[1])} Uhr` };
  for (let i = 0; i < 8; i++) {
    const d = addDays(today0(), i); if (closedDay(d)) continue;
    const s = HOURS[d.getDay()].find(([a]) => i > 0 || a > h);
    if (s) return { open: false, text: `Geschlossen · öffnet ${i === 0 ? "heute" : i === 1 ? "morgen" : DAYS[d.getDay()]} um ${fmtH(s[0])} Uhr` };
  }
  return { open: false, text: "Geschlossen" };
}
function renderOffice() {
  const st = officeStatus();
  const now = $("#officeNow");
  if (now) now.innerHTML = `<span class="dot ${st.open ? "on" : "off"}"></span>${st.open ? "Jetzt geöffnet" : "Geschlossen"}`;
  $$("[data-office-badge]").forEach(b => { b.textContent = st.text; b.className = "status " + (st.open ? "on" : "off"); });
  const hb = $("#hoursBody");
  if (hb) { const wd = new Date().getDay(); const idx = wd === 0 ? 6 : wd - 1; $$("tr", hb).forEach((tr, i) => tr.classList.toggle("today", i === idx)); }
}

/* ---------- Formulare → E-Mail ---------- */
const topic = params.get("anliegen");
if (topic && $("#mTopic")) { const o = [...$("#mTopic").options].find(o => o.text === topic); if (o) $("#mTopic").value = o.text; }
$$("form[data-mailform]").forEach(f => f.addEventListener("submit", e => {
  e.preventDefault();
  const fd = new FormData(f), lines = [];
  let subject = f.dataset.subject || "Anfrage";
  for (const [k, v] of fd) { if (!String(v).trim()) continue; if (k === "Anliegen") subject = "Anfrage: " + v; else lines.push(`${k}: ${v}`); }
  location.href = `mailto:pastoralbuero-wipp@erzbistum-koeln.de?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join("\n"))}`;
}));

window.addEventListener("beforeprint", () => $$("details").forEach(d => d.open = true));
renderNext(); initFinder(); renderOffice();
setInterval(() => { renderNext(); renderOffice(); }, 60000);
})();
