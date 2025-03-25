def get_unique_union(document_lists):
    # Flatten list of lists, and dedupe them
    deduped_docs = {
        doc.page_content: doc for sublist in document_lists for doc in sublist}
    # return a flat list of unique docs
    return list(deduped_docs.values())


def reciprocal_rank_fusion(results: list[list], k=60):
    """reciprocal rank fusion on multiple lists of ranked documents and an optional parameter k used in the RRF formula"""
    # Initialize a dictionary to hold fused scores for each document
    # Documents will be keyed by their contents to ensure uniqueness
    fused_scores = {}
    documents = {}
    for docs in results:
        # Iterate through each document in the list, with its rank (position in the list)
        for rank, doc in enumerate(docs):
            doc_str = doc.page_content
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
                documents[doc_str] = doc
            fused_scores[doc_str] += 1 / (rank + k)
    # sort the documents based on their fused scores in descending order to get the final reranked results
    reranked_doc_strs = sorted(
        fused_scores, key=lambda d: fused_scores[d], reverse=True)
    return [documents[doc_str] for doc_str in reranked_doc_strs]
