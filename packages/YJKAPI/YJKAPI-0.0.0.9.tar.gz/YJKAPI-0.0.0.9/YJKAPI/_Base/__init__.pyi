from enum import Enum

class _kColumInt:
    k:int          
    b:int
    h:int
    u:int
    t:int
    d:int
    f:int
    l:int
    m:int
    p:int
    name:str
    igzz:int
    b1:int
    id:int

class LinkType(Enum):
    ISOLATOR = 1,
    DAMPER=2,
    PLASTIC=3

