import math
import random
import sys
import importlib
#========================change variables here to modify scenario========================
path_to_folder = "C:\\Users\\LJMU\\Documents\\Felix\\OpenMATB_ScenarioCreator"
path_to_folder = "C:\\Users\\felix\\Desktop\\LJMU\\Scripts\\Python\\OpenMATB_ScenarioCreator"


#define MATB length
total_mins = 3
total_secs = total_mins * 60
buffer = 15 #seconds at the start and end where no events will be placed (safety measure for communication prompts and possibly unfair scale failures towards the end)

#import difficulty configuration
try:
    print ("Number of arguments: ", len(sys.argv))
    print ("The arguments are: " , str(sys.argv))
    cfg_file = sys.argv[1]
    diff = sys.argv[2]
    n_scenarios = sys.argv[3]
    mod = importlib.import_module(cfg_file)
    config = []
    if diff == 'easy':
        config = mod.easy
    if diff == 'medium':
        config = mod.medium
    if diff == 'hard':
        config = mod.hard
    if sys.argv[2] not in ['easy', 'medium' ,'hard']:
        raise
except Exception as exception: 
    print("---You need to pass three arguments: /config file name/ /difficulty (easy, medium or hard)/ /number of scenarios to generate/---")
    raise


#====================================Creating scenario========================================
#---define naming constants 

TIMEPOINTS = list(range(0,total_secs))
S_SYSMON = 'sysmon'
S_RESMAN = 'resman'
S_TRACK = 'track'
S_COMM = 'communications'
SYSTEMS = [S_SYSMON, S_RESMAN, S_TRACK, S_COMM]
PARAMETERS ={#needs more parameters:
    'target'    : 'tank-{}-target',
    'loss'      : 'lossperminute',
    'update'    : 'taskupdatetime',
    'alert'     : 'alerttimeout',
    'radius'    : 'targetradius',
    's-failure' : 'scales-{}-failure',
    'p-failure' : 'pump-{}-state',
    'prompt'    : 'radioprompt'
}

#define which pump and scales will be involved
PUMPS = config['pumpsToFail']
SCALES = config['scalesToFail']


#define frequency of events:
N_EVENTS = {
    's-failure' : config['scaleFailN'], #number of scale failures
    'p-failure' : config['pumpFailN'],  #number of pump failures
    'prompt'    : config['promptN'],    #number of prompts (whether own or other is 50/50)
}

#---define helper function:

#function that processes different paramater types (pumps need extra information for example))
def write_param(parameter,extra = 0, P=PARAMETERS):
    if extra == 0:
        return P[parameter]
    return P[parameter].format(extra)

#function that prints the time at the start of each line
def write_time(secs):
    str_hours = '0'
    str_minutes = '00'
    minutes = secs /60
    seconds = secs - (math.floor(minutes) * 60)
    if minutes >= 1:
        str_minutes = "0{}".format(math.floor(minutes))
    if seconds >= 10:
        str_seconds = "{}".format(seconds)
    else:
        str_seconds = "0{}".format(seconds)
    return "{}:{}:{}".format(str_hours,str_minutes,str_seconds)

#function that could write start and end commands..not in use at the moment
def make_command(time_t,system,command):
    return "{time_t};{system};{command}".format(time_t = time_t, system = system, command = command)

#function that prints parameter lines
def make_param(time_t, system, parameter, value):
    return "{time_t};{system};{parameter};{value}".format(time_t = time_t, system = system, parameter = parameter, value = value)

#function that makes sure spacings between events are as defined by the safezone variable (seconds around a certain event onset)
def removeFromTime(timePoints, timePoint, timePoint_idx, safeZone, previousEventTimes):
    for i in range(0,len(previousEventTimes)): # loop over events that were created so far
        x_before = set(range(previousEventTimes[i] - safeZone,previousEventTimes[i])) #These are sets of seconds that events last, with the intersection function we can check if they overlap
        x_after = set(range(previousEventTimes[i],previousEventTimes[i] + safeZone))
        y_before = set(range(timePoint - safeZone, timePoint))
        y_after = set(range(timePoint, timePoint + safeZone))
        if len(x_before.intersection(y_after) ) > 0: #Case 1 new event intersects with with safezone before previous event
            if len(x_before.intersection(y_after)) == safeZone:
                return timePoints[0:timePoint_idx - safeZone] + timePoints[timePoint_idx : -1]
            else:
                return timePoints[0:timePoint_idx - safeZone] + timePoints[timePoint_idx + len(x_before.intersection(y_after)) : -1]
        if len(x_after.intersection(y_before) ) > 0: #Case 2 new event intersects with with safezone after previous event
            if len(x_after.intersection(y_before)) == safeZone:
                return timePoints[0:timePoint_idx] + timePoints[timePoint_idx + safeZone : -1]
            else:
                return timePoints[0:timePoint_idx - len(x_after.intersection(y_before))] + timePoints[timePoint_idx  : -1]

    return timePoints[0:timePoint_idx - safeZone] + timePoints[timePoint_idx + safeZone : -1] # Case 3 new event does not overlap with previous events

#----Start defining variables to be written into the scenario file

#Start lines with modified starting values given by the chosen difficulty configuration
START_LINES = [
    "0:00:00;sysmon;scalestyle;2",
    "0:00:00;sysmon;feedbacks-positive-color;#00ff00",
    "0:00:00;sysmon;feedbacks-negative-color;#ff0000",
    "0:00:00;sysmon;alerttimeout;4000",
    "0:00:00;sysmon;safezonelength;{}".format(config['sysSafe']),
    "0:00:00;resman;tank-a-target;2000",
    "0:00:00;resman;tank-a-lossperminute;{}".format(config['lossA']),
    "0:00:00;resman;tank-b-target;1000",
    "0:00:00;resman;tank-b-lossperminute;{}".format(config['lossB']),
    "0:00:00;resman;taskupdatetime;200",
    "0:00:00;resman;tolerancelevel;{}".format(config['tankTolerance']),
    "0:00:00;track;cursorcolor;#009900",
    "0:00:00;track;targetradius;{}".format(config['trackingRad']),
    "0:00:00;communications;callsignregex;[A-Z][A-Z]\d\d",
    "0:00:00;communications;othercallsignnumber;5",
    "0:00:00;communications;voicegender;male",
    "0:00:00;communications;voiceidiom;english",
    "0:00:00;labstreaminglayer;start",
    "0:00:00;pumpstatus;start",
    "0:00:00;resman;start",
    "0:00:00;track;start",
    "0:00:00;sysmon;start",
    "0:00:00;communications;start",
    "0:00:00;scheduling;start",
    "0:00:00;participantinfo;start",
    "0:00:00;track;automaticsolver;False"
]

#define flow rates of the different pumps 
FLOW_LINES = []
for i in range(0,len(PUMPS)):
    p = PUMPS[i]
    if p < 7:
        FLOW_LINES.append("0:00:00;resman;pump-{}-flow;{}".format(p,config['flowStd']))
    else:
        FLOW_LINES.append("0:00:00;resman;pump-{}-flow;{}".format(p,config['flowBetween']))

#End lines with the correct end times
END_LINES = [
    "{};pumpstatus;stop".format(write_time(total_secs)),
    "{};resman;stop".format(write_time(total_secs)),
    "{};track;stop".format(write_time(total_secs)),
    "{};sysmon;stop".format(write_time(total_secs)),
    "{};communications;stop".format(write_time(total_secs)),
    "{};scheduling;stop".format(write_time(total_secs)),
    "{};labstreaminglayer;stop".format(write_time(total_secs)),
    "{};end".format(write_time(total_secs + 1)),
]
for n_scenario in range(1,int(n_scenarios)+1):
    #define all events
    event_lines = []
    safe_zone = config['safeZone']
    prompt_safe_zone = 20
    promptTime = TIMEPOINTS
    promptEvents = []
    for n in range(1,N_EVENTS['prompt']):
        timepoint_idx =  random.sample(range(buffer,len(promptTime) -buffer),1)[0]
        timepoint = promptTime[timepoint_idx]
        tmp_target = random.choices(["own", "other"], weights = [3,1],k = 1)[0]
        promptTime = removeFromTime(promptTime, timepoint, timepoint_idx, prompt_safe_zone, promptEvents)
        promptEvents.append(timepoint)
        event_lines.append(make_param(write_time(timepoint), S_COMM, PARAMETERS['prompt'],tmp_target))

    scaleTime = TIMEPOINTS
    scaleEvents = []
    for n in range(1,N_EVENTS['s-failure']):
        timepoint_idx =  random.sample(range(buffer,len(scaleTime) -buffer),1)[0]
        timepoint = scaleTime[timepoint_idx]
        tmp_scale =  random.sample(SCALES,1)[0]
        tmp_dir = random.sample(["up", "down"],1)[0]
        scaleTime = removeFromTime(scaleTime, timepoint, timepoint_idx, safe_zone, scaleEvents)
        scaleEvents.append(timepoint)
        event_lines.append(make_param(write_time(timepoint), S_SYSMON, PARAMETERS['s-failure'].format(tmp_scale),tmp_dir))

    pumpTime = TIMEPOINTS
    pumpEvents = []
    for n in range(1,N_EVENTS['p-failure']):
        timepoint_idx =  random.sample(range(buffer,len(pumpTime) -buffer),1)[0]
        timepoint = pumpTime[timepoint_idx]
        tmp_pump =  random.sample(PUMPS,1)[0]
        pumpTime = removeFromTime(pumpTime, timepoint, timepoint_idx, safe_zone, pumpEvents)
        pumpEvents.append(timepoint)
        event_lines.append(make_param(write_time(timepoint), S_RESMAN, PARAMETERS['p-failure'].format(tmp_pump),-1))
        event_lines.append(make_param(write_time(timepoint +10), S_RESMAN, PARAMETERS['p-failure'].format(tmp_pump),0))


    contents = START_LINES + FLOW_LINES + event_lines + END_LINES
    contents = [line + "\n" for line in contents]
    out_filename = "{cfg_file}_{diff}_{n}.txt".format(cfg_file = cfg_file, diff = diff, n = n_scenario)
    print(path_to_folder + "\\Scenarios\\" + out_filename,"w")
    file = open(path_to_folder + "\\Scenarios\\" + out_filename,"w")
    file.writelines(contents)
    file.close()