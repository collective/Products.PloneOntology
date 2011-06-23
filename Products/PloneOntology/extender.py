from zope.interface import implements
from zope.component import adapts

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField
from archetypes.referencebrowserwidget import ReferenceBrowserWidget

from Products.Archetypes.public import ReferenceField
from Products.Archetypes.interfaces import IBaseContent
from Products.CMFCore.permissions import ModifyPortalContent


class ClassificationField(ExtensionField, ReferenceField):
    """A specialized ReferenceField for use with the classification tool."""


class ClassificationExtender(object):
    """Extends existing types to add classification support."""

    adapts(IBaseContent)
    implements(ISchemaExtender)

    fields = [
        ClassificationField(
            "ontologyClassification",
            relationship = "classifiedAs_byPloneOntology",
            multiValued = True,
            isMetadata = True,
            languageIndependent = False,
            write_permission = ModifyPortalContent,
            schemata = "categorization",
            widget = ReferenceBrowserWidget(
                allow_search = True,
                allow_browse = True,
                show_indexes = False,
                restrict_browsing_to_startup_directory = True,
                startup_directory = "/ontologies",
                label = "Classification",
                description = ("The ontology keywords that relate "
                               "to this item, if applicable."),
                visible = {"edit" : "visible", "view" : "invisible" }
                )
            )
        ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
