# -*- coding: utf-8 -*-
"""
Created on Wed May 28 10:33:19 2025

@author: UVMInstaller
"""

# ***************************************************************************
# ***************************************************************************
# THIS CODE GENERATES A CT IMAGE WITH ONLY BONES AND CT WITH ONLY SOFT
# ***************************************************************************
# ***************************************************************************



import ants


# --- Load images  First is image VOLUME 11, next image Volume 12---
ct_img = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/volume-11.nii")
bone_mask_img = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/bones_only11.nii")

# --- Convert to NumPy arrays ---
ct_array = ct_img.numpy()
bone_mask_array = bone_mask_img.numpy()

# --- Check that shapes match ---
assert ct_array.shape == bone_mask_array.shape, "Image and mask must be the same shape"

# --- Create CT with only bones ---
ct_bone_only_array = ct_array * (bone_mask_array > 0)

# --- Create CT with bones removed (set bone voxels to 0) ---
ct_no_bone_array = ct_array.copy()
ct_no_bone_array[bone_mask_array > 0] = 0

 # --- Convert back to ANTs images ---
ct_bone_only_img = ants.from_numpy(ct_bone_only_array, spacing=ct_img.spacing, origin=ct_img.origin, direction=ct_img.direction)
ct_no_bone_img = ants.from_numpy(ct_no_bone_array, spacing=ct_img.spacing, origin=ct_img.origin, direction=ct_img.direction)

 # --- Save outputs ---
ct_bone_only_img.to_file("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume11_bone_only.nii.gz")
ct_no_bone_img.to_file("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume11_no_bone.nii.gz")

# ---------------------
# --- Load images  First is image VOLUME 11, next image Volume 12---
ct_img = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/volume-12.nii")
bone_mask_img = ants.image_read("C:/Users/UVMInstaller/Downloads/CT-ORG/final/bones_only12.nii")

# --- Convert to NumPy arrays ---
ct_array = ct_img.numpy()
bone_mask_array = bone_mask_img.numpy()

# --- Check that shapes match ---
assert ct_array.shape == bone_mask_array.shape, "Image and mask must be the same shape"

# --- Create CT with only bones ---
ct_bone_only_array = ct_array * (bone_mask_array > 0)

# --- Create CT with bones removed (set bone voxels to 0) ---
ct_no_bone_array = ct_array.copy()
ct_no_bone_array[bone_mask_array > 0] = 0

 # --- Convert back to ANTs images ---
ct_bone_only_img = ants.from_numpy(ct_bone_only_array, spacing=ct_img.spacing, origin=ct_img.origin, direction=ct_img.direction)
ct_no_bone_img = ants.from_numpy(ct_no_bone_array, spacing=ct_img.spacing, origin=ct_img.origin, direction=ct_img.direction)

 # --- Save outputs ---
ct_bone_only_img.to_file("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume12_bone_only.nii.gz")
ct_no_bone_img.to_file("C:/Users/UVMInstaller/Downloads/CT-ORG/final/ctvolume12_no_bone.nii.gz")