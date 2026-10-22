/* GOLD5 gold-value calculator. Computes only from user inputs; nothing is stored or sent. */
(function () {
  var FIN = { 10: 0.4167, 14: 0.5833, 18: 0.75, 22: 0.9167, 24: 0.9999 };
  var TROY = 31.1034768;
  var $ = function (id) { return document.getElementById(id); };
  var form = $('calc-form');
  if (!form) return;

  var money = function (n) {
    return '$' + Number(n).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  };
  var num = function (n, d) {
    return Number(n).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
  };

  function calc() {
    var grams = parseFloat($('grams').value);
    var karat = parseInt($('karat').value, 10);
    var spot = parseFloat($('spot').value);
    var price = parseFloat($('price').value);
    var fin = FIN[karat] || (karat / 24);
    var fine = $('r-fine'), value = $('r-value'), ratio = $('r-ratio');
    var fineD = $('r-fine-d'), valueD = $('r-value-d'), ratioD = $('r-ratio-d');
    var verdict = $('verdict');

    if (!isFinite(grams) || grams <= 0 || !isFinite(spot) || spot <= 0) {
      fine.textContent = '—'; value.textContent = '—'; ratio.textContent = '—';
      fineD.textContent = 'grams of pure gold';
      valueD.textContent = 'at your spot';
      ratioD.textContent = 'complete rings only';
      verdict.className = 'verdict';
      verdict.textContent = 'Enter a weight, a karat and a spot price to see the metal value. Add an asking price to see the ratio.';
      return;
    }

    var fg = grams * fin;
    var mv = fg * spot;
    fine.textContent = num(fg, 3) + ' g';
    fineD.textContent = num(grams, 2) + ' g × ' + num(fin * 100, 2) + '% (' + karat + 'K)';
    value.textContent = money(mv);
    valueD.textContent = num(fg, 3) + ' g × ' + money(spot) + '/g · ' + num(fg / TROY, 4) + ' troy oz';

    if (isFinite(price) && price > 0) {
      var r = price / mv;
      ratio.textContent = num(r, 2) + '×';
      ratioD.textContent = money(price) + ' ÷ ' + money(mv);
      if (r < 1) {
        verdict.className = 'verdict bad';
        verdict.innerHTML = '<b>Below the metal value — stop.</b> The asking price is below what the gold alone is worth. That is a fraud signal (or the item is not what it claims). Do not send money. See <a href="flagged.html#FL-01">FL-01</a>.';
      } else if (r < 1.6) {
        verdict.className = 'verdict warn';
        verdict.innerHTML = '<b>Thin margin over metal.</b> Plausible for a plain band, but confirm the item is solid (not hollow or plated), the weight is real, and the hallmark and return terms are in writing.';
      } else {
        verdict.className = 'verdict ok';
        verdict.innerHTML = '<b>' + num(r, 2) + '× the metal value.</b> Normal for a ring with stones and labour — not evidence of overcharging, and not a valuation of the diamond. Judge the stone separately.';
      }
    } else {
      ratio.textContent = '—';
      ratioD.textContent = 'add a price to compare';
      verdict.className = 'verdict';
      verdict.innerHTML = num(grams, 2) + ' g of ' + karat + 'K contains <b>' + num(fg, 3) + ' g</b> of fine gold, worth <b>' + money(mv) + '</b> at ' + money(spot) + '/g. Add an asking price to compare.';
    }
  }

  var preset = $('preset');
  if (preset) preset.addEventListener('change', function () {
    var o = preset.options[preset.selectedIndex];
    if (!o || !o.value) return;
    $('grams').value = o.dataset.grams;
    $('karat').value = o.dataset.karat;
    if (o.dataset.price !== '') $('price').value = o.dataset.price;
    calc();
  });

  ['grams', 'karat', 'spot', 'price'].forEach(function (id) {
    var el = $(id);
    if (el) el.addEventListener('input', calc);
    if (el) el.addEventListener('change', calc);
  });
  var btn = $('calc-btn');
  if (btn) btn.addEventListener('click', calc);
  form.addEventListener('submit', function (e) { e.preventDefault(); calc(); });
  calc();
})();
