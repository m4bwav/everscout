# Vocabulary: {{TITLE}}

The entities the tally counts. Each `## heading` is a facet and becomes a list field in every note's frontmatter (lower case, underscores: `## Techniques` gives `techniques: [...]`). Each line is `- canonical-id: alias, alias, alias`. The canonical id is lower case with `-`, `.` or `+`; aliases are what people actually write, matched case-insensitively on word boundaries by `everscout.py vocab-match` and `new-note`. A line with aliases matches only its aliases, never its id; a line with no aliases matches the id. Aliases must not be ordinary words: write `Logic Pro`, not `Logic`; `Warp Records`, not `Warp`. Add a line rather than inventing a spelling in a note; `validate` warns on values not listed here. Three to six facets; do not use a facet name that is also a note field (title, date, tags, summary, url, ...).

## How to use this file

Keep canonical ids stable: renaming one splits its history in the tallies. When a new version of something appears, add it as its own id if people talk about the versions separately, or as an alias if they do not.

## Tools

- example-tool: Example Tool, exampletool

## Techniques

- example-technique: example technique

## Topics

- example-topic: example topic
