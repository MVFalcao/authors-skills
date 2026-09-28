# Rules: design-editorial

> **Editable rules.** The skill reads this file first, and it overrides the defaults in SKILL.md.
> These are starting assumptions: add, change or delete rules freely. One rule per bullet.
> Remove a whole section if you do not want it.

## Defaults when the writer gives no preference
- Adult fiction in print: format **14x21 cm**, body **11/15 pt** in a book serif, margins interna 20, externa 15, superior 18, inferior 22 mm.
- Non-fiction with notes, tables or images: consider **16x23 cm** and say why.
- Paper: miolo in **pólen 80 g/m²** for long reading, **offset 90 g/m²** when there are line images, **couché** only for colour photos. Capa in **cartão 250–300 g/m²** with **laminação fosca**.
- Binding: **brochura** (lombada quadrada) with PUR glue; cadernos of 16 pages.
- Ebook: **EPUB 3 reflowable**. Fixed layout only for books where the image placement is the content (children's picture books, comics).
- List every default you used under `Premissas`, so the writer can change it.

## Typography
- Text lines of about 55–70 characters; never outside 45–75.
- Leading 120–140% of the body size.
- Prefer fonts with full PT-BR support (ã, õ, ç, accents, travessão) and a licence that allows print and ebook embedding. Suggest at least one free option (SIL Open Font License) next to any commercial font.
- At most two type families: one for text, one for display.
- Fiction: first-line indent of 1 em, no space between paragraphs, no indent after a title or scene break.
- Dialogue follows the manuscript's convention (travessão in PT-BR). Never change it in the spec.

## Layout
- No widows or orphans: at least 2 lines of a paragraph at the top or bottom of a page.
- Scene breaks get an ornament or asterism, not only a blank line (a blank line disappears at a page break).
- Chapters open on a new page with a sink of about one third of the page. Opening on the recto (odd page) is the writer's choice: it adds blank pages.
- No running head on chapter openers or blank pages.

## Production
- Never invent prices, delivery times or a print shop's paper stock. Give the checklist for asking a quote instead.
- Paper thickness (micra) and the spine width come from the print shop. Without their number, use a typical value, mark it `⚠️ verificar com a gráfica`, and say the cover must wait for their spine.
- Print-ready files: PDF/X-1a or PDF/X-4, fonts embedded, images at 300 dpi at final size, 3 mm bleed, crop marks. Ask the print shop for their own specs.
- Always recommend a physical proof (prova) before the full print run.

## Limits
- Ask at most one question per reply, about one input, including follow-ups at the end. Cover other missing inputs with the defaults under `Premissas`. Offer further work as a statement ("Posso montar…"), not a question.
- Specifications only: don't produce layout files, cover art or illustrations. Never create an image, SVG or HTML mock-up, even when asked for a cover; offer the technical cover spec instead.
- Write only the documents for the modes the writer asked for; offer the other modes in one line.
- Don't edit or rewrite the manuscript. Don't comment on the story; that's leitor-beta.
- Manuscript files are only opened to count words, never to read their content.

## Saving
- Check whether `design/` exists by listing the book folder itself (for example `ls`). A file search misses an empty folder. If listing isn't allowed, run `python3 -c "import os; print(os.path.isdir('design'))"`. If you can't check at all, say you couldn't check; never say the folder is missing.
- If `design/` already exists in the book folder, save the result there without asking, and give the file path in the reply.
- If `design/` doesn't exist, ask once before creating it. If the writer says no, return the result in the chat.
- File names: `design/projeto-grafico.md`, `design/diagramacao-impresso.md`, `design/diagramacao-ebook.md`, `design/producao-grafica.md`.
- Never overwrite an earlier result: if the file name is taken, add `-2`, `-3`, and so on.
