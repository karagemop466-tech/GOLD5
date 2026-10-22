const form = document.getElementById('gold-form');
const result = document.getElementById('result');
const detail = document.getElementById('result-detail');
const formula = document.getElementById('formula');
form.addEventListener('submit', event => {
  event.preventDefault();
  const weight = Number(form.elements.weight.value);
  const karat = Number(form.elements.karat.value);
  const spot = Number(form.elements.spot.value);
  const date = form.elements['price-date'].value;
  const rawUrl = form.elements['price-source'].value.trim();
  let source;
  try { source = new URL(rawUrl); } catch { source = null; }
  if (!(weight > 0) || !(karat > 0 && karat <= 24) || !(spot > 0) || !date || !source || source.protocol !== 'https:') {
    result.textContent = 'No estimate';
    detail.textContent = 'Enter positive documented values, an observation date, and an HTTPS price-source URL.';
    return;
  }
  const fineGoldGrams = weight * karat / 24;
  const estimatedMetalValue = fineGoldGrams * spot;
  result.textContent = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(estimatedMetalValue);
  detail.textContent = `Approx. ${fineGoldGrams.toFixed(4)} g fine-gold equivalent · based on ${weight} g ${karat}K alloy and your USD ${spot}/g input · price date ${date}.`;
  formula.replaceChildren(document.createTextNode('Fine-gold equivalent = '), document.createTextNode(`${weight} g × ${karat} ÷ 24 = ${fineGoldGrams.toFixed(4)} g`), document.createElement('br'), document.createTextNode('Metal-value proxy = '), document.createTextNode(`${fineGoldGrams.toFixed(4)} g × $${spot}/g = $${estimatedMetalValue.toFixed(2)} · source: `));
  const link = document.createElement('a');
  link.href = source.href;
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  link.textContent = 'open submitted source ↗';
  formula.append(link);
});
form.addEventListener('reset', () => {
  result.textContent = 'No estimate';
  detail.textContent = 'Enter complete, documented inputs. No current gold price is preloaded.';
  formula.replaceChildren(document.createTextNode('Fine-gold equivalent = gold-alloy weight × karat ÷ 24'), document.createElement('br'), document.createTextNode('Metal-value proxy = fine-gold equivalent × sourced spot price per fine-gold gram'));
});
