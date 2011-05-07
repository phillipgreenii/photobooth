import os
import os.path
import logging

class PhotoSession:
    def __init__(self,rootStorageDirectory, name):
        self.logger = logging.getLogger('photo.session')
        self._storage_directory = os.path.join(rootStorageDirectory, name)
        self.logger.debug('creating session storage at %s' % self._storage_directory)
        os.mkdir(self._storage_directory)
        self._name = name
        self._photo_counter = 0

    def addPhoto(self,photo):
        self.logger.debug('adding photo %s' % photo)
        new_name = ('%04d' % self._photo_counter) + '_' + os.path.basename(photo)
        self._photo_counter += 1
        new_location = os.path.join(self._storage_directory, new_name)
        os.rename(photo, new_location)

    def __repr__(self):
        return "%s(name=%s,photo_counter=%d,storage_directory=%s)" % (self.__class__,self._name, self._photo_counter, self._storage_directory)

    def __str__(self):
        return self._name
