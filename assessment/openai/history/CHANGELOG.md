## 2026-09-21T00:16:00Z

Schema migration — this run re-baselines OpenAI's assessment onto the current per-controversy clustering schema. The prior `assessment.json` used the older one-entry-per-source-file schema (`report_file`/`source_file`/`title`/`url`/`core_from`/`gap_fill`/`assessment`) predating controversy clustering, so a field-level diff against it would not be meaningful. No source content was discarded: the same 8 previously-collected report files were backfilled with `controversies` frontmatter labels and re-clustered, expanding to 10 distinct controversies (the Fortune "string of controversies" roundup article splits into 3 separate incident clusters: wikipedia-messaging-incident, benchmaxxing, navier-stokes-dispute). The Musk v. Altman case was re-gap-filled and its status updated from "Concluded" to "Partially Concluded" given a newly-confirmed pending Ninth Circuit appeal (No. 26-4486).

First run on the new schema — 10 controversies baselined.

## 2026-09-21T12:00:00Z

**New (5):** raine-v-openai-teen-suicide, florida-ag-lawsuit-chatgpt-safety, nyt-copyright-sanctions-discovery-misconduct, gpt-4o-retirement-broken-promise, rubygems-eu-ai-act-nonreporting
**No longer found (0):** none
**Changed (4):** effingham-county-data-center: Score 2→4, Flag Yellow→Yellow, Status Partially Concluded→Ongoing (project proceeding despite continued opposition; no completed remediation confirmed this run); hugging-face-unauthorized-access: Score 6→4, Flag Green→Yellow (new Senate investigation details — 1,200+ agents, 70,000+ messages, OpenAI resumed evaluations after learning of the issue — raised assessed scale); wikipedia-messaging-incident: Score 6→4, Flag Green→Yellow (gap-fill research found ongoing EU Commission review of an OpenAI-filed incident report, raising assessed scale from a single freshly-disclosed item to active multi-country regulatory scrutiny); musk-v-altman-fraud-case: Score 2→5, Flag Yellow→Green, Status unchanged (Partially Concluded — reconfirmed pending Ninth Circuit appeal)
**Unchanged:** 6 (chatgpt-environmental-footprint, doj-worker-discrimination-settlement, benchmaxxing, navier-stokes-dispute, models-acting-deceptively, tumbler-ridge-shooting-lawsuits)
