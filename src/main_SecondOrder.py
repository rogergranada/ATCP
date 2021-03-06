#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, os, datetime

from Parameters import Parameters
from Measures import Measures
from Miscelaneous import LogFile
from Thesaurus import Thesaurus
from Contexts import Contexts
from StanfordSyntacticContexts import StanfordSyntacticContexts

def main(type_atc, argv):
	date_start = datetime.datetime.now()
	date_start = date_start.strftime("%Y-%m-%d %H:%M:%S")
	
	parameters = Parameters(type_atc, argv)
	contexts = parameters.getContexts()
	input_folder = parameters.getInputFolder()
	language = parameters.getLanguage()
	min_word_size = parameters.getMinWordSize()
	max_qty_terms = int(parameters.getMaxQtyTerms())
	output_folder = parameters.getOutputFolder()
	temp_folder = parameters.getTempFolder()
	record_log = parameters.getRecordLog()
	record_intermediate = parameters.getRecordIntermediate()
	seeds_file = parameters.getSeedsFile()
	stoplist_file = parameters.getStoplistFile()
	sim_measure = parameters.getSimilarityMeasure()
	del parameters

	logfile = LogFile(record_log, str(date_start), None, input_folder, language, stoplist_file, min_word_size, max_qty_terms, None, output_folder, None, temp_folder, seeds_file, sim_measure)

	if contexts:
		logfile.writeLogfile('- Building syntactics relations from '+temp_folder)
		contexts = Contexts(temp_folder)
		del contexts
	else:
		logfile.writeLogfile('- Building syntactics relations from '+input_folder)
		ling_corpus = StanfordSyntacticContexts(input_folder, temp_folder, stoplist_file, min_word_size, record_intermediate)
		del ling_corpus

	logfile.writeLogfile('- Merging terms to '+temp_folder+'Relations2ndOrder.txt')

	command = 'cat '+temp_folder+'AN_Relations.txt '+temp_folder+'SV_Relations.txt '+temp_folder+'VO_Relations.txt '+' > '+temp_folder+'Relations2ndOrder.txt'
	os.system(command)

	logfile.writeLogfile('- Calculating similarity using '+sim_measure)
	measures = Measures(temp_folder+'Relations2ndOrder.txt', seeds_file)
	dic_topn = measures.getTopNToAllSeeds(sim_measure, max_qty_terms)
	del measures

	logfile.writeLogfile('- Building thesaurus in '+output_folder+'T_'+type_atc+'_'+sim_measure+'.xml')

	thesaurus = Thesaurus(output_folder+'T_'+type_atc+'_'+sim_measure+'.xml',max_qty_terms)
	thesaurus.write(dic_topn)
	del thesaurus

	date_end = datetime.datetime.now()
	date_end = date_end.strftime("%Y-%m-%d %H:%M:%S")
	logfile.writeLogfile('- Thesaurus sucessfully built!\nEnding process at: '+str(date_end)+'.\n')
	del logfile

if __name__ == "__main__":
   main('SecondOrder', sys.argv[1:])
