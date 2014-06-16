from django.db.models import Q, Min, Max, F
from broab.models import Event

def get_spikes_locked_to_events(unit,Q_obj,lock_end=False):
    events = Event.objects.filter(segment__spiketrains__unit=unit).filter(Q_obj).order_by('segment__rec_datetime','time')
            
    locked_times = []
    event_pks = []
    for event in events:
        event_time = event.time
        if lock_end:
            event_time += event.duration
        spike_times = event.segment.spiketrains.get(unit=unit).times
        locked_times.append([t - event_time for t in spike_times])
        event_pks.append(event.pk)
    return locked_times, event_pks

def get_spikes_locked_to_target(unit,context=None,target=None,lock_end=False):
                                                                                    
    if context is None:
        if target is None:
            name_Q = Q(name__contains='silence') & Q(label__name='wav')
            times, event_pks = get_spikes_locked_to_events(unit,name_Q,lock_end=lock_end)

        else:
            file_Q = Q(segment__events__name__contains='_'+target+'_')
            name_Q = Q(name=target) & Q(label__name='motif')
            times, event_pks = get_spikes_locked_to_events(unit,file_Q & name_Q,lock_end=lock_end)

    elif target is None:
        file_Q = Q(segment__events__name__contains='_'+context+'_')
        name_Q = Q(name=context) & Q(label__name='motif')
            
        times, event_pks = get_spikes_locked_to_events(unit,file_Q & name_Q,lock_end=True)
        times = [[t-0.1 for t in sptr] for sptr in times] 
    else:
        file_Q = Q(segment__events__name__contains='_'+context+target+'_')
        name_Q = Q(name=target) & Q(label__name='motif')
                
        events = Event.objects.filter(segment__spiketrains__unit=unit) \
                              .filter(file_Q & name_Q) \
                              .annotate(min_time=Min('segment__events__time')) \
                              .filter(time__gt=F('min_time')+0.7) \
                              .order_by('segment__rec_datetime','time')
                                        
        times = []
        event_pks = []
        for event in events:
            event_time = event.time
            if lock_end:
                event_time += event.duration
            spike_times = event.segment.spiketrains.get(unit=unit).times
            times.append([t - event_time for t in spike_times])
            event_pks.append(event.pk)
                                                                    
    return times, event_pks
