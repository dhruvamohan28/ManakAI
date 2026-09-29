import pandas as pd


# --------------------------------
# LOAD STANDARDS DATABASE
# --------------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "standards.csv")


# --------------------------------
# FIND MISSING REFERENCES
# --------------------------------

def check_missing_references(
    specification,
    recommended_standards
):

    missing_references = []

    specification_upper = specification.upper()

    for standard in recommended_standards:

        standard_number = standard["standard"]

        # Find standard in database
        matches = df[
            df["is_number"].str.upper()
            == standard_number.upper()
        ]

        if matches.empty:
            continue

        row = matches.iloc[0]

        # ----------------------------
        # NORMATIVE REFERENCES
        # ----------------------------

        normative = str(
            row.get(
                "normative_references",
                ""
            )
        )

        if normative and normative.lower() != "nan":

            references = [
                ref.strip()
                for ref in normative.split(";")
                if ref.strip()
            ]

            for reference in references:

                if reference.upper() not in specification_upper:

                    missing_references.append({

                        "recommended_standard":
                            standard_number,

                        "missing_standard":
                            reference,

                        "type":
                            "Normative Reference",

                        "message":
                            f"{reference} is associated "
                            f"with {standard_number} but "
                            f"was not mentioned in the "
                            f"specification."

                    })

        # ----------------------------
        # ALLIED STANDARDS
        # ----------------------------

        allied = str(
            row.get(
                "allied_standards",
                ""
            )
        )

        if allied and allied.lower() != "nan":

            references = [
                ref.strip()
                for ref in allied.split(";")
                if ref.strip()
            ]

            for reference in references:

                if reference.upper() not in specification_upper:

                    missing_references.append({

                        "recommended_standard":
                            standard_number,

                        "missing_standard":
                            reference,

                        "type":
                            "Allied Standard",

                        "message":
                            f"{reference} is associated "
                            f"with {standard_number} but "
                            f"was not mentioned in the "
                            f"specification."

                    })

    return missing_references


# --------------------------------
# TEST
# --------------------------------
if __name__ == "__main__":
    test_specification = """
    Structural steel plates for bridge construction
    with minimum yield strength of 250 MPa
    according to IS 2062:2025.
    """


    test_recommendations = [

        {
            "standard": "IS 2062"
        }

    ]


    results = check_missing_references(
        test_specification,
        test_recommendations
    )


    print("\nMISSING REFERENCE CHECK")
    print("-----------------------")


    if not results:

        print(
            "No potential missing references detected."
        )

    else:

        for result in results:

            print(
                "\n⚠ Potential Missing Reference"
            )

            print(
                "Recommended Standard:",
                result["recommended_standard"]
            )

            print(
                "Missing Standard:",
                result["missing_standard"]
            )

            print(
                "Type:",
                result["type"]
            )

            print(
                result["message"]
            )