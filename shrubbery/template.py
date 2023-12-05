"""
Shrubbery is a Smart Html Renderer (Using Blocks to Bind Expressions
RepeatedlY).

This is a simple templating engine designed to convert JSON_ data
into HTML or XML. The idea behind it is that templates are very
simple, containing only HTML tags, with nodes being repeated as
required by the number of elements in the data.

_JSON: http://json.org/

"""
import re
import cgi
import sgmllib

# Monkeypatch sgmllib to avoid breaking ampersands.
sgmllib.entityref = re.compile("[^\W\w]")

from BeautifulSoup import BeautifulSoup, NavigableString


# Basic regexp for matching all expressions in a template.
TOKEN = r"([\w_:-]+)(\[\d+\])*"
EXPR = re.compile(r"\{(%s(\.%s)*)\}" % (TOKEN, TOKEN))


class Template(BeautifulSoup):
    """A Shrubbery template.

    Shrubbery is a smart template that holds *no logic* whatsoever,
    with behavior being dictated by the data.

    """

    def process(self, data, remove_empty_nodes=True, escape=True):
        """Process the template given some data.

        Here, ``data`` should be a dict-like object with the variables
        to be replaced. If ``escape`` is true, any HTML in the data
        will be escaped before the replacement.

        The option ``remove_empty_nodes`` will remove nodes with
        replacements not present in ``data``.
        """
        # Get all namespaces available in the template.
        nstree = _get_namespaces(self)

        # Replace tree with elements from ``data``.
        tree = search(self.copy(), data, '', nstree,
                remove_empty_nodes, escape)

        # Fix tags in replacements.
        tree = apply(tree, "%SHRUBBERY_OPEN_TAG%", "{")
        tree = apply(tree, "%SHRUBBERY_CLOSE_TAG%", "}")

        return tree
    render = process

    def copy(self):
        """A lazy and *costy* copy of the template."""
        return Template(unicode(self))


def search(tree, data, ns, nstree, remove_empty_nodes, escape):
    """
    Search for all expressions inside a given namespace.

    This function finds all expressions inside a given namespace
    (say, ``entry`` or ``collection.id``). After that it locates
    the uppermost node common to all nodes, and replicates it
    according to the number of elements in the applied data. Each
    node is then processed to replace the expressions with the
    proper values.

    """
    # Search for all expressions inside a given namespace.
    regexp = re.compile(r"\{%s.*\}" % re.escape(ns.rstrip('.')))
    nodes = tree.findAll(replaceable(regexp)) + tree.findAll(text=regexp)
    if not nodes: return tree

    # Get the node in common, its parent and position.
    node = find_common_node(nodes)
    parent = node.parent
    index = parent.contents.index(node)

    # Now for every instance of ``data`` we will clone the
    # parent node, replacing the appropriate data values.
    # First a little cleanup...
    if not isinstance(data, list): data = [data]
    data = [v for v in data if v not in [None, {}, []]]
    for i, values in enumerate(data):
        # Return a node with the values applied.
        repl = apply(clone(node),
                "\{%s\}" % re.escape(ns.rstrip('.')),
                values, escape)
        parent.insert(index+i, repl)

        # Continue replacement in deeper namespaces.
        keys = nstree.keys()
        keys.sort()
        keys.reverse()  # make indexed ns be replaced first.
        for k in keys:
            new_ns = '%s%s.' % (ns, k)
            new_nstree = nstree.get(k)

            # Get any indexes.
            indexes = re.match(TOKEN, k)
            k, slice_ = indexes.groups()

            # Get subdata for this node.
            try:
                subdata = values.get(k)
            except:
                subdata = getattr(values, k, None)
            if slice_ and subdata:
                subdata = subdata[int(slice_[1:-1])]

            repl = search(repl, subdata, new_ns,
                    new_nstree, remove_empty_nodes, escape)

    # Remove this node from parent.
    if data or remove_empty_nodes: node.extract()
    return tree


def apply(tree, match, data, escape=False):
    """
    Apply replacement in expressions.

    This function replaces the expressions with the values in ``data``.

    """
    # Find all replaceable nodes from this namespace.
    regexp = re.compile(match)
    nodes = tree.findAll(replaceable(regexp)) + tree.findAll(text=regexp)

    # Normalize data. Data can be a dict or object when it's used
    # as a stub for defining the topmost element to repeat.
    if isinstance(data, (int, long, float)):
        data = unicode(data)
    elif isinstance(data, str):
        data = data.decode('utf-8')
    elif not isinstance(data, unicode):
        data = u''

    # Escape shrubbery tags inside replacement.
    data = EXPR.sub(lambda m:
            "%%SHRUBBERY_OPEN_TAG%%%s%%SHRUBBERY_CLOSE_TAG%%"
            % m.group(1), data)

    # Do the replacement.
    if escape: text = cgi.escape(data)
    else: text = data
    for node in nodes:
        if isinstance(node, NavigableString):
            repl = regexp.sub(text, node.string)
            if node.parent: node.replaceWith(repl)
        else:
            if node.string:
                node.string = regexp.sub(text, node.string)
            for k, v in node.attrs:
                node[k] = regexp.sub(data, v).strip()
                if not node[k]: del node[k]
    return tree


def find_common_node(nodes):
    """
    Return the lowest node in common given a list of nodes.

    Given the nodes in ``nodes``, this function returns the
    lowest parent in common to all nodes.

    """
    # Senseless for a single node.
    if len(nodes) == 1: return nodes[0]

    # Get a list of all parents.
    parents = [[node] + node.findParents() for node in nodes]
    # Here we use the smallest list, iterating over each element
    # and checking if the candidate appears in all list of
    # parents.
    parents.sort(key=len)
    for candidate in parents.pop(0):
        for other_parents in parents:
            if candidate not in other_parents: break
        else:
            return candidate


def _get_namespaces(soup):
    """
    Get all namespaces from the template.

    This function searches ``soup`` for all namespaces, and returns
    them as a nested dict. A template like this::

        <html>
            <div id="{entry.id}"></div>
        </html>

    Would return ``{u'entry': {u'id': {}}}``, eg.

    """
    namespaces = {}
    nodes = soup.findAll(replaceable(EXPR)) + soup.findAll(text=EXPR)
    for node in nodes:
        for ns in EXPR.findall(node.string or ''):
            ns = ns[0].split('.')
            root = namespaces
            for item in ns:
                root = root.setdefault(item, {})
        if hasattr(node, 'attrs'):
            for k, v in node.attrs:
                for ns in EXPR.findall(v):
                    ns = ns[0].split('.')
                    root = namespaces
                    for item in ns:
                        root = root.setdefault(item, {})
    return namespaces


def clone(node):
    """
    Clone a node.

    We simply parse the HTML from ``node`` to be copied. Yes, I'm lazy.

    """
    return Template(unicode(node))


def replaceable(regexp=EXPR):
    """
    Return function to find nodes that are replaceable in a given namespace.

    Given a namespace defined by ``regexp``, this function returns
    a callable that can be used in ``findAll`` to search for
    corresponding nodes.

    """

    def func(tag):
        """Check both text and attributes for ``regexp``."""
        if tag.string and regexp.search(tag.string): return True
        for (k, v) in tag.attrs:
            if regexp.search(v): return True
        return False
    return func
