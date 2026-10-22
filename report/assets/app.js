/* GOLD5 dashboard — table filter + gold calculator. No dependencies, no network calls. */
(function () {
  "use strict";

  /* ---------------- listings filter ---------------- */
  var table = document.getElementById("listings");
  if (table) {
    var q = document.getElementById("q");
    var onlyWeight = document.getElementById("onlyWeight");
    var count = document.getElementById("count");
    var rows = Array.prototype.slice.call(table.tBodies[0].rows);

    function apply() {
      var term = (q && q.value || "").trim().toLowerCase();
      var needW = !!(onlyWeight && onlyWeight.checked);
      var shown = 0;
      rows.forEach(function (tr) {
        var text = tr.textContent.toLowerCase();
        var weightCell = tr.cells[4] ? tr.cells[4].textContent.trim() : "";
        var hasW = weightCell && weightCell !== "—";
        var ok = (!term || text.indexOf(term) !== -1) && (!needW || hasW);
        tr.style.display = ok ? "" : "none";
        if (ok) shown++;
      });
      if (count) count.textContent = shown + " of " + rows.length + " rows shown";
    }
    if (q) q.addEventListener("input", apply);
    if (onlyWeight) onlyWeight.addEventListener("change", apply);
    apply();
  }

  /* ---------------- gold calculator ---------------- */
  var w = document.getElementById("cw");
  var k = document.getElementById("ck");
  var s = document.getElementById("cs");
  var p = document.getElementById("cp");
  var out = document.getElementById("cout");
  if (!w || !k || !s || !out) return;

  var TROY = 31.1034768;

  function usd(x, dp) {
    return "$" + x.toLocaleString("en-US", { minimumFractionDigits: dp, maximumFractionDigits: dp });
  }
  function num(el) {
    var v = parseFloat(el.value);
    return isFinite(v) && v >= 0 ? v : null;
  }

  function render() {
    var grams = num(w), karat = parseFloat(k.value), spot = num(s), price = num(p);
    if (grams === null || spot === null) {
      out.innerHTML = '<div class="cell"><div class="k">Waiting for input</div><div class="v">—</div></div>';
      return;
    }
    var fine = grams * karat / 24;
    var melt = fine * spot;
    if (!(melt > 0)) {
      out.innerHTML = '<div class="cell"><div class="k">Enter a weight above zero</div><div class="v">—</div></div>';
      return;
    }
    calc.fine = fine; calc.melt = melt; calc.premium = null;
    var cells = [
      ["Fine gold", fine.toFixed(4) + " g", ""],
      ["Gold in troy ounces", (grams / TROY).toFixed(4) + " oz", ""],
      ["Metal value at spot", usd(melt, 2), ""],
      ["Gold content", (karat / 24 * 100).toFixed(2) + "% of the weight", ""]
    ];
    if (price !== null && price > 0) {
      var prem = price / melt;
      calc.premium = prem;
      cells.push(["Price ÷ metal value", prem.toFixed(2) + "×", prem < 1 ? "red" : ""]);
      cells.push(["Not gold (stones, labour, margin)", usd(price - melt, 2), ""]);
      cells.push(["Price per fine gram", usd(price / fine, 2), ""]);
      cells.push([prem < 1 ? "Below metal value — fraud signal" : "Above metal value — expected retail",
                  prem < 1 ? "yes" : "normal", prem < 1 ? "red" : "green"]);
    }
    out.innerHTML = cells.map(function (c) {
      return '<div class="cell"><div class="k">' + c[0] + '</div><div class="v ' + c[2] + '">' + c[1] + "</div></div>";
    }).join("");
  }
  var calc = {};
  [w, k, s, p].forEach(function (el) { el.addEventListener("input", render); el.addEventListener("change", render); });
  render();
})();
