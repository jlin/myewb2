"""myEWB workspace models

This file is part of myEWB
Copyright 2010 Engineers Without Borders Canada
"""

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

import settings, os

class WorkspaceManager(models.Manager):
    def get_for_object(self, object):
        """
        Returns the workspace for a particular object (usually a group),
        creating one if needed.
        """
        w, c = self.get_query_set().get_or_create(content_type = ContentType.objects.get_for_model(object),
                                                  object_id = object.id)
        
        return w

        #if not helpers.is_visible(request.user, obj):
        #    return render_to_response('denied.html', context_instance=RequestContext(request))
            

class Workspace(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    objects = WorkspaceManager()

    # Get the filesystem directory for the workspace root, creating if needed
    def get_root(self):
        dir = os.path.join(settings.MEDIA_ROOT, 'workspace/files', str(self.id))
        if not os.path.isdir(dir):
            os.makedirs(dir, 0755)
        return dir
    
    # Get the filesystem directory for the workspace's preview cache,
    # creating if needed
    def get_cache_root(self):
        dir = os.path.join(settings.MEDIA_ROOT, 'workspace/cache', str(self.id))
        if not os.path.isdir(dir):
            os.makedirs(dir, 0755)
        return dir
    
    # Gets the filesystem directory for the given relative directory,
    # creating the filesystem root if needed.  If the requested directory 
    # contains invalid characters, False is returned.
    #
    # The optional keyword root allows a different filesystem root
    # (ie so we can use this for both files and caches)
    #
    #,The optional create flag controls whether the requested directory is created
    # if it does not exist, or if that results in an error (return False), 
    def get_dir(self, dir, root=None, create=False):
        if dir.find('.') > -1:       # do not allow any periods
            return False
        
        if dir[0:1] != '/':
            dir = '/' + dir
        if dir[0:-1] != '/':
            dir = dir + '/'
        
        if root:
            dir = root + dir
        else:
            dir = self.get_root() + dir
            
        if os.path.isdir(dir):
            return dir
        elif create:
            os.makedirs(dir, 0755)
        else:
            return False
        
    # Gets the full filesystem path to a given file.
    # Returns False if the file does not exist or is invalid.  
    def get_file(self, filepath):
        if not filepath:
            return False
        
        # split into path and file
        dir, file = os.path.split(filepath)
        
        #  check validity of path
        fullpath = self.get_dir(dir)
        if fullpath:
            # check existance of file
            if os.path.isfile(fullpath + file):
                return fullpath + file
        
        return False
    
    # Get the cache directory for a given file.
    # Returns False if the file does not exist or is invalid.  
    def get_cache(self, filepath):
        if not filepath or not self.get_file(filepath):
            return False

        # get or create the cache directory
        # (no error checking, since self.get_file(filepath) should do all
        #  the checking we need)
        return self.get_dir(filepath, root=self.get_cache_root())
    
    # returns a list of the workspace's directory tree
    def get_dir_tree(self):
        folders, path = build_dir_tree('', self.get_root(), [], [], 0)
        return folders
    
    
        
# recursive function to walk and build this workspace's file tree
def build_dir_tree(fname, dir, folders, path, counter):
    # currently in a directory?
    # (the counter is for paranoia, just in case an infinite loop gets created)
    if os.path.isdir(os.path.join(dir, fname)) and counter < 100:
        # add directory to path, and full path to list of folders
        path.append(fname)
        folders.append('/'.join(path))
        
        # build list of all contents
        subfolders = []
        for f in os.listdir(os.path.join(dir, fname)):
            subfolders.append(f)
            
        # sort.  WHY oh WHY doesn't os.listdir sort for you? :S
        subfolders.sort()
        
        # and go through, adding all the subdirectories as well
        for f in subfolders:
            folders, path = build_dir_tree(f, dir + '/' + fname, folders, path, counter+1)
        
        path.pop()
            
    return (folders, path)
