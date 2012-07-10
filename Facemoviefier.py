"""
.. module:: FaceMovifier
   :platform: Unix, Windows
   :synopsis: Higher class of the application. Used to handle the command line interface. Direclty interfaces user commands with FaceMovie actions.

.. moduleauthor:: Julien Lengrand-Lambert <jlengrand@gmail.com>

"""

# This file should never be imported anywhere
import os
import sys
import argparse

from facemovie import FacemovieThread
from facemovie import FaceParams
from facemovie import training_types

class Facemoviefier():
    """
    Class defining the interactions with the end user.
    Should be used as point of entry for all end users.
    """
    def __init__(self):    
        """
        Inits the Command Line Parser on Startup
        """
        self.args = self.initCLParser()
        
    def init_facemovie(self):
        """
        Inits the Facemovie parameters, so that it can be run efficiently

        ..note ::
            FIXME : par folder should be known (contained somewhere in the installation)
        """        
        if self.args['crop']:
            mode = "crop"
        else:
            mode = "conservative"

        par_fo = os.path.join(self.args['root'], "haarcascades")
        self.face_params = FaceParams.FaceParams(par_fo, # folder containing haar training
                                                self.args['input'], # folder containing images 
                                                self.args['output'], #folder containing video in the end 
                                                self.args['param'],
                                                self.args['sort'],
                                                mode, 
                                                self.args['speed']) # chosen type of face profile
        self.facemovie = FacemovieThread.FacemovieThread(self.face_params)

    def initCLParser(self):
        """
        Inits and Configures the command line parser designed to help the user configure the application 
        Defines all possible options, and also creats the Helper. 
        """
        parser = argparse.ArgumentParser(description="Creates a movie from a bunch of photos containing a Face.")
        
        # TODO: Integrate face params file choice, with list of possibilities. (ncurses)
        # First to check if user asks for information 
        params = training_types.simple_set.keys()
        params.append('?')
        parser.add_argument('-p', 
                            '--param', 
                            choices=params,
                            help='Choose the desired file for training the recognition phaze. Should be chosen depending on the face presentation (profile, whole body, ...)', 
                            default='frontal_face')     
    
        # --- Arguments to be processed (for now) ---
        #input folder
        parser.add_argument('-i', '--input',  help='Input folder of the images', required=True)
        # output folder
        parser.add_argument('-o', '--output', help='Output folder to save the results', required=True)
        
        # root folder
        parser.add_argument('-r', '--root', help='Root folder where the application is placed', default=".")

        # expand images or crop ? Default should be crop
        parser.add_argument('-c', 
                            '--crop', 
                            help='If this option is activated, images will be cropped and black borders will not be added' , 
                            action='store_true', 
                            default=False)

        # # Crop to custom dims if desired
        # parser.add_argument('-d', 
        #                     '--cropdims', 
        #                     help='Ignored if crop is not activated. Crops image to size x y' ,
        #                     nargs = 2)
        
        # type of output wanted (image, video, show)
        # parser.add_argument('-t', 
        #                     '--type', 
        #                     choices='vis',
        #                     help='Selects the kind of output desired. Valid choices are v (video), i (images), s (show). Default is video', 
        #                     default='v')        
        
        # how to sort images. Default is file name
        parser.add_argument('-s', 
                            '--sort', 
                            choices=['name','exif'],
                            help='Choose which way images are sorted. Can be either using file name or exif metadata (e). Default is n' , 
                            default='name')       

        # Number of frames per second in saved image
        parser.add_argument('--speed', 
                            choices=range(1, 4),
                            type=int,
                            help='Choose the pace of face switching in the final video. Possible options are (slow=1, normal=2, fast = 3). Default is normal',
                            default=2)       
        
        args = vars(parser.parse_args())
        return args
        
    def run(self):
        """
        Runs all the steps needed to get the desired output
        Checks which parameters have been run, and runs the algorithm accordingly.
        """
        # selects xml used to train the classifier 
        if self.args['param'] == '?':
            print "Available param files are :"
            print "==="
            for item in training_types.simple_set:
                print item
            print "==="                
            print 'Please choose your param file (or let default value) and restart the application'
            sys.exit(0)      
        else:
            # creates Facemovie object, loads param file
            print "Selected profile is : %s" %(self.args['param'])
            self.init_facemovie()
        

        if self.args['crop']:
            print "==="
            print "Crop mode activated"


        print "Starting Application !"
        self.facemovie.start()

        self.facemovie.join() # waiting for Thread to terminate

if __name__ == '__main__':
    my_job = Facemoviefier()
    my_job.run()
    print "FaceMovie exited successfully!"
