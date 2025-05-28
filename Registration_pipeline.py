# -*- coding: utf-8 -*-
"""
Created on Wed May 28 11:34:08 2025

@author: Mauricio Ortega
"""


import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk
import ants
import numpy as np

def plot_slices(fixed_array, moving_array, view='axial', step=10, cmap1='gray', cmap2='hot', alpha=0.5):
    assert view in ['axial', 'coronal', 'sagittal'], "Invalid view"
    if view == 'axial':
        num_slices = fixed_array.shape[0]
        get_slice = lambda a, i: a[i, :, :]
    elif view == 'coronal':
        num_slices = fixed_array.shape[1]
        get_slice = lambda a, i: a[:, i, :]
    elif view == 'sagittal':
        num_slices = fixed_array.shape[2]
        get_slice = lambda a, i: a[:, :, i]
     # Use range up to num_slices (not inclusive)
    for i in range(0, num_slices, step):
        if i >= fixed_array.shape[0] or i >= moving_array.shape[0]:
            break  # Just in case, avoid out-of-bounds
        fixed_slice = get_slice(fixed_array, i)
        moving_slice = get_slice(moving_array, i)
        plt.figure(figsize=(6, 6))
        plt.imshow(fixed_slice, cmap=cmap1)
        plt.imshow(moving_slice, cmap=cmap2, alpha=alpha)
        plt.title(f'{view.capitalize()} slice {i}/{num_slices}')
        plt.axis('off')
        plt.show()
        
 
# ***************************************************************************
# ***************************************************************************
#                       WE apply rigid registration
#     This is done between images with only bones and is done:
#     Volume 12 is fixed,   Volume 11 is moving    
# ***************************************************************************
# ***************************************************************************


# Fixed Image -> #12 ||  moving ->#11  /second approach is #114
fixed = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume12_bone_only.nii.gz")
moving = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume11_bone_only.nii.gz")
reg = ants.registration(fixed=fixed, moving=moving, type_of_transform='Rigid')
# ---  Thihs is to run for soft organs
#regb = ants.registration(fixed=fixed, moving=moving, type_of_transform='Rigid')

# the next instruction performs registration
aligned = reg['warpedmovout']
aligned.to_file("C:/Users/UVMInstaller/Downloads/CT-ORG/final/aligned_image_PP12_11.nii.gz")
# **************************************
#  print the registration Information
# **************************************
tx = ants.read_transform(reg['fwdtransforms'][0])
matrix = tx.parameters
print(matrix)

# ******************************************************************

# ***************************************************************************
# ***************************************************************************
# PLOT IN A LOOP
# ***************************************************************************
# ***************************************************************************


# **************************************
# Plot before registration
originalOO = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume12_bone_only.nii.gz", sitk.sitkFloat32)
movedOO = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume11_bone_only.nii.gz", sitk.sitkFloat32)
moving_arrayOO = sitk.GetArrayFromImage(movedOO)
fixed_arrayOO = sitk.GetArrayFromImage(originalOO)
plot_slices(fixed_arrayOO, moving_arrayOO, view='axial', step=80)
plot_slices(fixed_arrayOO, moving_arrayOO, view='coronal', step=80)
plot_slices(fixed_arrayOO, moving_arrayOO, view='sagittal', step=80)


# **************************************
# Plot after registration
originalO1 = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume12_bone_only.nii.gz", sitk.sitkFloat32)
movedO1 = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/final/aligned_image_PP12_11.nii.gz", sitk.sitkFloat32)
moving_arrayOO = sitk.GetArrayFromImage(movedO1)
fixed_arrayOO = sitk.GetArrayFromImage(originalO1)
plot_slices(fixed_arrayOO, moving_arrayOO, view='axial', step=80)
plot_slices(fixed_arrayOO, moving_arrayOO, view='coronal', step=80)
plot_slices(fixed_arrayOO, moving_arrayOO, view='sagittal', step=80)




# ******************************************************************
#    here we apply Affine registration
#   Second Variable 'regAf' will be used for deformable
# ****************************************************************** 
# Fixed Image -> #12 ||  moving ->#11
fixed = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume12_bone_only.nii.gz")
#fixed = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_bone_filtered_12/bones_only12.nii")
moving = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/aligned_image_PP12_11.nii.gz")
# these images are indeed: fixed and moved (after registration)

# Perform affine registration
regAf = ants.registration(fixed=fixed, moving=moving, type_of_transform='Affine')
# **************************************
#  print the registration Information
# **************************************
tx = ants.read_transform(regAf['fwdtransforms'][0])
matrix = tx.parameters
print(matrix)
print(tx.fixed_parameters)
# Get the aligned image
aligned = regAf['warpedmovout']

# Save the result
aligned.to_file("C:/Users/UVMInstaller/Downloads/CT-ORG/final/affined_image_PP12_11G.nii.gz")





# ******************************************************************
#   To apply deformable
#   1. The soft image (body organs) is applied the same rigid and affine registration 
#   2. A fast deformable registration (by downsampling and utilizing fast code)
# ****************************************************************** 

# This is the Deformable with a downsamplig of factor 2 and 4

# === Load input images ===
# Fixed ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Test1/nonbone11_ct_rigid.nii", sitk.sitkFloat32)
# Moving ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Test1/volume-12_no_bone.nii", sitk.sitkFloat32)

#moving = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume12_no_bone.nii.gz")
nonbone_ct_img = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume11_no_bone.nii.gz")


#reg = ants.registration(fixed=fixed_img, moving=bone_ct_img, type_of_transform='Rigid')
nonbone_ct_rigid = ants.apply_transforms(
    fixed=fixed,                      # <== use this, not reg['fixed']
    moving=nonbone_ct_img,
    transformlist=reg['fwdtransforms']

)


nonbone_ct_rigid.to_file("C:/Users/UVMInstaller/Downloads/CT-ORG/final/nonbone11_ct_rigid.nii.gz")


# == Here is where it is applied deformable registration ==

moving = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/nonbone11_ct_rigid.nii.gz")
fixed = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume12_no_bone.nii.gz")

# === Downsample images for speed ===
resample_factor = 2  # Use 4 for even faster but coarser
fixed_down = ants.resample_image(fixed, (fixed.shape[0]//resample_factor,
                                         fixed.shape[1]//resample_factor,
                                         fixed.shape[2]//resample_factor), use_voxels=True)
moving_down = ants.resample_image(moving, (moving.shape[0]//resample_factor,
                                           moving.shape[1]//resample_factor,
                                           moving.shape[2]//resample_factor), use_voxels=True)

# === Fast deformable registration ===
regD = ants.registration(fixed=fixed_down, moving=moving_down,
                        type_of_transform='SyN',
                        aff_metric='mattes',
                        syn_sampling=32,
                        reg_iterations=(40, 20, 0))  # Adjust for faster or more accurate results

# === Apply transforms to original high-res moving image ===
warped_fullres = ants.apply_transforms(fixed=fixed, moving=moving,
                                       transformlist=regD['fwdtransforms'])

# === Save outputs ===
warped_fullres.to_filename("C:/Users/UVMInstaller/Downloads/CT-ORG/final/FINAL_nobone11_ct_12_F2.nii")
print("Deformable registration completed and result saved as 'FINAL_nobone11_ct_12_F2.nii' for resample factor 2")




# ==== We compare the results of segmented mask after deformable registration ====
originalG = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/final/Soft_only12.nii", sitk.sitkFloat32)
movedG = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/final/Soft_only11.nii", sitk.sitkFloat32)
moving_array = sitk.GetArrayFromImage(movedG)
fixed_array = sitk.GetArrayFromImage(originalG)
plot_slices(fixed_array, moving_array, view='axial', step=80)
plot_slices(fixed_array, moving_array, view='coronal', step=80)
plot_slices(fixed_array, moving_array, view='sagittal', step=80)



originalG = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Soft_only12.nii", sitk.sitkFloat32)
movedG = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/final/MASK_nobone11_ct_12_OUT.nii", sitk.sitkFloat32)
moving_array = sitk.GetArrayFromImage(movedG)
fixed_array = sitk.GetArrayFromImage(originalG)
plot_slices(fixed_array, moving_array, view='axial', step=80)
plot_slices(fixed_array, moving_array, view='coronal', step=80)
plot_slices(fixed_array, moving_array, view='sagittal', step=80)






     




        