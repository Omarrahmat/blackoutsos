/* Blackout SOS — basket, forms and checkout. No framework, no tracking. */
(function () {
  'use strict';
  var API = 'https://vbgustjtxjmjlgukzcfa.supabase.co/functions/v1';
  var KEY = 'bsos.basket.v1';

  // Display catalogue. Prices are checked again on the server at checkout.
  var CATALOGUE = {
    'operator':   { name: 'Operator', variant: 'Adult', price: 19900, colour: '#1F5FBF', url: 'bags/operator.html' },
    'recruit':    { name: 'Recruit', variant: 'Child, 5 to 12', price: 8900, colour: '#D0202E', url: 'bags/recruit.html' },
    'cub-1':      { name: 'Cub 1', variant: '0 to 6 months', price: 14900, colour: '#F5C518', url: 'bags/cub.html' },
    'cub-2':      { name: 'Cub 2', variant: '6 to 12 months', price: 14900, colour: '#F5C518', url: 'bags/cub.html' },
    'cub-3':      { name: 'Cub 3', variant: '12 to 24 months', price: 14900, colour: '#F5C518', url: 'bags/cub.html' },
    'unit':       { name: 'Unit', variant: 'Family of four', price: 44900, colour: '#2BA84A', url: 'bags/unit.html' },
    'scout-dog':  { name: 'Scout', variant: 'Dog', price: 9900, colour: '#F28C28', url: 'bags/scout.html' },
    'scout-cat':  { name: 'Scout', variant: 'Cat', price: 9900, colour: '#F28C28', url: 'bags/scout.html' }
  };

  // Live availability: the database says which bags can be bought right now. Default markup shows "coming soon";
  // this only ever switches a bag ON after a successful check, so a failed check can never sell what isn't there.
  var REST = 'https://vbgustjtxjmjlgukzcfa.supabase.co/rest/v1/bsos_availability?select=sku,in_stock';
  var ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZiZ3VzdGp0eGptamxndWt6Y2ZhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTMxMzI1MjcsImV4cCI6MjEwODcwODUyN30.Y_gKh0rs7HVI6rf3z8mmCAh-LcT-cTqJypqawbkdw7w';
  var AVAILABLE = {};
  function applyAvailability() {
    var els = document.querySelectorAll('[data-avail]');
    for (var i = 0; i < els.length; i++) {
      var inStock = !!AVAILABLE[els[i].getAttribute('data-avail')];
      var when = els[i].getAttribute('data-when');
      els[i].hidden = (when === 'in') ? !inStock : inStock;
    }
    var any = false; for (var k in AVAILABLE) if (AVAILABLE[k]) any = true;
    var bar = document.querySelector('[data-launch-bar]'); if (bar) bar.hidden = any;
    document.querySelectorAll('.variant[data-sku]').forEach(function (v) { v.classList.toggle('soon', !AVAILABLE[v.getAttribute('data-sku')]); });
  }
  function loadAvailability() {
    if (!window.fetch) return;
    fetch(REST, { headers: { apikey: ANON, Authorization: 'Bearer ' + ANON } })
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (rows) { (rows || []).forEach(function (row) { AVAILABLE[row.sku] = !!row.in_stock; }); applyAvailability(); })
      .catch(function () {});
  }

  function gbp(p) { return '£' + (p / 100).toFixed(p % 100 ? 2 : 0); }
  function read() { try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; } }
  function write(b) { try { localStorage.setItem(KEY, JSON.stringify(b)); } catch (e) {} renderCount(); }
  function count(b) { var n = 0; for (var k in b) n += b[k]; return n; }
  function total(b) { var t = 0; for (var k in b) if (CATALOGUE[k]) t += CATALOGUE[k].price * b[k]; return t; }

  function renderCount() {
    var n = count(read());
    var els = document.querySelectorAll('[data-basket-count]');
    for (var i = 0; i < els.length; i++) els[i].textContent = 'Basket · ' + n;
  }

  var toastEl, toastT;
  function toast(msg) {
    if (!toastEl) { toastEl = document.createElement('div'); toastEl.className = 'toast'; toastEl.setAttribute('role', 'status'); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add('on');
    clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove('on'); }, 2200);
  }

  function add(sku, qty) {
    if (!AVAILABLE[sku]) { toast('Not available to order yet — join the list on the bag page and we will tell you the day it is.'); return; }
    if (!CATALOGUE[sku]) return;
    var b = read(); b[sku] = (b[sku] || 0) + (qty || 1); write(b);
    toast(CATALOGUE[sku].name + ' added to your basket');
  }
  function setQty(sku, qty) { var b = read(); if (qty <= 0) delete b[sku]; else b[sku] = qty; write(b); renderBasket(); }

  // Product page: variant buttons + add button
  function initProduct() {
    var form = document.querySelector('[data-product]');
    if (!form) return;
    var sku = form.getAttribute('data-product');
    var buttons = form.querySelectorAll('.variant');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener('click', function (e) {
        e.preventDefault();
        for (var j = 0; j < buttons.length; j++) buttons[j].setAttribute('aria-pressed', 'false');
        this.setAttribute('aria-pressed', 'true');
        sku = this.getAttribute('data-sku');
        var label = form.querySelector('[data-variant-label]'); if (label) label.textContent = this.getAttribute('data-label') || '';
        // the buy button and the notify-me box follow the chosen variant
        document.querySelectorAll('[data-avail][data-follow-variant]').forEach(function (el) { el.setAttribute('data-avail', sku); });
        applyAvailability();
      });
    }
    form.addEventListener('submit', function (e) { e.preventDefault(); add(sku, 1); });
  }

  // Basket page
  function renderBasket() {
    var box = document.querySelector('[data-basket]');
    if (!box) return;
    var b = read(), keys = Object.keys(b).filter(function (k) { return CATALOGUE[k]; });
    var empty = document.querySelector('[data-basket-empty]');
    var summary = document.querySelector('[data-basket-summary]');
    if (!keys.length) { box.innerHTML = ''; if (empty) empty.hidden = false; if (summary) summary.hidden = true; return; }
    if (empty) empty.hidden = true; if (summary) summary.hidden = false;
    var html = '';
    keys.forEach(function (k) {
      var p = CATALOGUE[k];
      html += '<div class="basket-line" data-sku="' + k + '">'
        + '<span class="tag" style="background:' + p.colour + '"></span>'
        + '<a href="' + p.url + '" style="flex:1 1 200px;min-width:0"><strong>' + p.name + '</strong><br><span class="muted small">' + p.variant + ' · ' + gbp(p.price) + '</span></a>'
        + '<div class="qty"><button type="button" aria-label="Remove one" data-dec>−</button><span>' + b[k] + '</span><button type="button" aria-label="Add one" data-inc>+</button></div>'
        + '<strong style="min-width:70px;text-align:right">' + gbp(p.price * b[k]) + '</strong>'
        + '<button type="button" class="pill sm" data-remove>Remove</button></div>';
    });
    box.innerHTML = html;
    var t = total(b);
    var tEl = document.querySelector('[data-basket-total]'); if (tEl) tEl.textContent = gbp(t);
    box.querySelectorAll('.basket-line').forEach(function (line) {
      var k = line.getAttribute('data-sku');
      line.querySelector('[data-dec]').onclick = function () { setQty(k, b[k] - 1); };
      line.querySelector('[data-inc]').onclick = function () { setQty(k, b[k] + 1); };
      line.querySelector('[data-remove]').onclick = function () { setQty(k, 0); };
    });
  }

  function post(path, body) {
    return fetch(API + path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, status: r.status, data: j }; }); });
  }

  function initCheckout() {
    var btn = document.querySelector('[data-checkout]');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var b = read(); var items = Object.keys(b).filter(function (k) { return CATALOGUE[k]; }).map(function (k) { return { sku: k, qty: b[k] }; });
      if (!items.length) return;
      btn.disabled = true; btn.textContent = 'Taking you to secure checkout…';
      var msg = document.querySelector('[data-checkout-msg]');
      post('/checkout', { items: items, base: location.href.replace(/[?#].*$/, '').replace(/[^/]*$/, '') })
        .then(function (res) {
          if (res.ok && res.data && res.data.url) { location.href = res.data.url; return; }
          btn.disabled = false; btn.textContent = 'Checkout';
          if (msg) { msg.hidden = false; msg.textContent = (res.data && res.data.error) || 'Checkout is not available right now. Email hello@blackoutsos.com and we will take your order by hand.'; }
        })
        .catch(function () { btn.disabled = false; btn.textContent = 'Checkout'; if (msg) { msg.hidden = false; msg.textContent = 'We could not reach the checkout. Please try again in a minute, or email hello@blackoutsos.com.'; } });
    });
  }

  // Forms: newsletter (subscribe) and enquiries
  function initForms() {
    document.querySelectorAll('form[data-api]').forEach(function (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var path = form.getAttribute('data-api');
        var data = {}; new FormData(form).forEach(function (v, k) { data[k] = v; });
        data.page = location.pathname;
        var btn = form.querySelector('button[type="submit"]'); var old = btn ? btn.textContent : '';
        if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
        var done = form.querySelector('[data-done]');
        post(path, data).then(function (res) {
          if (btn) { btn.disabled = false; btn.textContent = old; }
          if (res.ok) { form.reset(); if (done) { done.hidden = false; } else toast('Thank you. Received.'); }
          else toast((res.data && res.data.error) || 'That did not go through. Please try again.');
        }).catch(function () { if (btn) { btn.disabled = false; btn.textContent = old; } toast('That did not go through. Please try again.'); });
      });
    });
  }

  // After a paid checkout: clear the basket and record the order (idempotent on the server)
  function initSuccess() {
    var box = document.querySelector('[data-order-success]');
    if (!box) return;
    write({});
    var m = location.search.match(/[?&]session_id=([^&]+)/);
    if (!m) return;
    var ref = document.querySelector('[data-order-ref]');
    post('/confirm', { session_id: decodeURIComponent(m[1]) }).then(function (res) {
      if (res.ok && res.data && res.data.ok && ref) { ref.hidden = false; ref.textContent = 'Order reference: ' + String(res.data.order_id).slice(0, 8).toUpperCase() + (res.data.email ? ' · receipt sent to ' + res.data.email : ''); }
    }).catch(function () {});
  }

  document.addEventListener('DOMContentLoaded', function () {
    renderCount(); initProduct(); renderBasket(); initCheckout(); initForms(); initSuccess(); loadAvailability();
    document.querySelectorAll('[data-add]').forEach(function (el) { el.addEventListener('click', function (e) { e.preventDefault(); add(el.getAttribute('data-add'), 1); }); });
  });

  window.BSOS = { add: add, catalogue: CATALOGUE };
})();
