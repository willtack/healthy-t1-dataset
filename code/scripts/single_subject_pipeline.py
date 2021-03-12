# Script for single subject w-score pipeline
# - input a subject's age and results of get_vals.py
# - calculate w-score for each ROI of label-set
# - render a segmentation image with corresponding w-scores in place of label indices

import os
import pandas as pd
import glob

## Calculate subject-specific w-scores for each ROI
wsCoffs = pd.read_csv('/home/will/Projects/healthy-t1-dataset/ws_coeffs.csv') # w-score coefficients for norm data
# get atlas information, incl index label numbers
label_idx_file = '/home/will/Projects/healthy-t1-dataset/labels/Schaefer2018_200Parcels_17Networks_order.csv'
label_idxs = pd.read_csv(label_idx_file)
indices = list()
for ind in range(0,len(label_idxs)): # h
    i=label_idxs.label_number[ind]
    indices.append(i)
    
#### patient-specific data #########
# pt_data = pd.read_csv('/media/will/My Passport/Ubuntu/cortical_thickness_maps/ct/C472/work2/sub-C472_schaefer.csv')
# pt_data=pt_data[pt_data.type=="mean"]
# pt_age = 22
# label_img = '/media/will/My Passport/Ubuntu/cortical_thickness_maps/ct/C472/sub-C472_Schaefer2018_200x17.nii.gz'
# working_dir = '/media/will/My Passport/Ubuntu/cortical_thickness_maps/ct/C472/work2'

pt_data = pd.read_csv('/home/will/Projects/healthy-t1-dataset/test_sub/118785/sub-118785_schaefer.csv')
pt_data=pt_data[pt_data.type=="mean"]
pt_age = 22
label_img = '/home/will/Projects/healthy-t1-dataset/test_sub/118785/sub-118785_ses-20200820_Schaefer2018_200Parcels17Networks.nii.gz'
working_dir = '/home/will/Projects/healthy-t1-dataset/test_sub/118785/work'

os.chdir(working_dir)
#####################################


### wscore calculation! outputs DataSeries
wscores = (pt_data.value - wsCoffs.intercept - pt_age*wsCoffs.age_coefficient)/wsCoffs.residual_se

# save to DataFrame
d = {'label_number': indices, 'w-score': list(wscores)}
wscore_df = pd.DataFrame(data=d)
# wscore_df = wscore_df[0:10] # OPTIONAL
# wscore_df.head()


# loop through rows for ROI index (lbli) and wscore
# use fslmaths to convert label index numbers to corresponding w-score for all voxels in ROI
for index, row in wscore_df.iterrows():
    wscore = row['w-score']
    lbli = int(row['label_number'])
    #create temporary image for each ROI with w-score as value
    tmpOutput = os.path.join(working_dir, 'tmp{}.nii.gz'.format(lbli))
    cmd = "fslmaths '{0}' -thr {1} -uthr {2} -div {3} -mul {4} '{5}'".format(label_img, lbli-.5, lbli+.5, lbli, wscore, tmpOutput)
    print(cmd)
    os.system(cmd)
    
# merge all temporary ROI images together
image_list = glob.glob(os.path.join(working_dir, "tmp*.nii.gz"))
images_str = ' -add '.join('"{0}"'.format(img) for img in image_list) # string paths together, with single quotes around file paths
cmd2 = "fslmaths {} wscore_img.nii.gz".format(images_str)
print(cmd2)
os.system(cmd2)

# remove temporary files
cmd3 = "rm '{}'/tmp*.nii.gz".format(working_dir)
print(cmd3)
os.system(cmd3)