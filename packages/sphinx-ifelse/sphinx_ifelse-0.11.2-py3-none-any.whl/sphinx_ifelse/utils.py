
from typing import Tuple, List
from sphinx.util.docutils import SphinxDirective

from sphinx.util.tags import Tags

def directive2location(self: SphinxDirective) -> Tuple[str, int]:
    return (self.state.document.settings.env.docname, self.lineno)

def remove_all_childs_of_types(node, nodetypes : List[str]):
    # We have to run the list of children reversed,
    # as we change the parent during processing.
    for child in reversed(node.children):
        if len(child.children) > 0:
            remove_all_childs_of_types(child, nodetypes)
        for nodetype in nodetypes:
            if isinstance(child, nodetype):
                node.remove(child)
                break
    return
