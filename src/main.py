import os
import sys
import subprocess
import json
import glob
import random
import string
import tempfile
import traceback
import shutil


from os.path import join
from alchemyapi import AlchemyAPI
from PIL import Image


alch = AlchemyAPI()
inputPath = ''
allowedFileTypes = ['jpg', 'jpeg']

DEBUG = False


def process(inputPath):
    filesToBeProcessed = getValidFiles(inputPath)
    filesProcessed = 0
    print(str(len(filesToBeProcessed)) + ' files are ready to be processed!!!')
    for fname in filesToBeProcessed:
        try:
            processImage(fname)
        except Exception, e:
            print 'Error when processing file: ' + fname
            print(traceback.format_exc())
        else:
            filesProcessed += 1

    print(str(filesProcessed) + ' of ' + str(len(filesToBeProcessed)) + ' images have been successfully processed')



def processImage(filePath):
    tmpdir = tempfile.mkdtemp()
    predictable_filename = os.path.basename(filePath)

    # Ensure the file is read/write by the creator only
    saved_umask = os.umask(0077)

    path = os.path.join(tmpdir, predictable_filename)
    if DEBUG:
        print("Processing " + str(filePath))
        print("Actual Processing " + str(path))
    try:
        tmpImage = convertImage(filePath, tmpdir)
        tagList = getTags(tmpImage)
        print('Writing tags:' + str(tagList) + ' to:')
        print(filePath + '\n')
        writeTags(filePath, tagList)
    except Exception as e:
        raise e
    else:
        os.remove(path)
    finally:
        os.umask(saved_umask)
        shutil.rmtree(tmpdir)


def convertImage(inputFile, outputDir):
    inputFileName = os.path.basename(inputFile)
    if DEBUG:
        print("Converting image: " + str(inputFile) + "\n and " + str(inputFileName))
    basewidth = 300
    img = Image.open(inputFile)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    outputFile = os.path.join(outputDir, inputFileName)
    if DEBUG:
        print("Saving image: " + str(outputFile))
    img.save(outputFile, 'JPEG', quality=85)
    return outputFile


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
        ProcString = subprocess.check_output(XattrCommand, stderr=subprocess.STDOUT, shell=True)
        Result += ProcString
    return Result 



def getValidFiles(inputPath):
    '''
    return a list of supported image file paths under given directory
    '''
    allFiles = []
    # if inputPath is a image file
    if os.path.isfile(inputPath):
        if inputPath.lower().endswith(tuple(allowedFileTypes)):
            allFiles.append(inputPath)
        else:
            print('Unsupported file type! Currently only support file types in: ' + str(allowedFileTypes))
    # inputPath is a directory
    else:
        inputPath = os.path.abspath(inputPath)
        for root, dirs, files in os.walk(inputPath):
            for fname in files:
                if fname.lower().endswith(tuple(allowedFileTypes)):
                    allFiles.append(join(root, fname))
    return allFiles


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please input an image directy or an image file path.')
    else:
        inputPath = sys.argv[1]
        process(inputPath)
