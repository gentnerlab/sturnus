from django.core.management.base import BaseCommand, CommandError
from operant.models import ProtocolType, Protocol, Session, TrialType, TrialClass, Trial
from broab.models import Segment, Block
from husbandry.models import Subject
from datetime import datetime
from django.utils import timezone as tz

TRIAL_TYPES = {
    '1': 'Normal',
    '0': 'Correction',
}

TRIAL_CLASS = {
    'GNG': {
        '1': 'Center',
        '2': 'No Response',
    },
    '2AC': {
        '1': 'Left',
        '2': 'Right',
        '3': 'Probe',
    },
}

TRIAL_RESPONSE = {
    'GNG': {
        '0': 'No Response',
        '1': 'Center',
    },
    '2AC': {
        '0': 'No Response',
        '1': 'Left',
        '2': 'Right',
    },
    
}

BOOL = {
    '0': False,
    '1': True,
    '2': True,
    }

def time_of_trial(TOD,Date,start_time):
    start = datetime.strptime(start_time,"%a %b %d %H:%M:%S %Y")
    trial_time = datetime.strptime(TOD+Date,"%H%M%m%d")
    trial_time = trial_time.replace(year=start.year)
    while trial_time < datetime.now():
        trial_time = trial_time.replace(year=trial_time.year+1)
    if tz.is_naive(trial_time):
        trial_time = trial_time.replace(tzinfo=tz.get_default_timezone())
    return trial_time

def import_rDAT(rdat_file):
    with open(rdat_file) as fh:
        for line in fh:
            if 'File name' in line:
                file_origin = line.split(':')[-1].strip()

            elif 'Procedure source' in line:
                protocol_type = line.split(':')[-1].strip()
                protocol_type, created = ProtocolType.objects.get_or_create(name=protocol_type)

            elif 'Start time' in line:
                start_time = ':'.join(line.split(':')[1:]).strip()

            elif 'Subject ID' in line:
                subject_id = line.split(':')[-1].strip()
                subject_name = 'B'+subject_id
                subject, created = Subject.objects.get_or_create(name=subject_name)

            elif 'Stimulus source' in line:
                stim_source = line.split(':')[-1].strip()
                protocol, created = Protocol.objects.get_or_create(name=stim_source,
                                                                   type=protocol_type,
                                                                   )

            elif 'reinforcement is set in the .stim' in line:
                pass
            elif 'Sess#' in line:
                last_session = 0
            else:
                try: 
                    (Sess_N,Trl_N,TrlTyp,Stim,foo,Class,RspSL,RspAC,RspRT,Reinf,TOD,Date) = line.strip().split('\t')
                except ValueError:
                    print "could not parse line (%s) from %s" % (line,rdat_file)
                else:
                    session_num = int(Sess_N)

                    if session_num > last_session:
                        session_name = ','.join([subject.name,file_origin,start_time,Sess_N])
                        session, created = Session.objects.get_or_create(name=session_name,
                                                                  index=session_num,
                                                                  file_origin=file_origin,
                                                                  protocol=protocol,
                                                                  subject=subject,
                                                                  annotations={'Stimulus source': stim_source,
                                                                               'Start time': start_time,
                                                                               }
                                                                  )

                        block, created = Block.objects.get_or_create(name=session_name,
                                                                     file_origin=file_origin)
                        last_session = session_num

                    trial_num = int(Trl_N)
                    segment, created = Segment.objects.get_or_create(block=block,
                                                                     rec_datetime=time_of_trial(TOD,Date,start_time),
                                                                     index=trial_num,
                                                                     )
                    trial_type, created = TrialType.objects.get_or_create(name=TRIAL_TYPES[TrlTyp])
                    trial_class, created = TrialClass.objects.get_or_create(name=TRIAL_CLASS[protocol.type.name][Class])
                    trial_response, created = TrialClass.objects.get_or_create(name=TRIAL_RESPONSE[protocol.type.name][RspSL])

                    trial, created = Trial.objects.get_or_create(index=trial_num,
                    # trial= Trial(index=trial_num,
                                                                 tr_type=trial_type,
                                                                 tr_class=trial_class,
                                                                 stimulus=Stim,
                                                                 response=trial_response,
                                                                 correct=BOOL[RspAC],
                                                                 reaction_time=float(RspRT),
                                                                 reinforced=BOOL[Reinf],
                                                                 session=session,
                                                                 segment=segment,
                                                                 time=0.0,
                                                                 )
    return True


class Command(BaseCommand):
    args = '<rdat_files>'
    help = "imports an rdat file"
    can_import_settings = True

    def handle(self, *args, **options):
        for filename in args:
            if 'rDAT' in filename:
                import_rDAT(filename)
            else:
                raise CommandError('not an rDAT file')

