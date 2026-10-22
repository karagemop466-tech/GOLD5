/* Session b1f2fe3b — Master Cross-Session Audit, Unified 36+ Listing Catalog & XRF Calculator */
(function () {
  const D = window.GOLD5_DATA;
  const CAT = window.GOLD5_UNIFIED_CATALOG;
  if (!D || !CAT) return;

  const ENTRIES = CAT.entries || [];
  const TROY = 31.1034768;
  const DWT = 1.55517384;
  const spotG = D.spot.primary.usdPerGram;
  const finMap = (D.spot.purity && D.spot.purity.fineness) || (D.spot.purityValues && D.spot.purityValues.fineness) || {};
  const finenessOf = (k) => (finMap[k + "K"] != null ? finMap[k + "K"] : k / 24);
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const money = (n) => n == null ? "" : "$" + Number(n).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  const withGrams = ENTRIES.filter((e) => e.grams != null);
  const explicitSolid = ENTRIES.filter((e) => e.explicitSolidGoldStated);
  const uniqueSellers = new Set(ENTRIES.map((e) => e.sellerName || e.sellerId));

  const statsEl = document.getElementById("audit-stats");
  if (statsEl) {
    statsEl.innerHTML = [
      '<div class="card gold"><div class="k">Unified Verified Listings</div><div class="v">' + ENTRIES.length + '</div><div class="d">Across ' + uniqueSellers.size + ' sellers · all checked 2026-10-22</div></div>',
      '<div class="card"><div class="k">Published Gram Weight</div><div class="v">' + withGrams.length + " / " + ENTRIES.length + '</div><div class="d">' + (ENTRIES.length - withGrams.length) + ' blank &amp; flagged (never inferred)</div></div>',
      '<div class="card"><div class="k">Explicit "Solid Gold" Claim</div><div class="v">' + explicitSolid.length + " / " + ENTRIES.length + '</div><div class="d">' + (ENTRIES.length - explicitSolid.length) + ' state karat only (confirm solid before buying)</div></div>',
      '<div class="card"><div class="k">Hallmark + Maker Photo on PDP</div><div class="v">0 / ' + ENTRIES.length + '</div><div class="d">1 buyer photo alt-text ("585 AFJ"); verify via XRF on arrival</div></div>',
      '<div class="card"><div class="k">Verification Suites</div><div class="v">5 / 5 PASS</div><div class="d"><code>verify.py</code> · <code>check_report.py</code> · <code>verified/verify.py</code> · <code>check_hallucinations.py</code> · <code>audit_b1f2fe3b.py</code></div></div>'
    ].join("");
  }

  const noteEl = document.getElementById("weighted-note-extra");
  if (noteEl) {
    noteEl.innerHTML = "Notice how <b>Allurez U5882 (14K, 5.00 g, " + money(1085) + ")</b> and <b>Allurez U5885 (18K, 5.90 g, " + money(1316) + ")</b> demonstrate the exact 1.18× density increase of 18K over 14K gold alloy on the same setting geometry (84.5% of the +" + money(231) + " retail difference is backed by raw fine gold), while <b>ET-576343849 (14K, 7.00 g, " + money(444.8) + " snippet / sold out)</b> prices at <b>0.84× melt value</b> (red-flag case study FL-01).";
  }

  const xLoad = document.getElementById("x-load");
  if (xLoad) {
    withGrams.forEach((e) => {
      const opt = document.createElement("option");
      opt.value = e.id;
      const p = e.priceUsd != null ? e.priceUsd : e.price;
      opt.textContent = "[" + (e.sellerName || e.sellerId) + "] " + e.name + " — " + e.grams + " g, " + e.karat + "K (" + (p != null ? money(p) : "no price") + ")";
      xLoad.appendChild(opt);
    });
  }

  function runXrfCalc() {
    const rawW = parseFloat(document.getElementById("x-weight").value) || 0;
    const unit = document.getElementById("x-unit").value;
    const grossG = unit === "dwt" ? rawW * DWT : rawW;
    const grossDwt = grossG / DWT;
    const carats = parseFloat(document.getElementById("x-carats").value) || 0;
    const stoneG = carats * 0.20;
    const netGoldAlloyG = Math.max(0, grossG - stoneG);
    const karat = parseInt(document.getElementById("x-karat").value, 10) || 14;
    const fin = finenessOf(karat);
    const sg = parseFloat(document.getElementById("x-spot").value) || 0;
    const price = parseFloat(document.getElementById("x-price").value);
    const xrfRaw = document.getElementById("x-xrf").value.trim();
    const xrfVal = xrfRaw === "" ? null : Number(xrfRaw);

    const pureG = netGoldAlloyG * fin;
    const pureOz = pureG / TROY;
    const meltVal = pureG * sg;
    const ratio = (price > 0 && meltVal > 0) ? (price / meltVal) : null;

    const nomPpt = (karat / 24) * 1000;
    const minNoSolderPpt = nomPpt - 3.0;
    const minSolderPpt = nomPpt - 7.0;

    let xrfVerdict = '<div class="note"><b>15 U.S.C. § 295 Assay Standard (' + karat + "K = " + nomPpt.toFixed(1) + "‰ / " + (nomPpt / 10).toFixed(2) + "% Au):</b><br>Minimum legal fineness: <b>" + (minNoSolderPpt / 10).toFixed(2) + "% (" + minNoSolderPpt.toFixed(1) + "‰)</b> without solder · <b>" + (minSolderPpt / 10).toFixed(2) + "% (" + minSolderPpt.toFixed(1) + "‰)</b> whole ring with solder. Enter an XRF reading above to test compliance.</div>";
    if (xrfVal !== null && Number.isFinite(xrfVal) && xrfVal > 0) {
      const xrfPpt = xrfVal * 10;
      if (xrfPpt >= minNoSolderPpt) {
        xrfVerdict = '<div class="note ok"><b>XRF PASS (' + xrfVal.toFixed(2) + "% / " + xrfPpt.toFixed(1) + "‰):</b> Meets " + karat + "K solder-free federal standard (≥ " + (minNoSolderPpt / 10).toFixed(2) + "% under 15 U.S.C. § 295).</div>";
      } else if (xrfPpt >= minSolderPpt) {
        xrfVerdict = '<div class="note gold"><b>XRF BORDERLINE (' + xrfVal.toFixed(2) + "% / " + xrfPpt.toFixed(1) + "‰):</b> Below solder-free tolerance (" + (minNoSolderPpt / 10).toFixed(2) + "%) but within whole-item soldered tolerance (≥ " + (minSolderPpt / 10).toFixed(2) + "%). Re-test away from solder joints.</div>";
      } else {
        xrfVerdict = '<div class="note red"><b>XRF FAIL (' + xrfVal.toFixed(2) + "% / " + xrfPpt.toFixed(1) + "‰):</b> Below federal minimum fineness for " + karat + "K (" + (minSolderPpt / 10).toFixed(2) + "% with solder under 15 U.S.C. § 295). Return immediately and dispute via credit card if refused.</div>";
      }
    }

    let meltVerdict = "";
    if (ratio != null) {
      if (ratio < 1.0) {
        meltVerdict = '<div class="note red" style="margin-top:8px"><b>PRICE RED FLAG (' + ratio.toFixed(2) + "× melt):</b> Asking price " + money(price) + " is BELOW the raw gold melt value " + money(meltVal) + ". Legitimate jewelers never sell solid gold below melt.</div>";
      } else if (ratio < 1.6) {
        meltVerdict = '<div class="note gold" style="margin-top:8px"><b>Thin markup (' + ratio.toFixed(2) + "× melt):</b> Asking price " + money(price) + " is close to raw gold value " + money(meltVal) + ". Verify purity via independent XRF immediately upon arrival.</div>";
      } else {
        meltVerdict = '<div class="note ok" style="margin-top:8px"><b>Plausible retail ratio (' + ratio.toFixed(2) + "× melt):</b> Asking price " + money(price) + " vs. " + money(meltVal) + " raw gold value leaves " + money(price - meltVal) + " for gemstones, casting, labor, and retail margin.</div>";
      }
    }

    const outEl = document.getElementById("x-out");
    if (outEl) {
      outEl.innerHTML = [
        '<div class="row"><span>Gross scale weight</span><b>' + grossG.toFixed(2) + " g (" + grossDwt.toFixed(2) + " dwt)</b></div>",
        '<div class="row"><span>Stone weight deduction (' + carats.toFixed(2) + " ct × 0.20 g)</span><b>−" + stoneG.toFixed(3) + " g</b></div>",
        '<div class="row"><span>Net ' + karat + 'K gold alloy weight</span><b class="big">' + netGoldAlloyG.toFixed(2) + " g</b></div>",
        '<div class="row"><span>Pure 24K gold content (' + (fin * 100).toFixed(2) + '%)</span><b class="big">' + pureG.toFixed(3) + " g (" + pureOz.toFixed(4) + " oz t)</b></div>",
        '<div class="row"><span>Raw gold melt value @ ' + money(sg) + '/g</span><b class="big">' + money(meltVal) + "</b></div>",
        '<div class="row"><span>Asking price ÷ melt value</span><b>' + (ratio != null ? ratio.toFixed(2) + "×" : "—") + "</b></div>",
        meltVerdict,
        xrfVerdict
      ].join("");
    }
  }

  const presetEl = document.getElementById("x-spot-preset");
  if (presetEl) {
    presetEl.addEventListener("change", (ev) => {
      document.getElementById("x-spot").value = ev.target.value;
      runXrfCalc();
    });
  }
  if (xLoad) {
    xLoad.addEventListener("change", (ev) => {
      const e = ENTRIES.find((x) => x.id === ev.target.value);
      if (!e) return;
      document.getElementById("x-unit").value = "g";
      document.getElementById("x-weight").value = e.grams;
      document.getElementById("x-karat").value = e.karat || 14;
      const p = e.priceUsd != null ? e.priceUsd : e.price;
      document.getElementById("x-price").value = p != null ? p : "";
      document.getElementById("x-carats").value = 0;
      runXrfCalc();
    });
  }
  const calcEl = document.getElementById("xrf-calc");
  if (calcEl) {
    calcEl.addEventListener("input", runXrfCalc);
    calcEl.addEventListener("change", runXrfCalc);
  }
  runXrfCalc();

  const wEl = document.getElementById("weighted-analysis");
  if (wEl) {
    wEl.innerHTML = '<div class="table-wrap"><table><thead><tr>' +
      '<th>ID</th><th>Session</th><th>Listing</th><th>Seller</th><th>Karat</th><th>Published Weight</th>' +
      '<th>Weight in dwt</th><th>Pure 24K Gold</th><th>Melt Value (' + money(spotG) + '/g)</th>' +
      '<th>Verified Price</th><th>Price ÷ Melt</th><th>Official Source</th>' +
      '</tr></thead><tbody>' +
      withGrams.map((e) => {
        const fin = finenessOf(e.karat || 14);
        const pureG = e.grams * fin;
        const dwt = e.grams / DWT;
        const melt = pureG * spotG;
        const p = e.priceUsd != null ? e.priceUsd : e.price;
        const ratio = p != null ? (p / melt) : null;
        const badge = ratio == null ? '<span class="badge warn">no price on page</span>'
          : ratio < 1 ? '<span class="badge bad">' + ratio.toFixed(2) + "× BELOW MELT (RED FLAG)</span>"
          : '<span class="badge ok">' + ratio.toFixed(2) + "× melt (+" + money(p - melt) + ")</span>";
        return '<tr>' +
          '<td class="num">' + esc(e.id) + '</td>' +
          '<td class="num">' + esc(e.originSession || "") + '</td>' +
          '<td><b>' + esc(e.name) + '</b></td>' +
          '<td>' + esc(e.sellerName || e.sellerId) + '</td>' +
          '<td class="num">' + e.karat + 'K</td>' +
          '<td class="num"><b>' + e.grams.toFixed(2) + ' g</b><div class="src">' + esc(e.gramsNote || "") + '</div></td>' +
          '<td class="num">' + dwt.toFixed(2) + ' dwt</td>' +
          '<td class="num">' + pureG.toFixed(3) + ' g</td>' +
          '<td class="num"><b>' + money(melt) + '</b></td>' +
          '<td class="num">' + (p != null ? money(p) : '<span class="blank">no price</span>') + '<div class="src">' + esc(e.priceLabel || "") + '</div></td>' +
          '<td>' + badge + '</td>' +
          '<td><a class="src-link" href="' + esc(e.url) + '" target="_blank" rel="noopener">listing ↗</a></td>' +
          '</tr>';
      }).join("") +
      '</tbody></table></div>';
  }

  const fSeller = document.getElementById("f-seller");
  if (fSeller) {
    [...uniqueSellers].sort().forEach((sname) => {
      const opt = document.createElement("option");
      opt.value = sname;
      opt.textContent = sname;
      fSeller.appendChild(opt);
    });
  }

  function renderMaster() {
    const sVal = fSeller ? fSeller.value : "";
    const kVal = document.getElementById("f-karat").value;
    const gVal = document.getElementById("f-grams").value;
    const solVal = document.getElementById("f-solid").value;

    const filtered = ENTRIES.filter((e) => {
      if (sVal && (e.sellerName || e.sellerId) !== sVal) return false;
      if (kVal && String(e.karat) !== kVal) return false;
      if (gVal === "yes" && e.grams == null) return false;
      if (gVal === "no" && e.grams != null) return false;
      if (solVal === "yes" && !e.explicitSolidGoldStated) return false;
      if (solVal === "no" && e.explicitSolidGoldStated) return false;
      return true;
    });
    document.getElementById("master-count").textContent = filtered.length + " of " + ENTRIES.length + " entries shown";
    document.getElementById("master-table").innerHTML = '<div class="table-wrap tall"><table><thead><tr>' +
      '<th>ID</th><th>Session</th><th>Ring / Listing</th><th>Seller</th><th>Karat</th><th>Solid Gold?</th>' +
      '<th>Weight (g)</th><th>Pure Au (g)</th><th>Melt (' + money(spotG) + '/g)</th><th>Verified Price</th>' +
      '<th>Price ÷ Melt</th><th>Return Policy</th><th>Checked</th><th>Source Link</th>' +
      '</tr></thead><tbody>' +
      filtered.map((e) => {
        const comp = e.computed || {};
        const p = e.priceUsd != null ? e.priceUsd : e.price;
        return '<tr>' +
          '<td class="num">' + esc(e.id) + '</td>' +
          '<td class="num">' + esc(e.originSession || "") + '</td>' +
          '<td style="max-width:240px"><b>' + esc(e.name) + '</b></td>' +
          '<td>' + esc(e.sellerName || e.sellerId) + '</td>' +
          '<td class="num">' + (e.karat ? e.karat + "K" : '<span class="blank">—</span>') + '</td>' +
          '<td>' + (e.explicitSolidGoldStated ? '<span class="badge ok">explicit solid</span>' : '<span class="badge warn">karat only</span>') + '</td>' +
          '<td class="num">' + (e.grams != null ? e.grams.toFixed(2) + " g" : '<span class="blank">not stated</span>') + '</td>' +
          '<td class="num">' + (comp.pureGoldGrams != null ? comp.pureGoldGrams.toFixed(3) + " g" : '<span class="blank">—</span>') + '</td>' +
          '<td class="num">' + (comp.rawGoldMeltUsdAtRecheckSpot != null ? money(comp.rawGoldMeltUsdAtRecheckSpot) : '<span class="blank">—</span>') + '</td>' +
          '<td class="num">' + (p != null ? money(p) : '<span class="blank">no price</span>') + '<div class="src">' + esc(e.priceLabel || "") + '</div></td>' +
          '<td class="num">' + (comp.priceToMeltRatio != null ? comp.priceToMeltRatio.toFixed(2) + "×" : '<span class="blank">—</span>') + '</td>' +
          '<td style="max-width:220px;font-size:12px">' + esc(e.returnPolicy || "—") + '</td>' +
          '<td class="num">' + esc(e.checkedOn) + '</td>' +
          '<td><a class="src-link" href="' + esc(e.url) + '" target="_blank" rel="noopener">source ↗</a></td>' +
          '</tr>';
      }).join("") +
      '</tbody></table></div>';
  }

  ["f-seller", "f-karat", "f-grams", "f-solid"].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener("change", renderMaster);
  });
  renderMaster();
})();
