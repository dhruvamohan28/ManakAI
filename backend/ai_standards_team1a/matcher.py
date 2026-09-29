import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# --------------------------------
# 1. LOAD THE STANDARDS DATASET
# --------------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "standards.csv")


# --------------------------------
# 2. PREPARE STANDARD TEXT
# --------------------------------

df["combined_text"] = (
    df["title"].fillna("") + " " +
    df["description"].fillna("") + " " +
    df["keywords"].fillna("")
)


# --------------------------------
# 3. CREATE TF-IDF VECTORIZER
# --------------------------------

vectorizer = TfidfVectorizer(
    stop_words="english"
)


# Convert all standards into TF-IDF vectors
standard_vectors = vectorizer.fit_transform(
    df["combined_text"]
)

# --------------------------------
# SEMANTIC AI MODEL
# --------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

standard_embeddings = model.encode(
    df["combined_text"].tolist()
)

# --------------------------------
# 4. MATCH SPECIFICATION
# --------------------------------

def match_standards(specification, top_n=5):

    # Convert user's specification into TF-IDF
    query_vector = vectorizer.transform(
        [specification]
    )

    # Calculate similarity
    similarities = cosine_similarity(
        query_vector,
        standard_vectors
    )[0]

    # Semantic similarity
    query_embedding = model.encode(
        [specification]
    )

    semantic_scores = cosine_similarity(
        query_embedding,
        standard_embeddings
    )[0]

    # Combine TF-IDF and semantic similarity

    final_scores = (
        0.4 * similarities +
        0.6 * semantic_scores
    )

    # Copy dataset
    results = df.copy()

    # Add similarity scores
    results["similarity"] = final_scores

    # Sort highest similarity first
    results = results.sort_values(
        by="similarity",
        ascending=False
    )

    # Return top results
    # If the best match is too weak,
    # don't recommend a standard.

    if results.iloc[0]["similarity"] < 0.30:
      return None

    return results.head(top_n)


# --------------------------------
# 5. TEST THE MATCHING SYSTEM
# --------------------------------

if __name__ == "__main__":
    test_specification = """
    Structural steel plates for bridge construction with minimum yield strength of 250 MPa.
    """


    results = match_standards(
        test_specification,
        top_n=5
    )


    # --------------------------------
    # 6. DISPLAY RESULTS
    # --------------------------------

    if results is None:

        print("\nNo strong matching standard found.")

    else:

        for _, row in results.iterrows():

            score = row["similarity"] * 100

            print(
                f"{row['is_number']} "
                f"→ {score:.2f}%"
            )