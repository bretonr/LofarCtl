##### ##### #####
##### This file contains some important telescope configuration
##### ##### #####


##### Calibrator data
calibrator_data = """
3c48       01:37:41.3    +33:09:35      J2000.0
3c147      05:42:36.1    +49:51:07      J2000.0
3c196      08:13:36.0    +48:13:03      J2000.0
3c286      13:31:08.3    +30:30:33      J2000.0
3c287      13:30:37.7    +25:09:11      J2000.0
3c295      14:11:20.5    +52:12:10      J2000.0
3c380      18:29:31.8    +48:44:46      J2000.0
"""


##### Implemented antenna set configuration
antennaset = ["HBA_JOINED",
    "HBA_DUAL",
    "LBA_INNER"]


##### Implemented RCU modes
rcumode = [0,
    1,
    2,
    3,
    4,
    5,
    6,
    7]


##### Implemented coordinate systems
coordsys = ["AZELGEO",
    "J2000"]


##### Providing the default directory to write logs
log_directory = os.environ["HOME"]+"/LofarCtl_logs/"


