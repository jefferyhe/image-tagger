import sys
import subprocess
import json
import glob

from alchemyapi import AlchemyAPI


alch = AlchemyAPI()
inputPath = ''
DEBUG = False

def getTags(imagePath):	
	response = alch.imageTagging('image', imagePath)
	if response['status'] == 'OK':
		print('## Response Object ##')
		print(json.dumps(response, indent=4))
		tagList = []
		for tags in response['imageKeywords']:
			tagList.append(tags['text'])
			print (tags['text'])
		
		writeTags(imagePath, tagList)
		
	else:
		print('Error in image tagging call: ', response['statusInfo'])
	return


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

def process(path):
	if path.endswith('.jpg'):
		getTags(path)		
	else:
		path += "/*.jpg"
		print (path)
		for fname in glob.glob(path):
			getTags(fname)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please input an image directy or an image file path.')
    else:
        inputPath = sys.argv[1]
        process(inputPath)



