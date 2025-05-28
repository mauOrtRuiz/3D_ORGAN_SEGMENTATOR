# 3D_Rigid and deformable registration
Organ_3D_SEGMENTATOR

THIS IS THE CODE TO PERFORM 3D ORGAN REGISTRATION AND SEGMENTATION


import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk

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
