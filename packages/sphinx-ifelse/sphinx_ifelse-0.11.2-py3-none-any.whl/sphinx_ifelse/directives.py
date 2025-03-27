import copy

from docutils import nodes

from sphinx.util.docutils import SphinxDirective

from sphinx.util import logging

from sphinx_ifelse.utils import directive2location, remove_all_childs_of_types


logger = logging.getLogger(__name__)


class IfElseNode(nodes.General, nodes.Element):

    def __init__(self,
                 condition: str | None,
                 evaluatedto: bool,
                 previously_evaluatedtoTrue: bool,
                 location):
        self.condition = condition
        self.evaluatedto = evaluatedto
        self.previously_evaluatedtoTrue = previously_evaluatedtoTrue
        self.location = location
        super().__init__()

    def already_evaluatedtoTrue(self):
        return self.evaluatedto or self.previously_evaluatedtoTrue


class IfNode(IfElseNode):
    def __init__(self,
                 condition: str = '',
                 evaluatedto: bool = False,
                 location = None):
        super().__init__(condition = condition,
                         evaluatedto = evaluatedto,
                         previously_evaluatedtoTrue = False,
                         location = location)


class ElIfNode(IfElseNode):
    def __init__(self,
                 condition: str = '',
                 evaluatedto: bool = False,
                 previously_evaluatedtoTrue:bool = False,
                 location = None):
        super().__init__(condition = condition,
                         evaluatedto = evaluatedto,
                         previously_evaluatedtoTrue = previously_evaluatedtoTrue,
                         location = location)


class ElseNode(IfElseNode):
    def __init__(self,
                 previously_evaluatedtoTrue: bool = False,
                 location = None):
        super().__init__(condition = None,
                         evaluatedto = not previously_evaluatedtoTrue,
                         previously_evaluatedtoTrue = previously_evaluatedtoTrue,
                         location = location)


def process_ifelse_nodes(app, doctree, fromdocname):
    nodetypes = [IfNode, ElIfNode, ElseNode]
    remove_all_childs_of_types(doctree, nodetypes)
    return


class AbstractIfElseDirective(SphinxDirective):
    """
    Abstract class for common if/else logic.
    """

    def evaluate_condition(self, condition:str)->bool:
        """
        Determines if a previous sibling directive (if or elif)
        has already evaluated to True.

        Returns:
            bool: True if a previous sibling directive evaluated to True,
                  otherwise False.
        """

        env = self.state.document.settings.env
        app = env.app

        class_name = self.__class__.__name__

        variants = app.config.ifelse_variants

        # eval will change the globals variable, we have to avoid this,
        # so we create a deep copy
        variants_deep_copy = copy.deepcopy(variants)

        try:
            proceed = eval(condition, variants_deep_copy)
        except Exception as err:
            logger.warning(
                f"{class_name}: exception while evaluating expression: {err}",
                type="ifelse",
                subtype=class_name,
                location=directive2location(self)
            )
            proceed = True

        return proceed

    def fetch_already_evaluatedtoTrue(self)->bool:
        """
        Fetches the result of a already evaluated condition.

        Returns:
            bool: `True` if the condition was already evaluated to `True`,
                  otherwise `False`.
        """

        class_name = self.__class__.__name__

        parent = self.state.parent
        previously_evaluatedtoTrue:bool = False

        last_sibling = None

        # find last none 'nodes.comment'
        for last_sibling in reversed(parent):
            if not isinstance(last_sibling, nodes.comment):
                break

        if isinstance(last_sibling, IfNode) or isinstance(last_sibling, ElIfNode):
            previously_evaluatedtoTrue = last_sibling.already_evaluatedtoTrue()
        else:
            logger.warning(
                f"{class_name}: without a preceding IfDirective or ElIfDirective. "+ \
                f"Maybe there is something wrong with the intendition.",
                type="ifelse",
                subtype=class_name,
                location=directive2location(self)
            )
            previously_evaluatedtoTrue = False

        return previously_evaluatedtoTrue


class IfDirective(AbstractIfElseDirective):
    """Directive to switch between alternative content in the documentation.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True

    def run(self):
        condition = self.arguments[0]
        condition_evaluated_to = self.evaluate_condition(condition=condition)

        selfnode = IfNode(
            condition=condition,
            evaluatedto=condition_evaluated_to,
            location=directive2location(self)
        )

        if condition_evaluated_to:
            parsed = self.parse_content_to_nodes(allow_section_headings=True)
            parsed.append(selfnode)
            return parsed
        else:
            return [selfnode]


class ElIfDirective(AbstractIfElseDirective):
    """Directive to switch between alternative content in the documentation.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True

    def run(self):
        parent = self.state.parent
        env = self.state.document.settings.env
        app = env.app

        condition = self.arguments[0]
        condition_evaluated_to = self.evaluate_condition(condition=condition)

        previously_evaluatedtoTrue = self.fetch_already_evaluatedtoTrue()

        selfnode = ElIfNode(
            condition=condition,
            evaluatedto=condition_evaluated_to,
            previously_evaluatedtoTrue = previously_evaluatedtoTrue,
            location=directive2location(self)
        )

        process_content = condition_evaluated_to and not previously_evaluatedtoTrue

        if process_content:
            parsed = self.parse_content_to_nodes(allow_section_headings=True)
            parsed.append(selfnode)
            return parsed
        else:
            return [selfnode]



class ElseDirective(AbstractIfElseDirective):
    """Directive to switch between alternative content in the documentation.
    """

    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = True

    def run(self):
        previously_evaluatedtoTrue = self.fetch_already_evaluatedtoTrue()

        selfnode = ElseNode(
            previously_evaluatedtoTrue = previously_evaluatedtoTrue,
            location=directive2location(self)
        )

        if not previously_evaluatedtoTrue:
            parsed = self.parse_content_to_nodes(allow_section_headings=True)
            parsed.append(selfnode)
            return parsed
        else:
            return [selfnode]
