# Nature of Harm, Scale of Impact, Company Role, and Case Status

Reference rubrics used after the primary pillar (Environmental / Social / Governance) has been identified.

## Nature of Harm

Categorize as **Very Serious**, **Serious**, **Medium**, or **Minimal**. Criteria differ by pillar.

### Environmental
Based on the degree of damage and the irreversibility of damage.
- **Very Serious** — irretrievable or long-lasting environmental damage (extensive plant/wildlife death; ecosystem destruction beyond repair).
- **Serious** — significant but potentially remediable harm (severe injury/illness in plant or wildlife populations; major, hard-to-restore habitat/ecosystem damage).
- **Medium** — short-term, reversible harm (temporary impact on plant/wildlife health; short-term habitat damage).
- **Minimal** — anticipated or hypothetical impact with no immediate effects (e.g. projected impact of a proposed pipeline).

### Governance
Based on the type of violation — financial losses, value of bribes/unethical gains, and other adverse outcomes from illicit activity. Most cases default to Medium unless circumstances indicate heightened severity.
- **Very Serious** — activity substantially destabilized a national government or economy; total bribes/losses exceed USD 1B, or ill-gotten gains (e.g. taxes avoided) exceed USD 10B.
- **Serious** — activity caused bankruptcy for the company or a key client, or material financial impact on a government body; bribes exceed USD 100M or contracts obtained exceed USD 5B.
- **Medium** — allegations of corruption/fraud between business entities without direct impact on individual customers; most government fraud/corruption cases where harm is present but not highly concentrated.
- **Minimal** — impact is projected or not scoped out.

### Social
Based on the alleged irreversibility of damage to human health, livelihoods, or property.
- **Very Serious** — severe human rights violations (death, permanent disability, torture, rape, enslavement); destruction of livelihood/traditional way of life or property; product/practice is a leading cause of death or permanent disability.
- **Serious** — debilitating injury/illness; major property damage; significant impairment of livelihood or displacement; labor/civil rights violation with concrete resulting harm; product/practice poses health risk.
- **Medium** — treatable short-term injury/illness; minor, easily repaired property damage; limited impairment to livelihood; product/practice may have adverse effects but lacks direct causality.
- **Minimal** — minor inconveniences/disruptions; impact projected but lacking clear evidence or scope.

Respond with `{"Nature of harm": "<category>", "Details": "<explanation>"}`.

## Scale of Impact

Categorize as **Extremely Widespread**, **Extensive**, **Limited**, or **Low**. Cases with undetermined/unspecified scale default to Limited (Environmental) or Low (Social/Governance, per that pillar's criteria).

### Environmental
Determined by the size of the affected area (land, water, air) or the geographic range of impacted wildlife.
- **Extremely Widespread** — 100 km² or more, or an entire watershed; global species impact; spill over 60,000 barrels; involves a top-10 contributor (by sales/production) to a high-impact activity; long-lasting (over 5 years), very severe harm across multiple sovereign states.
- **Extensive** — 10–99 km², large bay or portion of river; regional/country species impact; spill 5,000–59,999 barrels; part of a broader industry activity/incident involving multiple companies.
- **Limited** — 1–9 km², stream/small river/lake; local wildlife impact; spill 1,500–4,999 barrels.
- **Low** — insignificant or not determined.

### Governance
Distinguish Business Ethics vs. Governance Structures issues.
- Business Ethics — assessed by size of affected market/government, or degree of involvement of executives/external parties (e.g. government officials).
- Governance Structures — assessed by % of shareholder votes or number of shareholders concerned, number/position of executives or directors involved, number/type of external parties commenting, portion of the company affected.
- **Extremely Widespread** — global or 3+ G20 countries; 1,000+ people involved.
- **Extensive** — 1 G20 country or 3+ non-G20 countries; 25+ people involved.
- **Limited** — 1–2 non-G20 countries or local municipalities; 10–24 people involved.
- **Low** — minimal or not determined.

### Social
Determined by the number of people or properties affected (e.g. activities damaging home values).
- **Extremely Widespread** — 1,000+ people or 2,000+ properties; involves a top-10 contributor to the issue; long-lasting (over 5 years), severe economic harm (over USD 10B) across multiple countries.
- **Extensive** — 25–999 people or 100–1,999 properties; one of many companies participating in the activity.
- **Limited** — 10–24 people or 10–99 properties.
- **Low** — insignificant, minimal, or indeterminate.

Respond with `{"Scale of impact": "<category>", "Details": "<explanation>"}`.

## Company Role

Categorize as **Direct** or **Indirect**.

- **Direct** — the negative impact is directly attributed to the company's own actions, practices, products, or businesses (harm could not have happened without them), or the controversy involves an entity/joint venture the company significantly controls.
  - Example: a company implicated in a workplace incident causing employee fatalities.
  - Example: an oil refiner facing community opposition to a pipeline built by a subsidiary it owns 30% of.
  - Example: a medical device manufacturer sued over injuries linked to its own pacemakers.
- **Indirect** — the negative impact may have been facilitated by the company's actions/products/business but the company did not play a critical or essential role; also applies to adverse impacts from natural causes where the company is still responsible for remediation.
  - Example: a company facing allegations of unsafe conditions at a supplier's factory.
  - Example: an oil refiner facing opposition to a pipeline managed by a joint venture in which it holds only 20%.
  - Example: a distributor linked to a lawsuit over pacemakers it sells but does not manufacture.

Respond with `{"Company role": "<category>", "Details": "<explanation>"}`.

## Case Status

Classify into a Category and Sub-Category.

**Active**
- **Ongoing** — no remediation steps implemented to satisfy affected stakeholders' claims (e.g. compensation funds allocated but undistributed).
- **Partially Concluded** — reasonable evidence the company has taken remediation action (penalties paid, compensation distributed, settlements, reclamation, discontinuing the practice, adopting best practices), while some concerns/disputes remain ongoing.
- **Concluded** — all remedial actions complete, no pending legal actions or criticisms.

**Inactive**
- **Archived** — no new escalations post-resolution.
- **Historical Concern** — high-profile, concluded case still considered significant to the company's ESG profile.

Respond with `{"Status A": "<Active|Inactive>", "Status B": "<Ongoing|Partially Concluded|Concluded|Archived|Historical Concern>", "Details": "<explanation>"}`.
