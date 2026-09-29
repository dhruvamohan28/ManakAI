import re


def analyze_specification(text):
    text_lower = text.lower()

    result = {
        "product": None,
        "material": None,
        "application": None,
        "properties": [],
        "values": []
    }

    # Material detection
    if "steel" in text_lower:
        result["material"] = "steel"

    elif "concrete" in text_lower:
        result["material"] = "concrete"

    elif "cement" in text_lower:
        result["material"] = "cement"

    elif "aluminium" in text_lower or "aluminum" in text_lower:
        result["material"] = "aluminium"

    # Product detection
    if "steel plate" in text_lower or "steel plates" in text_lower:
        result["product"] = "structural steel plates"

    elif "steel bar" in text_lower or "steel bars" in text_lower:
        result["product"] = "steel bars"

    elif "concrete" in text_lower:
        result["product"] = "concrete"

    elif "brick" in text_lower or "bricks" in text_lower:
        result["product"] = "building bricks"

    elif "cable" in text_lower or "cables" in text_lower:
        result["product"] = "electrical cables"

    # Application detection
    if "bridge" in text_lower:
        result["application"] = "bridge construction"

    elif "building" in text_lower:
        result["application"] = "building construction"

    elif "road" in text_lower:
        result["application"] = "road construction"

    elif "electrical" in text_lower or "wiring" in text_lower:
        result["application"] = "electrical installation"

    # Property detection
    if "yield strength" in text_lower:
        result["properties"].append("yield strength")

    if "tensile strength" in text_lower:
        result["properties"].append("tensile strength")

    if "compressive strength" in text_lower:
        result["properties"].append("compressive strength")

    if "waterproof" in text_lower or "waterproofing" in text_lower:
        result["properties"].append("waterproofing")

    if "seismic" in text_lower or "earthquake" in text_lower:
        result["properties"].append("seismic resistance")

    # Numerical values with units
    values = re.findall(
        r'\b\d+(?:\.\d+)?\s*(?:MPa|GPa|kN|N/mm2|mm|cm|m|kg|kg/m3|%)\b',
        text,
        re.IGNORECASE
    )

    result["values"] = values

    return result


# -------------------------------
# TEST THE SPECIFICATION ANALYZER
# -------------------------------

if __name__ == "__main__":
    test_text = """
    Structural steel plates for bridge construction
    with minimum yield strength of 250 MPa.
    """

    analysis = analyze_specification(test_text)

    print("\nAI SPECIFICATION ANALYSIS")
    print("-------------------------")

    print("Product     :", analysis["product"])
    print("Material    :", analysis["material"])
    print("Application :", analysis["application"])
    print("Properties  :", analysis["properties"])
    print("Values      :", analysis["values"])