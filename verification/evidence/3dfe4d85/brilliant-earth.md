# L09–L12 — Brilliant Earth pages opened (session `3dfe4d85`, 2026-10-25) — all four served EUR

Every one of the four product pages opened this pass rendered in **EUR** for this fetch origin
(currency strip on each page: "USD · EUR CAD AUD GBP" with a German country flag, and the gift-card
banner printed in EUR while its image block prints "USD$250 GIFT CARD WITH PURCHASE OVER USD$1,000").
No USD setting price was served, so **no USD price was refreshed**; no EUR figure was converted.
This is the same per-page geo behaviour FL-08 documents (2026-10-23: two pages served USD, two EUR;
2026-10-25: zero of four served USD).

## L09 — BE-1343 (canonical USD cell blank → stays blank; EUR observed again at €835.00)

<https://www.brilliantearth.com/Freesia-2mm-Solitaire-Ring-14K-Gold-BE1343-76787087/>

```
# Freesia 2mm Solitaire Ring in 14K Yellow Gold
€‌835.00(Setting Only)   (80) reviews
Banner: "ENDS SOON! Receive a €280.00 Gift Card With Purchase Over €1,150.00. Use Code GIFT in Cart."
Wizard step: "Setting freesia 2mm solitaire-€‌835.00"
Ring Information: Style: BE1343-14KY · Metal: 14K Yellow Gold · Width: 2-1.2 mm · Setting: Claw Prong
"Order now and your order ships by Wed, Nov 11, depending on center diamond."
We've Got You Covered: "Free Shipping & Returns · Free Lifetime Warranty · Lifetime Diamond Upgrade ·
Free 1-Year Resizing"
Financing: "Easy monthly payments with Affirm. From 0% APR financing. Up to 36 months. Subject to
credit approval. Special 12 month financing options available with Wells Fargo … Layaway options
also available."
Metal variants offered incl. 14K/18K White, 14K/18K Yellow, 14K Rose, Platinum
```

## L10 — BE-NADIA (**USD 1,250 not confirmable → row becomes a dated prior observation**)

<https://www.brilliantearth.com/Nadia-Diamond-Ring-14K-Gold-BE1D6013-76819968/>

```
# Nadia Diamond Ring in 14K Yellow Gold
€‌1,400.00(Setting Only)   (143) reviews
Wizard step: "Setting nadia-€‌1,400.00"
Product Details: "1.8mm band width — keeps a slim, comfortable profile" · "Claw prongs" ·
"Marquise and round diamond accents — prong-set at the gallery (0.06 and 0.05 ct. tw.)" ·
"Hand-engraved detailing" · "Low-profile fit"
Setting Carat Weight options: 1/10 · 2/5 · 1/2 ; Accent Stones:Diamonds ; Setting Type:Low Profile
"Order now and your order ships by Mon, Nov 16, depending on center diamond."
We've Got You Covered: Free Shipping & Returns · Free Lifetime Warranty · Lifetime Diamond Upgrade ·
Free 1-Year Resizing
```

Confirmed today by this read: title karat (14K Yellow Gold), band width 1.8 mm, metal/setting fields.
**Not** confirmable today: the USD setting price — the canonical $1,250.00 remains the 2026-10-23
USD read, now labelled `provenance: prior` with FL-08 + FL-33, and is presented on the site as a
dated observation, never as today's price.

## L11 — BE-1343HH (canonical USD cell blank → stays blank; €1,350.00 served)

<https://www.brilliantearth.com/Freesia-Hidden-Halo-Diamond-Ring-14K-Gold-BE1D3939-76789075/>

```
# Freesia Hidden Halo Diamond Ring in 14K Yellow Gold
€‌1,350.00(Setting Only)   (31) reviews
Wizard step: "Setting freesia hidden halo-€‌1,350.00"
Ring Information: Style: BE1D3939-14KY · Metal: 14K Yellow Gold · Width: 2-1.3 mm · Claw Prong
Accent Gemstones: 14 shared-prong round diamonds · Min. carat total weight 0.05 · F/G · SI1
"Order now and your order ships by Wed, Nov 11, depending on center diamond."
```

## L12 — BE-SECRET (**USD 1,090 not confirmable → row becomes a dated prior observation**)

<https://www.brilliantearth.com/Secret-Halo-1.5mm-Diamond-Ring-14K-Gold-BE1D13065-76823478/>

```
# Secret Halo 1.5mm Diamond Ring in 14K Yellow Gold
€‌1,250.00(Setting Only)   (92) reviews
Wizard step: "Setting secret halo 1.5mm-€‌1,250.00"
Ring Information: Style: BE1D13065-14KY · Metal: 14K Yellow Gold · Width: 1.5 mm · Claw Prong
Product Details: "1.5mm band width" · "Scalloped pavé accent — … 13 round diamonds (0.06 ct. tw.)"
Band Width options 1.5 / 2 · Prong Type:Four Prong
"Order now and your order ships by Mon, Nov 16, depending on center diamond."
```

## Cross-page observation published (no inference drawn)

The promo image block on all four pages prints USD figures ("RECEIVE A USD$250 GIFT CARD WITH
PURCHASE OVER USD$1,000. Applies to a future purchase of USD$250 or more.") while the page banner
and the price line print EUR ("€280.00 Gift Card With Purchase Over €1,150.00"). The mixed-currency
render is per template block, not per page — a promo block cannot be used as a price source and a
banner figure cannot be treated as a product price. Recorded for FL-08.
