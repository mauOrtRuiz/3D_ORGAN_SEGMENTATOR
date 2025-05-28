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



2.- The bones structures are now filtered, we obtain a CTimage file with only the bones and another CT image with bones removed and only the non-bones structures
Based on TotalSegmentator the bones structures have the following labels:


```bone_labels = [```


```    25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,  # Vertebrae L1–L12```

```    69, 70, 71, 72, 73, 74, 75, 76,   # Clavicles, sternum Ribs (left and right)```

```    91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115```

 ```   ]```

The file Filter_bones.py the input are the files *Mask_11.nii* and *Mask_12.nii* obtained in step 1 and the putput are files:   bones_only11.nii.gz and bones_only12.nii.gz

