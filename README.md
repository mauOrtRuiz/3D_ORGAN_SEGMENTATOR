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

For example, Mask of file #12 can be visualized by using 3D Slicer (image #11):

![image](https://github.com/user-attachments/assets/a0b8659c-6901-40bd-a79d-47541dd7a550)


3.-  The bones structures are now removed from the original CT images, and also images with soft organs removed are obtained. This is done in the file *Filter_CTimages.py*. This uses the poriginal Volume image (volume-11.nii and volume-12.nii) and it gives as an output the CT images already filtered. 

This is for example the CT bones image for volume 11 image:

![image](https://github.com/user-attachments/assets/85d74032-46a3-4a03-af0e-ff387cb631b9)

And this is the CT imaged without bone structures:

![image](https://github.com/user-attachments/assets/24619e89-1e52-4537-b330-4ce915cab5ac)


4.- Now we apply Rigid registration and we obtain the matrix transformation into the variable *reg*.  This and the next steps are implemented in the *Registration_pipeline.py* file

To visualize the result a routine calles *plot_slices* can be called to plpot 2D images of the sagittal, coronal and axial view to visualize a comparative image to see the alignment of both images
Here we can observe a sample of the same slice before and after rigid registration

![image](https://github.com/user-attachments/assets/90251872-28d6-4c3c-9674-330113f28462)

The main rigid registration command is:

```fixed = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume12_bone_only.nii.gz")```

```moving = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume11_bone_only.nii.gz")```

```reg = ants.registration(fixed=fixed, moving=moving, type_of_transform='Rigid')```





5.- Affine registration is applied, the main commands are:

```fixed = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume12_bone_only.nii.gz")```


```moving = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/aligned_image_PP12_11.nii.gz")```

```regAf = ants.registration(fixed=fixed, moving=moving, type_of_transform='Affine')```


6.-  Now deformable registratiopn is applied to the non-bones structure .nii file. For this operation the image is downsized by 2, next deformable registration is applied with next instructions:

```regD = ants.registration(fixed=fixed_down, moving=moving_down,```

                        ```type_of_transform='SyN',```
                        
                        ```aff_metric='mattes',```
                        
                        ```syn_sampling=32,```
                        
                        ```reg_iterations=(40, 20, 0))  # Adjust for faster or more accurate results```








