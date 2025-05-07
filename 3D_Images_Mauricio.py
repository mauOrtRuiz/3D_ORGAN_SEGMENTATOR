# -*- coding: utf-8 -*-
"""
Created on Tue May  6 13:45:15 2025

@author: UVMInstaller
"""

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk




# ***************************************************************************
# ***************************************************************************
# THE LABELS FROM THE ATLAS WAS READ JUST TO DETECT BONES LABEL NUMBERS
# ***************************************************************************
# ***************************************************************************

label_map_path = 'C:/Users/UVMInstaller/Downloads/CT-ORG/Test1/labels-10.nii'  # Replace with the actual file path
label_map = nib.load(label_map_path)

 

# Get the data as a NumPy array
label_data = label_map.get_fdata()

 

# Print some basic information
print("Label data shape:", label_data.shape)  # Print the shape of the 3D array (e.g., (x, y, z))
print("Unique labels in the data:", np.unique(label_data))  # Print all unique labels present

 

# Visualize a slice (e.g., middle slice in the z-axis)
slice_index = label_data.shape[2] // 2  # Middle slice
plt.imshow(label_data[:, :, slice_index], cmap='tab20', interpolation='nearest')
plt.colorbar()
plt.title(f"Slice {slice_index} of the Label Map")
plt.show()

 







# ***************************************************************************
# ***************************************************************************
# THIS CODE APPLY THE BONES EXTRACTOR TO GET A .nii FILE WITH ONLY BONES
# ***************************************************************************
# ***************************************************************************

seg=nib.load('C:/Users/UVMInstaller/Downloads/CT-ORG/Output_segmentator_114/OutA.nii')
seg_data=seg.get_fdata()


bone_labels = [

    25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,  # Vertebrae L1–L12
    69, 70, 71, 72, 73, 74, 75, 76,   # Clavicles, sternum Ribs (left and right)
    92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115
    ]



bone_mask=np.isin(seg_data, bone_labels)
bone_only=np.where(bone_mask,seg_data,0)
bone_img=nib.Nifti1Image(bone_only,seg.affine, seg.header)
nib.save(bone_img, "C:/Users/UVMInstaller/Downloads/CT-ORG/bones_only114.nii.gz")



#pip install SimpleITK 
import SimpleITK as stik

# Load fixed and moving images
fixed = stik.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Fixed_11.nii", stik.sitkFloat32)
moving = stik.ReadImage("C:/Users/UVMInstaller/Downloads/CT-ORG/Moving_114.nii", stik.sitkFloat32)

 
# ***************************************************************************
# ***************************************************************************
# PERFORMS REGISTRATION
# ***************************************************************************
# ***************************************************************************
# Initialize the registration
registration_method = stik.ImageRegistrationMethod()

 
# Similarity metric settings
registration_method.SetMetricAsMeanSquares()
registration_method.SetMetricSamplingStrategy(registration_method.NONE)

 

# Rigid transform
registration_method.SetOptimizerAsRegularStepGradientDescent(
    learningRate=2.0,
    minStep=1e-4,
    numberOfIterations=200

)

registration_method.SetInitialTransform(stik.CenteredTransformInitializer(
    fixed, moving, stik.Euler3DTransform(), stik.CenteredTransformInitializerFilter.GEOMETRY
))

 
registration_method.SetInterpolator(stik.sitkLinear)

 

# Run registration
# THIS DOES NOT PRESENT A BAR PROGRESS
final_transform = registration_method.Execute(fixed, moving)

 

# Apply the transformation
resampled = stik.Resample(moving, fixed, final_transform, stik.sitkLinear, 0.0, moving.GetPixelID())

 

# Save result
stik.WriteImage(resampled, "C:/Users/UVMInstaller/Downloads/CT-ORG/registered_image.nii")

 

print("Registration complete.")
print(final_transform)


# ***************************************************************************
# ***************************************************************************
# ANOTHER EXAMPLE TO PERFORM REGISTRATION AND NEXT PLOT THE RESULT
# ***************************************************************************
# ***************************************************************************


# WE USE THE SAME IMAGES, NEXT HERE IT RUNS THE REGISTRATION
registration_method = sitk.ImageRegistrationMethod()
registration_method.SetMetricAsMeanSquares()
registration_method.SetOptimizerAsRegularStepGradientDescent(learningRate=2.0, minStep=1e-4, numberOfIterations=100)
registration_method.SetInitialTransform(sitk.CenteredTransformInitializer(fixed, moving, sitk.Euler3DTransform(), sitk.CenteredTransformInitializerFilter.GEOMETRY))
registration_method.SetInterpolator(sitk.sitkLinear)

# THIS ADDS THE PROGRESS INFO
def command_iteration():
    print(f"Iteration: {registration_method.GetOptimizerIteration()}, "
          f"Metric Value: {registration_method.GetMetricValue()}")

registration_method.AddCommand(sitk.sitkIterationEvent, command_iteration)
final_transform = registration_method.Execute(fixed, moving)

# RESAMPLE MOVING I MAGE  
moving_registered = sitk.Resample(moving, fixed, final_transform, sitk.sitkLinear, 0.0, moving.GetPixelID())


#PLOT SUPERPOSITION BEFORE
def plot_superposition(fixed, moving, title):
    slice_idx = fixed.GetSize()[2] // 2  # middle slice (axial)
    fixed_array = sitk.GetArrayFromImage(fixed)
    moving_array = sitk.GetArrayFromImage(moving)

 

    plt.figure(figsize=(6, 6))
    plt.imshow(fixed_array[slice_idx], cmap='gray')
    plt.imshow(moving_array[slice_idx], cmap='hot', alpha=0.5)  # hot overlay
    plt.title(title)
    plt.axis('off')
    plt.show()

 

# Before registration

plot_superposition(fixed, moving, "Before Registration")



# ***************************************************************************
# ***************************************************************************
# PLOT IN A LOOP
# ***************************************************************************
# ***************************************************************************


# Load your images (SimpleITK images)

fixed_array = sitk.GetArrayFromImage(fixed)     # shape: [z, y, x]
moving_array = sitk.GetArrayFromImage(moving)
moving_array_registered = sitk.GetArrayFromImage(moving_registered)

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

 
 
# Before registration
plot_slices(fixed_array, moving_array, view='axial', step=20)

# After registration
plot_slices(fixed_array, moving_array_registered, view='axial', step=20)


# plot_slices(fixed_array, moving_array, view='coronal', step=20)

# plot_slices(fixed_array, moving_array, view='sagittal', step=20)