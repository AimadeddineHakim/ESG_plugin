# Worked example: Coca-Cola chemical leak

Manual regression fixture for the `esg-controversy-assessment` skill (ported from the original `assessement.ipynb`).

## Input

- **Company:** Coca-Cola
- **Text:**

> Hundreds of workers at a Coca-Cola plant in south-east London were evacuated following a chemical leak, with firefigthers working at the scene throughout the night.
> A hydrochloric acid leak at the plant on Cray Road in Sidcup caused the evacuation of around 200 workers before emergency services arrived on Wednesday evening.
> London Fire Brigade firefighters isolated the leak at 11.30pm and remained at the scene throughout the night taking readings of chemicals in the air.
> Teams used chemical equipment to test the levels of chemicals in the area and worked on site to disperse it.
> There were no reports of injuries.
> The Brigade was called at 8.39pm and the incident was handed over to onsite management at 05.26am.
> "The leak was isolated at approximately 23:30 and we remained on scene throughout the night doing checks before we left. The incident is now over," the Brigade said in a statement.
> "There was no evacuation of residents, and no-one was treated by emergency services. We are not aware of any advice to close windows and doors."
> A spokesperson for Coca-Cola Europacific Partners said: "Our production site at Sidcup was temporarily evacuated last night as a precautionary measure. There was no risk to any of our colleagues and the issue has now been resolved.
> "Our site is now back operating as normal. We would like to thank the emergency services for their swift response and support, and would like to apologise to local residents for any disruption caused overnight."
> Hydrochloric acid is used for refining ore in the production of tin and tantalum, for pickling and cleaning of metal products. It is a clear, colourless and pungent solution.

## Expected assessment

```json
{
  "Category": "Environmental",
  "Pillar": "Toxic Emissions & Waste",
  "Nature of harm": {
    "Nature of harm": "Minimal",
    "Details": "No reports of injuries, wildlife harm, or long-term environmental damage; the leak was contained and operations resumed normally."
  },
  "Scale of impact": {
    "Scale of impact": "Low",
    "Details": "Affected only the immediate plant area; no resident evacuation or documented environmental harm beyond the site."
  },
  "Role of the company": {
    "Company role": "Direct",
    "Details": "The leak occurred at the company's own production site and involved its own operations/safety protocols."
  },
  "status": {
    "Status A": "Active",
    "Status B": "Ongoing",
    "Details": "The leak was isolated and resolved, but no details are given on preventive measures for future incidents."
  },
  "Severity": "Minor",
  "Score": 6,
  "Flag": "Green Flag"
}
```

Verify the scoring step directly:

```
scripts/score.py "Minimal" "Low" "Direct" "Ongoing"
# Severity: Minor
# Score: 6
# Flag: Green Flag
```
