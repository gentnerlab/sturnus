import quantities as pq
from neo import io
from neo import core
from pytz import timezone
from django.utils import timezone as tz
from django.core.management.base import BaseCommand, CommandError
from broab.models import models
from extracellular.models import CoordinateSystem, Penetration, Location, Unit
from electrode.models import Electrode
from husbandry.models import Subject

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

def create_block(neo_block):
    """creates a block from a neo block"""
    block = models.Block()
    if neo_block.name is not None:
        block.name = neo_block.name
    if neo_block.description is not None:
        block.description = neo_block.description
    if neo_block.file_origin is not None:
        block.file_origin = neo_block.file_origin
    block.annotations = clean_annotations(neo_block.annotations)
    block.index = neo_block.index
    block.file_datetime = clean_datetime(neo_block.file_datetime)
    block.rec_datetime = clean_datetime(neo_block.rec_datetime)
    return block

def create_recording_channel_group(neo_recording_channel_group,block=None):
    """creates recording channel group from a neo recording channel group"""
    recording_channel_group = models.RecordingChannelGroup()
    if neo_recording_channel_group.name is not None:
        recording_channel_group.name = neo_recording_channel_group.name
    if neo_recording_channel_group.description is not None:
        recording_channel_group.description = neo_recording_channel_group.description
    if neo_recording_channel_group.file_origin is not None:
        recording_channel_group.file_origin = neo_recording_channel_group.file_origin
    recording_channel_group.annotations = clean_annotations(neo_recording_channel_group.annotations)
    if block is not None:
        recording_channel_group.block = block
    return recording_channel_group

def create_recording_channel(neo_recording_channel,recording_channel_group=None):
    """creates recording channel from a neo recording channel"""
    recording_channel = models.RecordingChannel()
    if neo_recording_channel.name is not None:
        recording_channel.name = neo_recording_channel.name
    if neo_recording_channel.description is not None:
        recording_channel.description = neo_recording_channel.description
    if neo_recording_channel.file_origin is not None:
        recording_channel.file_origin = neo_recording_channel.file_origin
    recording_channel.annotations = clean_annotations(neo_recording_channel.annotations)
    recording_channel.index = neo_recording_channel.index
    coord_units = 'um'
    coordinates = neo_recording_channel.coordinate.rescale(coord_units)
    x,y,z = [float(ii) for ii in coordinates]
    recording_channel.x_coord = x
    recording_channel.y_coord = y
    recording_channel.z_coord = z
    recording_channel.coord_units = coord_units
    return recording_channel

def create_unit(neo_unit,recording_channel_group=None):
    """creates recording channel from a neo recording channel"""
    unit = models.Unit()
    if neo_unit.name is not None:
        unit.name = unit.name
    if neo_unit.description is not None:
        unit.description = unit.description
    if neo_unit.file_origin is not None:
        unit.file_origin = neo_unit.file_origin
    unit.annotations = clean_annotations(neo_unit.annotations)
    if recording_channel_group is not None:
        unit.recording_channel_group = recording_channel_group
    return unit

def create_segment(neo_segment,block=None):
    """creates segment from a neo segment"""
    segment = models.Segment()
    if neo_segment.name is not None:
        segment.name = neo_segment.name
    if neo_segment.description is not None:
        segment.description = neo_segment.description
    if neo_segment.file_origin is not None:
        segment.file_origin = neo_segment.file_origin
    segment.index = neo_segment.index
    segment.file_datetime = clean_datetime(neo_segment.file_datetime)
    segment.rec_datetime = clean_datetime(neo_segment.rec_datetime)
    segment.annotations = clean_annotations(neo_segment.annotations)
    if block is not None:
        segment.block = block
    return segment

def create_event(neo_event,segment):
    """creates event from a neo event or epoch"""
    event = models.Event()
    if neo_event.name is not None:
        event.name = neo_event.name
    if neo_event.description is not None:
        event.description = neo_event.description
    if neo_event.file_origin is not None:
        event.file_origin = neo_event.file_origin
    event.annotations = clean_annotations(neo_event.annotations)

    event.time = float(neo_event.time.rescale('s'))
    try:
        event.duration = float(neo_event.duration.rescale('s'))
    except AttributeError:
        pass

    event_type, created = models.EventType.objects.get_or_create(name=neo_event.label)

    event.label = event_type
    event.segment = segment

    return event

def create_analog_signal(neo_analog_signal,segment,recording_channel=None):
    analog_signal = models.AnalogSignal()
    if neo_analog_signal.name is not None:
        analog_signal.name = neo_analog_signal.name
    if neo_analog_signal.description is not None:
        analog_signal.description = neo_analog_signal.description
    if neo_analog_signal.file_origin is not None:
        analog_signal.file_origin = neo_analog_signal.file_origin
    analog_signal.annotations = clean_annotations(neo_analog_signal.annotations)

    t_units = 's'
    t_start = neo_analog_signal.t_start.rescale(t_units)
    analog_signal.t_start = float(t_start)
    analog_signal.t_units = t_units

    try:
        signal_units = 'V'
        signal = neo_analog_signal.signal.rescale(signal_units)
    except ValueError, e:
        signal_units = 'A'
        signal = neo_analog_signal.signal.rescale(signal_units)
        
    analog_signal.signal = signal
    analog_signal.signal_units = signal_units
    if neo_analog_signal.sampling_rate is not None:
        analog_signal.sampling_rate = neo_analog_signal.sampling_rate
    elif neo_analog_signal.sampling_period is not None:
        analog_signal.sampling_rate = 1.0 / neo_analog_signal.sampling_period

    analog_signal.segment = segment
    if recording_channel is not None:
        analog_signal.recording_channel = recording_channel
    return analog_signal

def create_spike_train(neo_spike_train,segment_id,unit_id=None):
    spike_train = models.SpikeTrain()   
    if neo_spike_train.name is not None:
        spike_train.name = neo_spike_train.name
    if neo_spike_train.description is not None:
        spike_train.description = neo_spike_train.description
    if neo_spike_train.file_origin is not None:
        spike_train.file_origin = neo_spike_train.file_origin
    spike_train.annotations = clean_annotations(neo_spike_train.annotations)

    t_units = 's'
    times = neo_spike_train.times.rescale(t_units)
    spike_train.times = [float(t) for t in times]
    spike_train.t_start = float(neo_spike_train.t_start.rescale(t_units))
    spike_train.t_stop = float(neo_spike_train.t_stop.rescale(t_units))
    spike_train.t_units = t_units


    spike_train.segment_id = segment_id
    if unit_id is not None:
        spike_train.unit_id = unit_id

    return spike_train

def create_spike_train_full(neo_spike_train,segment_id,unit_id=None):
    spike_train = models.SpikeTrainFull()
    if neo_spike_train.name is not None:
        spike_train.name = neo_spike_train.name
    if neo_spike_train.description is not None:
        spike_train.description = neo_spike_train.description
    if neo_spike_train.file_origin is not None:
        spike_train.file_origin = neo_spike_train.file_origin
    spike_train.annotations = clean_annotations(neo_spike_train.annotations)

    t_units = 's'
    times = neo_spike_train.times.rescale(t_units)
    spike_train.times = [float(t) for t in times]
    spike_train.t_start = float(neo_spike_train.t_start.rescale(t_units))
    spike_train.t_stop = float(neo_spike_train.t_stop.rescale(t_units))
    spike_train.t_units = t_units

    waveform_units = 'V'
    try:
        waveforms = neo_spike_train.waveforms.rescale(waveform_units)
    except ValueError, e:
        waveforms = neo_spike_train.waveforms
    spike_train.waveforms = waveforms.base.tolist()
    spike_train.waveform_units = waveform_units

    spike_train.left_sweep = neo_spike_train.left_sweep
    spike_train.sampling_rate = neo_spike_train.sampling_rate
    if neo_spike_train.sort is not None:
        spike_train.sort = neo_spike_train.sort

    spike_train.segment_id = segment_id
    if unit_id is not None:
        spike_train.unit_id = unit_id

    return spike_train


class Command(BaseCommand):
    args = '<neo.h5>'
    help = "imports the neo hdf5 file from one of justin's experiments"
    can_import_settings = True
    
    def handle(self, *args, **options):
        for filename in args:
            # TODO: change reader based on filetype
            reader = io.NeoHdf5IO(filename)

            if core.block.Block in reader.readable_objects:
                # block
                self.stdout.write('Reading block(s)...')
                for bl in reader.read_all_blocks():
                    block = create_block(bl)
                    block.save()
                    bl.annotate(django_pk=block.pk)
                    self.stdout.write('Successfully saved block "%s"(pk=%s)' % (block,block.pk))

                    # make a location & penetration for this block, too

                    # recording channel groups
                    if core.recordingchannelgroup.RecordingChannelGroup in reader.readable_objects:
                        for rcg in bl.recordingchannelgroups:
                            recording_channel_group = create_recording_channel_group(rcg,block)
                            recording_channel_group.save()
                            rcg.annotate(django_pk=recording_channel_group.pk)
                            self.stdout.write('Successfully saved recording_channel_group "%s"(pk=%s)' % (recording_channel_group,recording_channel_group.pk))

                            # recording channels
                            if core.recordingchannel.RecordingChannel in reader.readable_objects:
                                for rc in rcg.recordingchannels:
                                    self.stdout.write('Checking if recording_channel already exists...')
                                    if 'django_pk' in rc.annotations:
                                        pk = rc.annotations['django_pk']
                                        self.stdout.write('Recording channel exists (pk=%s), adding %s to recording_channel_groups' % (pk,recording_channel_group))
                                        recording_channel = models.RecordingChannel.objects.get(pk=pk)
                                        # recording_channel.recording_channel_groups.add(recording_channel_group)
                                        # self.stdout.write('Successfully added recording_channel "%s"(pk=%s) to rcg "%s"' % (recording_channel,recording_channel.pk,recording_channel_group))
                                    else:
                                        recording_channel = create_recording_channel(rc,recording_channel_group)
                                        recording_channel.save()
                                        rc.annotate(django_pk=recording_channel.pk)
                                    recording_channel.recording_channel_groups.add(recording_channel_group)
                                    self.stdout.write('Successfully saved recording_channel "%s"(pk=%s)' % (recording_channel,recording_channel.pk))

                            # units
                            if core.unit.Unit in reader.readable_objects:
                                for u in rcg.units:
                                    unit = create_unit(u,recording_channel_group)
                                    unit.save()
                                    u.annotate(django_pk=unit.pk)
                                    self.stdout.write('Successfully saved unit "%s"(pk=%s)' % (unit,unit.pk))

                    # segment
                    if core.segment.Segment in reader.readable_objects:
                        for seg in bl.segments:
                            segment = create_segment(seg,block)
                            segment.save()
                            seg.annotate(django_pk=segment.pk)
                            self.stdout.write('Successfully saved segment "%s"(pk=%s)' % (segment,segment.pk))

                            # events
                            if core.event.Event in reader.readable_objects:
                                for ev in seg.events:
                                    event = create_event(ev,segment)
                                    event.save()
                                    ev.annotate(django_pk=event.pk)
                                    self.stdout.write('Successfully saved event "%s"(pk=%s)' % (event,event.pk))

                            # for ev_array in seg.event_arrays:
                            #     event_list = create_events_from_array(ev_array,segment)

                            # epochs
                            if core.epoch.Epoch in reader.readable_objects:
                                for ep in seg.epochs:
                                    event = create_event(ep,segment)
                                    event.save()
                                    ep.annotate(django_pk=event.pk)
                                    self.stdout.write('Successfully saved event "%s"(pk=%s)' % (event,event.pk))

                            # for ep_array in seg.epoch_arrays:
                            #     event_list = create_events_from_array(ep_array,segment)


                            # spike trains
                            if core.spiketrain.SpikeTrain in reader.readable_objects:
                                for sptr in seg.spiketrains:
                                    u = sptr.unit
                                    unit_id = u.annotations['django_pk']
                                    if sptr.waveforms is not None:
                                        spike_train = create_spike_train_full(sptr,segment.pk,unit_id)
                                        spike_train.save()
                                    else:
                                        spike_train = create_spike_train(sptr,segment.pk,unit_id)
                                        spike_train.save()

                                    
                                # if len(spike_train_set) > 999:
                                #     self.stdout.write('Creating %s SpikeTrain instances in bulk...' % (len(spike_train_set),))
                                #     models.SpikeTrain.objects.bulk_create(spike_train_set)
                                #     self.stdout.write('Success!')
                                #     spike_train_set = []


                                # if len(spike_train_full_set) > 999:
                                #     self.stdout.write('Creating %s SpikeTrainFull instances in bulk...' % (len(spike_train_full_set),))
                                #     models.SpikeTrainFull.objects.bulk_create(spike_train_full_set)
                                #     self.stdout.write('Success!')
                                #     spike_train_full_set = []

                            # # analog signals
                            # for ansig in seg.analog_signals:
                            #     analog_signal = create_analog_signal(ansig,segment,recording_channel)

                            # for ansig_array in seg.analogsignalarrays:
                            #     analog_signal_list = create_analog_signal_from_array(ansig_array,segment)
