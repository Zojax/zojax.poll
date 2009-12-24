from zope import event, component
from zope.app.component.site import SiteManagementFolder
from zope.lifecycleevent import ObjectCreatedEvent

def createUtility(site, id, factory, ifaces, container='system'):

    sm = site.getSiteManager()

    if container:
        if not sm.has_key(container):
            folder = SiteManagementFolder()
            event.notify(ObjectCreatedEvent(folder))
            sm[container] = folder

        container = sm[container]
    else:
        container = sm

    if id not in container:
        if callable(factory):
            utility = factory()
        else:
            utility = component.createObject(factory)

        container[id] = utility
        event.notify(ObjectCreatedEvent(utility))

        for iface, name in ifaces:
            sm.registerUtility(utility, iface, name)

    return container[id]
