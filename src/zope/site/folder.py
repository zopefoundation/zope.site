from zope.interface import implements, directlyProvides

from zope.site.interfaces import IFolder, IRootFolder
from zope.site.site import SiteManagerContainer
from zope.location.interfaces import ISite

from zope.container.folder import Folder

class Folder(Folder, SiteManagerContainer):

    implements(IFolder)

def rootFolder():
    f = Folder()
    directlyProvides(f, IRootFolder)
    return f

class FolderSublocations(object):
    """Get the sublocations of a folder

    The subobjects of a folder include it's contents and it's site manager if
    it is a site.

      >>> from zope.container.contained import Contained
      >>> folder = Folder()
      >>> folder['ob1'] = Contained()
      >>> folder['ob2'] = Contained()
      >>> folder['ob3'] = Contained()
      >>> subs = list(FolderSublocations(folder).sublocations())
      >>> subs.remove(folder['ob1'])
      >>> subs.remove(folder['ob2'])
      >>> subs.remove(folder['ob3'])
      >>> subs
      []

      >>> sm = Contained()
      >>> from zope.interface import directlyProvides
      >>> from zope.component.interfaces import IComponentLookup
      >>> directlyProvides(sm, IComponentLookup)
      >>> folder.setSiteManager(sm)
      >>> directlyProvides(folder, ISite)
      >>> subs = list(FolderSublocations(folder).sublocations())
      >>> subs.remove(folder['ob1'])
      >>> subs.remove(folder['ob2'])
      >>> subs.remove(folder['ob3'])
      >>> subs.remove(sm)
      >>> subs
      []
    """

    def __init__(self, folder):
        self.folder = folder

    def sublocations(self):
        folder = self.folder
        for key in folder:
            yield folder[key]

        if ISite.providedBy(folder):
            yield folder.getSiteManager()
