# Documentation labels and the paragraph functions

The original README human codebook has eight section roles, while our twelve functions describe work performed by passages. These are different layers. The downloaded CSV has **4,922 rows, including 696 excluded `-` rows**, leaving **4,226 coded section rows**. Original numeric codes 1–8 retain What, Why, How, When, Who, References, Contribution and Other. A classifier's merged What/Why label is a separate artifact.

The [machine-readable comparison](technical-crosswalk.json) covers all eight original README roles plus selected DITA task elements, WLP action/argument structures and OpenPI state fields. Its candidate mappings are contextual hypotheses. Neither headings nor type membership demonstrate successful writing.

- **Reuse section questions:** What does this do? Why use it? How does the reader act? What is its status? Who is responsible? Where are further resources? How can someone contribute?
- **Reuse optional task fields:** prerequisites, context, command, explanation, worked example and expected outcome. Keep complete steps as composite structures rather than force one function onto each.
- **Reuse action and state links:** validate referenced participants, offsets, ordering and supplied outcomes. Reader competence, actual executability and successful explanation still require review.

For a README, manual or tutorial, the harness can show the author section purpose first, then offer function cards for a particular passage. It should preserve the author's answers and wording. Common section labels should provide navigable choices, not mandatory sections or quotas.

DITA is a standard schema, not a measured corpus of successful procedures. WLP marks action/entity spans, and OpenPI supplies step-related state changes. Their source units must not become paragraph functions merely because we can parse them. Business reports, personal reflections and audience-specific vocabulary remain separate research needs.
