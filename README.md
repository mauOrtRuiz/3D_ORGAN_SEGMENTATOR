# 3D_Rigid and deformable registration
Organ_3D_SEGMENTATOR

THIS IS THE CODE TO PERFORM 3D ORGAN REGISTRATION AND SEGMENTATION
This experiment is used to perform deformable registration between two images. Images for the test came from the CANCER IMAGING ARCHIVE:
https://www.cancerimagingarchive.net/collection/ct-org/ 

Image #12 was selected as the fixed image and image #11 as the moving 
To run this experiment different steps must be exetuted in the next sequence:

1.- Totalsegmentator is applied to both images, then the corresponding masks are obtained from each image. The following commands can be used after installing TotalSegmentator:
conda activate totalseg

```TotalSegmentator -i C:\Users\UVMInstaller\Downloads\CT-ORG\Test1\volume-11.nii -o C:\Users\UVMInstaller\Downloads\CT-ORG\Output_bone_filtered_11\Mask_11 --fast --ml```


```TotalSegmentator -i C:\Users\UVMInstaller\Downloads\CT-ORG\Test1\volume-12.nii -o C:\Users\UVMInstaller\Downloads\CT-ORG\Output_bone_filtered_11\Mask_12 --fast --ml```

The segmented mask can be visualized in 3D Slicer
![image](https://github.com/user-attachments/assets/64ff4842-7886-4277-9e7a-c73526be0bc4)



2.- 
