/* GOLD5 — shared rendering (no build step, no external deps) */
(function () {
  const D = window.GOLD5_DATA;
  if (!D) { document.body.innerHTML = "<p style='padding:40px'>Data file missing (site/assets/data.js).</p>"; return; }

  const TROY_OZ_GRAMS = 31.1034768;
  const spot = D.spot.primary;
  const finenessOf = (k) => (D.spot.purityValues.fineness[k + "K"] != null ? D.spot.purityValues.fineness[k + "K"] : k / 24);

  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const money = (n) => n == null ? "" : "$" + Number(n).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const money0 = (n) => n == null ? "" : "$" + Math.round(n).toLocaleString("en-US");
  const seller = (id) => D.sellers.find((s) => s.id === id) || { name: id };
  const flagById = (id) => D.flags.find((f) => f.id === id);

  const NAV = [
    ["index.html", "Dashboard", "home"],
    ["site/listings.html", "Listings", "listings"],
    ["site/gold-price.html", "Gold Price", "gold-price"],
    ["site/calculator.html", "Calculator", "calculator"],
    ["site/checklist.html", "Checklist", "checklist"],
    ["site/sellers.html", "Sellers", "sellers"],
    ["site/flagged.html", "Flagged for Review", "flagged"],
    ["site/sources.html", "Sources", "sources"]
  ];

  function baseDir() {
    const p = location.pathname;
    // pages under /site/ go up one level
    return p.split("/").length >= 2 && /\/site\//.test(p) ? "../" : "";
  }

  function chrome(active) {
    const b = baseDir();
    document.body.insertAdjacentHTML("afterbegin", `
      <div class="banner"><div class="wrap">
        <span><strong>⚠ NO HALLUCINATIONS</strong> — every value on this site was verified from a linked official source on the check date. Blank cells = unverified (flagged, never inferred).</span>
        <span>After every review: <a href="${b}site/sources.html">re-run the verification pass</a> · data as of <b>${esc(D.meta.asOf)}</b></span>
      </div></div>`);
    document.body.insertAdjacentHTML("afterbegin", `
      <header class="site"><div class="wrap">
        <h1>GOLD5<span class="dot">·</span>Gold Ring Research</h1>
        <span class="sub">Solid gold engagement rings — collected, verified line-by-line, priced against the gold market</span>
      </div></header>`);
    document.body.insertAdjacentHTML("afterbegin", `
      <nav class="main"><div class="wrap">
        ${NAV.map(([href, label, key]) => `<a href="${b}${href}" class="${key === active ? "active" : ""}">${label}</a>`).join("")}
      </div></nav>`);
    document.body.insertAdjacentHTML("beforeend", `
      <footer class="site"><div class="wrap">
        <span>GOLD5 · verified ${esc(D.meta.asOf)} by ${esc(D.meta.checkedBy)}</span>
        <span>Verification harness: <code>python3 scripts/verify.py</code> (repo root)</span>
        <span><a href="${b}site/flagged.html">Flagged for Review</a></span>
      </div></footer>`);
    // move banner/header/nav to top in order
    const banner = document.querySelector(".banner");
    const header = document.querySelector("header.site");
    const nav = document.querySelector("nav.main");
    document.body.prepend(nav); document.body.prepend(header); document.body.prepend(banner);
  }

  /* ---------- badges ---------- */
  const FLAG_LABELS = {
    "no-gram-weight": ["gray", "no gram weight"],
    "price-below-metal-value": ["bad", "PRICE < METAL VALUE"],
    "off-platform-contact-in-listing-photos": ["bad", "off-platform contact in photos"],
    "grams-from-search-snippet": ["warn", "grams via snippet"],
    "price-from-search-snippet": ["warn", "price via snippet"],
    "sold-at-check": ["gray", "sold at check"],
    "cross-border-shipping": ["info", "cross-border"]
  };
  function flagBadges(flags) {
    return (flags || []).map((f) => {
      const [tone, label] = FLAG_LABELS[f] || ["gray", f];
      return `<span class="badge ${tone}">${esc(label)}</span>`;
    }).join(" ");
  }

  /* ---------- listings table ---------- */
  function listingsTable(rows) {
    return `<div class="table-scroll"><table>
      <thead><tr>
        <th>Ring / listing</th><th>Seller</th><th>Karat</th><th>Grams</th>
        <th>Price (verified)</th><th>Price vs. gold</th><th>Solid-gold claim</th>
        <th>Hallmark / maker</th><th>Return policy</th><th>Reputation</th>
        <th>Checked</th><th>Source link</th><th>Status</th>
      </tr></thead>
      <tbody>
      ${rows.map((e) => {
        const f = finenessOf(e.karat);
        const metal = e.grams != null ? e.grams * f : null;
        const metalVal = metal != null ? metal * spot.usdPerGram : null;
        const ratio = (metalVal != null && e.price != null) ? e.price / metalVal : null;
        let vs = '<span class="blank">n/a — no weight</span>';
        if (ratio != null) {
          const tone = ratio < 1 ? "bad" : ratio < 1.6 ? "warn" : "ok";
          const word = ratio < 1 ? "BELOW metal value — red flag" : ratio < 1.6 ? "thin margin for a ring" : "above metal value";
          vs = `<span class="num">${ratio.toFixed(2)}×</span> <span class="badge ${tone}">${word}</span><div class="src" style="color:var(--muted);font-size:11.5px">metal ≈ ${money(metalVal)} @ ${money(spot.usdPerGram)}/g</div>`;
        }
        const s = seller(e.sellerId);
        const status = e.status === "flagged"
          ? `<span class="badge bad">flagged</span>`
          : `<span class="badge ok">verified</span>`;
        return `<tr>
          <td><b>${esc(e.name)}</b><br><span class="src"><a href="${esc(e.url)}" target="_blank" rel="noopener">${esc(e.url)}</a></span></td>
          <td>${esc(s.name)}<br><span class="src"><a href="${esc(s.website)}" target="_blank" rel="noopener">profile</a></span></td>
          <td class="num">${e.karat}K ${esc(e.metalColor || "")}</td>
          <td>${e.grams != null ? `<span class="num">${e.grams} g</span>` : '<span class="blank">—</span>'}<div class="src" style="font-size:11px;color:var(--muted)">${esc(e.gramsNote || "")}</div></td>
          <td class="num">${e.price != null ? money(e.price) : '<span class="blank">—</span>'}<div class="src" style="font-size:11.5px;color:var(--muted)">${esc(e.priceLabel || "")}</div></td>
          <td>${vs}</td>
          <td style="max-width:220px">${esc(e.solidGold || "")}</td>
          <td style="max-width:180px">${esc(e.hallmark || "—")}${e.makerMark ? "<br>" + esc(e.makerMark) : ""}</td>
          <td style="max-width:200px">${esc(e.returnPolicy || "—")} ${e.returnUrl ? `<div class="src"><a href="${esc(e.returnUrl)}" target="_blank" rel="noopener">policy</a></div>` : ""}</td>
          <td>${esc(e.reviewScore || "—")}</td>
          <td class="num">${esc(e.checkedOn || "—")}</td>
          <td><a class="src" href="${esc(e.url)}" target="_blank" rel="noopener">official listing ↗</a></td>
          <td>${status} <span class="badges">${flagBadges(e.flags)}</span></td>
        </tr>`;
      }).join("")}
      </tbody></table></div>`;
  }

  /* ---------- gold price table ---------- */
  function spotTable() {
    const all = [
      { ...spot, primary: true },
      ...D.spot.crossChecks
    ];
    return `<div class="table-scroll"><table>
      <thead><tr><th>Source</th><th>USD / oz</th><th>USD / g</th><th>As of</th><th>How captured</th><th>Link</th></tr></thead>
      <tbody>
      ${all.map((q) => `<tr>
        <td><b>${esc(q.source)}</b>${q.primary ? ' <span class="badge ok">primary (used for calcs)</span>' : ""}</td>
        <td class="num">${money(q.usdPerOz)}</td>
        <td class="num">${q.usdPerGram != null ? money(q.usdPerGram) : '<span class="blank">—</span>'}</td>
        <td class="num">${esc(q.asOf)}</td>
        <td>${esc(q.kind || "")}${q.note ? `<div class="src" style="font-size:11.5px;color:var(--muted)">“${esc(q.note)}”</div>` : ""}</td>
        <td><a class="src" href="${esc(q.url)}" target="_blank" rel="noopener">source ↗</a></td>
      </tr>`).join("")}
      </tbody></table></div>
      <p class="note">Same-day cross-check: quotes agree within ~1.6%. The primary quote (Kitco, direct page fetch, latest timestamp) is used for every calculation on this site. Gram values were published by the source; consistency check: ${money(spot.usdPerOz)} ÷ ${TROY_OZ_GRAMS} g = ${money(spot.usdPerOz / TROY_OZ_GRAMS)} ≈ ${money(spot.usdPerGram)}. <b>Re-check before you buy — spot moves all day.</b></p>`;
  }

  function purityTable() {
    const p = D.spot.purityValues;
    const perG = (k) => (p.perOunce[k] / TROY_OZ_GRAMS);
    return `<div class="table-scroll"><table>
      <thead><tr><th>Fineness</th><th>Gold %</th><th>USD / oz (Kitco table)</th><th>USD / g (derived)</th><th>Stamp</th></tr></thead>
      <tbody>
      ${["24K", "22K", "18K", "14K", "10K"].map((k) => `<tr>
        <td><b>${k}</b></td>
        <td class="num">${(p.fineness[k] * 100).toFixed(2)}%</td>
        <td class="num">${money(p.perOunce[k])}</td>
        <td class="num">${money(perG(k))}</td>
        <td class="num">${k === "24K" ? "999" : k === "22K" ? "916/917" : k === "18K" ? "750" : k === "14K" ? "585" : "417"}</td>
      </tr>`).join("")}
      </tbody></table></div>
      <p class="note">Per-ounce values and fineness from the ${esc(p.source)} <a href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.url)}</a>. USD/g derived (÷ 31.1034768 g/oz). Stamps per 16 CFR Part 23 / FTC guides.</p>`;
  }

  /* ---------- calculator ---------- */
  function calculator() {
    const el = document.getElementById("calc");
    if (!el) return;
    el.innerHTML = `
      <div class="calc-grid">
        <div class="calc-box">
          <h3 style="margin-top:0">What are you paying for the gold itself?</h3>
          <label>Ring weight (grams)</label>
          <input id="c-weight" type="number" step="0.01" min="0" placeholder="e.g. 3.7">
          <label>Karat</label>
          <select id="c-karat">
            <option value="14" selected>14K (58.33%)</option>
            <option value="18">18K (75.00%)</option>
            <option value="10">10K (41.67%)</option>
            <option value="22">22K (91.67%)</option>
          </select>
          <label>Gold spot (USD / gram)</label>
          <input id="c-spot" type="number" step="0.01" min="0" value="${spot.usdPerGram}">
          <p class="note">Pre-filled from the verified primary quote: ${esc(spot.source)}, ${esc(spot.asOf)} — <a href="${esc(spot.url)}" target="_blank" rel="noopener">${esc(spot.url)}</a></p>
          <label>Paid price (USD, optional)</label>
          <input id="c-price" type="number" step="0.01" min="0" placeholder="e.g. 969">
          <label>Load a verified listing</label>
          <select id="c-load">
            <option value="">— choose —</option>
            ${D.entries.filter((e) => e.grams != null).map((e) => `<option value="${e.id}">${esc(e.name)} (${e.grams} g)</option>`).join("")}
          </select>
        </div>
        <div class="calc-box calc-out" id="c-out"></div>
      </div>`;
    const out = document.getElementById("c-out");
    const get = (id) => document.getElementById(id).value;
    function calc() {
      const w = parseFloat(get("c-weight")) || 0;
      const k = parseInt(get("c-karat"), 10);
      const sg = parseFloat(get("c-spot")) || 0;
      const price = parseFloat(get("c-price"));
      const f = finenessOf(k);
      const goldG = w * f;
      const oz = goldG / TROY_OZ_GRAMS;
      const val = goldG * sg;
      let verdict = "";
      if (w > 0 && sg > 0) {
        verdict = `<div class="verdict ${price != null ? (price / val < 1 ? "risk" : price / val < 1.6 ? "okay" : "good") : "okay"}">`;
        verdict += `<b>Raw gold content:</b> ${w} g × ${(f * 100).toFixed(2)}% = <b>${goldG.toFixed(2)} g</b> of pure gold (${oz.toFixed(4)} troy oz).<br>`;
        verdict += `<b>Metal value at spot:</b> ${money(val)}.`;
        if (price != null && price > 0) {
          const r = price / val;
          if (r < 1) verdict += ` Your price ${money(price)} is <b>below</b> the metal value (${r.toFixed(2)}×) — <b>red flag</b>, do not buy: no legitimate seller sells solid gold below melt.`;
          else if (r < 1.6) verdict += ` Price ${money(price)} is only ${r.toFixed(2)}× the metal value — thin for labor/design; scrutinize seller and request XRF testing.`;
          else verdict += ` Price ${money(price)} is ${r.toFixed(2)}× metal value — plausible room for stone(s), labor, and design. Still verify purity independently after delivery.`;
        } else {
          verdict += ` Enter the paid price to see the price-to-metal ratio.`;
        }
        verdict += `</div>`;
      }
      out.innerHTML = `
        <div class="row"><span>Pure gold content</span><b class="big">${goldG.toFixed(3)} g</b></div>
        <div class="row"><span>In troy ounces</span><b>${oz.toFixed(4)} oz</b></div>
        <div class="row"><span>Spot price used</span><b>${money(sg)}/g</b></div>
        <div class="row"><span>Raw gold (metal) value</span><b class="big">${money(val)}</b></div>
        <div class="row"><span>Price paid</span><b>${price != null && price > 0 ? money(price) : "—"}</b></div>
        <div class="row"><span>Price ÷ metal value</span><b>${price != null && val > 0 ? (price / val).toFixed(2) + "×" : "—"}</b></div>
        ${verdict}
        <p class="note" style="margin-top:12px">Formula: gold&nbsp;g = weight&nbsp;g × karat/24 · value = gold&nbsp;g × spot&nbsp;$/g · 1 troy oz = ${TROY_OZ_GRAMS} g. Values computed live in your browser from raw inputs — nothing pre-stored, nothing inferred.</p>`;
    }
    el.addEventListener("input", calc);
    el.addEventListener("change", calc);
    document.getElementById("c-load").addEventListener("change", (ev) => {
      const e = D.entries.find((x) => x.id === ev.target.value);
      if (!e) return;
      document.getElementById("c-weight").value = e.grams;
      document.getElementById("c-karat").value = e.karat;
      document.getElementById("c-price").value = e.price;
      calc();
    });
    calc();
  }

  /* ---------- sellers ---------- */
  function sellersCards() {
    return D.sellers.map((s) => `
      <div class="card" style="margin-bottom:14px">
        <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px">
          <b style="font-size:15px">${esc(s.name)}</b>
          <span><a href="${esc(s.website)}" target="_blank" rel="noopener">website ↗</a> ${s.bbb ? ' · <a href="' + esc(s.bbb.url) + '" target="_blank" rel="noopener">BBB ↗</a>' : ""}</span>
        </div>
        <div class="kv" style="margin-top:10px">
          ${s.phone ? `<div><b>Phone</b> ${esc(s.phone)}</div>` : ""}
          ${s.email ? `<div><b>Email</b> ${esc(s.email)}</div>` : ""}
          ${s.hqNote ? `<div><b>HQ / notes</b> ${esc(s.hqNote)}</div>` : ""}
          ${s.bbb ? `<div><b>BBB</b> ${esc(s.bbb.rating)} · ${s.bbb.complaints3yr} complaints / 3 yrs (${esc(s.bbb.complaints12mo || "")}) · BBB reviews avg ${esc(s.bbb.bbbReviewAvg || "n/a")} <span class="src">(captured ${esc(s.bbb.checkedOn)} via ${esc(s.bbb.via)})</span></div>` : `<div><b>BBB</b> <span class="blank">n/a (Etsy shop — use shop reviews + purchase protection)</span></div>`}
          ${s.otherReputation && s.otherReputation.length ? `<div><b>Other reviews</b> ${s.otherReputation.map((r) => `<a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.note)}</a>`).join(" · ")}</div>` : ""}
          <div><b>Return policy</b> ${esc(s.returnPolicy.summary)} <a href="${esc(s.returnPolicy.url)}" target="_blank" rel="noopener">policy ↗</a></div>
          <div><b>Warranty</b> ${esc(s.warranty.summary)} ${s.warranty.url ? `<a href="${esc(s.warranty.url)}" target="_blank" rel="noopener">↗</a>` : ""}</div>
          <div><b>Payment</b> ${esc(s.payment)}</div>
        </div>
      </div>`).join("");
  }

  /* ---------- flags ---------- */
  function flagCards() {
    const order = { high: 0, medium: 1, low: 2, info: 3 };
    return [...D.flags].sort((a, b) => order[a.severity] - order[b.severity]).map((f) => `
      <div class="flag ${f.severity}" id="${f.id}">
        <h4><span class="badge ${f.severity === "high" ? "bad" : f.severity === "medium" ? "warn" : f.severity === "low" ? "info" : "gray"}">${f.severity}</span>&nbsp; ${esc(f.id)} — ${esc(f.title)}</h4>
        <p style="font-size:13.5px;margin:6px 0">${esc(f.detail)}</p>
        <div class="meta">Source: ${/https?:/.test(f.source) ? `<a href="${esc(f.source)}" target="_blank" rel="noopener">${esc(f.source)}</a>` : esc(f.source)} · Status: ${esc(f.status)} · Entries: ${(f.entryIds || []).join(", ") || "—"}</div>
      </div>`).join("");
  }

  /* ---------- sources ---------- */
  function sourcesTable() {
    const rows = [];
    const push = (what, url, how, date) => rows.push([what, url, how, date]);
    D.spot.primary && push(`Primary spot price: ${money(D.spot.primary.usdPerOz)}/oz, ${money(D.spot.primary.usdPerGram)}/g (${D.spot.primary.asOf})`, D.spot.primary.url, D.spot.primary.method, D.meta.asOf);
    D.spot.crossChecks.forEach((q) => push(`Cross-check spot: ${money(q.usdPerOz)}/oz (${q.asOf})`, q.url, "search snippet of official page", D.meta.asOf));
    push("Karat fineness & per-ounce purity values (24K/22K/18K/14K/10K)", D.spot.purityValues.url, D.spot.purityValues.method, D.meta.asOf);
    D.entries.forEach((e) => push(`Listing: ${e.name} — ${e.price != null ? money(e.price) : "n/a"}${e.grams != null ? `, ${e.grams} g` : ""}`, e.url, (e.flags || []).includes("price-from-search-snippet") ? "direct page fetch (sold) / price via search snippet" : "direct page fetch", e.checkedOn));
    D.sellers.forEach((s) => {
      (s.sources || []).forEach((u) => push(`Seller facts: ${s.name}`, u, "direct fetch / search snippet", s.checkedOn));
    });
    D.references.forEach((r) => push(`Reference: ${r.title}`, r.url, r.method, r.checkedOn));
    return `<div class="table-scroll"><table>
      <thead><tr><th>What it verifies</th><th>Source URL</th><th>How captured</th><th>Date</th></tr></thead>
      <tbody>
      ${rows.map((r) => `<tr><td>${esc(r[0])}</td><td><a href="${esc(r[1])}" target="_blank" rel="noopener">${esc(r[1])}</a></td><td>${esc(r[2])}</td><td class="num">${esc(r[3])}</td></tr>`).join("")}
      </tbody></table></div>`;
  }

  window.GOLD5 = { D, chrome, listingsTable, spotTable, purityTable, calculator, sellersCards, flagCards, sourcesTable, money, esc, finenessOf };
})();
