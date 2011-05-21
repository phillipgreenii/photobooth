import os
import os.path
import time
import logging

class PhotoSession:
    def __init__(self,rootStorageDirectory, photosToTake):
        self.logger = logging.getLogger('photo.session')
        name = '%012d' % time.time()
        self._storage_directory = os.path.join(rootStorageDirectory, name)
        self.logger.debug('creating session storage at %s' % self._storage_directory)
        os.mkdir(self._storage_directory)
        self._name = name
        self._photos = []
        self._photos_to_take = photosToTake
        self._collage = None

    def get_name(self):
        return self._name

    def get_storage_directory(self):
        return self._storage_directory;

    def total_photos_to_take(self):
        return self._photos_to_take

    def addPhoto(self,photo):
        #TODO add check so no more than _photos_to_take are added
        self.logger.debug('adding photo %s' % photo)
        (ignore,extension) = os.path.splitext(photo)
        new_name = '%04d_%012d%s' % (len(self._photos),time.time(), extension)
        self.logger.debug('new photo name %s' % new_name)
        new_location = os.path.join(self._storage_directory, new_name)
        os.rename(photo, new_location)
        self._photos.append(new_location)

    def setCollage(self,collage):
        self.logger.debug('setting collage %s' % collage)
        (ignore,extension) = os.path.splitext(collage)
        new_name = self._name +  extension
        self.logger.debug('new collage name %s' % new_name)
        new_location = os.path.join(self._storage_directory, new_name)
        os.rename(collage, new_location)
        self._collage = new_location

    def get_collage(self):
        return self._collage

    def get_photos(self):
        return tuple(self._photos)

    def is_complete(self):
        return len(self._photos) == self._photos_to_take

    def __repr__(self):
        return "%s(name=%s,photos=%s,storage_directory=%s,photos_to_take=%d,collage=%s)" % \
               (self.__class__,self._name, str(self._photos), self._storage_directory, self._photos_to_take, self._collage)

    def __str__(self):
        return "%s(name=%s)" % (self.__class__,self._name)
