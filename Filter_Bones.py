# -*- coding: utf-8 -*-
"""
Created on Wed May 28 10:19:58 2025

@author: Mauricio Ortega
"""

# ***************************************************************************
# ***************************************************************************
# THIS CODE APPLY THE BONES EXTRACTOR TO GET A .nii FILE WITH ONLY BONES
# ***************************************************************************
# ***************************************************************************
import nibabel as nib
import numpy as np

seg=nib.load('C:/Users/UVMInstaller/Downloads/CT-ORG/final/Mask_11.nii')
seg_data=seg.get_fdata()


bone_labels = [

    25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,  # Vertebrae L1–L12
    69, 70, 71, 72, 73, 74, 75, 76,   # Clavicles, sternum Ribs (left and right)
    91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115
    ]



bone_mask=np.isin(seg_data, bone_labels)
bone_only=np.where(bone_mask,seg_data,0)
bone_img=nib.Nifti1Image(bone_only,seg.affine, seg.header)
nib.save(bone_img, "C:/Users/UVMInstaller/Downloads/CT-ORG/final/bones_only11.nii.gz")
