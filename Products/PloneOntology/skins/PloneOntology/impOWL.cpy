## Script (Python) "impOWL"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=file, ontology=None
##title=
##
ctool = context.portal_classification
msg = ctool.importOWL(file, ontologyId=ontology)

return state.set(portal_status_message='Ontology from %s imported.\n%s' % (file.filename, msg))