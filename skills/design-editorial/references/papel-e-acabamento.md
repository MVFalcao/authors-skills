# Papel, impressão, acabamento e gráfica

Use this for the print production role: technical feasibility, cost drivers,
paper and finishes, files and the proof. Never quote prices; list what drives
the cost and what to ask the print shop.

## Paper for the text block (miolo)

| Paper | Look | Typical use |
|---|---|---|
| Pólen (creamy, uncoated), 70–90 g/m² | Warm, low glare | Fiction and long reading |
| Offset (white, uncoated), 75–90 g/m² | Neutral, crisp | Non-fiction, line drawings, textbooks |
| Couché (coated) fosco/brilho, 90–150 g/m² | Smooth, sharp colour | Photos, colour illustrations |

Brand names such as Pólen Soft or Pólen Bold belong to specific mills; offer
them as examples and mark availability `⚠️ verificar com a gráfica`.

Thickness per sheet (micra) decides the spine. Uncoated book papers of
70–90 g/m² are often around 90–130 µm per sheet, and bulky papers are thicker
at the same weight. Use the print shop's figure; a typical value is only a
placeholder marked `⚠️ verificar com a gráfica`.

## Cover (capa)

- Cartão (for example triplex or supremo) 250–300 g/m², printed 4x0 (CMYK on
  the outside only).
- Protection: laminação fosca (matte), brilho (gloss) or soft touch.
- Highlights: verniz UV localizado, hot stamping, relevo seco (blind emboss).
  Each adds cost and a separate file layer.
- Orelhas (flaps) of about 7–9 cm add perceived value and cost.
- Cover size: `calc_producao.py capa` with the spine from `lombada`. The cover
  file waits for the print shop to confirm the spine.

## Printing method

- **Digital** printing: economical for short runs and print on demand; good
  for proofs and first editions.
- **Offset**: set-up cost, lower unit cost as the run grows. The run where
  offset becomes cheaper than digital depends on the shop, page count and
  paper: `⚠️ verificar com a gráfica` (ask both quotes).
- Colours: miolo 1x1 (black both sides) for prose; 4x4 only for colour
  throughout. Mixing colour pages increases cost; group them in one signature
  when possible.

## Binding

- **Brochura** (lombada quadrada, perfect binding): the standard for trade
  books. PUR glue is more durable and opens flatter than hot-melt (EVA).
  Sewn signatures plus glue (costurada) last longest.
- **Capa dura** (cartonado): premium, durable, much more expensive.
- **Canoa** (saddle stitch, grampo): thin books only, page count a multiple
  of 4, usually up to about 64 pages.

## Files for the print shop

- PDF/X-1a or PDF/X-4 as the shop asks; fonts embedded; no RGB images when the
  shop requires CMYK (ask for their colour profile).
- Images at 300 dpi at final size (line art 600–1200 dpi).
- 3 mm bleed (sangria) on everything that touches the trim; crop marks.
- Miolo and capa as separate PDFs; single pages in reading order, not spreads,
  unless the shop asks otherwise.
- Rich black only for large cover areas; 100% K for text.

## Quote request (pedido de orçamento)

Ask every shop for the same items so quotes compare: tiragem (and a second
run size), formato, número de páginas, papel e gramatura do miolo e da capa,
cores (miolo e capa), acabamentos, encadernação, orelhas, tipo de prova,
embalagem, frete até o endereço, prazo, condições de pagamento, and whether
the price includes the files check (pré-impressão).

## Proof checklist (prova)

- Page order, blank pages and signatures; folios and running heads.
- Margins: nothing important lost in the binding; text not too close to the
  trim.
- Colour and density of the cover versus the approved file; black text sharp.
- Spine text centred and readable; barcode (ISBN) scans.
- Paper, finish and binding match the quote.
- Sign off only when every item is checked; changes after the proof cost money.
