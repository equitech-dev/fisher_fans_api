from enum import Enum

class StatusEnum(Enum):
    INDIVIDUAL = "particulier"
    PROFESSIONAL = "professionnel"
    
class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"

class ActivityTypeEnum(str, Enum):
    RENTAL = "RENTAL"
    GUIDE = "GUIDE"

class MotorEnum(str, Enum):
    DIESEL = "DIESEL"
    GASOLINE = "GASOLINE"
    NOTHING = "NOTHING"

class LicenseEnum(str, Enum):
    COASTAL = "COASTAL"
    INLAND = "INLAND"

class BoatTypeEnum(str, Enum):
    OPEN = "OPEN"
    CABIN = "CABIN"
    CATAMARAN = "CATAMARAN"
    VOILER = "VOILER"
    JETSKI = "JETSKI"
    CANOE = "CANOE"

class EquipmentEnum(str, Enum):
    FISHFINDER = "FISHFINDER"
    LIVEWELL = "LIVEWELL"
    LADDER = "LADDER"
    GPS = "GPS"
    ROD_HOLDERS = "ROD_HOLDERS"
    RADIO = "RADIO"

class PricingTypeEnum(str, Enum):
    GLOBAL = "GLOBAL"
    PER_PERSON = "PER_PERSON"

class TripTypeEnum(str, Enum):
    DAILY = "DAILY"
    RECURRING = "RECURRING"
