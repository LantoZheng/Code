import numpy as np


def offset_adjuster(loc795,loc632,offset,step):
    ret=offset
    n795=len(loc795)
    n632=len(loc632)
    # adjust to make the 795nm line to appear
    if n795<=0:
        ret+=step
        return ret
    elif n795>2:
        ret-=step
        return ret
    
    p795=loc795[0]
    if n632==1:
        if p795<=loc632[0]:
            ret+=step
        else:
            ret-=step
        return ret
    elif (n632>2):
        ret-=step
        return ret
    return ret