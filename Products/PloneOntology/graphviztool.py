import Products.CMFCore.utils
from AccessControl.SecurityInfo import ClassSecurityInfo

try:
    from AccessControl.class_init import InitializeClass
except ImportError:
    from Globals import InitializeClass

import os

import OFS.PropertyManager
import OFS.SimpleItem
import Products.CMFCore.ActionProviderBase

from warnings import warn
from config import *

from subprocess import Popen, PIPE, STDOUT


class GraphVizTool(Products.CMFCore.utils.UniqueObject,
                   OFS.PropertyManager.PropertyManager,
                   OFS.SimpleItem.SimpleItem,
                   Products.CMFCore.ActionProviderBase.ActionProviderBase):
    """A tool to provide graph rendering.

    Based on the GraphViz layout programs (http://www.graphviz.org)
    """

    id = 'graphviz_tool'
    meta_type= 'GraphViz Tool'

    plone_tool = 1

    security = ClassSecurityInfo()
    security.declareObjectPublic()

    _toollist = ('dot','twopi','neato','fdp','circo')

    def __init__(self):
        self._layouter = 'fdp'

    def toollist(self):
        """returns a list of the graphviz rendering tools.
        """
        return self._toollist

    def getLayouter(self):
        """Return the currently used GraphViz layouter.
        """
        return self._layouter

    def getTool(self):
        """Deprecated, use getLayouter.
        """
        warn("getTool() is deprecated. Please use getLayouter() instead.",
             DeprecationWarning)
        return self.getLayouter()

    def setLayouter(self, layouter='fdp'):
        """Set the currently used GraphViz layouter.
        """

        if not layouter in self._toollist:
            raise KeyError, "Layouter not known: %s. Please choose one of %s" % (layouter, self._toollist)
        else:
            self._layouter = layouter

    def setTool(self, tool='fdp'):
        """Deprecated, use setLayouter instead.
        """
        warn("setTool() is deprecated. Please use setLayouter() instead.",
             DeprecationWarning)
        self.setLayouter(tool)

    def isLayouterPresent(self, layouter=""):
        """Check if current or specified layouter is present on the system.
        """

        if not layouter:
            layouter = self.getLayouter()

        layouter = os.path.join(GV_BIN_PATH, layouter)
        if not (os.path.exists(layouter) and os.access(layouter, os.X_OK)):
            return False

        p = Popen("%s -V" % layouter, shell=True, stdin=PIPE, stdout=PIPE,
                  stderr=STDOUT, close_fds=True)
        (pout, pin) = p.stdout, p.stdin
        pin.close()
        output = pout.read()
        pout.close()

        return "version" in output

    def renderGraph(self, graph, tool='', options=[]):
        """Renders the given graph.

        Returns file like object with result which type is dependable on options and an error string, empty if none.
        """
        if not tool:
            tool = self.getLayouter()

        tool = os.path.join(GV_BIN_PATH, tool)

        options = " ".join(options)

        # 2006-08-03 Seperate streams for output and error. Avoids problems with fonts not found.
        p = Popen("%s %s" % (tool, options), shell=True,
                  stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        (pout, pin, perr) = p.stdout, p.stdin, p.stderr
        pin.write(graph)
        pin.close()

        data  = pout.read()
        pout.close()
        error = perr.read()
        perr.close()

        return (data, error)

InitializeClass(GraphVizTool)
