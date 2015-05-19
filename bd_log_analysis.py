# -*- coding: utf-8 -*-

""" Compares new borrowdirect api results against current in-production deprecated code.
    Parses logging added to controller that summarizes differences between new and old tunneler calls. """

import glob, os, pprint


class Analyzer( object ):

    def __init__( self ):
        self.LOGS_DIR = unicode( os.environ[u'BDLOG_ANALYSIS__LOGS_DIR'] )
        self.filepaths_list = []
        self.labels = [ u'new_api_found', u'new_api_requestable', u'old_api_found', u'old_api_requestable' ]
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
                lines_utf8 = f.readlines()
                self.parse_log_file( lines_utf8 )
        return

    ## helpers

    def parse_log_file( self, lines_utf8 ):
        """ Parses given lines to update counts.
            Called by process_log_files() """
        relevant_segments = self.find_relevant_segments( lines_utf8 )
        pprint.pprint( relevant_segments )
        return

    def find_relevant_segments( self, lines_utf8 ):
        """ Finds comparison lines and merges them into single string.
            Called by parse_log_file() """
        ( segments, segment ) = ( [], [] )
        for line_utf8 in lines_utf8:
            line = line_utf8.decode( u'utf-8' )
            for label in self.labels:
                if label in line:
                    segment.append( line )
            if len( segment ) == 4:
                joined_segment = u''.join( segment )
                segments.append( joined_segment )
                segment = []
        return segments






if __name__ == u'__main__':
    """ Loads and parses logs and prints summary.
        Called manually. """
    anlyzr = Analyzer()
    anlyzr.prep_filepaths_list()
    # pprint.pprint( anlyzr.filepaths_list )
    anlyzr.process_log_files()
    print anlyzr.summary
