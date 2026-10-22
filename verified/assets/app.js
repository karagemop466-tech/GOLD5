/* GOLD5 — table filtering, sorting, nav toggle and the gold calculator.
   All arithmetic mirrors the formula printed on the page and the captured spot value. */
(function () {
  "use strict";

  // ---------------------------------------------------------------- nav
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // -------------------------------------------------------------- tables
  document.querySelectorAll("[data-tools]").forEach(function (bar) {
    var scope = bar.parentElement;
    var table = scope.querySelector("table.data-table");
    var status = scope.querySelector("[data-table-status]");
    if (!table) return;
    var tbody = table.querySelector("tbody");
    var rows = Array.prototype.slice.call(tbody.querySelectorAll("tr.ring-row"));

    var q = bar.querySelector(".tool-search");
    var karat = bar.querySelector(".tool-karat");
    var solid = bar.querySelector(".tool-solid");
    var price = bar.querySelector(".tool-price");
    var sort = bar.querySelector(".tool-sort");
    var reset = bar.querySelector(".tool-reset");

    function matches(row) {
      if (q && q.value) {
        var needle = q.value.trim().toLowerCase();
        if (needle && row.dataset.search.indexOf(needle) === -1) return false;
      }
      if (karat && karat.value && row.dataset.karat !== karat.value) return false;
      if (solid && solid.value && row.dataset.solid !== solid.value) return false;
      if (price && price.value) {
        var raw = row.dataset.price;
        if (price.value === "unverified") {
          if (raw !== "") return false;
        } else {
          if (raw === "") return false;
          var value = parseFloat(raw);
          var bounds = price.value.split("-").map(parseFloat);
          if (value < bounds[0] || value >= bounds[1]) return false;
        }
      }
      return true;
    }

    function apply() {
      var shown = 0;
      rows.forEach(function (row) {
        var ok = matches(row);
        row.hidden = !ok;
        if (ok) shown += 1;
      });
      if (status) {
        var total = rows.length;
        status.textContent = shown === total
          ? "Showing all " + total + " entries."
          : "Showing " + shown + " of " + total + " entries.";
      }
    }

    function sortRows() {
      if (!sort || !sort.value) return;
      var mode = sort.value;
      var sorted = rows.slice().sort(function (a, b) {
        if (mode === "seller") return a.dataset.seller.localeCompare(b.dataset.seller);
        if (mode === "karat") return parseInt(a.dataset.karat || "0", 10) - parseInt(b.dataset.karat || "0", 10);
        var ap = a.dataset.price === "" ? Infinity : parseFloat(a.dataset.price);
        var bp = b.dataset.price === "" ? Infinity : parseFloat(b.dataset.price);
        return mode === "price-desc" ? bp - ap : ap - bp;
      });
      sorted.forEach(function (row) { tbody.appendChild(row); });
    }

    [q, karat, solid, price].forEach(function (el) {
      if (el) el.addEventListener("input", apply);
      if (el) el.addEventListener("change", apply);
    });
    if (sort) sort.addEventListener("change", function () { sortRows(); apply(); });
    if (reset) {
      reset.addEventListener("click", function () {
        if (q) q.value = "";
        if (karat) karat.value = "";
        if (solid) solid.value = "";
        if (price) price.value = "";
        if (sort) sort.value = "";
        rows.forEach(function (row) { tbody.appendChild(row); });
        apply();
      });
    }
    apply();
  });

  // --------------------------------------------------------- calculator
  var calc = document.getElementById("calculator");
  if (calc) {
    var oz = 31.1034768;
    var spot = parseFloat(calc.dataset.spot);
    var perGram = spot / oz;
    var grams = document.getElementById("calc-grams");
    var karatSel = document.getElementById("calc-karat");
    var priceIn = document.getElementById("calc-price");
    var outFine = document.getElementById("out-fine");
    var outValue = document.getElementById("out-value");
    var outMult = document.getElementById("out-mult");
    var outNote = document.getElementById("out-note");

    var money = function (n) {
      return "$" + n.toLocaleString("en-US", { maximumFractionDigits: 2, minimumFractionDigits: 2 });
    };

    function update() {
      var g = parseFloat(grams.value);
      var k = parseFloat(karatSel.value);
      if (!isFinite(g) || g < 0) {
        outFine.textContent = "—";
        outValue.textContent = "—";
        outMult.textContent = "—";
        return;
      }
      var fine = g * (k / 24);
      var melt = fine * perGram;
      outFine.textContent = fine.toFixed(2) + " g";
      outValue.textContent = money(melt);
      var paid = parseFloat(priceIn.value);
      if (isFinite(paid) && paid > 0 && melt > 0) {
        outMult.textContent = (paid / melt).toFixed(2) + "×";
        outNote.textContent = paid < melt
          ? "The price is below the melt value of that weight — a red flag. Re-check the weight and the karat in writing."
          : "Multiplier = price paid ÷ melt value at the captured spot. It is a sanity check, not an appraisal.";
      } else {
        outMult.textContent = "—";
        outNote.textContent = "Enter the price you were quoted to see how many times the metal value you are being asked to pay.";
      }
    }

    [grams, karatSel, priceIn].forEach(function (el) {
      el.addEventListener("input", update);
      el.addEventListener("change", update);
    });
    update();
  }
})();
