// ============================================================================
// GOLD5 — Gold Engagement Ring Buying Checklist
// Site JavaScript
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
  // Highlight current page in nav
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  const navLinks = document.querySelectorAll('.navbar__links a');
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === 'index.html' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  // Calculator functionality (gold value calculator)
  const calcForm = document.getElementById('gold-calculator');
  if (calcForm) {
    calcForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const weight = parseFloat(document.getElementById('ring-weight').value);
      const karat = parseFloat(document.getElementById('ring-karat').value);
      const pricePerGram = parseFloat(document.getElementById('gold-price').value);

      if (isNaN(weight) || isNaN(karat) || isNaN(pricePerGram)) {
        document.getElementById('calc-result').innerHTML =
          '<span class="badge badge--unverified">Please enter valid numbers</span>';
        return;
      }

      const purity = karat / 24;
      const pureGoldWeight = weight * purity;
      const goldValue = pureGoldWeight * pricePerGram;

      document.getElementById('calc-result').innerHTML = `
        <p><strong>Pure gold weight:</strong> ${pureGoldWeight.toFixed(3)} g</p>
        <p><strong>Estimated gold melt value:</strong> $${goldValue.toFixed(2)} USD</p>
        <p style="font-size:0.875rem;color:#6b7280;margin-top:0.5rem;">
          This is the raw gold value only. It does not include craftsmanship,
          gemstones, brand premium, or retail markup.
        </p>
      `;
    });
  }
});
