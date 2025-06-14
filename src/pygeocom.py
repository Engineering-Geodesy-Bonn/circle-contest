from typing import Tuple, Any, Callable
from enum import Enum, IntFlag
from datetime import datetime
from collections import namedtuple
from time import time

GRC_TPS = 0x0000  # main return codes (identical to RC_SUP!!)
GRC_SUP = 0x0000  # supervisor task (identical to RCBETA!!)
GRC_ANG = 0x0100  # angle- and inclination
GRC_ATA = 0x0200  # automatic target acquisition
GRC_EDM = 0x0300  # electronic distance meter
GRC_GMF = 0x0400  # geodesy mathematics & formulas
GRC_TMC = 0x0500  # measurement & calc
GRC_MEM = 0x0600  # memory management
GRC_MOT = 0x0700  # motorization
GRC_LDR = 0x0800  # program loader
GRC_BMM = 0x0900  # basics of man machine interface
GRC_TXT = 0x0A00  # text management
GRC_MMI = 0x0B00  # man machine interface
GRC_COM = 0x0C00  # communication
GRC_DBM = 0x0D00  # data base management
GRC_DEL = 0x0E00  # dynamic event logging
GRC_FIL = 0x0F00  # file system
GRC_CSV = 0x1000  # central services
GRC_CTL = 0x1100  # controlling task
GRC_STP = 0x1200  # start + stop task
GRC_DPL = 0x1300  # data pool
GRC_WIR = 0x1400  # wi registration
GRC_USR = 0x2000  # user task
GRC_ALT = 0x2100  # alternate user task
GRC_AUT = 0x2200  # automatization
GRC_AUS = 0x2300  # alternative user
GRC_BAP = 0x2400  # basic applications
GRC_SAP = 0x2500  # system applications
GRC_COD = 0x2600  # standard code function
GRC_BAS = 0x2700  # GeoBasic interpreter
GRC_IOS = 0x2800  # Input-/ output- system
GRC_CNF = 0x2900  # configuration facilities
GRC_XIT = 0x2E00  # XIT subsystem (Excite-Level LIS)
GRC_DNA = 0x2F00  # DNA2 subsystem
GRC_ICD = 0x3000  # cal data management
GRC_KDM = 0x3100  # keyboard display module
GRC_LOD = 0x3200  # firmware loader
GRC_FTR = 0x3300  # file transfer
GRC_VNF = 0x3F00  # reserved for new TPS1200 subsystem
GRC_GPS = 0x4000  # GPS subsystem
GRC_TST = 0x4100  # Test subsystem
GRC_PTF = 0x4F00  # reserved for new GPS1200 subsystem
GRC_APP = 0x5000  # offset for all applications
GRC_RES = 0x7000  # reserved code range


class ReturnCode(Enum):
    GRC_OK = GRC_TPS + 0  # Function successfully completed.
    GRC_UNDEFINED = GRC_TPS + 1  # Unknown error result unspecified.
    GRC_IVPARAM = GRC_TPS + 2  # Invalid parameter detected.\nResult unspecified.
    GRC_IVRESULT = GRC_TPS + 3  # Invalid result.
    GRC_FATAL = GRC_TPS + 4  # Fatal error.
    GRC_NOT_IMPL = GRC_TPS + 5  # Not implemented yet.
    GRC_TIME_OUT = GRC_TPS + 6  # Function execution timed out.\nResult unspecified.
    GRC_SET_INCOMPL = GRC_TPS + 7  # Parameter setup for subsystem is incomplete.
    GRC_ABORT = GRC_TPS + 8  # Function execution has been aborted.
    GRC_NOMEMORY = GRC_TPS + 9  # Fatal error - not enough memory.
    GRC_NOTINIT = GRC_TPS + 10  # Fatal error - subsystem not initialized.
    GRC_SHUT_DOWN = GRC_TPS + 12  # Subsystem is down.
    GRC_SYSBUSY = (
        GRC_TPS + 13
    )  # System busy/already in use of another process.\nCannot execute function.
    GRC_HWFAILURE = GRC_TPS + 14  # Fatal error - hardware failure.
    GRC_ABORT_APPL = (
        GRC_TPS + 15
    )  # Execution of application has been aborted (SHIFT-ESC).
    GRC_LOW_POWER = GRC_TPS + 16  # Operation aborted - insufficient power supply level.
    GRC_IVVERSION = GRC_TPS + 17  # Invalid version of file ...
    GRC_BATT_EMPTY = GRC_TPS + 18  # Battery empty
    GRC_NO_EVENT = GRC_TPS + 20  # no event pending.
    GRC_OUT_OF_TEMP = GRC_TPS + 21  # out of temperature range
    GRC_INSTRUMENT_TILT = GRC_TPS + 22  # intrument tilting out of range
    GRC_COM_SETTING = GRC_TPS + 23  # communication error
    GRC_NO_ACTION = GRC_TPS + 24  # GRC_TYPE Input 'do no action'
    GRC_SLEEP_MODE = GRC_TPS + 25  # Instr. run into the sleep mode
    GRC_NOTOK = GRC_TPS + 26  # Function not successfully completed.
    GRC_NA = GRC_TPS + 27  # Not available
    GRC_OVERFLOW = GRC_TPS + 28  # Overflow error
    GRC_STOPPED = GRC_TPS + 29  # System or subsystem has been stopped

    GRC_COM_ERO = GRC_COM + 0  #  Initiate Extended Runtime Operation (ERO).
    GRC_COM_CANT_ENCODE = GRC_COM + 1  #  Cannot encode arguments in client.
    GRC_COM_CANT_DECODE = GRC_COM + 2  #  Cannot decode results in client.
    GRC_COM_CANT_SEND = GRC_COM + 3  #  Hardware error while sending.
    GRC_COM_CANT_RECV = GRC_COM + 4  #  Hardware error while receiving.
    GRC_COM_TIMEDOUT = GRC_COM + 5  #  Request timed out.
    GRC_COM_WRONG_FORMAT = GRC_COM + 6  #  Packet format error.
    GRC_COM_VER_MISMATCH = GRC_COM + 7  #  Version mismatch between client and server.
    GRC_COM_CANT_DECODE_REQ = GRC_COM + 8  #  Cannot decode arguments in server.
    GRC_COM_PROC_UNAVAIL = GRC_COM + 9  #  Unknown RPC, procedure ID invalid.
    GRC_COM_CANT_ENCODE_REP = GRC_COM + 10  #  Cannot encode results in server.
    GRC_COM_SYSTEM_ERR = GRC_COM + 11  #  Unspecified generic system error.
    GRC_COM_UNKNOWN_HOST = GRC_COM + 12  #  (Unused error code)
    GRC_COM_FAILED = GRC_COM + 13  #  Unspecified error.
    GRC_COM_NO_BINARY = GRC_COM + 14  #  Binary protocol not available.
    GRC_COM_INTR = GRC_COM + 15  #  Call interrupted.
    GRC_COM_UNKNOWN_ADDR = GRC_COM + 16  #  (Unused error code)
    GRC_COM_NO_BROADCAST = GRC_COM + 17  #  (Unused error code)
    GRC_COM_REQUIRES_8DBITS = GRC_COM + 18  #  Protocol needs 8bit encoded chararacters.
    GRC_COM_UD_ERROR = GRC_COM + 19  #  (Unused error code)
    GRC_COM_LOST_REQ = GRC_COM + 20  #  (Unused error code)
    GRC_COM_TR_ID_MISMATCH = GRC_COM + 21  #  Transacation ID mismatch error.
    GRC_COM_NOT_GEOCOM = GRC_COM + 22  #  Protocol not recognizeable.
    GRC_COM_UNKNOWN_PORT = GRC_COM + 23  #  (WIN) Invalid port address.
    GRC_COM_ILLEGAL_TRPT_SELECTOR = GRC_COM + 24  #  (Unused error code)
    GRC_COM_TRPT_SELECTOR_IN_USE = GRC_COM + 25  #  (Unused error code)
    GRC_COM_INACTIVE_TRPT_SELECTOR = GRC_COM + 26  #  (Unused error code)
    GRC_COM_ERO_END = GRC_COM + 27  #  ERO is terminating.
    GRC_COM_OVERRUN = GRC_COM + 28  #  Internal error: data buffer overflow.
    GRC_COM_SRVR_RX_CHECKSUM_ERROR = (
        GRC_COM + 29
    )  #  Invalid checksum on server side received.
    GRC_COM_CLNT_RX_CHECKSUM_ERROR = (
        GRC_COM + 30
    )  #  Invalid checksum on client side received.
    GRC_COM_PORT_NOT_AVAILABLE = GRC_COM + 31  #  (WIN) Port not available.
    GRC_COM_PORT_NOT_OPEN = GRC_COM + 32  #  (WIN) Port not opened.
    GRC_COM_NO_PARTNER = GRC_COM + 33  #  (WIN) Unable to find TPS.
    GRC_COM_ERO_NOT_STARTED = (
        GRC_COM + 34
    )  #  Extended Runtime Operation could not be started.
    GRC_COM_CONS_REQ = GRC_COM + 35  #  Att to send cons reqs
    GRC_COM_SRVR_IS_SLEEPING = (
        GRC_COM + 36
    )  #  TPS has gone to sleep. Wait and try again.
    GRC_COM_SRVR_IS_OFF = GRC_COM + 37  #  TPS has shut down. Wait and try again.

    GRC_EDM_SYSTEM_ERR = (
        GRC_EDM + 1
    )  # Fatal EDM sensor error. See for the exact reason the original EDM sensor error number. In the most cases a service problem.
    # Sensor user errors
    GRC_EDM_INVALID_COMMAND = (
        GRC_EDM + 2
    )  # Invalid command or unknown command, see command syntax.
    GRC_EDM_BOOM_ERR = GRC_EDM + 3  # Boomerang error.
    GRC_EDM_SIGN_LOW_ERR = (
        GRC_EDM + 4
    )  # Received signal to low, prisma to far away, or natural barrier, bad environment, etc.
    GRC_EDM_DIL_ERR = GRC_EDM + 5  # Obsolete
    GRC_EDM_SIGN_HIGH_ERR = (
        GRC_EDM + 6
    )  # Received signal to strong, prism too near, stranger light effect.
    # New TPS1200 sensor user errors
    GRC_EDM_TIMEOUT = (
        GRC_EDM + 7
    )  # Timeout, measuring time exceeded (signal too weak, beam interrupted,..)
    GRC_EDM_FLUKT_ERR = GRC_EDM + 8  # Too much turbulences or distractions
    GRC_EDM_FMOT_ERR = GRC_EDM + 9  # Filter motor defective

    # Subsystem errors
    GRC_EDM_DEV_NOT_INSTALLED = GRC_EDM + 10  # Device like EGL, DL is not installed.
    GRC_EDM_NOT_FOUND = (
        GRC_EDM + 11
    )  # Search result invalid. For the exact explanation \nsee in the description of the called function.
    GRC_EDM_ERROR_RECEIVED = (
        GRC_EDM + 12
    )  # Communication ok, but an error\nreported from the EDM sensor.
    GRC_EDM_MISSING_SRVPWD = GRC_EDM + 13  # No service password is set.
    GRC_EDM_INVALID_ANSWER = (
        GRC_EDM + 14
    )  # Communication ok, but an unexpected\nanswer received.
    GRC_EDM_SEND_ERR = GRC_EDM + 15  # Data send error, sending buffer is full.
    GRC_EDM_RECEIVE_ERR = (
        GRC_EDM + 16
    )  # Data receive error, like\nparity buffer overflow.
    GRC_EDM_INTERNAL_ERR = GRC_EDM + 17  # Internal EDM subsystem error.
    GRC_EDM_BUSY = (
        GRC_EDM + 18
    )  # Sensor is working already,\nabort current measuring first.
    GRC_EDM_NO_MEASACTIVITY = GRC_EDM + 19  # No measurement activity started.
    GRC_EDM_CHKSUM_ERR = (
        GRC_EDM + 20
    )  # Calculated checksum, resp. received data wrong\n(only in binary communication mode possible).
    GRC_EDM_INIT_OR_STOP_ERR = (
        GRC_EDM + 21
    )  # During start up or shut down phase an\nerror occured. It is saved in the DEL buffer.
    GRC_EDM_SRL_NOT_AVAILABLE = (
        GRC_EDM + 22
    )  # Red laser not available on this sensor HW.
    GRC_EDM_MEAS_ABORTED = (
        GRC_EDM + 23
    )  # Measurement will be aborted (will be used for the lasersecurity)

    # New TPS1200 sensor user error
    GRC_EDM_SLDR_TRANSFER_PENDING = GRC_EDM + 30  # Multiple OpenTransfer calls.
    GRC_EDM_SLDR_TRANSFER_ILLEGAL = GRC_EDM + 31  # No opentransfer happened.
    GRC_EDM_SLDR_DATA_ERROR = GRC_EDM + 32  # Unexpected data format received.
    GRC_EDM_SLDR_CHK_SUM_ERROR = GRC_EDM + 33  # Checksum error in transmitted data.
    GRC_EDM_SLDR_ADDR_ERROR = GRC_EDM + 34  # Address out of valid range.
    GRC_EDM_SLDR_INV_LOADFILE = GRC_EDM + 35  # Firmware file has invalid format.
    GRC_EDM_SLDR_UNSUPPORTED = (
        GRC_EDM + 36
    )  # Current (loaded) firmware doesn't support upload.
    GRC_EDM_UNKNOW_ERR = (
        GRC_EDM + 40
    )  # Undocumented error from the\nEDM sensor, should not occur.

    GRC_EDM_DISTRANGE_ERR = (
        GRC_EDM + 50
    )  # Out of distance range (dist too small or large)
    GRC_EDM_SIGNTONOISE_ERR = GRC_EDM + 51  # Signal to noise ratio too small
    GRC_EDM_NOISEHIGH_ERR = GRC_EDM + 52  # Noise to high
    GRC_EDM_PWD_NOTSET = GRC_EDM + 53  # Password is not set
    GRC_EDM_ACTION_NO_MORE_VALID = (
        GRC_EDM + 54
    )  # Elapsed time between prepare und start fast measurement for ATR to long
    GRC_EDM_MULTRG_ERR = (
        GRC_EDM + 55
    )  # Possibly more than one target (also a sensor error)

    GRC_MOT_UNREADY = GRC_MOT + 0  # motorization is not ready (1792)
    GRC_MOT_BUSY = GRC_MOT + 1  # motorization is handling another task (1793)
    GRC_MOT_NOT_OCONST = GRC_MOT + 2  # motorization is not in velocity mode (1794)
    GRC_MOT_NOT_CONFIG = GRC_MOT + 3  # motorization is in the wrong mode or busy (1795)
    GRC_MOT_NOT_POSIT = GRC_MOT + 4  # motorization is not in posit mode (1796)
    GRC_MOT_NOT_SERVICE = GRC_MOT + 5  # motorization is not in service mode (1797)
    GRC_MOT_NOT_BUSY = GRC_MOT + 6  # motorization is handling no task (1798)
    GRC_MOT_NOT_LOCK = GRC_MOT + 7  # motorization is not in tracking mode (1799)
    GRC_MOT_NOT_SPIRAL = GRC_MOT + 8  # motorization is not in spiral mode (1800)

    GRC_TMC_NO_FULL_CORRECTION = (
        GRC_TMC + 3
    )  # Warning: measurment without full correction
    GRC_TMC_ACCURACY_GUARANTEE = GRC_TMC + 4  # Info   : accuracy can not be guarantee

    GRC_TMC_ANGLE_OK = GRC_TMC + 5  # Warning: only angle measurement valid
    GRC_TMC_ANGLE_NOT_FULL_CORR = (
        GRC_TMC + 8
    )  # Warning: only angle measurement valid but without full correction
    GRC_TMC_ANGLE_NO_ACC_GUARANTY = (
        GRC_TMC + 9
    )  # Info   : only angle measurement valid but accuracy can not be guarantee

    GRC_TMC_ANGLE_ERROR = GRC_TMC + 10  # Error  : no angle measurement

    GRC_TMC_DIST_PPM = GRC_TMC + 11  # Error  : wrong setting of PPM or MM on EDM
    GRC_TMC_DIST_ERROR = (
        GRC_TMC + 12
    )  # Error  : distance measurement not done (no aim, etc.)
    GRC_TMC_BUSY = GRC_TMC + 13  # Error  : system is busy (no measurement done)
    GRC_TMC_SIGNAL_ERROR = (
        GRC_TMC + 14
    )  # Error  : no signal on EDM (only in signal mode)

    GRC_BMM_XFER_PENDING = GRC_BMM + 1  # Loading process already opened
    GRC_BMM_NO_XFER_OPEN = GRC_BMM + 2  # Transfer not opened
    GRC_BMM_UNKNOWN_CHARSET = GRC_BMM + 3  # Unknown character set
    GRC_BMM_NOT_INSTALLED = GRC_BMM + 4  # Display module not present
    GRC_BMM_ALREADY_EXIST = GRC_BMM + 5  # Character set already exists
    GRC_BMM_CANT_DELETE = GRC_BMM + 6  # Character set cannot be deleted
    GRC_BMM_MEM_ERROR = GRC_BMM + 7  # Memory cannot be allocated
    GRC_BMM_CHARSET_USED = GRC_BMM + 8  # Character set still used
    GRC_BMM_CHARSET_SAVED = GRC_BMM + 9  # Charset cannot be deleted or is protected
    GRC_BMM_INVALID_ADR = (
        GRC_BMM + 10
    )  # Attempt to copy a character block\noutside the allocated memory
    GRC_BMM_CANCELANDADR_ERROR = (
        GRC_BMM + 11
    )  # Error during release of allocated memory
    GRC_BMM_INVALID_SIZE = (
        GRC_BMM + 12
    )  # Number of bytes specified in header\ndoes not match the bytes read
    GRC_BMM_CANCELANDINVSIZE_ERROR = (
        GRC_BMM + 13
    )  # Allocated memory could not be released
    GRC_BMM_ALL_GROUP_OCC = GRC_BMM + 14  # Max. number of character sets already loaded
    GRC_BMM_CANT_DEL_LAYERS = GRC_BMM + 15  # Layer cannot be deleted
    GRC_BMM_UNKNOWN_LAYER = GRC_BMM + 16  # Required layer does not exist
    GRC_BMM_INVALID_LAYERLEN = GRC_BMM + 17  # Layer length exceeds maximum

    AUT_RC_TIMEOUT = GRC_AUT  # Timeout, no target found
    AUT_RC_DETENT_ERROR = GRC_AUT + 1  #
    AUT_RC_ANGLE_ERROR = GRC_AUT + 2  #
    AUT_RC_MOTOR_ERROR = GRC_AUT + 3  # Motorisation error
    AUT_RC_INCACC = GRC_AUT + 4  #
    AUT_RC_DEV_ERROR = GRC_AUT + 5  # Deviation measurement error
    AUT_RC_NO_TARGET = GRC_AUT + 6  # No target detected
    AUT_RC_MULTIPLE_TARGETS = GRC_AUT + 7  # Multiple targets detected
    AUT_RC_BAD_ENVIRONMENT = GRC_AUT + 8  # Bad environment conditions
    AUT_RC_DETECTOR_ERROR = GRC_AUT + 9  #
    AUT_RC_NOT_ENABLED = GRC_AUT + 10  #
    AUT_RC_CALACC = GRC_AUT + 11  #
    AUT_RC_ACCURACY = GRC_AUT + 12  # Position not exactly reached


class byte(int):
    def __new__(cls, value, *args, **kwargs):
        if type(value) == str:
            value = int(value.strip("'"), 16)
        elif type(value) == bytes:
            value = int(value.strip(b"'"), 16)

        if value < 0:
            raise ValueError("byte types must not be less than zero")
        if value > 255:
            raise ValueError("byte types must not be more than 255 (0xff)")

        return super(cls, cls).__new__(cls, value)


class PrismType(Enum):
    LEICA_ROUND = 0  # Prism type: Leica circular prism
    LEICA_MINI = 1  # Prism type: Leica mini prism
    LEICA_TAPE = 2  # Prism type: Leica reflective tape
    LEICA_360 = 3  # Prism type: Leica 360° prism
    USER1 = 4  # Prism type: User defined 1
    USER2 = 5  # Prism type: User defined 2
    USER3 = 6  # Prism type: User defined 3
    LEICA_360_MINI = 7  # Prism type: Leica 360° mini
    LEICA_MINI_ZERO = 8  # Prism type: Leica mini zero
    LEICA_USER = 9  # Prism type: user???
    LEICA_HDS_TAPE = 10  # Prism type: tape cyra???
    LEICA_GRZ121_ROUND = 11  # Prism type: Leica GRZ121 round for machine guidance


class ReflectorType(Enum):
    UNDEFINED = 0
    PRISM = 1
    TAPE = 2


class TargetType(Enum):
    REFLECTOR = 0
    REFLECTORLESS = 1


class InclinationSensorProgram(Enum):
    TMC_MEA_INC = 0  # Use sensor (apriori sigma)
    TMC_AUTO_INC = 1  # Automatic mode (sensor/plane)
    TMC_PLANE_INC = 2  # Use plane (apriori sigma)


class EDMMode(Enum):
    EDM_MODE_NOT_USED = 0  # Init value
    EDM_SINGLE_TAPE = 1  # Single measurement with tape
    EDM_SINGLE_STANDARD = 2  # Standard single measurement
    EDM_SINGLE_FAST = 3  # Fast single measurement
    EDM_SINGLE_LRANGE = 4  # Long range single measurement
    EDM_SINGLE_SRANGE = 5  # Short range single measurement
    EDM_CONT_STANDARD = 6  # Standard repeated measurement
    EDM_CONT_DYNAMIC = 7  # Dynamic repeated measurement
    EDM_CONT_REFLESS = 8  # Reflectorless repeated measurement
    EDM_CONT_FAST = 9  # Fast repeated measurement
    EDM_AVERAGE_IR = 10  # Standard average measurement
    EDM_AVERAGE_SR = 11  # Short range average measurement
    EDM_AVERAGE_LR = 12  # Long range average measurement


class DeviceClass(Enum):
    # TPS1000 Family        ------------------------ accuracy
    TPS_CLASS_1100 = 0  # TPS1000 family member, 1 mgon,   3"
    TPS_CLASS_1700 = 1  # TPS1000 family member, 0.5 mgon, 1.5"
    TPS_CLASS_1800 = 2  # TPS1000 family member, 0.3 mgon, 1"
    TPS_CLASS_5000 = 3  # TPS2000 family member
    TPS_CLASS_6000 = 4  # TPS2000 family member
    TPS_CLASS_1500 = 5  # TPS1000 family member
    TPS_CLASS_2003 = 6  # TPS2000 family member
    TPS_CLASS_5005 = 7  # TPS5000      "
    TPS_CLASS_5100 = 8  # TPS5000      "

    # TPS1100 Family        ------------------------ accuracy
    TPS_CLASS_1102 = 100  # TPS1000 family member, 2"
    TPS_CLASS_1103 = 101  # TPS1000 family member, 3"
    TPS_CLASS_1105 = 102  # TPS1000 family member, 5"
    TPS_CLASS_1101 = 103  # TPS1000 family member, 1."

    # TPS1200 Family        ------------------------ accuracy
    TPS_CLASS_1202 = 200  # TPS1200 family member, 2"
    TPS_CLASS_1203 = 201  # TPS1200 family member, 3"
    TPS_CLASS_1205 = 202  # TPS1200 family member, 5"
    TPS_CLASS_1201 = 203  # TPS1200 family member, 1"


class DeviceType(IntFlag):
    # TPS1x00 common
    TPS_DEVICE_T = 0x00000  # Theodolite without built-in EDM
    TPS_DEVICE_MOT = 0x00004  # Motorized device
    TPS_DEVICE_ATR = 0x00008  # Automatic Target Recognition
    TPS_DEVICE_EGL = 0x00010  # Electronic Guide Light
    TPS_DEVICE_DB = 0x00020  # reserved (Database, not GSI)
    TPS_DEVICE_DL = 0x00040  # Diode laser
    TPS_DEVICE_LP = 0x00080  # Laser plumbed

    # TPS1000 specific
    TPS_DEVICE_TC1 = 0x00001  # tachymeter (TCW1)
    TPS_DEVICE_TC2 = 0x00002  # tachymeter (TCW2)

    # TPS1100/TPS1200 specific
    TPS_DEVICE_TC = 0x00001  # tachymeter (TCW3)
    TPS_DEVICE_TCR = 0x00002  # tachymeter (TCW3 with red laser)
    TPS_DEVICE_ATC = 0x00100  # Autocollimation lamp (used only PMU)
    TPS_DEVICE_LPNT = 0x00200  # Laserpointer
    TPS_DEVICE_RL_EXT = (
        0x00400  # Reflectorless EDM with extended range (Pinpoint R100,R300)
    )
    TPS_DEVICE_PS = 0x00800  # Power Search

    # TPSSim specific
    TPS_DEVICE_SIM = 0x04000  # runs on Simulation, no Hardware


class PowerPath(Enum):
    CURRENT_POWER = 0
    EXTERNAL_POWER = 1
    INTERNAL_POWER = 2


class RecordFormat(Enum):
    GSI_8 = 0
    GSI_16 = 1


class TPSStatus(Enum):
    OFF = 0
    SLEEPING = 1
    ONLINE = 2
    LOCAL = 3
    UNKNOWN = 4


class OnOff(Enum):
    OFF = 0
    ON = 1


class BOOLE(Enum):
    TRUE = 1
    FALSE = 0


class lDirection(Enum):
    CLKW = 1
    ACLKW = -1


class EGLIntensity(Enum):
    OFF = 0
    LOW = 1
    MID = 2
    HIGH = 3


class ControllerMode(Enum):
    RELATIVE_POSITIONING = 0
    CONSTANT_SPEED = 1
    MANUAL_POSITIONING = 2
    LOCK_IN = 3
    BRAKE = 4
    TERMINATE = 7


class ControllerStopMode(Enum):
    NORMAL = 0
    SHUTDOWN = 1


class LockInStatus(Enum):
    LOCKED_OUT = 0
    LOCKED_IN = 1
    PREDICTION = 2


class MeasurementMode(Enum):
    NO_MEASUREMENTS = 0  # No measurements, take last one
    NO_DISTANCE = 1  # No distance measurement, angles only
    DEFAULT_DISTANCE = (
        2  # Default distance measurements, pre-defined using MeasurementProgram
    )
    CLEAR_DISTANCE = 5  # Clear distances
    STOP_TRACKING = 6  # Stop tracking laser


class MeasurementProgram(Enum):
    SINGLE_REF_STANDARD = 0  # standard single IR distance with reflector
    SINGLE_REF_FAST = 1  # fast single IR distance with reflector
    SINGLE_REF_VISIBLE = 2  # long range distance with reflector (red laser)
    SINGLE_RLESS_VISIBLE = 3  # single RL distance reflector free (red laser)
    CONT_REF_STANDARD = 4  # tracking IR distance with reflector
    CONT_REF_FAST = 5  # fast tracking IR distance with reflector
    CONT_RLESS_VISIBLE = 6  # fast tracking RL distance reflector free (red)
    AVG_REF_STANDARD = 7  # Average IR distance with reflector
    AVG_REF_VISIBLE = 8  # Average long range dist. with reflector (red)
    AVG_RLESS_VISIBLE = 9  # Average RL distance reflector free (red laser)


class PositionMode(Enum):
    NORMAL = 0
    PRECISE = 1


class FineAdjustPositionMode(Enum):
    NORM = 0  # Angle tolerance
    POINT = 1  # Point tolerance
    DEFINE = (
        2  # System independent positioning tolerance; set wit PyGeoCom.set_tolerance()
    )


class ATRRecognitionMode(Enum):
    POSITION = 0  # Positioning to the horizontal and vertical angle
    TARGET = 1  # Positioning to a target in the environment of the horizontal and vertical angle


class TMCInclinationMode(Enum):
    USE_SENSOR = 0
    AUTOMATIC = 1
    USE_PLANE = 2


class TMCMeasurementMode(Enum):
    STOP = 0  # Stop measurement program
    DEFAULT_DISTANCE = 1  # Default DIST-measurement program
    DISTANCE_TRACKING = 2  # Distance-TRK measurement program
    STOP_AND_CLEAR = 3  # TMC_STOP and clear data
    SIGNAL = 4  # Signal measurement (test function)
    RESTART = 6  # (Re)start measurement task
    DISTANCE_RAPID_TRACKING = 8  # Distance-TRK measurement program
    RED_LASER_TRACKING = 10  # Red laser tracking
    TESTING_FREQUENCY = 11  # Frequency measurement (test)


class EDMMeasurementMode(Enum):
    MODE_NOT_USER = 0
    SINGLE_TAPE = 1
    SINGLE_STANDARD = 2
    SINGLE_FAST = 3
    SINGLE_LRANGE = 4
    SINGLE_SRANGE = 5
    CONTINUOUS_STANDARD = 6
    CONTINUOUS_DYNAMIC = 7
    CONTINUOUS_REFLECTORLESS = 8
    CONTINUOUS_FAST = 9
    AVERAGE_IR = 10
    AVERAGE_SR = 11
    AVERAGE_LR = 12


class FacePosition(Enum):
    NORMAL = 0
    TURNED = 1


class ActualFace(Enum):
    FACE_1 = 0
    FACE_2 = 1


Coordinate = namedtuple("Coordinate", "east north height")
Angles = namedtuple("Angles", "hz, v")


def decode_string(data: bytes) -> str:
    return data.decode("unicode_escape").strip('"')


def default_return_code_handler(return_code: int):
    if return_code != ReturnCode.GRC_OK:
        raise Exception(return_code)


def noop_return_code_handler(return_code: int):
    return


class PyGeoCom:
    def __init__(self, stream, debug: bool = False):
        self._stream = stream
        self._stream.write(b"\n")
        self._debug = debug
        self.req_len = []
        self.req_time = []
        self.resp_len = []
        self.resp_time = []

    def _request(
        self,
        rpc_id: int,
        args: Tuple[Any, ...] = (),
        return_code_handler: Callable[[int], None] = default_return_code_handler,
    ) -> Tuple[Any, ...]:
        def encode(arg) -> str:
            if type(arg) == str:
                return '"{}"'.format(arg)
            elif type(arg) == int:
                return "{}".format(arg)
            elif type(arg) == float:
                return "{}".format(arg)
            elif type(arg) == bool:
                return "1" if arg == True else "0"
            elif type(arg) == byte:
                return "'{:02X}'".format(arg)

        d = "\n%R1Q,{}:{}\r\n".format(
            rpc_id, ",".join([encode(a) for a in args])
        ).encode("ascii")
        if self._debug:
            print(b">> " + d)
        self.req_len = len(d)
        self.req_time = time()
        self._stream.write(d)

        d = self._stream.readline()
        self.resp_time = time()
        self.resp_len = len(d)
        if self._debug:
            print(b"<< " + d)
        header, parameters = d.split(b":", 1)

        reply_type, geocom_return_code, transaction_id = header.split(b",")
        assert reply_type == b"%R1P"
        geocom_return_code = int(geocom_return_code)
        transaction_id = int(transaction_id)

        parameters = parameters.rstrip()
        rpc_return_code, *p = parameters.split(b",")
        rpc_return_code = ReturnCode(int(rpc_return_code))

        return_code_handler(rpc_return_code)

        return (geocom_return_code, rpc_return_code) + tuple(p)

    def get_instrument_number(self) -> int:
        (
            _,
            _,
            instrument_number,
        ) = self._request(5003)
        return int(instrument_number)

    def get_instrument_name(self) -> str:
        _, _, instrument_name = self._request(5004)
        return decode_string(instrument_name)

    def get_device_config(self) -> DeviceType:
        _, _, device_class, device_type = self._request(5035)
        return DeviceClass(int(device_class)), DeviceType(int(device_type))

    def get_date_time(self) -> datetime:
        _, _, year, month, day, hour, minute, second = self._request(5008)
        year = int(year)
        month = byte(month)
        day = byte(day)
        hour = byte(hour)
        minute = byte(minute)
        second = byte(second)
        return datetime(year, month, day, hour, minute, second)

    def set_date_time(self, dt: datetime):
        self._request(
            5007,
            (
                dt.year,
                byte(dt.month),
                byte(dt.day),
                byte(dt.hour),
                byte(dt.minute),
                byte(dt.second),
            ),
        )

    def get_software_version(self) -> Tuple[int, int, int]:
        _, _, release, version, subversion = self._request(5034)
        return int(release), int(version), int(subversion)

    def check_power(self) -> Tuple[int, PowerPath, PowerPath]:
        _, _, capacity, active_power, power_suggest = self._request(5039)
        return (
            int(capacity),
            PowerPath(int(active_power)),
            PowerPath(int(power_suggest)),
        )

    def get_memory_voltage(self) -> float:
        _, _, memory_voltage = self._request(5010)
        return float(memory_voltage)

    def get_internal_temperature(self) -> float:
        _, _, internal_temperature = self._request(5011)
        return float(internal_temperature)

    def get_up_counter(self) -> Tuple[int, int]:
        _, _, power_on, wake_up = self._request(12003)
        return int(power_on), int(wake_up)

    def get_binary_available(self) -> bool:
        (
            _,
            _,
            binary_available,
        ) = self._request(113)
        return bool(binary_available)

    def get_record_format(self) -> RecordFormat:
        (
            _,
            _,
            record_format,
        ) = self._request(8011)
        return (RecordFormat(int(record_format)),)

    def set_record_format(self, record_format: RecordFormat):
        self._request(8012, (record_format.value,))

    def get_double_precision_setting(self) -> int:
        (
            _,
            _,
            number_of_digits,
        ) = self._request(108)
        return int(number_of_digits)

    def set_double_precision_setting(self, number_of_digits: int):
        if number_of_digits < 0:
            raise ValueError("Number of digits must be greater than or equal to 0")
        if number_of_digits > 15:
            raise ValueError("Number of digits must be lesser than or equal to 15")
        self._request(107, (number_of_digits,))

    def laser_pointer(self, state: OnOff):
        self._request(1004, (state.value,))

    def laser_pointer_on(self):
        self.laser_pointer(OnOff.ON)

    def laser_pointer_off(self):
        self.laser_pointer(OnOff.OFF)

    # Not tested as I don't have a device with an EGL
    def get_egl_intensity(self) -> EGLIntensity:
        (
            _,
            _,
            intensity,
        ) = self._request(1058)
        return EGLIntensity(int(intensity))

    # Not tested as I don't have a device with an EGL
    def set_egl_intensity(self, intensity: EGLIntensity):
        self._request(1059, (intensity.value,))

    def get_motor_lock_status(self) -> LockInStatus:
        (
            _,
            _,
            motor_lock_status,
        ) = self._request(6021)
        return LockInStatus(int(motor_lock_status))

    def start_controller(self, controller_mode: ControllerMode):
        self._request(6001, (controller_mode.value,))

    def stop_controller(self, controller_stop_mode: ControllerStopMode):
        self._request(6002, (controller_stop_mode.value,))

    # Speed is in radians/second, with a maximum of ±0.79rad/s each
    def set_velocity(self, hoziontal_speed: float, vertical_speed: float):
        MAX_SPEED = 0.79  # rad/s
        if abs(hoziontal_speed) > MAX_SPEED:
            raise ValueError("Horizontal speed exceeds the ±0.79 range")
        if abs(vertical_speed) > MAX_SPEED:
            raise ValueError("Horizontal speed exceeds the ±0.79 range")
        self._request(6004, (hoziontal_speed, vertical_speed))

    def get_target_type(self) -> TargetType:
        (
            _,
            _,
            target_type,
        ) = self._request(17022)
        return TargetType(int(target_type))

    def set_target_type(self, target_type: TargetType):
        self._request(17021, (target_type.value,))

    def get_prism_type(self) -> PrismType:
        (
            _,
            _,
            prism_type,
        ) = self._request(17009)
        return PrismType(int(prism_type))

    def set_prism_type(self, prism_type: PrismType):
        self._request(17008, (prism_type.value,))

    def get_prism_definition(
        self, prism_type: PrismType
    ) -> Tuple[str, float, ReflectorType]:
        _, _, name, correction, reflector_type = self._request(
            17023, (prism_type.value,)
        )
        name = decode_string(name)
        correction = float(correction)
        reflector_type = ReflectorType(int(reflector_type))
        return name, correction, reflector_type

    def set_prism_definition(
        self,
        prism_type: PrismType,
        name: str,
        correction: float,
        reflector_type: ReflectorType,
    ):
        self._request(17024, (prism_type.value, name, correction, reflector_type.value))

    def get_measurement_program(self) -> MeasurementProgram:
        (
            _,
            _,
            measurement_program,
        ) = self._request(17018)
        return MeasurementProgram(int(measurement_program))

    def set_measurement_program(self, measurement_program: MeasurementProgram):
        self._request(17019, (measurement_program.value,))

    def set_edm_mode(self, edm_mode: EDMMeasurementMode):
        self._request(2020, (edm_mode.value,))

    def measure_distance_and_angles(
        self, measurement_mode: MeasurementMode
    ) -> Tuple[MeasurementMode, float, float, float]:
        _, _, horizontal, vertical, distance, measurement_mode = self._request(
            17017, (measurement_mode.value,)
        )
        horizontal = float(horizontal)
        vertical = float(vertical)
        distance = float(distance)
        measurement_mode = MeasurementMode(int(measurement_mode))

        return measurement_mode, horizontal, vertical, distance

    def search_target(self):
        self._request(17020, (0,))

    def ps_set_range(self, lMinDist: int, lMaxDist: int):
        self._request(9047, (lMinDist, lMaxDist))

    def ps_enable_range(self, bool: BOOLE):
        self._request(9048, (bool.value,))

    def ps_search_window(self):
        self._request(9052)

    def ps_search_next(self, l_direction: lDirection, bool: BOOLE):
        self._request(9051, (l_direction.value, bool.value))

    def get_server_software_version(self) -> Tuple[int, int, int]:
        _, _, release, version, subversion = self._request(110)
        return int(release), int(version), int(subversion)

    def set_send_delay(self, delay_ms: int):
        self._request(109, (delay_ms,))

    def local_mode(self):
        self._request(1)

    def get_user_atr_state(self) -> OnOff:
        (
            _,
            _,
            atr_state,
        ) = self._request(18006)
        return OnOff(int(atr_state))

    def set_user_atr_state(self, atr_state: OnOff):
        self._request(18005, (atr_state.value,))

    def user_atr_state_on(self):
        self.set_user_atr_state(OnOff.ON)

    def user_atr_state_off(self):
        self.set_user_atr_state(OnOff.OFF)

    def get_user_lock_state(self) -> OnOff:
        (
            _,
            _,
            lock_state,
        ) = self._request(18008)
        return OnOff(int(lock_state))

    def set_user_lock_state(self, lock_state: OnOff):
        self._request(18007, (lock_state.value,))

    def user_lock_state_on(self):
        self.set_user_lock_state(OnOff.ON)

    def user_lock_state_off(self):
        self.set_user_lock_state(OnOff.OFF)

    def get_rcs_search_switch(self) -> OnOff:
        """This command gets the current RCS-Searching mode switch. If RCS style searching
        is enabled, then the extended searching for BAP_SearchTarget or after a loss of
        lock is activated. This command is valid for TCA instruments only.

        :returns: state of the RCS searching switch
        :rtype: OnOff
        """
        (
            _,
            _,
            search_switch,
        ) = self._request(18010)
        return OnOff(int(search_switch))

    def switch_rcs_search(self, search_switch: OnOff):
        self._request(18009, (search_switch.value,))

    def get_tolerance(self) -> Tuple[float, float]:
        _, _, horizontal_tolerance, vertical_tolerance = self._request(9008)
        return float(horizontal_tolerance), float(vertical_tolerance)

    def set_tolerance(self, horizontal_tolerance: float, vertical_tolerance: float):
        self._request(9007, (horizontal_tolerance, vertical_tolerance))

    def get_positioning_timeout(self) -> Tuple[float, float]:
        _, _, horizontal_timeout, vertical_timeout = self._request(9012)
        return float(horizontal_timeout), float(vertical_timeout)

    def set_positioning_timeout(
        self, horizontal_timeout: float, vertical_timeout: float
    ):
        self._request(9011, (horizontal_timeout, vertical_timeout))

    def position(
        self,
        horizontal: float,
        vertical: float,
        position_mode: PositionMode = PositionMode.NORMAL,
        atr_mode: ATRRecognitionMode = ATRRecognitionMode.POSITION,
    ):
        self._request(
            9027, (horizontal, vertical, position_mode.value, atr_mode.value, False)
        )

    def change_face(
        self,
        position_mode: PositionMode = PositionMode.NORMAL,
        atr_mode: ATRRecognitionMode = ATRRecognitionMode.POSITION,
    ):
        self._request(9028, (position_mode.value, atr_mode.value, False))

    def fine_adjust(self, horizontal_search_range: float, vertical_search_range: float):
        self._request(9037, (horizontal_search_range, vertical_search_range, False))

    def search(self, horizontal_search_range: float, vertical_search_range: float):
        self._request(9029, (horizontal_search_range, vertical_search_range, False))

    def get_fine_adjust_mode(self) -> FineAdjustPositionMode:
        (
            _,
            _,
            fine_adjust_mode,
        ) = self._request(9030)
        return FineAdjustPositionMode(float(fine_adjust_mode))

    def set_fine_adjust_mode(self, fine_adjust_mode: FineAdjustPositionMode):
        self._request(9031, (fine_adjust_mode.value,))

    def lock_in(self):
        self._request(9013)

    def get_search_area(self) -> Tuple[float, float, float, float, bool]:
        (
            _,
            _,
            horizontal_centre,
            vertical_centre,
            horizontal_range,
            vertical_range,
            enabled,
        ) = self._request(9042)
        horizontal_centre = float(horizontal_centre)
        vertical_centre = float(vertical_centre)
        horizontal_range = float(horizontal_range)
        vertical_range = float(vertical_range)
        enabled = bool(enabled)
        return (
            horizontal_centre,
            vertical_centre,
            horizontal_range,
            vertical_range,
            enabled,
        )

    def set_search_area(
        self,
        horizontal_centre: float,
        vertical_centre: float,
        horizontal_range: float,
        vertical_range: float,
        enabled: bool,
    ):
        self._request(
            9043,
            (
                horizontal_centre,
                vertical_centre,
                horizontal_range,
                vertical_range,
                enabled,
            ),
        )

    def get_search_spiral(self) -> Tuple[float, float]:
        _, _, horizontal_range, vertical_range = self._request(9040)
        return float(horizontal_range), float(vertical_range)

    def set_search_spiral(self, horizontal_range: float, vertical_range: float):
        self._request(9041, (horizontal_range, vertical_range))

    def get_signal(self):
        _, _, signal_intensity, time = self._request(2022)
        return float(signal_intensity), int(time)

    def get_face(self) -> int:
        _, _, face = self._request(2026)
        return int(face)

    def get_coordinate(
        self, inclination_mode: TMCInclinationMode, wait_time: int = 1000
    ) -> Tuple[Coordinate, int, Coordinate, int]:
        (
            _,
            _,
            e,
            n,
            h,
            measure_time,
            e_cont,
            n_cont,
            h_cont,
            measure_time_cont,
        ) = self._request(
            2082,
            (wait_time, inclination_mode.value),
            return_code_handler=noop_return_code_handler,
        )
        coordinate = Coordinate(float(e), float(n), float(h))
        coordinate_cont = Coordinate(float(e_cont), float(n_cont), float(h_cont))
        measure_time = int(measure_time)
        measure_time_cont = int(measure_time_cont)
        return coordinate, measure_time, coordinate_cont, measure_time_cont

    # UNDOCUMENTED MEASUREMENT MODE TMC_GetFullMeas 2167
    def get_full_measurement(
        self, inclination_mode: TMCInclinationMode, wait_time: int = 1000
    ) -> Tuple[Coordinate, int, Coordinate, int]:
        (
            _,
            _,
            horizontal,
            vertical,
            accIncl,
            crossIncl,
            lenIncl,
            accIncl,
            slope_distance,
            measure_time,
        ) = self._request(
            2167,
            (wait_time, inclination_mode.value),
            return_code_handler=noop_return_code_handler,
        )
        slope_distance = float(slope_distance)
        measure_time = int(measure_time)
        return (
            measure_time,
            float(horizontal),
            float(vertical),
            slope_distance,
            float(accIncl),
            float(crossIncl),
            float(lenIncl),
        )

    def get_simple_measurement(
        self, inclination_mode: TMCInclinationMode, wait_time: int = 1000
    ) -> Tuple[Angles, float]:
        _, _, horizontal, vertical, slope_distance = self._request(
            2108,
            (
                wait_time,
                inclination_mode.value,
            ),
        )
        angles = Angles(float(horizontal), float(vertical))
        slope_distance = float(slope_distance)
        return angles, slope_distance

    def get_angles_simple(self, inclination_mode: TMCInclinationMode) -> Angles:
        _, _, horizontal, vertical = self._request(2107, (inclination_mode.value,))
        return Angles(float(horizontal), float(vertical))

    def get_angles_complete(
        self, inclination_mode: TMCInclinationMode
    ) -> Tuple[Angles, float, int, float, float, float, int, FacePosition]:
        (
            _,
            _,
            horizontal,
            vertical,
            angle_accuracy,
            angle_measure_time,
            cross_inclincation,
            length_inclination,
            incline_accuracy,
            incline_measurement_time,
            face_position,
        ) = self._request(2003, (inclination_mode.value,))
        angles = Angles(float(horizontal), float(vertical))
        angle_accuracy = float(angle_accuracy)
        angle_measure_time = float(angle_measure_time)
        cross_inclincation = float(cross_inclincation)
        length_inclination = float(length_inclination)
        incline_accuracy = float(incline_accuracy)
        incline_measurement_time = int(incline_measurement_time)
        face_position = FacePosition(int(face_position))
        return (
            angles,
            angle_accuracy,
            angle_measure_time,
            cross_inclincation,
            length_inclination,
            incline_accuracy,
            incline_measurement_time,
            face_position,
        )

    def do_measure(
        self, measurement_mode: TMCMeasurementMode, inclination_mode: TMCInclinationMode
    ):
        self._request(
            2008,
            (
                measurement_mode.value,
                inclination_mode.value,
            ),
        )

    def beep_alarm_triple(self):
        self._request(11004)

    def beep_alarm_normal(self):
        self._request(11003)

    def beep_on(self, intensity: int):
        self._request(20001, (intensity,))

    def beep_off(self):
        self._request(20000)
