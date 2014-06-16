import os, wave, re, glob, datetime
from pytz import timezone
import scipy.io
import numpy as np
from django.utils import timezone as tz
from django.core.management.base import BaseCommand, CommandError
from husbandry.models import Subject
from electrode.models import Electrode
from extracellular.models import Penetration, Location, SortedUnit, SortQualityMethod, Population
from broab.models import Block, RecordingChannelGroup, RecordingChannel, Segment, EventLabel, Event, Unit, Array, SpikeTrain

def clean_annotations(annotations):
    """ makes sure that keys & values of annotations are all strings """
    new = {}
    for key,val in annotations.iteritems():
        new[str(key)] = str(val)
    return new

def clean_datetime(neo_datetime):
    """ adds django timezone & adjusts year if year is < 13"""
    if neo_datetime is None:
        return None
    elif tz.is_aware(neo_datetime):
        dt = neo_datetime
    elif tz.is_naive(neo_datetime):
        dt = neo_datetime.replace(tzinfo=tz.get_default_timezone())
    else:
        raise TypeError('Not a datetime')

    if dt.year <= tz.now().year%2000:
        dt = dt.replace(year=dt.year+2000)        
    return dt

def loadmat(filename):
    '''
    this function should be called instead of direct scipy.io.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = scipy.io.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''
    for key in dict:
        if isinstance(dict[key], scipy.io.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict        

def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, scipy.io.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict

def chan_map(channel):
    if 'a1x32-10mm50' in electrode_model.lower():
        return {17:1,
                18:32,
                19:2,
                20:31,
                21:3,
                22:30,
                23:4,
                24:29,
                25:5,
                26:28,
                27:6,
                28:27,
                29:7,
                33:26,
                34:8,
                35:25,
                36:9,
                37:24,
                38:10,
                39:23,
                40:11,
                41:22,
                42:12,
                43:21,
                44:13,
                45:20,
                46:14,
                47:19,
                48:15,
                49:18,
                50:16,
                51:17,
                }

def electrode_map(electrode_model):
    if 'a1x32-10mm50' in electrode_model.lower():
        return {17:{'coords':[0,0,0],'name':'1x32 ch1'},
                18:{'coords':[0,0,50],'name':'1x32 ch32'},
                19:{'coords':[0,0,100],'name':'1x32 ch2'},
                20:{'coords':[0,0,150],'name':'1x32 ch31'},
                21:{'coords':[0,0,200],'name':'1x32 ch2'},
                22:{'coords':[0,0,250],'name':'1x32 ch30'},
                23:{'coords':[0,0,300],'name':'1x32 ch4'},
                24:{'coords':[0,0,350],'name':'1x32 ch29'},
                25:{'coords':[0,0,400],'name':'1x32 ch5'},
                26:{'coords':[0,0,450],'name':'1x32 ch28'},
                27:{'coords':[0,0,500],'name':'1x32 ch6'},
                28:{'coords':[0,0,550],'name':'1x32 ch27'},
                29:{'coords':[0,0,600],'name':'1x32 ch7'},
                33:{'coords':[0,0,650],'name':'1x32 ch26'},
                34:{'coords':[0,0,700],'name':'1x32 ch8'},
                35:{'coords':[0,0,750],'name':'1x32 ch25'},
                36:{'coords':[0,0,800],'name':'1x32 ch9'},
                37:{'coords':[0,0,850],'name':'1x32 ch24'},
                38:{'coords':[0,0,900],'name':'1x32 ch10'},
                39:{'coords':[0,0,950],'name':'1x32 ch23'},
                40:{'coords':[0,0,1000],'name':'1x32 ch11'},
                41:{'coords':[0,0,1050],'name':'1x32 ch22'},
                42:{'coords':[0,0,1100],'name':'1x32 ch12'},
                43:{'coords':[0,0,1150],'name':'1x32 ch21'},
                44:{'coords':[0,0,1200],'name':'1x32 ch13'},
                45:{'coords':[0,0,1250],'name':'1x32 ch20'},
                46:{'coords':[0,0,1300],'name':'1x32 ch14'},
                47:{'coords':[0,0,1350],'name':'1x32 ch19'},
                48:{'coords':[0,0,1400],'name':'1x32 ch15'},
                49:{'coords':[0,0,1450],'name':'1x32 ch18'},
                50:{'coords':[0,0,1500],'name':'1x32 ch16'},
                51:{'coords':[0,0,1550],'name':'1x32 ch17'},
                }
    elif 'a1x16-5mm50' in electrode_model.lower(): 
        return {1:{'coords':[0,0,0],'name':'1x16 ch6'},
                2:{'coords':[0,0,50],'name':'1x16 ch11'},
                3:{'coords':[0,0,100],'name':'1x16 ch3'},
                4:{'coords':[0,0,150],'name':'1x16 ch14'},
                5:{'coords':[0,0,200],'name':'1x16 ch1'},
                6:{'coords':[0,0,250],'name':'1x16 ch16'},
                7:{'coords':[0,0,300],'name':'1x16 ch2'},
                8:{'coords':[0,0,350],'name':'1x16 ch15'},
                9:{'coords':[0,0,400],'name':'1x16 ch5'},
                10:{'coords':[0,0,450],'name':'1x16 ch12'},
                11:{'coords':[0,0,500],'name':'1x16 ch4'},
                12:{'coords':[0,0,550],'name':'1x16 ch13'},
                13:{'coords':[0,0,600],'name':'1x16 ch7'},
                14:{'coords':[0,0,650],'name':'1x16 ch10'},
                15:{'coords':[0,0,700],'name':'1x16 ch8'},
                16:{'coords':[0,0,750],'name':'1x16 ch9'},
                }
    else:
        return None  

def get_info_from_filename(mat_file):
    info = {}
    m_subj = re.search(r'st(?P<subject>[\d]+)',mat_file)
    m_pen = re.search(r'pen_(?P<hemi>[A-Za-z]+)_16R(?P<sixteenR>[\d]+)_16L(?P<sixteenL>[\d]+)_16A(?P<sixteenA>[\d]+)_32R(?P<thirtytwoR>[\d]+)_32L(?P<thirtytwoL>[\d]+)_32A(?P<thirtytwoA>[\d]+)',mat_file)
    m_site = re.search(r'site_16Z(?P<sixteenZ>[\d]+)_32Z(?P<thirtytwoZ>[\d]+)',mat_file)

    info = {'subject_id': m_subj.group('subject'),
            '16ch': {'hemisphere': m_pen.group('hemi'),
                     'rostral': m_pen.group('sixteenR'),
                     'lateral': m_pen.group('sixteenL'),
                     'alpha': m_pen.group('sixteenA'),
                     'depth': m_site.group('sixteenZ'),
                     },
            '32ch': {'hemisphere': m_pen.group('hemi'),
                     'rostral': m_pen.group('thirtytwoR'),
                     'lateral': m_pen.group('thirtytwoL'),
                     'alpha': m_pen.group('thirtytwoA'),
                     'depth': m_site.group('thirtytwoZ'),
                     },
            }
    
    return info

def get_wav_params(wav_path):
    params = {}
    wav_reader = wave.open(wav_path,'r')
    (params['nchannels'], 
     params['sampwidth'], 
     params['framerate'], 
     params['nframes'], 
     params['comptype'], 
     params['compname'],) = wav_reader.getparams()
    wav_reader.close()
    (params['path'], params['filename']) = os.path.split(wav_path)
    params['duration'] = float(params['nframes'])/float(params['framerate'])
    return params
       

class Command(BaseCommand):
    args = '<spike2_export_folder>'
    help = "imports the folder of Spike2 exported mat files from st632,st636,st1109,st1124"
    can_import_settings = True
    
    def handle(self, *args, **options):
        pop_good, created = Population.objects.get_or_create(name='gngseq good')
        pop_very, created = Population.objects.get_or_create(name='gngseq very good')
        pop_old, created = Population.objects.get_or_create(name='gngseq old')

        for block_path in args:
            
            # block
            self.stdout.write('Reading block...')

            block_info = get_info_from_filename(block_path)

            # make a location & penetration for this block, too
            subject, created = Subject.objects.get_or_create(name='B'+block_info['subject_id'])

            electrode_serial = 'nXXXX'
            electrode_model = 'a1x32-10mm50'

            electrode, created = Electrode.objects.get_or_create(
                serial_number=electrode_serial,
                notes=electrode_model,
                )
            penetration, created = Penetration.objects.get_or_create(
                hemisphere=block_info['32ch']['hemisphere'][0],
                rostral=block_info['32ch']['rostral'],
                lateral=block_info['32ch']['lateral'],
                alpha_angle=block_info['32ch']['alpha'],
                electrode=electrode,
                subject=subject,
                )
            location, created = Location.objects.get_or_create(
                depth=block_info['32ch']['depth'],
                penetration=penetration,
                )
            file_origin = block_path.split('/')[1]
            block_name = file_origin
            block = Block(name=block_name,
                          file_origin=file_origin)
            block.save()
            location.blocks.add(block)
            self.stdout.write('Successfully saved block "%s"(pk=%s)' % (block,block.pk))

            # make electrode recording channel group
            electrode_rcg = RecordingChannelGroup(name=electrode_model,block=block)
            electrode_rcg.save()
            self.stdout.write('Successfully saved recording_channel_group "%s"(pk=%s)' % (electrode_rcg,electrode_rcg.pk))
            
            # make channels for electrode rcg
            for chan_id, meta in electrode_map(electrode_model).iteritems():
                rec_chan = RecordingChannel(index=chan_id,
                                            name=meta['name'],
                                            x_coord=meta['coords'][0],
                                            y_coord=meta['coords'][1],
                                            z_coord=meta['coords'][2])
                rec_chan.save()
                rec_chan.recording_channel_groups.add(electrode_rcg)
            

            # define stims used in this block
            stim_path = os.path.realpath(os.path.join('./media/stims'))
            stim_list = glob.glob(os.path.join(stim_path,'*.wav'))
            stim_info = {}
            for stim in stim_list:
                stim_info[stim.split(os.sep)[-1].split('.')[0]] = get_wav_params(stim)

            with open('./media/population.txt') as pop_f:
                old_population = [line.strip() for line in pop_f]
            
            trial_lookup = {}
    
            sort_list = glob.glob(os.path.join(block_path,'concat_*'))
            for sort_path in sort_list:
                # try to load the metadata, otherwise skip this sort
                sort_string = sort_path.split('/')[-1]
                sort_info = sort_string.split('_')
                code = sort_info.pop()

                try:
                    metadata_fname = os.path.join(sort_path,code+'_metadata.txt')
                    unit_annotations = {}
                    with open(metadata_fname) as f:
                        for line in f:
                            if 'Source Channel' in line:
                                key, val = line.split(':')
                                unit_annotations[key] = val
                            elif 'trigger level' in line:
                                key, val = line.split(':')
                                unit_annotations[key] = val
                            elif 'Template' in line:
                                key, val = line.split(':')
                                unit_annotations[key] = val
                            elif 'Number of Traces' in line:
                                key, val = line.split(':')
                                unit_annotations[key] = val
                            elif 'Trial (Inclusive)' in line:
                                key, val = line.split(':')
                                unit_annotations[key] = val
                            elif 'Isolation' in line:
                                key, val = line.split(':')
                                unit_annotations[key] = val
                except IOError:
                    continue

                # add rcg if necessary
                rcg_string = '_'.join(sort_info)
                sort_group,created = RecordingChannelGroup.objects.get_or_create(name=rcg_string,
                                                                                 block=block)
                # define sort channels as recording channel groups
                if created:
                    rcg_info = rcg_string.split('_')
                    chan_set = [int(rcg_info[2]),int(rcg_info[3])]
                    
                    chan_names = [electrode_map(electrode_model)[ch]['name'] for ch in chan_set]
                    sort_group.description=','.join(chan_names)
                    sort_group.save()

                    for ch in chan_set:
                        #find recording channel
                        rc = electrode_rcg.recording_channels.get(index=ch)
                        rc.recording_channel_groups.add(sort_group)

                # add unit
                sort_quality = float(unit_annotations['Isolation Quality'])

                method, created = SortQualityMethod.objects.get_or_create(name="justin's eyeball")

                unit = SortedUnit(name=code,
                                  sort_quality_method=method,
                                  sort_quality=sort_quality,
                                  recording_channel_group=sort_group)
                unit.save()

                if unit.sort_quality >= 3.0:
                    pop_good.units.add(unit)
                    if unit.sort_quality >= 4.0:
                        pop_very.units.add(unit)

                block_sort = '/'.join((block_name,sort_string))
                self.stdout.write(block_sort)
                if block_sort in old_population:
                    pop_old.units.add(unit)

                self.stdout.write("added unit %s to recording group %s" % (unit,sort_group.name))

                mat_string = os.path.join(sort_path,'*40kHz.mat')
                #self.stdout.write("looking for mat files %s" % (mat_string))
                mat_list = glob.glob(mat_string)

                
                for mat in mat_list:
                    self.stdout.write(mat)
                    data = loadmat(mat)

                    try:
                        trial_data = data['StimNum']
                        stimulus_data = data['Stimulus']
                        stim_start_data = data['StimStart']
                        spike_data = data['sp_shapes']
                    except KeyError:
                        unit.description = unit.description + '\ncould not import from %s' % mat
                        unit.save()
                        continue

                    iti = 1.0

                    if trial_data['length'] == 1:
                        trial_data['times'] = np.array([trial_data['times']])
                        trial_data['text'] = np.array([trial_data['text']])
                        stimulus_data['times'] = np.array([stimulus_data['times']])
                        stimulus_data['text'] = np.array([stimulus_data['text']])
                        stim_start_data['times'] = np.array([stim_start_data['times']])


                    for ii, tr_start in enumerate(trial_data['times']):

                        #define the segment
                        name = trial_data['text'][ii]
                        file_origin = name.split(' ')[-1]
                        (mm,dd,yy,HH,MM,SS,_,_,_,_,_,_) = file_origin.split('-')
                        trial_datetime = clean_datetime(
                            datetime.datetime(
                                year=int(yy),
                                month=int(mm),
                                day=int(dd),
                                hour=int(HH),
                                minute=int(MM),
                                second=int(SS)
                                )
                            )
                        segment, created = Segment.objects.get_or_create(
                            name=name,
                            index=int(name.split(':')[0].strip()),
                            file_origin=file_origin,
                            file_datetime=trial_datetime,
                            rec_datetime=trial_datetime,
                            block=block
                            )

                        stim_name = stimulus_data['text'][ii]
                        stim_starttime = (stim_start_data['times'][ii]-trial_data['times'][ii])
                        stim_duration = stim_info[stim_name]['duration']
                        tr_length = 2.0 * stim_starttime + stim_duration 

                        if created:
                            segment.annotations=clean_annotations({'concat_time':trial_data['times'][ii]})
                            segment.save()

                            trial_lookup[segment.index] = segment.pk
                            self.stdout.write('Successfully saved segment "%s"(pk=%s)' % (segment,segment.pk))

                            #define the stimulus event
                            

                            event_label, created = EventLabel.objects.get_or_create(name='wav')
                            
                            stim_event = Event(
                                time=stim_starttime,
                                duration=stim_duration,
                                label=event_label,
                                name=stim_name,
                                annotations=clean_annotations(stim_info[stim_name]),
                                segment=segment
                                )
                            stim_event.save()

                
                        # define time boundaries for this segment
                        try:
                            tr_stop = trial_data['times'][ii+1] - iti/2
                        except IndexError:
                            tr_stop = tr_start + 60.0

                    
                        tr_start_mask = spike_data['times'] > tr_start
                        tr_stop_mask = spike_data['times'] < tr_stop
                        trial_unit_mask = tr_start_mask * tr_stop_mask

                        if isinstance(trial_unit_mask,np.bool_):
                            trial_unit_mask = np.array([trial_unit_mask])
                            spike_data['times'] = np.array([spike_data['times']])
                            spike_data['values'] = np.array([spike_data['values']])

                        spike_times = spike_data['times'][trial_unit_mask] - tr_start
                        waveforms = spike_data['values'][trial_unit_mask]

                    
                        waveform_array = Array(data=waveforms.tolist())
                        waveform_array.save()

                        spike_train = SpikeTrain(times=spike_times.tolist(),
                                                 waveform_array=waveform_array,
                                                 waveform_units='V',
                                                 t_start=0.0,
                                                 t_stop=tr_length,
                                                 t_units='s',
                                                 sampling_rate=1/spike_data['interval'],
                                                 left_sweep=spike_data['trigger']*spike_data['interval'],
                                                 unit=unit,
                                                 segment=segment
                                                 )
                        spike_train.save()


                        
