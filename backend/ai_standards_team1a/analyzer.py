from .ai_engine import analyze_specification
from .matcher import match_standards
from .validator import validate_versions
from .reference_checker import check_missing_references
from .relationship_mapper import get_related_standards


# ==================================================
# MAIN PROCUREMENT ANALYSIS FUNCTION
# ==================================================

def analyze_procurement_specification(specification):

    # ----------------------------------------------
    # 1. ANALYZE SPECIFICATION
    # ----------------------------------------------

    analysis = analyze_specification(
        specification
    )

    # ----------------------------------------------
    # 2. VALIDATE STANDARD VERSIONS
    # ----------------------------------------------

    version_check = validate_versions(
        specification
    )

    # ----------------------------------------------
    # 3. FIND MATCHING STANDARDS
    # ----------------------------------------------

    matches = match_standards(
        specification,
        top_n=5
    )

    # ----------------------------------------------
    # 4. PREPARE RECOMMENDATIONS
    # ----------------------------------------------

    recommendations = []

    if matches is not None:

        for _, row in matches.iterrows():

            recommendations.append({

                "standard": str(
                    row["is_number"]
                ),

                "title": str(
                    row["title"]
                ),

                "match": round(
                    float(row["similarity"]) * 100,
                    2
                ),

                "domain": str(
                    row["domain"]
                ),

                "revision": str(
                    row["revision"]
                ),

                "status": str(
                    row["status"]
                )
            })

    # ----------------------------------------------
    # 5. CHECK MISSING REFERENCES
    # ----------------------------------------------

    missing_references = (
        check_missing_references(
            specification,
            recommendations
        )
    )

    # ----------------------------------------------
    # 6. FIND RELATED STANDARDS
    # ----------------------------------------------

    related_standards = []

    for recommendation in recommendations:

        relationship = get_related_standards(
            recommendation["standard"]
        )

        related_standards.append(
            relationship
        )

    # ----------------------------------------------
    # 7. CREATE FINAL RESULT
    # ----------------------------------------------

    result = {

        "specification": specification,

        "analysis": analysis,

        "recommendations": recommendations,

        "version_check": version_check,

        "missing_references": missing_references,

        "related_standards": related_standards
    }

    return result


# ==================================================
# TEST THE COMPLETE SYSTEM
# ==================================================

if __name__ == "__main__":

    test_specification = """
    Structural steel plates for bridge construction
    with minimum yield strength of 250 MPa
    according to IS 2062:2011.
    """

    result = analyze_procurement_specification(
        test_specification
    )

    # ----------------------------------------------
    # DISPLAY RESULT
    # ----------------------------------------------

    print("\n")
    print("=" * 60)
    print("AI PROCUREMENT SPECIFICATION ANALYSIS")
    print("=" * 60)

    print("\nSPECIFICATION")
    print("-------------")
    print(result["specification"])

    # ----------------------------------------------
    # ANALYSIS
    # ----------------------------------------------

    print("\nEXTRACTED INFORMATION")
    print("---------------------")

    analysis = result["analysis"]

    print(
        "Product     :",
        analysis["product"]
    )

    print(
        "Material    :",
        analysis["material"]
    )

    print(
        "Application :",
        analysis["application"]
    )

    print(
        "Properties  :",
        analysis["properties"]
    )

    print(
        "Values      :",
        analysis["values"]
    )

    # ----------------------------------------------
    # RECOMMENDATIONS
    # ----------------------------------------------

    print("\nRECOMMENDED STANDARDS")
    print("---------------------")

    if not result["recommendations"]:

        print(
            "No strong matching standard found."
        )

    else:

        for index, standard in enumerate(
            result["recommendations"],
            start=1
        ):

            print(
                f"\n{index}. "
                f"{standard['standard']}"
            )

            print(
                "   Title     :",
                standard["title"]
            )

            print(
                "   Match     :",
                f"{standard['match']}%"
            )

            print(
                "   Domain    :",
                standard["domain"]
            )

            print(
                "   Revision  :",
                standard["revision"]
            )

            print(
                "   Status    :",
                standard["status"]
            )

    # ----------------------------------------------
    # VERSION VALIDATION
    # ----------------------------------------------

    print("\nVERSION VALIDATION")
    print("------------------")

    if not result["version_check"]:

        print(
            "No explicit standard version found."
        )

    else:

        for version in result["version_check"]:

            print(
                "\nStandard:",
                version["standard"]
            )

            print(
                "Referenced:",
                version["referenced_revision"]
            )

            if version.get("outdated") is True:

                print(
                    "⚠ OUTDATED"
                )

                print(
                    "Latest:",
                    version["latest_revision"]
                )

                print(
                    version["message"]
                )

            elif version.get("outdated") is False:

                print(
                    "✓ CURRENT"
                )

                print(
                    "Latest:",
                    version["latest_revision"]
                )

            else:

                print(
                    "Status:",
                    version["status"]
                )

    # ----------------------------------------------
    # MISSING REFERENCES
    # ----------------------------------------------

    print("\nMISSING REFERENCE CHECK")
    print("-----------------------")

    if not result["missing_references"]:

        print(
            "No potential missing references detected."
        )

    else:

        for reference in result[
            "missing_references"
        ]:

            print(
                "\n⚠ Potential Missing Reference"
            )

            print(
                "Recommended Standard:",
                reference[
                    "recommended_standard"
                ]
            )

            print(
                "Missing Standard:",
                reference[
                    "missing_standard"
                ]
            )

            print(
                "Type:",
                reference["type"]
            )

    # ----------------------------------------------
    # RELATED STANDARDS
    # ----------------------------------------------

    print("\nRELATED STANDARDS")
    print("-----------------")

    if not result["related_standards"]:

        print(
            "No related standards found."
        )

    else:

        for relationship in result[
            "related_standards"
        ]:

            print(
                "\nMain Standard:",
                relationship["standard"]
            )

            print("  Allied:")

            if relationship["allied"]:

                for standard in relationship["allied"]:

                    print(
                        "    →",
                        standard
                    )

            else:

                print("    None")

            print("  Normative:")

            if relationship["normative"]:

                for standard in relationship[
                    "normative"
                ]:

                    print(
                        "    →",
                        standard
                    )

            else:

                print("    None")

            print("  Cross References:")

            if relationship[
                "cross_references"
            ]:

                for standard in relationship[
                    "cross_references"
                ]:

                    print(
                        "    →",
                        standard
                    )

            else:

                print("    None")