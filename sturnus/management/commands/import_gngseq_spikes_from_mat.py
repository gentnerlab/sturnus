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
    args = '<spike2_export.mat>'
    help = "imports the Spike2 exported mat file from st699 or st888"
    can_import_settings = True
    
    def handle(self, *args, **options):
        pop_good, created = Population.objects.get_or_create(name='gngseq good')
        pop_very, created = Population.objects.get_or_create(name='gngseq very good')

        for filename in args:
            
            # block
            self.stdout.write('Reading block...')

            block_info = get_info_from_filename(filename)

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
            file_origin = filename.split('/')[-1]
            block_name = '_'.join(file_origin.split('_')[:-1])
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

            # load data
            data = loadmat(filename)
            sort_notes=np.genfromtxt('media/sort_notes.csv',delimiter=',',names=True,dtype=None)

            # define stims used in this block
            stim_path = os.path.realpath(os.path.join('./media/stims'))
            stim_list = glob.glob(os.path.join(stim_path,'*.wav'))
            stim_info = {}
            for stim in stim_list:
                stim_info[stim.split(os.sep)[-1].split('.')[0]] = get_wav_params(stim)
            
            # segment
            trial_data = data['StimNum']
            stimulus_data = data['Stimulus']
            
            trial_lookup = {}
            for trial in range(trial_data['length']):
                #define the segment
                name = trial_data['text'][trial]
                file_origin = name.split(' ')[-1]
                (mm,dd,yy,HH,MM,SS,_,_,_,_,_,_) = file_origin.split('-')
                trial_datetime = clean_datetime(datetime.datetime(year=int(yy),
                                                                  month=int(mm),
                                                                  day=int(dd),
                                                                  hour=int(HH),
                                                                  minute=int(MM),
                                                                  second=int(SS)))
                segment = Segment(name=name,
                              index=int(name.split(':')[0].strip()),
                              file_origin=file_origin,
                              file_datetime=trial_datetime,
                              rec_datetime=trial_datetime,
                              annotations=clean_annotations({'concat_time':trial_data['times'][trial]}),
                              block=block)
                segment.save()
                trial_lookup[segment.index] = segment.pk
                self.stdout.write('Successfully saved segment "%s"(pk=%s)' % (segment,segment.pk))

                #define the stimulus event
                stim_name = stimulus_data['text'][trial]
                stim_starttime = (stimulus_data['times'][trial]-trial_data['times'][trial])
                stim_duration = stim_info[stim_name]['duration']

                event_label, created = EventLabel.objects.get_or_create(name='wav')
                
                stim_event = Event(time=stim_starttime,
                                   duration=stim_duration,
                                   label=event_label,
                                   name=stim_name,
                                   annotations=clean_annotations(stim_info[stim_name]),
                                   segment=segment
                                   )
                stim_event.save()

            subject_mask = sort_notes['subject']=='st'+block_info['subject_id']
            pen_str = 'pen_%s_16R%s_16L%s_16A%s_32R%s_32L%s_32A%s' % (block_info['32ch']['hemisphere'],
                                                                      block_info['16ch']['rostral'],
                                                                      block_info['16ch']['lateral'],
                                                                      block_info['16ch']['alpha'],
                                                                      block_info['32ch']['rostral'],
                                                                      block_info['32ch']['lateral'],
                                                                      block_info['32ch']['alpha'])
            pen_mask = sort_notes['pen']==pen_str
            site_str = 'site_16Z%s_32Z%s' % (block_info['16ch']['depth'],
                                             block_info['32ch']['depth'])
            site_mask = sort_notes['site']==site_str

            mask = subject_mask * pen_mask * site_mask

            for sorted_unit in sort_notes[mask]:
                label = 'V'+sorted_unit['rcg']
                try:
                    sort_data = data[label]
                except KeyError:
                    continue

                sort_group,created = RecordingChannelGroup.objects.get_or_create(name=label,
                                                                                 block=block,
                                                                                 )
                # define sort channels as recording channel groups
                if created:
                    chan_set = [sorted_unit['sortchannel1'],sorted_unit['sortchannel2']]
                    if sorted_unit['sortchannel3']>0:
                        chan_set.append(sorted_unit['sortchannel3'])
                        chan_set.append(sorted_unit['sortchannel4'])

                    chan_names = [electrode_map(electrode_model)[ch]['name'] for ch in chan_set]
                    sort_group.description=','.join(chan_names)+'\n'+sort_data['comment']
                    sort_group.save()

                    for ch in chan_set:
                        #find recording channel
                        rc = electrode_rcg.recording_channels.get(index=ch)
                        rc.recording_channel_groups.add(sort_group)

                # define unit
                method, created = SortQualityMethod.objects.get_or_create(name="justin's eyeball")
                unit = SortedUnit(name='code%0.2d' % sorted_unit['marker'],
                                  sort_quality_method=method,
                                  sort_quality=float(sorted_unit['sort_rating_05']),
                                  description=sorted_unit['notes'],
                                  recording_channel_group=sort_group)
                unit.save()

                if unit.sort_quality >= 3.0:
                    pop_good.units.add(unit)
                    if unit.sort_quality >= 4.0:
                        pop_very.units.add(unit)

                self.stdout.write("adding unit %s to recording group %s" % (unit,sort_group.name))

                code_mask = sort_data['codes'][:,0] == sorted_unit['marker']

                # populate segments with spiketrains from units
                iti = 1.0
                starttime_mask = trial_data['times'] > sorted_unit['starttimeofsort']
                if 'max' not in sorted_unit['endtimeofsort']:
                    endtimeofsort = float(sorted_unit['endtimeofsort'])
                    endtime_mask = trial_data['times'] < endtimeofsort
                    time_mask = starttime_mask * endtime_mask
                else:
                    time_mask = starttime_mask
                trial_times = trial_data['times'][time_mask]
                trial_indices = [int(name.split(':')[0].strip()) for name in trial_data['text'][time_mask]]
                trial_pks = [trial_lookup[idx] for idx in trial_indices]

                for ii, tr_start in enumerate(trial_times):
                    # define time boundaries for this segment
                    try:
                        tr_stop = trial_times[ii+1] - iti
                    except IndexError:
                        tr_stop = tr_start + 60.0
                    
                    tr_start_mask = sort_data['times'] > tr_start
                    tr_stop_mask = sort_data['times'] < tr_stop
                    trial_unit_mask = code_mask * tr_start_mask * tr_stop_mask

                    spike_times = sort_data['times'][trial_unit_mask] - tr_start
                    waveforms = sort_data['values'][trial_unit_mask]
                    
                    waveform_array = Array(data=waveforms.tolist())
                    waveform_array.save()

                    segment = Segment.objects.get(pk=trial_pks[ii])
                    spike_train = SpikeTrain(times=spike_times.tolist(),
                                             waveform_array=waveform_array,
                                             waveform_units='V',
                                             t_start=0.0,
                                             t_stop=(tr_stop-tr_start),
                                             t_units='s',
                                             sampling_rate=1/data[label]['interval'],
                                             left_sweep=data[label]['trigger']*data[label]['interval'],
                                             unit=unit,
                                             segment_id=trial_pks[ii]
                                             )
                    spike_train.save()

                        
