import re
import pandas as pd


# --------------------------------
# LOAD STANDARDS DATABASE
# --------------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "standards.csv")


# --------------------------------
# VERSION VALIDATION FUNCTION
# --------------------------------

def validate_versions(specification):

    results = []

    # Find standards written like:
    # IS 2062:2011
    # IS 800:2007
    # IS 456-2000

    pattern = r'\bIS\s*(\d+)\s*[:\-]\s*(\d{4})\b'

    references = re.findall(
        pattern,
        specification,
        re.IGNORECASE
    )

    for standard_number, referenced_year in references:

        standard_number = f"IS {standard_number}"

        referenced_year = int(referenced_year)

        # Find the standard in our database
        matches = df[
            df["is_number"].str.upper() == standard_number.upper()
        ]

        if matches.empty:

            results.append({
                "standard": standard_number,
                "referenced_revision": referenced_year,
                "status": "Not found in database"
            })

            continue

        # Get latest revision from database
        latest_year = int(
            matches["revision"].max()
        )

        if referenced_year < latest_year:

            results.append({
                "standard": standard_number,
                "referenced_revision": referenced_year,
                "latest_revision": latest_year,
                "outdated": True,
                "message": (
                    f"{standard_number}:{referenced_year} "
                    f"is older than "
                    f"{standard_number}:{latest_year}"
                )
            })

        else:

            results.append({
                "standard": standard_number,
                "referenced_revision": referenced_year,
                "latest_revision": latest_year,
                "outdated": False,
                "message": (
                    f"{standard_number}:{referenced_year} "
                    f"is current according to the database"
                )
            })

    return results


# --------------------------------
# TEST
# --------------------------------
if __name__ == "__main__":
    test_specification = """
    Structural steel plates for bridge construction
    .
    """


    results = validate_versions(
        test_specification
    )


    print("\nVERSION VALIDATION")
    print("------------------")

    if not results:

        print("No explicit standard version found.")

    else:

        for result in results:

            print("\nStandard:", result["standard"])
            print(
                "Referenced revision:",
                result["referenced_revision"]
            )

            if result.get("outdated") is True:

               print(
                    "⚠ OUTDATED"
                )

               print(
                    "Latest revision:",
                    result["latest_revision"]
                )

               print(
                    result["message"]
                )

            elif result.get("outdated") is False:

                print("✓ CURRENT")

                print(
                    "Latest revision:",
                    result["latest_revision"]
                )

            else:

                print(
                   "Status:",
                   result["status"]
                )