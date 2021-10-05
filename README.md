# NFT_Project Version 0.5
A project using the NFT_Maker_api_v1 to interact with the NFT_Maker sever allowing for uploading of NFTs and retrevial of their details

### Running the program
The program is typically run through the python3 command. However, when the project is fully built, it will be run through an exe. A typical call to the program looks like: 
'python3 uploadNFT.py /*FoldeName*' where *FolderName* is the filepath to the folder that you want to upload. The program will check for absolute paths or relative paths and account.
However, it is easiest to copy the images and metadata you want to upload to the '/data' folder in the project and just run 'python3 uploadNFT.py data'

### Expected data formatting
The program expects .png images paired with a .json metadata file. They both are required to have the same name. 'name.png' and 'name.json' would be an example.
It is ok if a file does not have metadata, however, it is prefereable. 
