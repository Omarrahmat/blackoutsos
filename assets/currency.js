/* Local-currency prices. Rates from bsos_fx_public (refreshed daily); the same rounding runs at checkout, so the price shown is the price charged. */
(function () {
  'use strict';
  var EUR = ['AT','BE','HR','CY','EE','FI','FR','DE','GR','IE','IT','LV','LT','LU','MT','NL','PT','SK','SI','ES','AD','MC','SM','VA','ME','XK'];
  var MAP = { US:'USD', PR:'USD', CA:'CAD', AU:'AUD', NZ:'NZD', CH:'CHF', LI:'CHF', SE:'SEK', NO:'NOK', DK:'DKK', PL:'PLN', CZ:'CZK', HU:'HUF', JP:'JPY', KR:'KRW', SG:'SGD', HK:'HKD', AE:'AED', SA:'SAR', IN:'INR', ZA:'ZAR', MX:'MXN', BR:'BRL', IL:'ILS', MY:'MYR', TR:'TRY', RO:'RON', IS:'ISK', PH:'PHP', TH:'THB', TW:'TWD', GB:'GBP', JE:'GBP', GG:'GBP', IM:'GBP' };
  EUR.forEach(function (c) { MAP[c] = 'EUR'; });
  var ZERO = { JPY: 1, KRW: 1, ISK: 1 };
  var RATES = { GBP: 1 }, CUR = 'GBP', LOCALE = navigator.language || 'en-GB';
  function nice(x) {
    if (x <= 0) return 0;
    if (x < 1000) return Math.ceil((x + 1) / 5) * 5 - 1;
    var m = Math.pow(10, Math.floor(Math.log10(x)) - 1); return Math.ceil(x / m) * m;
  }
  // pence in GBP -> amount in the currency's major unit (what we show and charge)
  function local(pence, cur) { cur = cur || CUR; if (cur === 'GBP' || !RATES[cur]) return pence / 100; return nice(pence / 100 * RATES[cur]); }
  function fmt(amount, cur) { cur = cur || CUR; var whole = Math.round(amount * 100) % 100 === 0;
    try { return new Intl.NumberFormat(LOCALE, { style: 'currency', currency: cur, minimumFractionDigits: whole ? 0 : 2, maximumFractionDigits: whole ? 0 : 2 }).format(amount); } catch (e) { return cur + ' ' + amount; } }
  function money(pence) { return fmt(local(pence)); }
  function apply() { document.querySelectorAll('[data-gbp]').forEach(function (el) { el.textContent = money(+el.getAttribute('data-gbp')); }); document.dispatchEvent(new CustomEvent('bsos:currency', { detail: CUR })); }
  function setCountry(cc) {
    var cur = MAP[cc] || 'USD';
    if (cur !== 'GBP' && !RATES[cur]) cur = (RATES.USD ? 'USD' : 'GBP');
    if (cur === CUR && apply.done) return; CUR = cur; apply.done = 1; apply();
  }
  var ready = fetch('https://vbgustjtxjmjlgukzcfa.supabase.co/rest/v1/bsos_fx_public?select=code,per_gbp', { headers: { apikey: window.BSOS_ANON, Authorization: 'Bearer ' + window.BSOS_ANON } })
    .then(function (r) { return r.ok ? r.json() : []; }).then(function (rows) { (rows || []).forEach(function (x) { RATES[x.code] = +x.per_gbp; }); }).catch(function () {});
  var pending = null;
  document.addEventListener('bsos:loc', function (e) { pending = e.detail && e.detail.country; try { var v = localStorage.getItem('bsos.ship.v1'); if (v) pending = v; } catch (x) {} ready.then(function () { setCountry(pending); }); });
  window.BSOS_CUR = { money: money, local: local, fmt: fmt, current: function () { return CUR; }, setCountry: function (cc) { ready.then(function () { setCountry(cc); }); }, ready: ready };
})();
