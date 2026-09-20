#!/usr/bin/env python3
"""CLI: given nature-of-harm, scale-of-impact, company role, and case status,
print the deterministic severity level and (score, flag) from the ESG scoring matrix."""

import sys

SEVERITY_MATRIX = {
    "Extremely Widespread": {
        "Very Serious": "Very Severe",
        "Serious": "Severe",
        "Medium": "Severe",
        "Minimal": "Moderate",
    },
    "Extensive": {
        "Very Serious": "Very Severe",
        "Serious": "Severe",
        "Medium": "Moderate",
        "Minimal": "Moderate",
    },
    "Limited": {
        "Very Serious": "Severe",
        "Serious": "Moderate",
        "Medium": "Minor",
        "Minimal": "Minor",
    },
    "Low": {
        "Very Serious": "Moderate",
        "Serious": "Moderate",
        "Medium": "Minor",
        "Minimal": "Minor",
    },
}

SCORING_MATRIX = {
    ("Very Severe", "Direct", "Ongoing"): (0, "Red Flag"),
    ("Very Severe", "Direct", "Partially Concluded"): (1, "Orange Flag"),
    ("Very Severe", "Direct", "Concluded"): (2, "Yellow Flag"),
    ("Very Severe", "Indirect", "Ongoing"): (1, "Orange Flag"),
    ("Very Severe", "Indirect", "Partially Concluded"): (2, "Yellow Flag"),
    ("Very Severe", "Indirect", "Concluded"): (3, "Yellow Flag"),

    ("Severe", "Direct", "Ongoing"): (1, "Orange Flag"),
    ("Severe", "Direct", "Partially Concluded"): (2, "Yellow Flag"),
    ("Severe", "Direct", "Concluded"): (3, "Yellow Flag"),
    ("Severe", "Indirect", "Ongoing"): (2, "Yellow Flag"),
    ("Severe", "Indirect", "Partially Concluded"): (3, "Yellow Flag"),
    ("Severe", "Indirect", "Concluded"): (4, "Green Flag"),

    ("Moderate", "Direct", "Ongoing"): (4, "Yellow Flag"),
    ("Moderate", "Direct", "Partially Concluded"): (5, "Green Flag"),
    ("Moderate", "Direct", "Concluded"): (6, "Green Flag"),
    ("Moderate", "Indirect", "Ongoing"): (5, "Green Flag"),
    ("Moderate", "Indirect", "Partially Concluded"): (6, "Green Flag"),
    ("Moderate", "Indirect", "Concluded"): (7, "Green Flag"),

    ("Minor", "Direct", "Ongoing"): (6, "Green Flag"),
    ("Minor", "Direct", "Partially Concluded"): (7, "Green Flag"),
    ("Minor", "Direct", "Concluded"): (8, "Green Flag"),
    ("Minor", "Indirect", "Ongoing"): (7, "Green Flag"),
    ("Minor", "Indirect", "Partially Concluded"): (8, "Green Flag"),
    ("Minor", "Indirect", "Concluded"): (9, "Green Flag"),
}


def severity(harm, impact):
    if impact in SEVERITY_MATRIX and harm in SEVERITY_MATRIX[impact]:
        return SEVERITY_MATRIX[impact][harm]
    return "Invalid input"


def assessment_score(severity_level, role, status):
    return SCORING_MATRIX.get((severity_level, role, status), (None, "Invalid Input"))


def main():
    if len(sys.argv) != 5:
        print(
            "Usage: score.py <nature_of_harm> <scale_of_impact> <company_role> <case_status>\n"
            "  nature_of_harm  : Very Serious | Serious | Medium | Minimal\n"
            "  scale_of_impact : Extremely Widespread | Extensive | Limited | Low\n"
            "  company_role    : Direct | Indirect\n"
            "  case_status     : Ongoing | Partially Concluded | Concluded",
            file=sys.stderr,
        )
        sys.exit(1)

    harm, impact, role, status = sys.argv[1:5]

    severity_level = severity(harm, impact)
    if severity_level == "Invalid input":
        print(f"Invalid input: unrecognized nature_of_harm/scale_of_impact combination ({harm!r}, {impact!r})", file=sys.stderr)
        sys.exit(1)

    score, flag = assessment_score(severity_level, role, status)
    if score is None:
        print(f"Invalid input: unrecognized severity/role/status combination ({severity_level!r}, {role!r}, {status!r})", file=sys.stderr)
        sys.exit(1)

    print(f"Severity: {severity_level}")
    print(f"Score: {score}")
    print(f"Flag: {flag}")


if __name__ == "__main__":
    main()
