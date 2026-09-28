# Diagramação digital (ebook)

Use this for EPUB and digital PDF. A reflowable ebook has no fixed page: the
reader chooses font, size and margins. Specify structure and styles, not page
positions.

## Choosing the format

- **EPUB 3 reflowable**: prose, most non-fiction. Accepted by the main stores.
- **EPUB 3 fixed layout**: when the position of images on the page is the
  content (picture books, comics, some cookbooks).
- **PDF**: only for direct sales or review copies; it doesn't reflow on
  phones.

Store requirements change: mark any store-specific limit (cover pixel size,
file size, accepted formats) `⚠️ verificar` with the store's current help pages.

## Structure

- One file per chapter, headings in order (h1 for chapter, h2 for sections).
- Language set to `pt-BR` on the book and on every file.
- A navigation table of contents (nav) and a readable sumário.
- Metadata: title, author, language, publisher, ISBN for the ebook edition
  (different from the print ISBN), description.
- Pre-text pages: keep credits and dedication short; move long front matter
  to the back so the sample shows the story.

## Styles (CSS)

- Sizes in `em` or `%`, never fixed `px` for text.
- Body text without a forced font size or colour; let the reader choose.
- Paragraphs: first-line indent 1–1.5 em, no margin between paragraphs; no
  indent after headings and scene breaks (a class, not manual spaces).
- Scene breaks as an element with an ornament and `role`/text that screen
  readers can announce, not an empty paragraph.
- Embedded fonts only when the licence allows ebook embedding
  (`⚠️ verificar licença`); readers may override them anyway.
- Dialogue with the travessão as typed in the manuscript.

## Images

- Width in `%` of the screen, with `max-width: 100%`; no fixed heights.
- Alt text (texto alternativo) for every meaningful image; empty alt only for
  decoration.
- JPEG for photos, PNG or SVG for line art; keep file sizes modest.
- Captions in the same block as the image so they don't separate.

## Accessibility and checks

- Follow EPUB Accessibility 1.1 where possible: reading order, alt text,
  headings, language, accessibility metadata.
- Validate with EPUBCheck before submitting.
- Test on at least one phone app and one e-reader (for example Kindle and a
  Kobo/Apple Books app), with large and small font settings.
