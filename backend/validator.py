import pandas as pd
import re

# Load standards database
df = pd.read_csv("standards.csv")


def normalize_standard(standard):
    """
    Converts different standard formats into:
    standard number + revision year

    Examples:
    IS 2062:2011
    IS-2062:2011
    IS 2062 2011

    Result:
    IS 2062, 2011
    """

    if not standard:
        return None, None

    standard = str(standard).upper().strip()

    match = re.search(r"(IS[-\s]*\d+)\s*:?\s*(\d{4})?", standard)

    if not match:
        return None, None

    standard_number = match.group(1).replace("-", " ")
    standard_number = re.sub(r"\s+", " ", standard_number)

    revision = match.group(2)

    return standard_number, revision


def validate_version(standard):
    """
    Checks whether a standard version is current,
    outdated, or newer than the database.
    """

    standard_number, revision = normalize_standard(standard)

    if not standard_number:
        return {
            "standard": standard,
            "found": False,
            "status": "invalid",
            "outdated": False,
            "message": "Could not understand the standard number."
        }

    result = df[df["is_number"].str.upper() == standard_number]

    if result.empty:
        return {
            "standard": standard,
            "found": False,
            "status": "not_found",
            "outdated": False,
            "message": "Standard not found in database."
        }

    latest_revision = str(result.iloc[0]["revision"])

    # No revision supplied
    if not revision:
        return {
            "standard": standard,
            "found": True,
            "status": "revision_not_provided",
            "outdated": False,
            "latest_revision": latest_revision,
            "message": "Revision year was not provided."
        }

    current_year = int(revision)
    latest_year = int(latest_revision)

    # Older than database version
    if current_year < latest_year:
        return {
            "standard": standard,
            "found": True,
            "status": "outdated",
            "outdated": True,
            "current_revision": revision,
            "latest_revision": latest_revision,
            "message": f"Outdated. Latest revision is {latest_revision}."
        }

    # Same as database version
    if current_year == latest_year:
        return {
            "standard": standard,
            "found": True,
            "status": "current",
            "outdated": False,
            "current_revision": revision,
            "latest_revision": latest_revision,
            "message": "Standard version is current."
        }

    # Newer than database version
    return {
        "standard": standard,
        "found": True,
        "status": "newer_than_database",
        "outdated": False,
        "current_revision": revision,
        "latest_revision": latest_revision,
        "message": (
            f"Revision {revision} is newer than the database "
            f"revision {latest_revision}."
        )
    }


def check_missing_references(standard, specification_text):
    """
    Checks whether normative references of a standard
    are mentioned in the specification text.
    """

    standard_number, revision = normalize_standard(standard)

    if not standard_number:
        return []

    result = df[df["is_number"].str.upper() == standard_number]

    if result.empty:
        return []

    row = result.iloc[0]

    normative = []

    if not pd.isna(row["normative_references"]):
        normative = [
            item.strip()
            for item in str(row["normative_references"]).split(",")
            if item.strip()
        ]

    specification_text = str(specification_text).upper()

    missing = []

    for reference in normative:
        if reference.upper() not in specification_text:
            missing.append(reference)

    return missing


# Test
if __name__ == "__main__":

    print("\n--- Version Validation Test ---")

    tests = [
        "IS 2062:2011",
        "IS 2062:2025",
        "IS-2062:2025",
        "IS 9999:2020",
        "IS 2062:2030"
    ]

    for test in tests:
        print("\nInput:", test)
        print(validate_version(test))