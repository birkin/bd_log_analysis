# -*- coding: utf-8 -*-

""" Compares new borrowdirect api results against current in-production deprecated code.
    Parses logging added to controller that summarizes differences between new and old tunneler calls. """

import glob, os, pprint


class Analyzer( object ):

    def __init__( self ):
        self.LOGS_DIR = unicode( os.environ[u'BDLOG_ANALYSIS__LOGS_DIR'] )
        self.filepaths_list = []
        self.summary = {}

    def prep_filepaths_list( self ):
        """ Creates array filepaths.
            Called by if __name__ """
        os.chdir( self.LOGS_DIR )
        for f in glob.glob("easyborrow_controller.log*"):
            filepath = os.path.join( self.LOGS_DIR, f )
            self.filepaths_list.append( filepath )
        return

    def process_log_files( self ):
        """ Processes each log file, updating counts.
            Called by if __name__ """
        for filepath in self.filepaths_list:
            with open( filepath ) as f:
                txt_utf8 = f.read()
                txt = txt_utf8.decode( u'utf-8' )

    def parse_log_file( self ):
        """



    ## helpers



if __name__ == u'__main__':
    """ Loads and parses logs and prints summary.
        Called manually. """
    anlyzr = Analyzer()
    anlyzr.prep_filepaths_list()
    # pprint.pprint( anlyzr.filepaths_list )
    anlyzr.process_log_files()
    print anlyzr.summary
