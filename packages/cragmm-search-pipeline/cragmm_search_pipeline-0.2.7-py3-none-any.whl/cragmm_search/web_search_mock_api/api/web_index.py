from .web_search import extract_features, index_web_data, web_search


class CragMockWeb(object):
    def __init__(
        self, emb_model, tokenizer, text_index_path,
    ):
        self.vector_db = index_web_data(hf_path=text_index_path)
        self.emb_model = emb_model
        self.tokenizer = tokenizer
        self.index_to_metadata = dict(zip(self.vector_db.get()['ids'], self.vector_db.get(include=["metadatas"])['metadatas']))

    def search(self, query, k=5):
        # Make sure the query is processed on the same device as the model
        device = self.emb_model.device
        query_emb = extract_features(self.emb_model, self.tokenizer, query, device)
        top_k = web_search(query_emb, self.vector_db, top_n=k)
        return top_k

    def get_page_name(self, idx):
        # Return the page name for a given index
        return self.index_to_metadata[str(idx)]["page_name"]

    def get_page_snippet(self, idx):
        # Return the page name for a given index
        return self.index_to_metadata[str(idx)]["page_snippet"]

    def get_page_url(self, idx):
        # Return the page URL for a given index
        return self.index_to_metadata[str(idx)]["page_url"]
