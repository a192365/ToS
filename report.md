# Technical Report

## Objectives 

Develop a system to analyze Terms of Service clauses using:
- semantic search  
- classification  

This report presents the main steps (EDA, modeling, evaluation) and key decisions.

## Dataset Overview

### Dataset Structure

Each row represents a clause from a company’s Terms of Service and includes:

- **company**: source of the clause  
- **sentence_id**: position in the original document  
- **sentence**: clause text  
- **label**: whether the clause is potentially unfair (`1`) or not (`-1`)  

The dataset was built by aligning sentence files with their corresponding labels, resulting in a structured dataset suitable for both retrieval and classification tasks.

For this project, only the `Sentences` and `Labels` folders were used, as they provide the necessary information for modeling. In future iterations, additional files could be explored to incorporate more contextual or metadata information.

---

## EDA Highlights

- The dataset contains **9,414 clauses from 50 companies**, providing a diverse set of real Terms of Service data.

- The label distribution is **highly imbalanced**, with **8,382 fair clauses and 1,032 unfair clauses (~11%)**.  
  This reflects real-world scenarios but introduces a modeling challenge, as the model tends to favor the majority class.

- Clause length shows **high variability**, with an average of **32 words** and a maximum of **441 words**.  
  This motivated the use of **sentence embeddings**, which better capture semantic meaning across different text lengths.

- There is a clear **variation across companies**. For example:
  - **Twitter**: ~22.5% unfair clauses  
  - **Tinder**: ~14.9%  
  - **Microsoft**: ~5.47%  

  This indicates differences in legal style and risk patterns across companies.

- The dataset is also **unevenly distributed across companies**, with:
  - **Microsoft** contributing ~5.82% of the dataset  
  - **Airbnb** ~4.15%  

  This may introduce bias, as the model is more exposed to certain writing styles.

- Manual inspection revealed consistent **semantic patterns in unfair clauses**, such as:
  - unilateral actions (*“we may terminate your account at any time”*)  
  - lack of notice (*“without notice”*)  
  - limitation of liability (*“we are not liable for damages”*)  

  These patterns were later reflected in model predictions.

- The dataset presents **semantic variability**, meaning that the same idea can be expressed in different ways. For example:

  - *“we may terminate your account without notice”*  
  - *“your access may be suspended at any time without prior notification”*

  Although the wording is different, both clauses express the same underlying concept.  
  This motivated the use of **semantic embeddings**, which capture meaning beyond exact word matching.

- Qualitative comparison across companies (e.g., **Tinder vs Microsoft vs Twitter**) showed differences in tone:
  - **Tinder** uses stronger unilateral language  
  - **Microsoft** uses more formal and procedural wording  
  - **Twitter** includes neutral disclaimers  

  This reinforces the need for semantic representations that capture **context and tone**, not only keywords.

- Some clauses are **semantically similar but differ in user impact**, which makes classification difficult.  
  This motivated:
  - manual analysis of **borderline cases**  
  - the use of **probability outputs** to reflect model uncertainty  

- The dataset structure was leveraged to support two tasks:
  - **semantic search (FAISS)** for retrieving similar clauses  
  - **classification (Logistic Regression)** for estimating unfairness  

  These characteristics directly influenced the modeling choices in this project.

  ## Semantic Search

The semantic search component was designed to retrieve clauses that are similar in meaning to a user query. This decision was motivated by the observations in the EDA, where clauses showed high variability in wording, length, and structure, even when expressing similar ideas.

To address this, the project uses **sentence embeddings (SentenceTransformers)**, which convert each clause into a vector representation that captures semantic meaning. This allows the system to retrieve similar clauses even when the wording is different, which would not be possible with keyword-based approaches.

For efficient retrieval, the system uses **FAISS**, which enables fast nearest-neighbor search over the embedding space. This is important since each query needs to be compared against thousands of clauses.

The similarity between the query and each clause is measured using a **distance score**:
- **lower score → more similar clause**
- **higher score → less similar clause**

This score is used only to rank results and does not indicate whether a clause is fair or unfair.

Since no ground-truth relevance labels are available for search, the evaluation was performed qualitatively. Several test queries (e.g., *"terminate without notice"*, *"not liable for damages"*) returned clauses with consistent semantic meaning, even when phrased differently. This indicates that the embedding-based approach is effective in capturing semantic similarity.

However, this component has limitations:
- no formal evaluation metric was used  
- relevance is assessed manually  
- future improvements could include building a labeled dataset for retrieval evaluation  

---

## Clause Classification

The classification component estimates whether a clause may be **potentially unfair**, based on patterns learned from the dataset.

A **Logistic Regression model** was chosen as a baseline because it is simple, interpretable, and performs well when combined with embedding-based features. Each clause is first converted into a sentence embedding, which is then used as input to the classifier.

The model outputs:
- a **prediction** (potentially unfair or not)  
- a **probability**, representing how likely the clause is to be unfair  

This probability is particularly important:
- **higher values → higher risk of unfairness**
- **lower values → lower risk**

For example:
- clauses like *“we may change these terms at any time without notice”* received high probabilities (~90%), indicating strong unfair patterns  
- more neutral clauses like *“you may close your account at any time”* received lower probabilities (~20%)  

This shows that the model captures different levels of risk, rather than making only binary decisions.

The evaluation showed that:
- the model performs well on **fair clauses**  
- performance is lower on **unfair clauses**, due to class imbalance (~11% unfair)  

Additionally, manual inspection revealed that the model struggles with **borderline cases**, where clauses are semantically similar but differ in user impact. For example:
- *“you may close your account at any time”*  
- vs *“we may terminate your account at any time without notice”*  

These observations led to two key decisions:
- use **probability outputs** to reflect uncertainty  
- include **manual analysis** to better understand model limitations  

Overall, the model captures meaningful semantic patterns, but unfair clauses remain harder to detect consistently, especially in ambiguous cases.

### Future Work

- Improve classification (handle imbalance, test stronger models)  
- Add quantitative evaluation for search (e.g., precision@k), once a ground-truth dataset with query–relevance pairs is available  
- Incorporate more dataset information (context, structure)  
- Improve UI and result explanations  
- Extend to document-level analysis  