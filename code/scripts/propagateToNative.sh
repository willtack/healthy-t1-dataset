#!/bin/bash
#
# Script for propagating the Schaefer 2018 200 parcels x 17 networks label set to native space 
# Adapted from github.com/ftdc-picsl/antsct-aging/runAntsCT_nonBIDS.pl
#
#
templateDir=/home/will/.templateflow
atlasPath=${templateDir}/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-01_atlas-Schaefer2018_desc-200Parcels17Networks_dseg.nii.gz
outputParentDir=/media/will/My\ Passport/Ubuntu/cortical_thickness_maps/ct
ANTSPATH=/usr/local/ANTs/bin

error_exit()
{
	echo "$@" 1>&2
	exit 1
}

# Map cortical labels to the subject GM, mask with GM and propagate through GM mask
#
# args: corticalMask - binary image to label
#       labelImage - label image in template space, to warp
#       outputRoot - output root for antsCT. Used to find warps and name output
#       outputLabelName - added to output root, eg "DKT31"
#
# propagateCorticalLabelsToNativeSpace($gmMask, $labelImage, $mniSpace, $outputRoot, $outputLabelName) 
#

propagateCorticalLabelsToNativeSpace ()
{
    corticalMask=$1
    labelImage=$2
    outputRoot=$3
    outputLabelName=$4
    extractedBrain=$5
    affineMatrix=$6
    warpFile=$7
    
    tmpLabels="${outputRoot}/tmp${outputLabelName}.nii.gz"
    # Run warp command 
    ${ANTSPATH}/antsApplyTransforms -d 3 -r "${extractedBrain}" -t "${affineMatrix}" -t "${warpFile}" \
                                    -t ${templateDir}/MNI152NLin2009cAsymToTemplateWarp.nii.gz \
                                    -n GenericLabel -i ${labelImage} -o "${tmpLabels}" || error_exit "Could not warp labels $labelImage to subject space"
    # Propagate Labels
    ${ANTSPATH}/ImageMath 3 "${outputRoot}/${outputLabelName}.nii.gz" PropagateLabelsThroughMask "${corticalMask}" "${tmpLabels}" 8 0 || \
        error_exit "Could not propagate labels ${labelImage} through cortical mask"
    # Make QC file
#     ${ANTSPATH}/LabelOverlapMeasures 3 "${outputRoot}/${outputLabelName}.nii.gz" "${tmpLabels}" "${outputRoot}/{$outputLabelName}WarpedvsPropagated.csv"
    
    rm -rf "${tmpLabels}"
}

for subjectDir in "${outputParentDir}"/*; do #loop through subject folders in already-existing ct folder
    subjectName=$(basename "${subjectDir}")
    echo "Propagating Labels for ${subjectName}..."
    #check if propagation already completed for subject
    file=$(find "${subjectDir}" -type f | grep Schaefer)
    if [ -f "${file}" ]; then
        echo "   Already processed ${subjectName}."
        continue
    fi
    # locate necessary files in original subject folder
    corticalMask=$(find "${subjectDir}" -type f | grep CorticalMask)
    extractedBrain=$(find "${subjectDir}" -type f | grep ExtractedBrain)
    affineMatrix=$(find "${subjectDir}" -type f | grep GenericAffine)
    warpFile=$(find "${subjectDir}" -type f | grep Warp)
    # run the command
    propagateCorticalLabelsToNativeSpace "${corticalMask}" "${atlasPath}" "${subjectDir}" "${subjectName}_Schaefer2018_200x17" "${extractedBrain}" "${affineMatrix}" "${warpFile}"
done