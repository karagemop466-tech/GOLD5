const money = (value, currency = 'USD') => typeof value === 'number' && Number.isFinite(value)
  ? new Intl.NumberFormat('en-US', { style: 'currency', currency, maximumFractionDigits: 2 }).format(value)
  : '';
const cellText = value => value === null || value === undefined || value === '' ? 'Unverified — blank' : String(value);
function addTextCell(row, text, className = '') {
  const td = document.createElement('td');
  if (className) td.className = className;
  td.textContent = text;
  row.append(td);
  return td;
}
function addSourceCell(row, records) {
  const td = document.createElement('td');
  for (const [record, label] of records) {
    if (!record) continue;
    const link = document.createElement('a');
    link.href = record.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.className = 'source-link';
    link.textContent = label;
    td.append(link, document.createTextNode(' '));
  }
  row.append(td);
}
async function loadJson(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Could not load ${path}: ${response.status}`);
  return response.json();
}
function productRow(product, source, returnSource, reputationSources) {
  const row = document.createElement('tr');
  const name = addTextCell(row, product.name, 'primary-cell');
  const sub = document.createElement('span');
  sub.className = 'sub-cell';
  sub.textContent = product.productType;
  name.append(sub);
  addTextCell(row, cellText(product.listedMetal));
  addTextCell(row, cellText(product.explicitSolidGold));
  addTextCell(row, cellText(product.hallmark));
  addTextCell(row, cellText(product.goldAlloyWeightGrams));
  const priceCell = document.createElement('td');
  if (Number.isFinite(product.priceUsd)) {
    const price = document.createElement('span');
    price.className = 'price';
    price.textContent = money(product.priceUsd);
    priceCell.append(price, document.createTextNode(` · ${product.priceScope}`));
    const subNote = document.createElement('span');
    subNote.className = 'sub-cell';
    subNote.textContent = `Observed ${product.priceObserved}; may change`;
    priceCell.append(subNote);
  } else {
    priceCell.textContent = 'Unverified — blank';
  }
  row.append(priceCell);
  addTextCell(row, cellText(product.returnTerms));
  addTextCell(row, cellText(product.sellerReputation));
  const status = document.createElement('td');
  const badge = document.createElement('span');
  badge.className = 'badge flag';
  badge.textContent = product.status;
  status.append(badge);
  row.append(status);
  addSourceCell(row, [[source, 'Listing ↗'], [returnSource, 'Returns ↗'], ...reputationSources.map((record, index) => [record, index === 0 ? 'BBB reviews ↗' : 'BBB complaints ↗'])]);
  return row;
}
function overviewRow(product, sourceMap) {
  const row = document.createElement('tr');
  const name = addTextCell(row, product.name, 'primary-cell');
  const sub = document.createElement('span');
  sub.className = 'sub-cell';
  sub.textContent = `${product.seller} · ${product.productType}`;
  name.append(sub);
  addTextCell(row, cellText(product.listedMetal));
  const price = document.createElement('td');
  if (Number.isFinite(product.priceUsd)) {
    const amount = document.createElement('span');
    amount.className = 'price';
    amount.textContent = money(product.priceUsd);
    const scope = document.createElement('span');
    scope.className = 'sub-cell';
    scope.textContent = `${product.priceScope} · observed ${product.priceObserved}`;
    price.append(amount, scope);
  } else price.textContent = 'Unverified — blank';
  row.append(price);
  addTextCell(row, cellText(product.goldAlloyWeightGrams));
  addTextCell(row, cellText(product.sellerReputation));
  const status = document.createElement('td');
  const badge = document.createElement('span');
  badge.className = 'badge flag';
  badge.textContent = product.status;
  status.append(badge);
  row.append(status);
  const reputation = (product.reputationSourceIds || []).map(id => sourceMap.get(id)).filter(Boolean);
  addSourceCell(row, [[sourceMap.get(product.sourceId), 'Listing ↗'], [sourceMap.get(product.returnSourceId), 'Returns ↗'], ...reputation.map((record, index) => [record, index === 0 ? 'BBB reviews ↗' : 'BBB complaints ↗'])]);
  return row;
}
async function renderProducts() {
  const tbody = document.querySelector('[data-products]');
  const overview = document.querySelector('[data-overview-products]');
  if (!tbody && !overview) return;
  const [products, sources] = await Promise.all([loadJson('data/products.json'), loadJson('data/sources.json')]);
  const sourceMap = new Map(sources.map(source => [source.id, source]));
  if (tbody) tbody.replaceChildren();
  if (overview) overview.replaceChildren();
  for (const product of products) {
    const source = sourceMap.get(product.sourceId);
    const returnSource = sourceMap.get(product.returnSourceId);
    const reputationSources = (product.reputationSourceIds || []).map(id => sourceMap.get(id)).filter(Boolean);
    if (source && tbody) tbody.append(productRow(product, source, returnSource, reputationSources));
    if (overview) overview.append(overviewRow(product, sourceMap));
  }
  const search = document.querySelector('[data-search]');
  if (search && tbody) search.addEventListener('input', () => {
    const query = search.value.trim().toLowerCase();
    for (const row of tbody.rows) row.hidden = !row.textContent.toLowerCase().includes(query);
  });
  const count = document.querySelector('[data-product-count]');
  if (count) count.textContent = String(products.length);
  const ready = document.querySelector('[data-ready-count]');
  if (ready) ready.textContent = String(products.filter(p => p.status === 'Ready for independent verification').length);
  const flaggedCount = document.querySelector('[data-flag-count]');
  if (flaggedCount) flaggedCount.textContent = String(document.querySelectorAll('[data-flag-item]').length);
}
async function renderSources() {
  const host = document.querySelector('[data-sources]');
  if (!host) return;
  const sources = await loadJson('data/sources.json');
  host.replaceChildren();
  for (const source of sources) {
    const row = document.createElement('tr');
    const identity = document.createElement('td');
    identity.className = 'primary-cell';
    identity.textContent = source.title;
    const publisher = document.createElement('span');
    publisher.className = 'sub-cell';
    publisher.textContent = source.publisher;
    identity.append(publisher);
    row.append(identity);
    const type = document.createElement('td');
    const badge = document.createElement('span');
    badge.className = 'badge info';
    badge.textContent = source.sourceType;
    const date = document.createElement('span');
    date.className = 'sub-cell';
    date.textContent = `Accessed ${source.accessed}`;
    type.append(badge, date);
    row.append(type);
    addTextCell(row, source.supports);
    const linkCell = document.createElement('td');
    const link = document.createElement('a');
    link.href = source.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.className = 'source-link';
    link.textContent = 'Open source ↗';
    linkCell.append(link);
    row.append(linkCell);
    host.append(row);
  }
}
renderProducts().catch(error => console.error('Product data could not be rendered.', error));
renderSources().catch(error => console.error('Source data could not be rendered.', error));

async function renderFlags() {
  const tbody = document.querySelector('[data-flags]');
  if (!tbody) return;
  const [flags, sources] = await Promise.all([loadJson('data/flags.json'), loadJson('data/sources.json')]);
  const sourceMap = new Map(sources.map(source => [source.id, source]));
  tbody.replaceChildren();
  for (const flag of flags) {
    const row = document.createElement('tr');
    addTextCell(row, flag.category);
    const issueCell = document.createElement('td');
    const badge = document.createElement('span');
    badge.className = 'badge flag';
    badge.textContent = flag.title;
    issueCell.append(badge);
    row.append(issueCell);
    addTextCell(row, flag.detail);
    const evidence = document.createElement('td');
    for (const item of flag.sources) {
      const source = sourceMap.get(item.id);
      if (!source) continue;
      const link = document.createElement('a');
      link.href = source.url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.className = 'source-link';
      link.textContent = item.label;
      evidence.append(link, document.createTextNode(' '));
    }
    row.append(evidence);
    tbody.append(row);
  }
}
renderFlags().catch(error => console.error('Flag register could not be rendered.', error));
