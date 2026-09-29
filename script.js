const API_URL = "http://127.0.0.1:5000/analyze";

const specificationInput = document.getElementById("specification");
const charCount = document.getElementById("charCount");


// Character counter
if (specificationInput && charCount) {
    specificationInput.addEventListener("input", function () {
        charCount.textContent = this.value.length;
    });
}


// Scroll to Analyzer
function scrollToAnalyzer() {
    const analyzer = document.getElementById("analyzer");

    if (analyzer) {
        analyzer.scrollIntoView({
            behavior: "smooth"
        });
    }
}


// Scroll to How It Works
function scrollToHowItWorks() {
    const section = document.getElementById("how-it-works");

    if (section) {
        section.scrollIntoView({
            behavior: "smooth"
        });
    }
}


// Main Analyze Function
async function analyzeSpecification() {

    const specification = specificationInput.value.trim();

    if (!specification) {
        alert("Please enter a technical specification first.");
        return;
    }

    // Hide analyzer
    document.getElementById("analyzer").classList.add("hidden");

    // Show loading
    document.getElementById("loading-section").classList.remove("hidden");

    try {

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                specification: specification
            })
        });

        if (!response.ok) {
            throw new Error("Backend request failed");
        }

        const data = await response.json();

        console.log("Backend Response:", data);

        // Hide loading
        document.getElementById("loading-section").classList.add("hidden");

        // Show results
        document.getElementById("results-section").classList.remove("hidden");

        // Display backend results
        displayBackendResults(data);

        // Scroll to results
        document.getElementById("results-section").scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {

        console.error("API Error:", error);

        document.getElementById("loading-section").classList.add("hidden");

        document.getElementById("analyzer").classList.remove("hidden");

        alert(
            "Unable to connect to the AI backend.\n\n" +
            "Please make sure Team 1 backend is running."
        );
    }
}


// Display Backend Results
function displayBackendResults(data) {

    const recommendations = data.recommendations || [];
    const missingReferences = data.missing_references || [];
    const versionCheck = data.version_check || {};

    console.log("Recommendations:", recommendations);
    console.log("Missing References:", missingReferences);
    console.log("Version Check:", versionCheck);


    // -----------------------------
    // Summary Boxes
    // -----------------------------

    const summaryBoxes = document.querySelectorAll(".summary-box");

    if (summaryBoxes.length >= 4) {

        // Standards Found
        summaryBoxes[0].querySelector("strong").textContent =
            String(recommendations.length).padStart(2, "0");


        // Top Match
        if (recommendations.length > 0) {

            summaryBoxes[1].querySelector("strong").textContent =
                Math.round(recommendations[0].match) + "%";

        } else {

            summaryBoxes[1].querySelector("strong").textContent =
                "0%";
        }


        // Validation
        const hasMissingReferences =
            missingReferences.length > 0;

        summaryBoxes[2].querySelector("strong").textContent =
            hasMissingReferences ? "Review" : "Passed";


        // References
        summaryBoxes[3].querySelector("strong").textContent =
            String(missingReferences.length).padStart(2, "0");
    }


    // -----------------------------
    // Recommended Standards
    // -----------------------------

    // -----------------------------
// Recommended Standards
// -----------------------------

const recommendedContainer =
    document.getElementById("recommended-standards-container");

if (recommendedContainer) {

    recommendedContainer.innerHTML = "";

    if (recommendations.length === 0) {

        recommendedContainer.innerHTML = `
            <div class="standard-card">
                <div class="standard-title">
                    No recommendations found
                </div>

                <div class="standard-description">
                    The AI backend did not return any matching standards.
                </div>
            </div>
        `;

    } else {

        recommendations.forEach((standard) => {

            const card =
                document.createElement("div");

            card.className = "standard-card";

            const matchValue =
                Math.round(Number(standard.match) || 0);

            card.innerHTML = `
                <div class="standard-main">

                    <div>

                        <div class="standard-title">
                            ${standard.standard}:${standard.revision}
                        </div>

                        <div class="standard-description">
                            ${standard.title}
                        </div>

                    </div>

                    <div class="match-score">

                        <strong>
                            ${matchValue}%
                        </strong>

                        <span>
                            Match
                        </span>

                    </div>

                </div>


                <div class="match-bar">

                    <div
                        class="match-progress"
                        style="width: ${matchValue}%"
                    ></div>

                </div>


                <div class="recommendation-reason">

                    <strong>
                        Why recommended?
                    </strong>

                    <ul>

                        <li>
                            ✓ Product context matches
                        </li>

                        <li>
                            ✓ Application/domain: ${standard.domain}
                        </li>

                        <li>
                            ✓ Standard status: ${standard.status}
                        </li>

                    </ul>

                </div>

            `;

            recommendedContainer.appendChild(card);

        });
    }
}
    // -----------------------------
    // Missing References
    // -----------------------------

    const missingContainer =
        document.getElementById(
            "missing-references-container"
        );


    if (missingContainer) {

        if (missingReferences.length === 0) {

            missingContainer.innerHTML = `
                <div class="no-missing-references">
                    No missing references detected.
                </div>
            `;

        } else {

            missingContainer.innerHTML = "";


            missingReferences.forEach(reference => {

                const card =
                    document.createElement("div");

                card.className =
                    "missing-reference-item";


                card.innerHTML = `
                    <div>
                        <strong>
                            ${reference.missing_standard}
                        </strong>

                        <p>
                            ${reference.message}
                        </p>
                    </div>

                    <span class="reference-type">
                        ${reference.type}
                    </span>
                `;


                missingContainer.appendChild(card);

            });
        }
    }
}
// -----------------------------
// Final Recommendation
// -----------------------------

const finalRecommendation =
    document.getElementById("final-recommendation-text");

if (finalRecommendation) {

    if (recommendations.length > 0) {

        const topStandard = recommendations[0];

        finalRecommendation.textContent =
            `Review ${topStandard.standard}:${topStandard.revision} ` +
            `(${topStandard.title}) and its associated standards ` +
            `before finalizing the procurement specification.`;

    } else {

        finalRecommendation.textContent =
            "No matching Indian Standard was identified. " +
            "Please review the specification manually.";

    }
}

// New Analysis
function newAnalysis() {

    document
        .getElementById("results-section")
        .classList.add("hidden");


    document
        .getElementById("analyzer")
        .classList.remove("hidden");


    specificationInput.value = "";


    if (charCount) {
        charCount.textContent = "0";
    }


    scrollToAnalyzer();
}