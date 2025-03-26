# Histomics slide(WSI) analysis toolkit
get_histomics_features.py was adapted from *https://github.com/arunima2/histomicstk_feature_extraction*

## Usage
```
python get_histomics_features.py <path of image to analyze> <path of image to normalize the input image to> <minimum nuclei area in px for an object to be labeled nuclie> <foreground threshold to identify nuclei in grayscale> <path of folder where output files should be stored>
```
  
### Example Usage
```
python get_histomics_features.py ../prostate_images/T4--33-B6-L_L3R5_T4_22.png ../prostate_images/T4--33_B6_R_L1R6_T4_3.png 15 100 histomics_output/
```