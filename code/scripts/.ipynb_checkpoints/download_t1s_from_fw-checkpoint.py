import flywheel

# get collection and its sessions
fw = flywheel.Client()
collection_id = '5eb5081448fe1b1e5792a7a9'
sessions = [fw.get_session(x.id) for x in fw.get_collection_sessions(collection_id)]
collection = fw.get(collection_id)

# start with an empty list for t1 acquisition containers
t1_list = []
# for ses in sessions:
for ses in sessions[400:420]:
    potential_T1s = []
    for acq in ses.acquisitions():
        if 'ABCD_T1w_vNav_passive_RMS' in acq.label or 'Sagittal_MPRage' in acq.label or 't1_mpr_AX_MPRAGE' in acq.label:
            potential_T1s.append(acq)
        else: 
            # check if acq has a Measurement classification
            has_mes = 'Measurement' in acq.files[0]['classification']
            if has_mes:
                # check if the Measurement is a T1
                has_t1 = 'T1' in acq.files[0]['classification']['Measurement']
            # If it is a T1, add the acquisition container to the list
            if has_mes and has_t1:
                print('is T1')
                potential_T1s.append(acq)
    print('{} has {} potential T1s.'.format(ses.label, len(potential_T1s)))     
    if len(potential_T1s) == 1:
        t1_list.append(potential_t1s[0])
        print("Downloading " + ses.label + "'s " + potential_T1s[0].label)
    elif len(potential_T1s) > 1:
        for i in range(len(potential_T1s)):
            if 'ABCD_T1w_vNav_passive_RMS' in potential_T1s[i].label:
                t1_list.append(potential_T1s[i])
                print("Downloading " + ses.label + "'s " + potential_T1s[i].label)
            else:
                t1_list.append(potential_T1s[0])
                print("Downloading " + ses.label + "'s " + potential_T1s[0].label)
    elif len(potential_T1s) == 0:
        print(ses.label + " did not have a T1 acquisition.")
        continue            

            # collection.download_file() wouldn't work for some reason

fw.download_tar(t1_list, '/home/will/Desktop/test.tar')
