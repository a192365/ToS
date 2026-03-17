import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Clause Risk Detector",
    page_icon="🔎",
    layout="wide"
)

st.markdown(
    """
    <style>
    h1 {
        font-size: 2.2rem !important;
        margin-bottom: 0.2rem !important;
    }
    h2 {
        font-size: 1.5rem !important;
        margin-top: 1.2rem !important;
        margin-bottom: 0.5rem !important;
    }
    h3 {
        font-size: 1.15rem !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.3rem !important;
    }
    p, li {
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    .block-container {
        padding-top: 2rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def label_text(label: int) -> str:
    return "Potentially unfair" if label == 1 else "Not unfair"


def label_icon(label: int) -> str:
    return "⚠️" if label == 1 else "✅"


def similarity_level(score: float) -> str:
    # lower FAISS L2 distance = more similar
    if score < 0.45:
        return "High similarity"
    elif score < 0.75:
        return "Medium similarity"
    return "Low similarity"


st.markdown("# Clause Risk Detector")
st.caption(
    "Analyzes Terms of Service clauses to identify potential risks and detect clauses that may be unfair."
)

st.markdown(
    """
This tool helps you explore Terms of Service clauses in two ways:

- **Semantic Search**: find clauses from real companies that are similar to a concern or clause you type
- **Clause Classification**: estimate whether a clause may be unfair
"""
)

tab1, tab2 = st.tabs(["Semantic Search", "Clause Classification"])


with tab1:
    st.markdown("## Semantic Search")

    st.markdown(
        """
### What is this tool for?

Use **Semantic Search** if your goal is to:

- check whether a clause in your contract looks similar to clauses found in other Terms of Service documents
- find examples of how other companies write similar clauses
- compare wording across companies
"""
    )

    st.markdown(
        """
### How to use it

1. Type a **concern** or a **clause** in the text box below  
2. Choose how many results you want to see  
3. Click **Search**
"""
    )

    query = st.text_area(
        "Type a concern or clause",
        value="we may change these terms at any time without notice",
        height=120,
    )

    top_k = st.number_input("Number of results", min_value=1, max_value=20, value=5)

    st.markdown(
        """
### How to interpret the results

For each result, the tool shows:

- the **company** where the clause was found
- the **clause text**
- the **dataset label** (`Potentially unfair` or `Not unfair`)
- the **similarity score**

**Important:**  
- **smaller score = more similar clause**
- similarity levels are defined as:
  - **High similarity**: score **< 0.45**
  - **Medium similarity**: score **>= 0.45 and < 0.75**
  - **Low similarity**: score **>= 0.75**
"""
    )

    if st.button("Search", use_container_width=True):
        response = requests.post(
            f"{API_URL}/search",
            json={"query": query, "top_k": int(top_k)},
            timeout=60,
        )

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])

            st.divider()
            st.markdown("### Your query")
            st.code(query, language=None)

            st.markdown("### Clauses found")

            if not results:
                st.warning("No clauses were found.")
            else:
                for i, item in enumerate(results, start=1):
                    score = float(item["score"])

                    with st.container(border=True):
                        st.markdown(f"### Result {i}")

                        col1, col2 = st.columns([2, 1])

                        with col1:
                            st.markdown(f"**Company**: {item['company']}")
                            st.markdown("**Clause found**:")
                            st.write(item["sentence"])

                        with col2:
                            st.markdown(f"**Score**: {score:.3f}")
                            st.markdown(f"**Similarity**: {similarity_level(score)}")
                            st.markdown(
                                f"**Dataset label**: {label_icon(item['label'])} {label_text(item['label'])}"
                            )

                        st.caption(
                            "Lower score means the clause is closer to your query. "
                            "Rule used: High < 0.45, Medium 0.45-0.74, Low >= 0.75."
                        )
        else:
            st.error(f"Search request failed: {response.text}")


with tab2:
    st.markdown("## Clause Classification")

    st.markdown(
        """
### What is this tool for?

Use **Clause Classification** if your goal is to:

- understand whether a clause may be unfair
- get a quick estimate of clause risk
- compare clauses before reviewing them in more detail
"""
    )

    st.markdown(
        """
### How to use it

1. Paste a clause into the text box below  
2. Click **Classify**
"""
    )

    text = st.text_area(
        "Type a clause to classify",
        value="we may terminate your account at any time without notice",
        height=120,
    )

    st.markdown(
        """
### How to interpret the result

The tool returns:

- a **prediction**
- a **percentage** showing how likely the clause is to be unfair

**Important:**  
- **higher percentage = more likely to be unfair**
- **lower percentage = more likely to be acceptable**
"""
    )

    if st.button("Classify", use_container_width=True):
        response = requests.post(
            f"{API_URL}/classify",
            json={"text": text},
            timeout=60,
        )

        if response.status_code == 200:
            data = response.json()

            label = int(data["label"])
            probability = float(data["probability"])

            st.divider()
            st.markdown("### Clause submitted")
            st.code(text, language=None)

            col1, col2 = st.columns(2)

            with col1:
                if label == 1:
                    st.error("⚠️ Prediction: Potentially unfair")
                else:
                    st.success("✅ Prediction: Not unfair")

            with col2:
                st.metric("Estimated chance of being unfair", f"{probability:.2%}")

            st.markdown("### Explanation")
            if label == 1:
                st.write(
                    "This result suggests that the clause may give the company too much power or limit user rights."
                )
            else:
                st.write(
                    "This clause does not appear to contain strong signs of being unfair."
                )

        else:
            st.error(f"Classification request failed: {response.text}")