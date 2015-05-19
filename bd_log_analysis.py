# -*- coding: utf-8 -*-

""" Compares new borrowdirect api results against current in-production deprecated code.
    Parses logging added to controller that summarizes differences between new and old tunneler calls. """

import glob, json, os, pprint


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
            # break
        return

    ## helpers

    def parse_log_file( self, lines_utf8 ):
        """ Parses given lines to update counts.
            Called by process_log_files() """
        relevant_segments = self.find_relevant_segments( lines_utf8 )
        cleaned_lines = self.clean_relevant_segments( relevant_segments )
        self.run_counts( cleaned_lines )
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

    def clean_relevant_segments( self, relevant_segments ):
        """ Turns each messy line into a json string; json isn't used, it's to normalize the strings.
            Called by parse_log_file() """
        cleaned_lines = []
        for line in relevant_segments:
            start = line.find( u'`' ) + 1
            end = line.rfind( u'`' )
            str1 = line[start:end]
            str2 = self.run_replaces( str1 )
            dct = json.loads( str2  )
            jsn = json.dumps( dct, sort_keys=True )
            cleaned_lines.append( jsn.decode(u'utf-8') )
        return cleaned_lines

    def run_replaces( self, str1 ):
        """ Runs a series of replaces to normalize string.
            Called by clean_relevant_segments() """
        str2 = str1.replace( u'\n', u'' )
        str3 = str2.replace( u"'", u'"' )
        str4 = str3.replace( u'u"', u'"' )
        str5 = str4.replace( u'True', u'true' )
        str6 = str5.replace( u'False', u'false' )
        str7 = str6.replace( u'None', u'null' )
        return str7

    def run_counts( self, cleaned_lines ):
        """ Checks and updates patterns, and counts.
            Called by parse_log_file() """
        if u'total_entries' in self.summary.keys():
            self.summary[u'total_entries'] += len(cleaned_lines)
        else:
            self.summary[u'total_entries'] = len(cleaned_lines)
        for pattern in cleaned_lines:
            if pattern in self.summary.keys():
                self.summary[pattern] += 1
            else:
                self.summary[pattern] = 0
        return




if __name__ == u'__main__':
    """ Loads and parses logs and prints summary.
        Called manually. """
    anlyzr = Analyzer()
    anlyzr.prep_filepaths_list()
    # pprint.pprint( anlyzr.filepaths_list )
    anlyzr.process_log_files()
    pprint.pprint( anlyzr.summary )
