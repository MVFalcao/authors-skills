# Formatos, grid e margens

Use this when choosing the trim size, the text block (mancha) and the margins.
Compute every figure with `scripts/calc_producao.py mancha` and `paginas`.

## Common trim sizes in Brazil

| Formato (cm) | Typical use | Notes |
|---|---|---|
| 14 x 21 | Adult fiction, essays, most trade books | The default. Comfortable in the hand; ~280–330 words per page at 11/15 pt. |
| 16 x 23 | Non-fiction, textbooks, books with notes or tables | Wider line: check characters per line; may need 11.5–12 pt or wider margins. |
| 12 x 18 / 11 x 18 | Pocket editions | Smaller body (10–10.5 pt), tighter margins; more pages. |
| 21 x 28 | Illustrated books, children's, cookbooks | Often two columns or image-led layouts. |
| 20 x 20 (quadrado) | Picture books, photo books | Usually fixed layout in the ebook version. |

A trim size that fits the print shop's press sheet (for example 66x96 or
76x112 cm) wastes less paper. Which sizes fit depends on their press and the
page count: mark sheet-efficiency claims `⚠️ verificar com a gráfica`.

For print on demand (Amazon KDP and similar), use the platform's own trim list
(for example 5.5 x 8.5 in ≈ 13,97 x 21,59 cm, 6 x 9 in ≈ 15,24 x 22,86 cm) and
its minimum margins; mark them `⚠️ verificar` because platforms change them.

## Margins

- **Interna (medianiz)** is the largest horizontal margin in a perfect-bound
  book: part of it disappears into the binding. Add a few millimetres for a
  thick book (roughly above 300 pages).
- **Externa** holds the thumb: at least 12–15 mm.
- **Inferior** is usually the largest vertical margin; the folio sits there
  when page numbers are at the foot.
- **Superior** leaves room for the running head (cabeço) when there is one.
- A classical proportion for fine editions is interna : superior : externa :
  inferior ≈ 2 : 3 : 4 : 6. Trade books use tighter margins to save pages;
  explain the trade-off (more margin = more pages = higher cost).

Starting point for 14 x 21 cm: interna 20, externa 15, superior 18,
inferior 22 mm. This gives a 105 x 170 mm block, 32 lines at 11/15 pt and about
58 characters per line.

## Grid

- Use a **baseline grid** equal to the leading (for example 15 pt), so lines
  on facing pages and on both sides of the sheet line up.
- Titles, subtitles and spacing around them are multiples of the leading, so
  text after a heading returns to the grid.
- Images and captions snap to whole lines of the grid.
- One column for prose. Two columns only for reference works, large formats or
  dense notes.

## Page estimate

`calc_producao.py paginas` counts words per page from the text block, adds a
chapter-opening overhead and the pre/post-text pages, and rounds up to whole
signatures (cadernos of 8, 16 or 32 pages). Present it as an estimate: the
real count comes from the layout. Offer the levers that change it: body size,
leading, margins, chapters opening on recto, format.
