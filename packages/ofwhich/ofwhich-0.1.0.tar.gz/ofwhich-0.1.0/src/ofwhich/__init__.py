class Node:
    def __init__(self, parent: 'Node | None', name: str, qty: float):
        self.parent = parent
        self.name = name
        self.qty = qty
        self.level = self._compute_level()

    def _compute_level(self):
        if self.parent is not None:
            return self.parent.level + 1
        return 0

    def __repr__(self):
        parent_name = self.parent.name if self.parent is not None else 'root'
        return f'Node(name={self.name}, parent={parent_name}, qty={self.qty})'


class OfWhich:
    def __init__(self, df: 'DataFrame', *args):
        self.level_names = [arg for arg in args if arg in df.columns]
        if len(self.level_names) == 0:
            return df
        self.df = df[self.level_names]

        self.nodes = [Node(None, 'Total', len(df))]
        self._discover_children(self.nodes[0], self.df, 1)
        self.render()

    def _discover_children(self, parent_node, parent_df, level):
        if level > len(self.level_names):
            return None  # We reached the lowest level
        level_name = self.level_names[level - 1]

        nodes_on_this_level = (
            parent_df[level_name].value_counts().reset_index()
            .apply(lambda row: Node(parent=parent_node, name=row[level_name], qty=row['count']), axis=1).to_list()
        )
        for node in nodes_on_this_level:
            self.nodes.append(node)
            self._discover_children(node, parent_df.loc[parent_df[level_name] == node.name], level + 1)

    def render(self, debug=False):
        for node in self.nodes:
            indent = 4 * node.level * ' ' if node.parent is not None else ''
            prefix = 'Of which ' if node.parent is not None else ''
            print(indent + prefix + f'{node.name} {node.qty} records' + (f'| {node}' if debug else ''))

