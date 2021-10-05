import sys
import os
import base64
import json
from typing import cast
import requests

apiKey = "e37deceb9d334ceaa1033ee7b0027a75"
projectId = "18942"

# UploadNFTs.py. 
# 
# Overview:
#   Given a folder location as an argument (tbd), this program will loop through all
#   png's in the folder which will be paired with a .jSon file of the same name as the png.
#   The png will be encoded in Base64 and the metadata of the .jSon file will be concatinated
#   into the return value of the API. 
#   
#   Before the images are uploaded, A check will be done where all the images will be listed.    
#   /UploadNFT will then be called, uploading each one indvidually.  
#
# TODO: Get a file to easily change apiKey and projectId
# TODO: Add a layer of interpreation around the responses to uploads to give a clear indication of what was successful and what was not.

def main():
    # Get the directory specified
    try:
        directory = getDirectory()
    except Exception as e:
        directory = ""
        print(f"Error: {e}")
        print("Exiting Program...")

    # Loop through each image, finding the associated jSon file and print them out.
    check = checkToUploadFiles(directory)
    if (check == False):
        print("Not continuing with upload. Exiting Program...")
        exit
    
    uploadFiles(directory)

def getDirectory():
    '''
    Reads from command line arguments, gets and validates the directory provided.
    Handles errors:
      Error when directory doesnt exist
      Error when directory does not have any pngs in it.
      Error when given no arguemtns
      Error when given too many arguements
    '''

    arguments = sys.argv

    # Check for the correct number of arugments
    if (len(arguments) != 2):
        raise(ValueError("Incorrect number of arguments. Please input a single directory with png files in it"))

    # Check that the given file is a filepath
    # isabs() checks if the given string starts with a / or not.
    path = ""
    if (os.path.isabs(arguments[1])):
        dirName = os.path.dirname(__file__)
        path = os.paht.join(dirName, arguments[1])
    else:
        path = arguments[1]

    # Check that the given argument is actually a directory.
    if (not os.path.isdir(path)):
        raise(ValueError("Given path is not a directory."))
    
    # Loop through each file in the directory to check that there is at least 1 png to upload.
    pngExists = False
    for fileName in os.listdir(path):
        if fileName.endswith(".png"):
            pngExists = True
            break
    if (not pngExists):
        raise(ValueError("Given directory does not contain any .png's to upload."))
    
    return path

def checkToUploadFiles(directory):
    '''
     Loops throug all files looking for png files. When it finds them,
     the program also tries to find an associated .jSon file with the same name
     
     Prints out these files to let the user check that all files are inteded to be uploaded.
    '''
    # TODO: Remove extra path & json variables if they are not used.

    print("Files exposed for uploading: ")
    for entry in os.scandir(directory):
        path = ""
        jSon = ""
        
        # Found a file that ends with .png, so find the associated .json file
        if (entry.path.endswith(".png")):

            path = entry.path                                   # Extract the pathname and look
            jSonPath = entry.path[:len(path) - 4] + ".json"     # for the corresponding .json file with the same name
            
            if (os.path.isfile(jSonPath)):
                jSon = jSonPath
                print(f"    {path} - {jSonPath}")
                continue
            else:
                print(f"    {path} - No associated json found")

    response = input("Continue with file upload? [y/n] ").lower()
    if response == "y":
        return True
    else:
        return False
    
def uploadFiles(directory):
    """
    Uploads all the files in a given directory to the NFT_Maker servers.
    The given directory is scanned for .png and matching .json files and
    then callUploadNFT() is called on each pair.
    """
    # Loop through each png in the folder
    fileCount = 0
    for entry in os.scandir(directory):

        b64ImageEncode = ""
        imageMetaData = {}
        if not entry.path.endswith(".png"): # Skip file if it is not a png
            continue

        fileCount += 1
        # Grab the base64 encoding of the file and store it in b64ImageEncode
        with open(entry.path, "rb") as currImage:
            b64ImageEncode = base64.b64encode(currImage.read()).decode("utf-8")
        
        jSonPath = entry.path[:len(entry.path)-4] + ".json"
        if os.path.isfile(jSonPath):  # If the .json file of the same name exists..

            # Read the .json file and store its contents in imageMetatData
            with open(jSonPath) as jsonFile:
                imageMetaData = json.load(jsonFile)    
        
                callUploadNFT(b64ImageEncode, imageMetaData, fileCount)
        
def callUploadNFT(imageAsBase64, imageMetaData, fileCount):
    """
    Makes an html request to https://api.nft-maker.io/UploadNft.
    This uploads the given base64 encoded file and image metaData
    """

    global apiKey
    global projectId
    
    # The data given through the html requiest
    uploadPayload ={
            "assetName": f"ManageNFT{fileCount}",
            "previewImageNft": {
                "mimetype": "image/png",
                "fileFromBase64": imageAsBase64,
                "metadataPlaceholder": [
                    imageMetaData
                ]
            }
            }

    # Make the request
    url = fr"https://api.nft-maker.io/UploadNft/{apiKey}/{projectId}"
    head = {"Content-Type":"application/json", "Accept":"application/json"}
    response = requests.post(url, json=uploadPayload, headers=head)

    # Print response.
    print(f"Response:\n{response}\n")
    print(f"Response text:\n{response.text}\n")
    print(f"Response raw:\n{response.raw}\n")

if __name__ == "__main__":
    main()
