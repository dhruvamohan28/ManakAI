import pandas as pd


# --------------------------------
# LOAD STANDARDS DATABASE
# --------------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "standards.csv")


# --------------------------------
# HELPER FUNCTION
# --------------------------------

def get_references(value):

    if pd.isna(value):
        return []

    value = str(value).strip()

    if not value:
        return []

    return [
        item.strip()
        for item in value.split(";")
        if item.strip()
    ]


# --------------------------------
# FIND RELATED STANDARDS
# --------------------------------

def get_related_standards(standard_number):

    matches = df[
        df["is_number"].str.upper()
        == standard_number.upper()
    ]

    if matches.empty:
        return {
            "standard": standard_number,
            "allied": [],
            "normative": [],
            "cross_references": []
        }

    row = matches.iloc[0]

    allied = get_references(
        row.get("allied_standards", "")
    )

    normative = get_references(
        row.get("normative_references", "")
    )

    cross_references = get_references(
        row.get("cross_references", "")
    )

    return {
        "standard": standard_number,
        "allied": allied,
        "normative": normative,
        "cross_references": cross_references
    }


# --------------------------------
# TEST
# --------------------------------
if __name__ == "__main__":
    test_standard = "IS 2062"

    result = get_related_standards(
        test_standard
    )


    print("\nRELATED STANDARDS")
    print("-----------------")

    print(
        "\nMain Standard:",
        result["standard"]
    )


    print("\nAllied Standards:")

    if result["allied"]:

        for standard in result["allied"]:
            print("  →", standard)

    else:

        print("  None")


    print("\nNormative References:")

    if result["normative"]:

        for standard in result["normative"]:
            print("  →", standard)

    else:

        print("  None")


    print("\nCross References:")

    if result["cross_references"]:

        for standard in result["cross_references"]:
            print("  →", standard)

    else:

         print("  None")