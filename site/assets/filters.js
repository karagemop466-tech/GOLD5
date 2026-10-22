/* Listings filter + sort. No dependencies. */
(function () {
  var rows = Array.prototype.slice.call(document.querySelectorAll('#listings tbody tr'));
  rows.forEach(function (r, i) { r.dataset.idx = i; });
  var els = {
    seller: document.getElementById('f-seller'),
    cat: document.getElementById('f-cat'),
    karat: document.getElementById('f-karat'),
    weight: document.getElementById('f-weight'),
    sort: document.getElementById('f-sort')
  };
  var count = document.getElementById('count');
  var tbody = document.querySelector('#listings tbody');

  function val(id) { return els[id] ? els[id].value : ''; }

  function apply() {
    var s = val('seller'), c = val('cat'), k = val('karat'), w = val('weight');
    var shown = 0;
    rows.forEach(function (r) {
      var ok = (!s || r.dataset.seller === s) &&
               (!c || r.dataset.cat === c) &&
               (!k || r.dataset.karat === k) &&
               (!w || r.dataset.weight === w);
      r.classList.toggle('row-hidden', !ok);
      if (ok) shown++;
    });
    if (count) {
      count.textContent = shown + ' of ' + rows.length + ' rows shown' +
        (shown === 0 ? ' — nothing matches; clear a filter' : '') +
        (shown !== rows.length ? ' (blank cells in hidden rows are still flagged)' : '');
    }
    var sort = val('sort');
    if (!sort) {
      rows.slice().sort(function (a, b) { return a.dataset.idx - b.dataset.idx; })
          .forEach(function (r) { tbody.appendChild(r); });
      return;
    }
    var key = sort.indexOf('price') === 0 ? 'price' : 'ratio';
    var dir = sort.indexOf('asc') > -1 ? 1 : -1;
    rows.slice().sort(function (a, b) {
      var av = a.dataset[key], bv = b.dataset[key];
      if (av === '' && bv === '') return a.dataset.idx - b.dataset.idx;
      if (av === '') return 1;   // blanks always last
      if (bv === '') return -1;
      return (parseFloat(av) - parseFloat(bv)) * dir;
    }).forEach(function (r) { tbody.appendChild(r); });
  }

  Object.keys(els).forEach(function (k) {
    if (els[k]) els[k].addEventListener('change', apply);
  });
  var clear = document.getElementById('f-clear');
  if (clear) clear.addEventListener('click', function () {
    Object.keys(els).forEach(function (k) { if (els[k]) els[k].value = ''; });
    apply();
  });
  apply();
})();
