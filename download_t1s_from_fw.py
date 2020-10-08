import flywheel

# get collection and its sessions
fw = flywheel.Client()
collection_id = '5eb5081448fe1b1e5792a7a9'
sessions = [fw.get_session(x.id) for x in fw.get_collection_sessions(collection_id)]
collection = fw.get(collection_id)

# start with an empty list for t1 acquisition containers
t1_list = []
# for ses in sessions:
for ses in sessions[100:120]:
    for acq in ses.acquisitions():
        # check if acq has a Measurement classification
        has_mes = 'Measurement' in acq.files[0]['classification']
        if has_mes:
            # check if the Measurement is a T1
            has_t1 = 'T1' in acq.files[0]['classification']['Measurement']
        else:
            continue
        # If it is a T1, add the acquisition container to the list
        if has_mes and has_t1:
            print('is T1')
            t1_list.append(acq)
            # collection.download_file() wouldn't work for some reason

fw.download_tar(t1_list, '/home/will/Desktop/test.download_tar')
