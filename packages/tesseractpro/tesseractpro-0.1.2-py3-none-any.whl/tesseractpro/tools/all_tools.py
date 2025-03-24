
from .turningpoint import TurningPoint
from .image import Image
from .magbox import MagBox
from .spiral import Spiral
from .marker import Marker
from .curve import Curve
from .line import Line
from .circle import Circle
from .angleline import AngleLine
from .vertical_ray import VerticalRay
from .horizontal_ray import HorizontalRay
from .arrow import Arrow
from .text import Text
from .protractor import Protractor
from .gann_grid import GannGrid
from .gann_square import GannSquare
from .gann_box import GannBox
from .gannfan import GannFan
from .fib_retracement import FibRetracement
from .pitchfork import PitchFork

TOOL_TYPE_TO_CLASS = {
    TurningPoint.type: TurningPoint,
    Image.type: Image,
    MagBox.type: MagBox,
    Spiral.type: Spiral,
    Marker.type: Marker,
    Curve.type: Curve,
    Line.type: Line,
    Circle.type: Circle,
    AngleLine.type: AngleLine,
    VerticalRay.type: VerticalRay,
    HorizontalRay.type: HorizontalRay,
    Arrow.type: Arrow,
    Text.type: Text,
    Protractor.type: Protractor,
    GannGrid.type: GannGrid,
    GannSquare.type: GannSquare,
    GannBox.type: GannBox,
    GannFan.type: GannFan,
    FibRetracement.type: FibRetracement,
    PitchFork.type: PitchFork,
}

def get_tool_instance_by_type(type, options):
    try:
        cls = TOOL_TYPE_TO_CLASS[type]
        return cls(options)
    except KeyError:
        raise ValueError(f"No class found with type: {type}")
