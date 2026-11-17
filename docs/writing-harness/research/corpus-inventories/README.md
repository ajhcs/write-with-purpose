# Acquired discovery inventories

Acquired 16 November 2026. These files preserve discovery metadata, not a collection of screened writing exemplars or locally analyzed full texts. Acquisition details, timestamps and SHA-256 hashes are in [acquisition-receipts.json](acquisition-receipts.json).

| File | Actual contents | What the count means |
| --- | --- | --- |
| [longform-post-candidates.csv](longform-post-candidates.csv) | 13,053 sitemap entries with Longform URL and source last-modified value | Discovery posts, not necessarily distinct original nonfiction articles. No individual eligibility or availability review has been performed. |
| [readme-section-source.csv](readme-section-source.csv) | Original annotation CSV from the READMEClassifier research repository: 4,922 rows | Includes 696 rows with excluded `-` code. The raw source has 435 distinct URL values. |
| [readme-document-candidates.csv](readme-document-candidates.csv) | 393 distinct repository URL values after excluding `-` rows, with retained section counts and source file IDs | Derived document candidates corresponding to 4,226 retained section rows; matches the published study's stated sample. Not 393 locally reviewed writing exemplars. |

Longform source: [official posts sitemap](https://longform.org/sitemap/posts.xml), declared through its [robots file](https://longform.org/robots.txt) and sitemap index. Its homepage describes more than 10,000 nonfiction recommendations from April 2010 through December 2022. The larger sitemap includes other kinds of post and potential duplicates. `lastmod` is not an original publication date. Resolve the original article URL, author, outlet, form, original publication date, and selection reason before inclusion. “Most clicked” requires a particular ranked list and date window; a sitemap entry has no such status by default.

README source: [official combined annotation CSV](https://github.com/gprana/READMEClassifier/blob/master/input/dataset_combined.csv), fetched from its branch URL. The subagent inspected Git blob `4765ca26ad3b6f4095654e0c5d43bf7db7a02801`; the acquired bytes are independently pinned by SHA-256 in the receipt. A Git blob ID is not a commit ID and cannot be substituted into a raw-file commit URL. The live branch may subsequently change.

Derivation: parse the source as CSV; retain rows whose `Codes with >= 2 votes` field, after whitespace stripping, is not `-`; group by the exact `url` field; count retained rows and retain unique `file-id` values. Repository URLs are historical research identifiers, not guaranteed links to an unchanged README version. The research repository's stored text directory has a different file count from the eligible labeled sample.

The READMEClassifier repository declares MIT licensing; original README provenance and upstream document licenses still matter for text reuse. Longform links lead to separately owned publications. No original article bodies or README bodies were acquired in this step. Do not infer text redistribution rights from public discoverability or from an annotation repository's software license.

To reproduce the counts from these saved files:

```sh
python3 - <<'PY'
import csv
from pathlib import Path
base = Path('docs/writing-harness/research/corpus-inventories')
with (base / 'longform-post-candidates.csv').open(newline='') as f:
    print('Longform discovery entries:', sum(1 for _ in csv.DictReader(f)))
with (base / 'readme-section-source.csv').open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))
selected = [r for r in rows if r['Codes with >= 2 votes'].strip() != '-']
print('README raw rows:', len(rows))
print('README retained sections:', len(selected))
print('README retained document URLs:', len({r['url'] for r in selected}))
PY
```

Separate future ledgers should record **discovered → screened → eligible → text available → annotated → reviewed → held out**. An existing study's annotation is evidence about that dataset, not proof that our own functions or quality criteria have been assessed.
