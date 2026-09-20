## 2026-09-21T00:16:00Z

Schema migration — this run re-baselines OpenAI's assessment onto the current per-controversy clustering schema. The prior `assessment.json` used the older one-entry-per-source-file schema (`report_file`/`source_file`/`title`/`url`/`core_from`/`gap_fill`/`assessment`) predating controversy clustering, so a field-level diff against it would not be meaningful. No source content was discarded: the same 8 previously-collected report files were backfilled with `controversies` frontmatter labels and re-clustered, expanding to 10 distinct controversies (the Fortune "string of controversies" roundup article splits into 3 separate incident clusters: wikipedia-messaging-incident, benchmaxxing, navier-stokes-dispute). The Musk v. Altman case was re-gap-filled and its status updated from "Concluded" to "Partially Concluded" given a newly-confirmed pending Ninth Circuit appeal (No. 26-4486).

First run on the new schema — 10 controversies baselined.
