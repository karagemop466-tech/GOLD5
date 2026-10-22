/* GOLD5 dashboard behaviour. No dependencies, no network calls, no tracking.
   Everything runs locally in the browser. */
(function () {
  "use strict";

  /* ---------- entry tables: filter + sort ---------- */
  var tbl = document.getElementById("tbl");
  if (tbl) {
    var q = document.getElementById("q"),
        fc = document.getElementById("fcat"),
        ft = document.getElementById("ftier"),
        fw = document.getElementById("fweight"),
        fp = document.getElementById("fprice"),
        cnt = document.getElementById("count");
    var bodyRows = Array.prototype.slice.call(tbl.tBodies[0].rows);

    function apply() {
      var term = (q.value || "").toLowerCase().trim(),
          shown = 0, priced = 0, weighted = 0;
      bodyRows.forEach(function (tr) {
        var ok = true;
        if (term && (tr.getAttribute("data-search") || "").indexOf(term) < 0) ok = false;
        if (fc.value && tr.getAttribute("data-cat") !== fc.value) ok = false;
        if (ft.value && tr.getAttribute("data-tier") !== ft.value) ok = false;
        if (fw.checked && tr.getAttribute("data-weight") !== "1") ok = false;
        if (fp.checked && tr.getAttribute("data-price") === "") ok = false;
        tr.style.display = ok ? "" : "none";
        if (ok) {
          shown++;
          if (tr.getAttribute("data-price") !== "") priced++;
          if (tr.getAttribute("data-weight") === "1") weighted++;
        }
      });
      if (cnt) cnt.textContent = shown + " of " + bodyRows.length + " rows shown · " +
        priced + " with a sourced price · " + weighted + " with a published gram weight";
    }
    [q, fc, ft].forEach(function (el) { el && el.addEventListener("input", apply); });
    [fw, fp].forEach(function (el) { el && el.addEventListener("change", apply); });
    apply();

    /* click a header to sort */
    Array.prototype.slice.call(tbl.tHead.rows[0].cells).forEach(function (th, idx) {
      th.style.cursor = "pointer";
      th.title = "Click to sort";
      var asc = true;
      th.addEventListener("click", function () {
        var sorted = bodyRows.slice().sort(function (a, b) {
          var x = a.cells[idx] ? a.cells[idx].textContent.trim() : "",
              y = b.cells[idx] ? b.cells[idx].textContent.trim() : "";
          var nx = parseFloat(x.replace(/[^0-9.\-]/g, "")),
              ny = parseFloat(y.replace(/[^0-9.\-]/g, ""));
          var both = !isNaN(nx) && !isNaN(ny) && x !== "— blank —" && y !== "— blank —";
          if (both) return asc ? nx - ny : ny - nx;
          return asc ? x.localeCompare(y) : y.localeCompare(x);
        });
        sorted.forEach(function (tr) { tbl.tBodies[0].appendChild(tr); });
        bodyRows = sorted;
        asc = !asc;
      });
    });
  }

  /* ---------- gold calculator ---------- */
  var TROY_OZ_GRAMS = 31.1034768;   /* NIST */
  var DWT_GRAMS = 1.55517384;       /* NIST */
  var wEl = document.getElementById("c-weight"),
      kEl = document.getElementById("c-karat"),
      fEl = document.getElementById("c-fineness"),
      pEl = document.getElementById("c-price"),
      rEl = document.getElementById("c-retail"),
      exEl = document.getElementById("c-example"),
      grossEl = document.getElementById("c-gross"),
      out = document.getElementById("c-out");

  function fmt(n, d) { return isNaN(n) ? "—" : n.toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d }); }
  function usd(n) { return isNaN(n) ? "—" : "$" + fmt(n, 2); }

  function calc() {
    if (!out) return;
    var w = parseFloat(wEl.value), k = parseFloat(kEl.value), p = parseFloat(pEl.value),
        rr = rEl.value === "" ? NaN : parseFloat(rEl.value);
    var fin = k / 24 * 100;
    if (fEl.value !== "") { fin = parseFloat(fEl.value); k = fin / 100 * 24; }
    var pure = isNaN(w) || isNaN(fin) ? NaN : w * fin / 100;
    var ozt = isNaN(pure) ? NaN : pure / TROY_OZ_GRAMS;
    var dwt = isNaN(pure) ? NaN : pure / DWT_GRAMS;
    var val = isNaN(pure) || isNaN(p) ? NaN : ozt * p;
    var perG = isNaN(p) ? NaN : p / TROY_OZ_GRAMS;

    function row(label, value, note) {
      return "<tr><td>" + label + "</td><td class='num'>" + value + "</td><td class='small'>" + (note || "") + "</td></tr>";
    }
    var h = "<table><tbody>";
    h += row("Alloy fineness", fmt(fin, 2) + " %", "karat &divide; 24 &times; 100");
    h += row("Total weight entered", fmt(w, 3) + " g", grossEl && grossEl.checked ?
      "<b>declared as GROSS weight (stones included)</b> &mdash; pure-gold result is an over-estimate" : "assumed metal-only weight");
    h += row("Pure gold content", fmt(pure, 3) + " g", "total weight &times; fineness");
    h += row("Pure gold content", fmt(ozt, 5) + " troy oz", "pure grams &divide; 31.1034768 (NIST)");
    h += row("Pure gold content", fmt(dwt, 3) + " dwt", "pure grams &divide; 1.55517384 (NIST)");
    h += row("Gold price used", usd(p) + " / troy oz", isNaN(perG) ? "enter a price" : "= " + usd(perG) + " per gram of pure gold");
    h += row("<b>Intrinsic gold value</b>", "<b>" + usd(val) + "</b>", "metal only &mdash; excludes labour, design, brand and stones");
    if (!isNaN(rr)) {
      h += row("Asking price", usd(rr), "the price you were quoted");
      h += row("Premium over gold content", usd(rr - val), "asking price &minus; intrinsic gold value");
      h += row("Asking price as a multiple of gold content", fmt(rr / val, 2) + " &times;",
        val > 0 ? "normal for finished jewellery; a value far below 1&times; is a red flag" : "");
    } else {
      h += row("Asking price", "&mdash; blank &mdash;", "optional: enter it to see the premium over gold content");
    }
    h += "</tbody></table>";
    out.innerHTML = h;
  }

  if (wEl) {
    [wEl, kEl, fEl, pEl, rEl].forEach(function (el) { el.addEventListener("input", calc); });
    if (grossEl) grossEl.addEventListener("change", calc);
    if (fEl) fEl.addEventListener("input", function () { if (fEl.value !== "") kEl.value = ""; });
    if (kEl) kEl.addEventListener("input", function () { if (kEl.value !== "") fEl.value = ""; });
    if (exEl) exEl.addEventListener("change", function () {
      if (!exEl.value) return;
      var d = JSON.parse(exEl.value);
      wEl.value = d.w; kEl.value = d.k; fEl.value = "";
      var t = document.getElementById("c-example-src");
      if (t) t.innerHTML = "Loaded from <b>" + d.id + "</b> (" + d.ret + "): seller-published weight " + d.w +
        " g at " + d.k + ". Source: <a href='" + d.url + "' target='_blank' rel='noopener noreferrer'>" + d.url + "</a>" +
        " &mdash; observed " + d.at + " UTC. <b>Confirm the weight with the seller before relying on it.</b>";
      calc();
    });
    /* observation buttons: fill the price from a sourced, timestamped observation */
    Array.prototype.forEach.call(document.querySelectorAll("[data-fill-price]"), function (b) {
      b.addEventListener("click", function () {
        pEl.value = b.getAttribute("data-fill-price");
        var t = document.getElementById("c-price-src");
        if (t) t.innerHTML = "Price loaded from <b>" + b.getAttribute("data-src-pub") + "</b>, " +
          b.getAttribute("data-src-asof") + ". Source: <a href='" + b.getAttribute("data-src-url") +
          "' target='_blank' rel='noopener noreferrer'>" + b.getAttribute("data-src-url") +
          "</a>. This is a past observation, not a live quote &mdash; re-check before paying.";
        calc();
      });
    });
    calc();
  }
})();
