/* Blackout SOS — live official warnings for the viewer's own area.
   Data: bsos_alerts_public (Supabase), refreshed server-side every 15 minutes from the Met Office, Environment Agency,
   US National Weather Service, MeteoAlarm (37 European services) and GDACS. Location is the viewer's choice, stored on
   their device; the first guess comes from the device's time zone. Nothing about the viewer is sent anywhere. */
(function () {
  'use strict';
  var G = window.BSOS_GEO || { tz: {}, names: {}, regions: {}, usTz: {}, covered: [] };
  var REST = 'https://vbgustjtxjmjlgukzcfa.supabase.co/rest/v1/bsos_alerts_public';
  var ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZiZ3VzdGp0eGptamxndWt6Y2ZhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTMxMzI1MjcsImV4cCI6MjEwODcwODUyN30.Y_gKh0rs7HVI6rf3z8mmCAh-LcT-cTqJypqawbkdw7w';
  var KEY = 'bsos.loc.v1';
  var SOURCES = { metoffice: 'Met Office', ea: 'Environment Agency', nws: 'National Weather Service', meteoalarm: 'MeteoAlarm', gdacs: 'GDACS' };
  var LEVEL = { 1: 'red', 2: 'amber', 3: 'yellow', 4: 'info' };

  // ---- location ----
  function detect() {
    var tz = ''; try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) {}
    var country = G.tz[tz] || '';
    if (!country) { var m = String(navigator.language || '').match(/[-_]([A-Za-z]{2})$/); if (m) country = m[1].toUpperCase(); }
    if (!country) country = 'GB';
    var region = country === 'US' ? (G.usTz[tz] || '') : '';
    return { country: country, region: region, guessed: true };
  }
  function getLoc() { try { var v = JSON.parse(localStorage.getItem(KEY) || 'null'); if (v && v.country) return v; } catch (e) {} return detect(); }
  function setLoc(loc) { try { localStorage.setItem(KEY, JSON.stringify({ country: loc.country, region: loc.region || '' })); } catch (e) {} }
  function regionName(loc) { var list = G.regions[loc.country] || []; for (var i = 0; i < list.length; i++) if (list[i][0] === loc.region) return list[i][1]; return ''; }
  function placeName(loc) { return regionName(loc) || G.names[loc.country] || loc.country; }
  function covered(country) { return G.covered.indexOf(country) >= 0; }

  // ---- data ----
  var cache = {};
  function load(country) {
    if (cache[country]) return Promise.resolve(cache[country]);
    if (!window.fetch) return Promise.resolve([]);
    var url = REST + '?country=eq.' + encodeURIComponent(country) + '&order=level.asc,issued_at.desc&limit=200';
    return fetch(url, { headers: { apikey: ANON, Authorization: 'Bearer ' + ANON } })
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (rows) { cache[country] = rows || []; return cache[country]; })
      .catch(function () { return []; });
  }
  function forLoc(rows, loc) {
    if (!loc.region) return rows;
    return rows.filter(function (a) { return !a.regions || !a.regions.length || a.regions.indexOf(loc.region) >= 0; });
  }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function when(iso) { var d = new Date(iso); if (isNaN(d)) return ''; var diff = (Date.now() - d.getTime()) / 60000; if (diff < 60) return Math.max(1, Math.round(diff)) + ' min ago'; if (diff < 1440) return Math.round(diff / 60) + ' h ago'; return d.toLocaleDateString(undefined, { day: 'numeric', month: 'short' }); }
  function until(iso) { if (!iso) return ''; var d = new Date(iso); if (isNaN(d)) return ''; return 'until ' + d.toLocaleString(undefined, { weekday: 'short', hour: '2-digit', minute: '2-digit' }); }

  // ---- ticker (every page) ----
  function renderTicker(loc, rows) {
    var el = document.querySelector('[data-ticker]'); if (!el) return;
    var list = forLoc(rows, loc).filter(function (a) { return a.level <= 3; }).slice(0, 12);
    var place = placeName(loc);
    var items = '';
    if (list.length) {
      items = list.map(function (a) {
        return '<a class="tk-item" href="' + esc(a.link || '#') + '" target="_blank" rel="noopener"><span class="tk-dot ' + LEVEL[a.level] + '"></span><strong>' + esc(a.event) + '</strong> — ' + esc(a.area || G.names[a.country] || '') + ' <span class="tk-src">' + esc(SOURCES[a.source] || a.source) + '</span></a>';
      }).join('');
      el.className = 'ticker live lvl-' + LEVEL[list[0].level];
    } else {
      var note = covered(loc.country) ? 'No official warnings in force for ' + esc(place) + ' right now.' : 'No major events reported for ' + esc(place) + ' right now.';
      items = '<span class="tk-item"><span class="tk-dot none"></span>' + note + ' <a class="tk-src" href="' + el.getAttribute('data-ready-href') + '">The 72-hour checklist →</a></span>';
      el.className = 'ticker quiet';
    }
    var html = '<div class="tk-track">' + items + '</div>';
    var moving = list.length > 0 && !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    el.innerHTML = '<div class="tk-view' + (moving ? ' moving' : '') + '">' + html + (moving ? html : '') + '</div>' +
      '<button type="button" class="tk-loc" data-loc-open aria-haspopup="dialog">' + esc(place) + ' ▾</button>';
    var track = el.querySelector('.tk-track');
    if (moving && track) { var w = track.scrollWidth; el.style.setProperty('--tk-dur', Math.max(18, Math.round(w / 60)) + 's'); }
  }

  // ---- selector dialog ----
  function openSelector(loc, onChange) {
    var old = document.querySelector('.loc-dialog'); if (old) old.remove();
    var countries = Object.keys(G.names).sort(function (a, b) { return G.names[a] < G.names[b] ? -1 : 1; });
    var d = document.createElement('div'); d.className = 'loc-dialog'; d.setAttribute('role', 'dialog'); d.setAttribute('aria-label', 'Choose your area');
    function regionOptions(cc, cur) {
      var list = G.regions[cc]; if (!list) return '';
      return '<label class="field">' + (cc === 'US' ? 'State' : 'Region') + '<select name="region"><option value="">All of ' + esc(G.names[cc]) + '</option>' + list.map(function (r) { return '<option value="' + r[0] + '"' + (r[0] === cur ? ' selected' : '') + '>' + esc(r[1]) + '</option>'; }).join('') + '</select></label>';
    }
    d.innerHTML = '<div class="loc-box stack" style="gap:14px"><div style="display:flex;justify-content:space-between;align-items:center"><strong>Warnings for your area</strong><button type="button" class="pill sm" data-close>Close</button></div>' +
      '<label class="field">Country<select name="country">' + countries.map(function (c) { return '<option value="' + c + '"' + (c === loc.country ? ' selected' : '') + '>' + esc(G.names[c]) + '</option>'; }).join('') + '</select></label>' +
      '<div data-region>' + regionOptions(loc.country, loc.region) + '</div>' +
      '<p class="p small" data-cov></p>' +
      '<button type="button" class="pill solid" data-save>Show warnings</button></div>';
    document.body.appendChild(d);
    var cSel = d.querySelector('select[name=country]'); var cov = d.querySelector('[data-cov]');
    function covText(cc) { cov.textContent = covered(cc) ? 'Official national warnings for ' + G.names[cc] + ', plus worldwide disaster reports.' : 'Worldwide disaster reports (earthquakes, cyclones, floods) for ' + G.names[cc] + '. National weather warnings for this country are not in our feed yet.'; }
    covText(loc.country);
    cSel.addEventListener('change', function () { d.querySelector('[data-region]').innerHTML = regionOptions(cSel.value, ''); covText(cSel.value); });
    d.querySelector('[data-close]').addEventListener('click', function () { d.remove(); });
    d.addEventListener('click', function (e) { if (e.target === d) d.remove(); });
    d.querySelector('[data-save]').addEventListener('click', function () {
      var rSel = d.querySelector('select[name=region]');
      var next = { country: cSel.value, region: rSel ? rSel.value : '' };
      setLoc(next); d.remove(); onChange(next);
    });
  }

  // ---- alerts page ----
  function renderPage(loc, rows) {
    var box = document.querySelector('[data-alerts-page]'); if (!box) return;
    var list = forLoc(rows, loc);
    var place = placeName(loc);
    var title = document.querySelector('[data-alerts-place]'); if (title) title.textContent = place;
    var updated = rows.length ? rows.reduce(function (m, a) { return a.fetched_at > m ? a.fetched_at : m; }, '') : '';
    var upd = document.querySelector('[data-alerts-updated]'); if (upd) upd.textContent = updated ? 'Feed checked ' + when(updated) + ' · refreshed every 15 minutes' : 'Live feed · refreshed every 15 minutes';
    if (!list.length) {
      box.innerHTML = '<div class="card stack" style="gap:8px"><p class="h4 sans" style="font-weight:600">Nothing in force for ' + esc(place) + '</p><p class="p">' + (covered(loc.country) ? 'No official warnings from the national service right now. ' : 'No major events reported by GDACS right now. ') + 'A quiet day is the day to pack the bag.</p></div>';
      return;
    }
    var groups = [[1, 'Red — take action now'], [2, 'Amber — be prepared'], [3, 'Yellow — be aware'], [4, 'Information']];
    box.innerHTML = groups.map(function (g) {
      var rows2 = list.filter(function (a) { return a.level === g[0]; }); if (!rows2.length) return '';
      return '<div class="stack" style="gap:12px"><p class="eyebrow" style="display:flex;align-items:center;gap:10px"><span class="tk-dot ' + LEVEL[g[0]] + '"></span>' + g[1] + ' · ' + rows2.length + '</p>' +
        rows2.map(function (a) {
          return '<a class="card alert-card ' + LEVEL[a.level] + '" href="' + esc(a.link || '#') + '" target="_blank" rel="noopener"><div class="stack" style="gap:6px"><strong>' + esc(a.event) + '</strong><span class="p small">' + esc(a.area || G.names[a.country] || '') + '</span>' + (a.summary ? '<span class="p small" style="color:var(--soft)">' + esc(a.summary) + '</span>' : '') + '<span class="muted small">' + esc(SOURCES[a.source] || a.source) + ' · issued ' + when(a.issued_at) + (a.expires_at ? ' · ' + until(a.expires_at) : '') + '</span></div></a>';
        }).join('') + '</div>';
    }).join('');
  }

  // ---- forms: every signup carries the viewer's chosen country and region ----
  function stampForms(loc) {
    document.querySelectorAll('form[data-api="/subscribe"], form[data-api="/enquiry"]').forEach(function (f) {
      ['country', 'region'].forEach(function (k) {
        var inp = f.querySelector('input[name="' + k + '"]');
        if (!inp) { inp = document.createElement('input'); inp.type = 'hidden'; inp.name = k; f.appendChild(inp); }
        inp.value = loc[k] || '';
      });
      var loc2 = f.querySelector('input[name="locale"]');
      if (!loc2) { loc2 = document.createElement('input'); loc2.type = 'hidden'; loc2.name = 'locale'; f.appendChild(loc2); }
      loc2.value = String(navigator.language || '').slice(0, 12);
    });
    document.querySelectorAll('[data-loc-name]').forEach(function (el) { el.textContent = placeName(loc); });
  }

  // ---- one page view per load: no cookies, a random id for this tab, the viewer's chosen area ----
  function beacon(loc) {
    try {
      if (location.protocol === 'file:' || /^(localhost|127\.)/.test(location.hostname) || navigator.webdriver) return;
      var sid = sessionStorage.getItem('bsos.sid');
      if (!sid) { sid = Array.from(crypto.getRandomValues(new Uint8Array(12))).map(function (b) { return ('0' + b.toString(16)).slice(-2); }).join(''); sessionStorage.setItem('bsos.sid', sid); }
      var body = JSON.stringify({ s: sid, p: location.pathname, r: document.referrer || '', c: loc.country, g: loc.region || '', l: String(navigator.language || '').slice(0, 12), d: window.innerWidth < 760 ? 'm' : 'd' });
      var url = 'https://vbgustjtxjmjlgukzcfa.supabase.co/functions/v1/hit';
      if (navigator.sendBeacon) navigator.sendBeacon(url, new Blob([body], { type: 'application/json' }));
      else fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: body, keepalive: true }).catch(function () {});
    } catch (e) {}
  }

  function run(loc) {
    stampForms(loc);
    load(loc.country).then(function (rows) { renderTicker(loc, rows); renderPage(loc, rows); });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-loc-open]'); if (!b) return;
    e.preventDefault(); openSelector(getLoc(), run);
  });
  document.addEventListener('DOMContentLoaded', function () {
    var loc = getLoc(); run(loc); beacon(loc);
    // keep the ticker fresh on long-open pages
    setInterval(function () { cache = {}; run(getLoc()); }, 15 * 60 * 1000);
  });
  window.BSOS_ALERTS = { getLoc: getLoc, setLoc: setLoc, load: load };
})();
