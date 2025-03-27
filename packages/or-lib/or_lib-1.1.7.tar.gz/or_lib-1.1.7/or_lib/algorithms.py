import networkx as nx

class GraphAlgorithms:
    def __init__(self, directed=True):
        self.directed = directed
        self.graph = nx.DiGraph() if directed else nx.Graph()

    def get_edge_tuple(self, edge):
        """Extracts (src, tgt) tuple from edge, supporting different formats."""
        if "src_tgt" in edge:
            return edge["src_tgt"]
        elif "src_id" in edge and "tgt_id" in edge:
            return (edge["src_id"], edge["tgt_id"])
        else:
            raise KeyError("Edge data format not recognized!")

    def compute_degree_centrality(self, node_datas, edge_datas, k, weighted=False):
        self.graph.clear()
        for edge in edge_datas:
            src, tgt = self.get_edge_tuple(edge)
            weight = edge.get("weight", 1.0) if weighted else 1.0
            self.graph.add_edge(src, tgt, weight=weight)

        if weighted:
            degree_centrality = {node: sum(d["weight"] for _, d in self.graph[node].items()) for node in self.graph}
        else:
            degree_centrality = nx.degree_centrality(self.graph)

        for node in node_datas:
            entity_name = node.get("source_id") or node.get("entity_name")
            node["degree_centrality"] = degree_centrality.get(entity_name, 0.0)
        return node_datas[:k]

    def compute_pagerank(self, node_datas, edge_datas, k):
        self.graph.clear()
        for edge in edge_datas:
            src, tgt = self.get_edge_tuple(edge)
            weight = edge.get("weight", 1.0)
            self.graph.add_edge(src, tgt, weight=weight)

        pagerank_scores = nx.pagerank(self.graph, weight="weight")

        for node in node_datas:
            entity_name = node.get("source_id") or node.get("entity_name")
            node["rank"] = pagerank_scores.get(entity_name, 0.0)
        return node_datas[:k]

    def compute_article_rank(self, node_datas, edge_data, k, damping_factor=0.85, max_iter=100, tol=1e-6):
        self.graph.clear()
        
        for node in node_datas:
            entity_name = node.get("source_id") or node.get("entity_name")
            self.graph.add_node(entity_name)

        for edge in edge_data:
            src, tgt = self.get_edge_tuple(edge)
            weight = edge.get("weight", 1.0)
            self.graph.add_edge(src, tgt, weight=weight)

        pagerank_scores = nx.pagerank(self.graph, alpha=damping_factor, max_iter=max_iter, tol=tol, weight='weight')

        for node in node_datas:
            entity_name = node.get("source_id") or node.get("entity_name")
            node["rank"] = pagerank_scores.get(entity_name, 0.0)
        return node_datas[:k]

    def compute_betweenness_centrality(self, node_datas, edge_datas, k):
        self.graph.clear()
        
        for node in node_datas:
            entity_name = node.get("source_id") or node.get("entity_name")
            self.graph.add_node(entity_name)

        for edge in edge_datas:
            src, tgt = self.get_edge_tuple(edge)
            self.graph.add_edge(src, tgt, weight=edge.get("weight", 1.0))

        betweenness_scores = nx.betweenness_centrality(self.graph, weight="weight", normalized=True)

        for node in node_datas:
            entity_name = node.get("source_id") or node.get("entity_name")
            node["rank"] = betweenness_scores.get(entity_name, 0.0)
        return node_datas[:k]

    def celf_influence_maximization(self, node_datas, edge_datas, k):
        self.graph.clear()
        
        for node in node_datas:
            entity_name = node.get("source_id") or node.get("entity_name")
            self.graph.add_node(entity_name)

        for edge in edge_datas:
            src, tgt = self.get_edge_tuple(edge)
            self.graph.add_edge(src, tgt, weight=edge.get("weight", 1.0))

        influence_scores = nx.betweenness_centrality(self.graph, weight="weight")
        ranked_node_datas = sorted(influence_scores.items(), key=lambda x: x[1], reverse=True)
        top_k_half_node_datas = ranked_node_datas[: max(5, k )]

        for node in node_datas:
            entity_name = node.get("source_id") or node.get("entity_name")
            node["rank"] = influence_scores.get(entity_name, 0.0)
        
        return [node for node in node_datas if node.get("source_id") or node.get("entity_name") in dict(top_k_half_node_datas)]
