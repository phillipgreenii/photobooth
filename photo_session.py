import os
import os.path
import logging

class PhotoSession:
    def __init__(self,rootStorageDirectory, name, photosToTake):
        self.logger = logging.getLogger('photo.session')
        self._storage_directory = os.path.join(rootStorageDirectory, name)
        self.logger.debug('creating session storage at %s' % self._storage_directory)
        os.mkdir(self._storage_directory)
        self._name = name
        self._photos = []
        self._photos_to_take = photosToTake
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(repr(self))    

    def get_name(self):
        return self._name

    def get_storage_directory(self):
        return self._storage_directory;

    def total_photos_to_take(self):
        return self._photos_to_take

    def addPhoto(self,photo):
        #TODO add check so no more than _photos_to_take are added
        self.logger.debug('adding photo %s' % photo)
        new_name = ('%04d' % len(self._photos)) + '_' + os.path.basename(photo)
        new_location = os.path.join(self._storage_directory, new_name)
        os.rename(photo, new_location)
        self._photos.append(new_location)

    def get_photos(self):
        return tuple(self._photos)

    def is_complete(self):
        return len(self._photos) == self._photos_to_take

    def __repr__(self):
        return "%s(name=%s,photos=%s,storage_directory=%s,photos_to_take=%d)" % \
               (self.__class__,self._name, str(self._photos), self._storage_directory, self._photos_to_take)

    def __str__(self):
        return self._name
