from typing import Optional

class HsvFilter:
    def __init__( 
                 hMin: Optional[int] = None, 
                 sMin: Optional[int] = None, 
                 vMin: Optional[int] = None, 
                 hMax: Optional[int] = None, 
                 sMax: Optional[int] = None, 
                 vMax: Optional[int] = None, 
                 sAdd: Optional[int] = None, 
                 sSub: Optional[int] = None, 
                 vAdd: Optional[int] = None, 
                 vSub: Optional[int] = None) -> None:
        ...

def apply_hsv_filter(original_image, hsv_filter=None):
    ...

def shift_channel(c, amount):
    ...