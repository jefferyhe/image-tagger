# image-tagger
**image-tagger** is a tool that analysis your local images files, generate tags(keywords) for the images, and automatically add those tags to your files on your MacOS, so that you can search your images by tags on your Mac. You don't need to upload your files to Web hosting services, it all happens on your local hard disks or even your external hard drivers.



## Preview
This program will add tags to you image file:

![image](screenshot1.png)

Then you can search tags use Finder or Spotlight

![image](screenshot2.png)




## Getting Started

First you need to get a free api key from [here](http://www.alchemyapi.com/api/register.html)

Simply fill out the forms then you will receive a free api key.

Clone the repository

```
# Get the latest snapshot
git clone https://github.com/jefferyhe/imageTagger.git

# Change directory
cd src

# Apply api key
python alchemyapi.py your-api-key

# Begin rock n' roll
python main.py "dragonfly.jpg"

# The parameter could be a path of image file or a directory containing image files
```
Currently only support jpg files, more file types support is comming!


