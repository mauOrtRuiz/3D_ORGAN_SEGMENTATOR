
# -*- coding: utf-8 -*-
"""
Created on Sat May 10 10:25:27 2025

@author: UVMInstaller

THIS IS A FULL PIPELINE TO PERFORM RIGID REGISTRATION
"""



# ******************************************
#  Sagittal flipp before do registration
#  We just flippp the moving image
import ants
import numpy as np

# Load your image
image = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_bone_filtered_114/bones_only114.nii")

# Convert to NumPy array
image_np = image.numpy()

# Flip along x-axis (sagittal axis)
flipped_np = np.flip(image_np, axis=0)

 
# Create a new ANTs image with the same spacing, origin, and direction
flipped_image = ants.from_numpy(flipped_np,
                                 spacing=image.spacing,
                                 origin=image.origin,
                                 direction=image.direction)

# Save the flipped image
flipped_image.to_file("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_bone_filtered_114/flipped_image.nii.gz")





# ******************************************************************
#    here we apply rigid registration}

# Fixed Image -> #12 ||  moving ->#114
fixed = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_bone_filtered_12/bones_only12.nii")
moving = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_bone_filtered_114/bones_only114.nii")
reg = ants.registration(fixed=fixed, moving=moving, type_of_transform='Rigid')
aligned = reg['warpedmovout']
aligned.to_file("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_segmentator_114/aligned_image_PP12_114.nii.gz")
# **************************************
#  print the registration Information
# **************************************
tx = ants.read_transform(reg['fwdtransforms'][0])
matrix = tx.parameters
print(matrix)

# ******************************************************************
# Here we see the result

import sys
import os
import SimpleITK as sitk
import matplotlib.pyplot as plt


def command_iteration(method):
    """ Callback invoked each iteration. """
    if method.GetOptimizerIteration() == 0:
        print(f"\tLevel: {method.GetCurrentLevel()}")
        print(f"\tScales: {method.GetOptimizerScales()}")
    print(f"#{method.GetOptimizerIteration()}")
    print(f"\tMetric Value: {method.GetMetricValue():10.5f}")
    print(f"\tLearningRate: {method.GetOptimizerLearningRate():10.5f}")
    if method.GetOptimizerConvergenceValue() != sys.float_info.max:
        print("\tConvergence Value: " + f"{method.GetOptimizerConvergenceValue():.5e}")


def command_multiresolution_iteration(method):
    """ Callback invoked at the end of each multi-resolution level. """
    print(f"\tStop Condition: {method.GetOptimizerStopConditionDescription()}")
    print("============= Resolution Change =============")


if len(sys.argv) < 4:
    print(
        "Usage:",
        sys.argv[0],
        "<fixedImageFilter> <movingImageFile>",
        "<outputTransformFile>",
    )
    sys.exit
    
# ***************************************
# View the result
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
       





# **************************************
#before registration
originalOO = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_bone_filtered_12/bones_only12.nii", sitk.sitkFloat32)
movedOO = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_bone_filtered_114/bones_only114.nii", sitk.sitkFloat32)
moving_arrayOO = sitk.GetArrayFromImage(movedOO)
fixed_arrayOO = sitk.GetArrayFromImage(originalOO)
plot_slices(fixed_arrayOO, moving_arrayOO, view='axial', step=80)
plot_slices(fixed_arrayOO, moving_arrayOO, view='coronal', step=80)
plot_slices(fixed_arrayOO, moving_arrayOO, view='sagittal', step=80)


# **************************************
#after registration
original = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_bone_filtered_12/bones_only12.nii", sitk.sitkFloat32)
moved = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_segmentator_114/aligned_image_PP12_114.nii", sitk.sitkFloat32)


moving_array = sitk.GetArrayFromImage(moved)
fixed_array = sitk.GetArrayFromImage(original)

     
             
# After registration
plot_slices(fixed_array, moving_array, view='axial', step=80)
plot_slices(fixed_array, moving_array, view='coronal', step=80)
plot_slices(fixed_array, moving_array, view='sagittal', step=80)

# ***************************************************************************
# ***************************************************************************
# Dummy movement example 
# ***************************************************************************
# ***************************************************************************
import sys
import os
import SimpleITK as sitk
import matplotlib.pyplot as plt
def command_iteration(method):
    """ Callback invoked each iteration. """
    if method.GetOptimizerIteration() == 0:
        print(f"\tLevel: {method.GetCurrentLevel()}")
        print(f"\tScales: {method.GetOptimizerScales()}")
    print(f"#{method.GetOptimizerIteration()}")
    print(f"\tMetric Value: {method.GetMetricValue():10.5f}")
    print(f"\tLearningRate: {method.GetOptimizerLearningRate():10.5f}")
    if method.GetOptimizerConvergenceValue() != sys.float_info.max:
        print("\tConvergence Value: " + f"{method.GetOptimizerConvergenceValue():.5e}")


def command_multiresolution_iteration(method):
    """ Callback invoked at the end of each multi-resolution level. """
    print(f"\tStop Condition: {method.GetOptimizerStopConditionDescription()}")
    print("============= Resolution Change =============")


if len(sys.argv) < 4:
    print(
        "Usage:",
        sys.argv[0],
        "<fixedImageFilter> <movingImageFile>",
        "<outputTransformFile>",
    )
    sys.exit
    
 
original = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Moving_114.nii", sitk.sitkFloat32)

 
transform = sitk.Euler3DTransform()
#transform.SetTranslation((10.0, 5.0, -7.0))  # in mm
transform.SetTranslation((5.0, 0.0, 0.0))  # Keep small to ensure overlap

moved = sitk.Resample(original, original, transform, sitk.sitkLinear, 0.0, original.GetPixelID())   

sitk.WriteImage(moved,"C:/Users/UVMInstaller/Downloads/CT-ORG/Moved_dummy_image.nii") 
transform.SetTranslation((10.0, 5.0, -7.0))  # Keep small to ensure overlap
moved = sitk.Resample(original, original, transform, sitk.sitkLinear, 0.0, original.GetPixelID())   
sitk.WriteImage(moved,"C:/Users/UVMInstaller/Downloads/CT-ORG/Moved_dummyB_image.nii") 
sitk.WriteImage(original,"C:/Users/UVMInstaller/Downloads/CT-ORG/Original_dummy_image.nii")

# **************************************************
#  Nucleu need to be reinitiated
#    here we apply rigid registration to the dummy
# Fixed Image -> #12 ||  moving ->#114
import ants
import numpy as np

fixed = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/Original_dummy_image.nii")
moving = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/Moved_dummy_image.nii")
reg = ants.registration(fixed=fixed, moving=moving, type_of_transform='Rigid')
aligned = reg['warpedmovout']
aligned.to_file("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_segmentator_114/aligned_dummy_image_PP12_114.nii.gz")
#  View The dummy

originalO = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Original_dummy_image.nii", sitk.sitkFloat32)
movedO = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Moved_dummy_image.nii", sitk.sitkFloat32)
movedOO = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_segmentator_114/aligned_dummy_image_PP12_114.nii", sitk.sitkFloat32)
moving_arrayO = sitk.GetArrayFromImage(movedO)
moving_arrayOO = sitk.GetArrayFromImage(movedOO)
fixed_arrayO = sitk.GetArrayFromImage(originalO)
plot_slices(fixed_arrayO, moving_arrayO, view='axial', step=80)
plot_slices(fixed_arrayO, moving_arrayO, view='coronal', step=80)
plot_slices(fixed_arrayO, moving_arrayO, view='sagittal', step=80)

plot_slices(fixed_arrayO, moving_arrayOO, view='axial', step=80)
plot_slices(fixed_arrayO, moving_arrayOO, view='coronal', step=80)
plot_slices(fixed_arrayO, moving_arrayOO, view='sagittal', step=80)

#  DUMMY EXAMPLE 2
fixed = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/Original_dummy_image.nii")
moving = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/Moved_dummyB_image.nii")
reg = ants.registration(fixed=fixed, moving=moving, type_of_transform='Rigid')
aligned = reg['warpedmovout']
aligned.to_file("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_segmentator_114/aligned_dummyB_image_PP12_114.nii.gz")



# **************************************
#  print the registration Information
# **************************************
tx = ants.read_transform(reg['fwdtransforms'][0])
matrix = tx.parameters
print(matrix)
print(tx.fixed_parameters)

originalOB = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Original_dummy_image.nii", sitk.sitkFloat32)
movedOB = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_segmentator_114/aligned_dummyB_image_PP12_114.nii", sitk.sitkFloat32)
movedNotB = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Moved_dummyB_image.nii", sitk.sitkFloat32)
moving_arrayOB = sitk.GetArrayFromImage(movedOB)
moving_arrayNotB = sitk.GetArrayFromImage(movedNotB)
fixed_arrayOB = sitk.GetArrayFromImage(originalOB)
# This is before registration
plot_slices(fixed_arrayOB, moving_arrayNotB, view='axial', step=80)
plot_slices(fixed_arrayOB, moving_arrayNotB, view='coronal', step=80)
plot_slices(fixed_arrayOB, moving_arrayNotB, view='sagittal', step=80)

# This is after registration
plot_slices(fixed_arrayOB, moving_arrayOB, view='axial', step=80)
plot_slices(fixed_arrayOB, moving_arrayOB, view='coronal', step=80)
plot_slices(fixed_arrayOB, moving_arrayOB, view='sagittal', step=80)


# ******************************************************************
#    here we apply Affine registration
# Fixed Image -> #12 ||  moving ->#114
fixed = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_bone_filtered_12/bones_only12.nii")
moving = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_segmentator_114/aligned_image_PP12_114.nii")
# these images are indeed: fixed and moved (after registration)

# Perform affine registration
reg = ants.registration(fixed=fixed, moving=moving, type_of_transform='Affine')
# **************************************
#  print the registration Information
# **************************************
tx = ants.read_transform(reg['fwdtransforms'][0])
matrix = tx.parameters
print(matrix)
print(tx.fixed_parameters)
# Get the aligned image
aligned = reg['warpedmovout']

# Save the result
aligned.to_file("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_segmentator_114/affined_image_PP12_114.nii.gz")


#after registration
original = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_bone_filtered_12/bones_only12.nii", sitk.sitkFloat32)
moved = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_segmentator_114/affined_image_PP12_114.nii", sitk.sitkFloat32)
movedO = sitk.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Output_bone_filtered_114/bones_only114.nii", sitk.sitkFloat32)
moving_arrayO = sitk.GetArrayFromImage(movedO)
moving_array = sitk.GetArrayFromImage(moved)
fixed_array = sitk.GetArrayFromImage(original)
# After registration
plot_slices(fixed_array, moving_arrayO, view='axial', step=80)
plot_slices(fixed_array, moving_arrayO, view='coronal', step=80)
plot_slices(fixed_array, moving_arrayO, view='sagittal', step=80)

plot_slices(fixed_array, moving_array, view='axial', step=80)
plot_slices(fixed_array, moving_array, view='coronal', step=80)
plot_slices(fixed_array, moving_array, view='sagittal', step=80)


