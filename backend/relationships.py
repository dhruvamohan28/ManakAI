import pandas as pd
import re

# Load standards database
df = pd.read_csv("standards.csv")


def normalize_standard(standard):
    """
    Converts:
    IS 2062:2025
    IS-2062:2025
    IS 2062 2025

    into:
    IS 2062
    """

    if not standard:
        return None

    standard = str(standard).upper().strip()

    match = re.search(r"(IS[-\s]*\d+)", standard)

    if not match:
        return None

    standard_number = match.group(1).replace("-", " ")
    standard_number = re.sub(r"\s+", " ", standard_number)

    return standard_number


def split_references(value):
    """
    Converts a reference field into a clean list.
    """

    if pd.isna(value) or str(value).strip() == "":
        return []

    return [
        item.strip()
        for item in str(value).split(",")
        if item.strip()
    ]


def get_relationships(standard):
    """
    Finds allied, normative and cross-reference standards.
    """

    standard_number = normalize_standard(standard)

    if not standard_number:
        return {
            "found": False,
            "allied": [],
            "normative": [],
            "cross_reference": []
        }

    result = df[
        df["is_number"].str.upper() == standard_number
    ]

    if result.empty:
        return {
            "found": False,
            "allied": [],
            "normative": [],
            "cross_reference": []
        }

    row = result.iloc[0]

    return {
        "found": True,
        "allied": split_references(row["allied_standards"]),
        "normative": split_references(row["normative_references"]),
        "cross_reference": split_references(row["cross_references"])
    }


# Test
if __name__ == "__main__":

    print("\n--- Relationship Mapping Test ---")

    tests = [
        "IS 2062",
        "IS 2062:2025",
        "IS-2062:2025",
        "IS 9999"
    ]

    for test_standard in tests:

        print("\nStandard:", test_standard)

        result = get_relationships(test_standard)

        print("Found:", result["found"])
        print("Allied:", result["allied"])
        print("Normative:", result["normative"])
        print("Cross-reference:", result["cross_reference"])
        