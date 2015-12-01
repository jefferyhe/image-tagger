import os
import sys
import subprocess
import json
import glob

from os.path import join
from alchemyapi import AlchemyAPI


alch = AlchemyAPI()
inputPath = ''
allowedFileTypes = ['jpg', 'jpeg']

DEBUG = False

def process(inputPath):
	filesToBeProcessed = getValidFiles(inputPath)
	print(str(len(filesToBeProcessed)) + ' files are ready to be processed!!!')
	for fname in filesToBeProcessed:
		tagList = getTags(fname)
		print('Writing tags:' + str(tagList) + ' to:')
		print(fname + '\n')
		writeTags(fname, tagList)


def getValidFiles(inputPath):
	'''
	return a list of supported image file paths under given directory
	'''
	allFiles = []
	if os.path.isfile(inputPath): 
		if inputPath.lower().endswith(tuple(allowedFileTypes)):
			allFiles.append(inputPath)
		else:
			print('Unsupported file type! Currently only support file types in: ' + str(allowedFileTypes))
	else:
		inputPath = os.path.abspath(inputPath)
		for root, dirs, files in os.walk(inputPath):
			for fname in files:
				if fname.lower().endswith(tuple(allowedFileTypes)):
					allFiles.append(join(root, fname))	
	return allFiles


def getTags(imagePath):	
	'''
	return tags for given image file path
	'''
	tagList = []
	response = alch.imageTagging('image', imagePath)
	if response['status'] == 'OK':
		#print('## Response Object ##')
		#print(json.dumps(response, indent=4))
		for tags in response['imageKeywords']:
			tagList.append(tags['text'])

	else:
		print('Error in image tagging call: ', response['statusInfo'])
	return tagList


def writeTags(F,TagList):
    """ writeTags(F,TagList):
    writes the list of tags to three xattr fields on a file-by file basis:
    "kMDItemFinderComment","_kMDItemUserTags","kMDItemOMUserTags
    Uses subprocess instead of xattr module. Slower but no dependencies"""

    Result = ""

    plistFront = '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><array>'
    plistEnd = '</array></plist>'
    plistTagString = ''
    for Tag in TagList:
        plistTagString = plistTagString + '<string>{}</string>'.format(Tag.replace("'","-"))
    TagText = plistFront + plistTagString + plistEnd

    OptionalTag = "com.apple.metadata:"
    XattrList = ["kMDItemFinderComment","_kMDItemUserTags","kMDItemOMUserTags"]
    for Field in XattrList:    
    	XattrCommand = 'xattr -w {0} \'{1}\' "{2}"'.format(OptionalTag + Field,TagText.encode("utf8"),F)
    	if DEBUG:
            sys.stderr.write("XATTR: {}\n".format(XattrCommand))
        ProcString = subprocess.check_output(XattrCommand, stderr=subprocess.STDOUT,shell=True) 
        Result += ProcString
    return Result



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please input an image directy or an image file path.')
    else:
        inputPath = sys.argv[1]
        process(inputPath)


