# Prompt to Add a New Book Review (with all related references)

Use this prompt with Copilot/LLM to add one new book into this bookshelf codebase, matching existing page style and updating all related references.

---

## Copy-paste prompt

```text
You are editing the repo at bookshelf/. Add ONE new book review page and update every related reference so navigation and cross-links stay consistent.

ONLY REQUIRED USER INPUT:
- Book title: <TITLE>
- Author: <AUTHOR>

AUTO-POPULATE RULES (do not ask user for these):
- FILE_SLUG: derive from title in existing repo style (PascalCase, no spaces/special chars).
- Review page file: BookReviews/<FILE_SLUG>.html
- Language: default English unless author/title strongly indicates Marathi.
- Category text: infer from book theme/genre and existing category taxonomy.
- ISBN: if confidently known use it; otherwise set exactly: ISBN Not available.
- Rating: auto-assign between 4.2 and 4.9 based on review tone consistency.
- Rating label: map rating to short label (e.g., Great Read / Must Read / Excellent Read).
- Cover image filenames:
  - Primary expected cover: <FILE_SLUG>.jpg
  - Alternate expected cover: <FILE_SLUG>.png
  - Placeholder from bookshelf root (if cover missing): img/BookCovers/<FILE_SLUG>.jpg
  - Placeholder from BookReviews page (if cover missing): ../img/BookCovers/<FILE_SLUG>.jpg
- Meta description: generate <=160 chars.
- OG URL: generate placeholder using filename slug.
- Quote text: generate one relevant quote/line from Given Book.
- Review body: generate 2-4 readable paragraphs in same tone as existing pages.
- Tags: generate 3-4 tags pipe-separated.
- Similar books: auto-select 2-3 existing review pages from repo relevance.
- Home "Currently Reading" feature: default no; set yes only if the book is high-priority/popular.

REQUIREMENTS:
1) Create new review page
- Use BookReviews/template.html structure and conventions from existing pages.
- Include:
  - proper <title>, meta description, og tags
  - header-component via pageheader.js
  - cover, rating, quote, description section
  - tags section
  - "Similar Books" cards linking to existing review pages
  - footer copyright exactly with Ganesh Kedari
- Keep relative paths exactly like existing review pages.
- For cover image in the page and arrays:
  - use real cover file if available in img/BookCovers.
  - else use placeholder path img/BookCovers/PLACEHOLDER_<FILE_SLUG>.jpg consistently.

2) Update data/catalog sources
- Update BookReviews/booklist.csv with a new row:
  Book Name, Author, Language, Category, ISBN, Book Tags, Similar Books
- Update BookReviews/booklist.md with the same book metadata.

3) Update home page references
- In index.html:
  - Add the new entry to const allBooks array with href, img, alt.
  - If auto feature flag is yes, add one new slide in "Currently Reading" swiper using same markup pattern.

4) Update category pages that should include this book
- Based on category and tags, insert new book card object in each relevant page’s const books array:
  - Fiction.html
  - MysteryThriller.html
  - Fantasy.html
  - ScienceFiction.html
  - Historical.html
  - BiographyMemoir.html
  - KnowledgeLearning.html
  - SelfHelp.html
- Only add where semantically relevant; do not add blindly to all pages.
- Object format must match existing:
  { href: 'BookReviews/<FILE_SLUG>.html', img: 'img/BookCovers/<COVER_FILE_OR_PLACEHOLDER>', alt: '<TITLE>' },

5) Update reciprocal related-book links (important)
- In new page, add Similar Books cards for SIM1/SIM2/SIM3.
- In each SIM page, add a reciprocal card linking back to <FILE_SLUG>.html in its Similar/Related Books section.
- Keep each Similar Books section tidy and at most 3 cards (if >3 after insertion, remove weakest/oldest one).

6) Consistency checks
- Ensure filename/href case matches exactly everywhere.
- Ensure image path case matches real file name.
- Ensure no broken relative links from BookReviews pages.
- Preserve existing formatting/style; do not refactor unrelated code.

7) Validation (run and report)
- Search for new filename references across bookshelf:
  - BookReviews/<FILE_SLUG>.html appears in all expected places.
- Verify all Similar Books href targets exist as files.
- Verify cover reference exists; if not, verify placeholder path is used in every new reference.
- Verify new page contains Ganesh Kedari copyright line.

8) Output
- Return:
  - list of files changed
  - brief summary of what was added/updated
  - any warnings (missing images, ambiguous category mapping, etc.)

Implement the edits directly in files. Do not provide pseudo-code.
```

---

## Notes for this repo

- Review page template source is `BookReviews/template.html`.
- Book review header nav component is `BookReviews/pageheader.js`.
- Main home catalog list is `index.html` (`const allBooks`).
- Category pages are driven by inline JS arrays (`const books`) in each category HTML page.
- Existing files have inconsistent filename casing in some places; keep your new references internally consistent and exact.

### Quick use

Replace only these two lines before running:
- Book title: <TITLE>
- Author: <AUTHOR>
