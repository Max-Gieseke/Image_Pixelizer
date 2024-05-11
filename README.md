# Running the Code
This code was developed using Python 3.12, so for best results this make sure that you have this version available. To run the code, first clone the repository and navigate to the newly created Pixel_Art folder. Then once there, run 
```
pip install -r requirements.txt
```
to install the required pacakges. Then to run the program, 
```
python pixelize.py
```
# Creating a Pixelized Image
First, download an image of your choosing and move it to the ```photos``` folder. Then, aftering running the program, type in the name of the image that you placed in the photos folder. Then you will be asked to select the size of the new "pixels" formed and the number of colors to use in the new image. Once these choices are made, the code will begin to process and transform the image. Once it is done, a new image will be created in the ```pixelated_photos``` folder, where the file will be in the format ```<name>_<pixel size>_px_<palette size>pz.jpg```. 
