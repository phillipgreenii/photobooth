import os
import os.path

class PhotoSession:
    def __init__(self,rootStorageDirectory, name):
        self._storage_directory = os.path.join(rootStorageDirectory, name)
        os.mkdir(self._storage_directory)
        self._name = name
        self._photo_counter = 0

    def addPhoto(self,photo):
        print photo + " was taken"
        new_name = ('%04d' % self._photo_counter) + '_' + os.path.basename(photo)
        self._photo_counter += 1
        new_location = os.path.join(self._storage_directory, new_name)
        os.rename(photo, new_location)
