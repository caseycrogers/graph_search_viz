from matplotlib import transforms
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.text import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib import patches
from config import Config

from geometery_utils import *


class Color:
    def __init__(self, r, g, b, description):
        self.description = description
        self.r, self.g, self.b = r, g, b

    def __hash__(self):
        return hash((self.r, self.g, self.b, self.description))


CUT_THICK = Color(0, 0, 255, "CUT_THICK")
CUT_THIN = Color(255, 0, 0, "CUT_THIN")
ENGRAVE_THICK = Color(0, 128, 0, "ENGRAVE_THICK")
ENGRAVE_THIN = Color(255, 165, 0, "ENGRAVE_THIN")
FRAME = Color(128, 128, 128, "FRAME")
DEBUG = Color(0, 0, 0, "DEBUG")


class _MatPlotLibRenderer:
    def __init__(self, panels=True, axis_range=None):
        plt.axes().set_aspect('equal')
        self._ax = plt.subplot(111)
        self._colors = set()
        self._axis_range = axis_range
        if axis_range is not None:
            self._ax.set_xlim(left=0, right=axis_range[0])
            self._ax.set_ylim(bottom=0, top=axis_range[1])
        self._render_panels = panels

    @staticmethod
    def _convert_color(color):
        return color.r / 255.0, color.g / 255.0, color.b / 255.0

    def add_line(self, a, b, color=CUT_THICK, tab=0.0):
        if tab > 0:
            mid = midpoint(a, b)
            # leave a gap in the center
            self.add_line(a, mid - tab/2.0*normalized(mid - a), color=color)
            return self.add_line(mid + tab/2.0*normalized(mid - a), b, color=color)
        self._colors.add(color)
        self._ax.plot([a[0], b[0]], [a[1], b[1]], color=self._convert_color(color))

    def add_circle(self, a, d, color=CUT_THICK):
        self._colors.add(color)
        self._ax.add_patch(patches.Circle(a, d/2.0, color=self._convert_color(color)))

    def add_polygon(self, points, color=CUT_THICK):
        for a, b in adjacent_nlets(points, 2):
            self.add_line(a, b, color)

    def add_text(self, a, v, text, max_w, max_h, color=ENGRAVE_THICK, h_center=False, v_center=False):
        self._colors.add(color)
        text_path = TextPath([0, 0], text, font_properties=FontProperties(fname=Config.font_file))
        bb = text_path.get_extents()
        h_adjust, v_adjust = 0, 0
        if h_center:
            h_adjust = -(bb.xmin + bb.xmax) / 2
        if v_center:
            v_adjust = -(bb.ymin + bb.ymax) / 2
        text_path = text_path.transformed(
            transforms.Affine2D().translate(h_adjust, v_adjust)
        )
        x_scale = max_w / (bb.xmax - bb.xmin)
        y_scale = max_h / (bb.ymax - bb.ymin)
        text_path = text_path.transformed(
            transforms.Affine2D()
                # align text with the respective side
                .rotate(vector_angle_2d(v))
                # make text as large as will fit in x and y bounds
                .scale(min(x_scale, y_scale))
                # move the text to the text point
                .translate(a[0], a[1])
        )
        self._ax.add_patch(patches.PathPatch(text_path, facecolor='none', edgecolor=self._convert_color(color)))


class DXFRenderer(_MatPlotLibRenderer):
    def __init__(self, panels=True, axis_range=None):
        _MatPlotLibRenderer.__init__(self, panels=panels, axis_range=axis_range)
        plt.axis('off')
        plt.margins(0, 0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)

    def update(self):
        pass

    def finish(self, name):
        if self._axis_range is not None:
            x_bound = map(mm_to_inch, self._ax.get_xbound())
            y_bound = map(mm_to_inch, self._ax.get_ybound())
            plt.gcf().set_size_inches(x_bound[1] - x_bound[0], y_bound[1] - y_bound[0])
        plt.gcf().savefig('{0}.svg'.format(name, format='svg'), bbox_inches=0, pad_inches=0, transparent=True)
        plt.clf()


class DebugRenderer(_MatPlotLibRenderer):
    def update(self):
        colors, descriptions = zip(*[(c, c.description) for c in self._colors])
        self._ax.legend(
            [Line2D([0], [0], color=self._convert_color(c), lw=4) for c in colors],
            descriptions
        )
        plt.pause(.1)

    def finish(self, name):
        plt.show()
        plt.clf()
