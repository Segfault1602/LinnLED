"""Helper script to set LinnStrument's note pad color base on EDO tuning"""
from enum import IntEnum

import mido
from mido import Message

# Midi CC constant
LINN_CC_COL = 20
LINN_CC_ROW = 21
LINN_CC_COLOR = 22
LINN_CC_SAVE = 23
LINN_CC_CLEAR = 24


class LinnColor(IntEnum):
    """Color values used by LinnStrument"""
    DEFAULT = 0
    RED = 1
    YELLOW = 2
    GREEN = 3
    CYAN = 4
    BLUE = 5
    MAGENTA = 6
    OFF = 7
    WHITE = 8
    ORANGE = 9
    LIME = 10
    PINK = 11


class LinnSaveSlot(IntEnum):
    """Custom memory slot for saving light pattern"""
    A = 0
    A_SHARP = 1
    B = 2


# 19 EDO.
# Octave is blue
# Fifth (3:2) is orange
# Major 2nd(9:8), Major 3rd(5:4), fourth(4:3), Major 6th (5:3), Major
# 7th(15:8) are green
EDO_19_TEMPLATE = [
    LinnColor.OFF,
    LinnColor.OFF,
    LinnColor.GREEN,
    LinnColor.OFF,
    LinnColor.OFF,
    LinnColor.GREEN,
    LinnColor.OFF,
    LinnColor.GREEN,
    LinnColor.OFF,
    LinnColor.OFF,
    LinnColor.ORANGE,
    LinnColor.OFF,
    LinnColor.OFF,
    LinnColor.GREEN,
    LinnColor.OFF,
    LinnColor.OFF,
    LinnColor.GREEN,
    LinnColor.OFF,
    LinnColor.BLUE]

# Change this variable to control which degree of your scale should
# correspond to the bottom left pads. A start offset of 0 means that the
# root of your scales will be in the bottom left corner.
START_OFFSET = 2

# Change this variable to control the offset between each rows. For
# example, in 19EDO, an offset of 6 means that each row will be a fourth
# apart.
ROW_OFFSET = 6


def set_color(linnstrument, col, row, color):
    """Set a LinnStrument's note pad to a specified color"""

    # First send CC20 and CC21 to select the column and row to be lit, then
    # send CC22 to light it.

    # 1) CC20: Column number of note pad to change (control key column is 0,
    # left play column is 1, right play column is 25)
    msg = Message('control_change', control=LINN_CC_COL, value=col)
    linnstrument.send(msg)

    # 2) CC21: Row number of note pad to change (bottom row is 0, top is 7)
    msg = Message('control_change', control=LINN_CC_ROW, value=row)
    linnstrument.send(msg)

    # 3) CC22: Color to change it to
    msg = Message('control_change', control=LINN_CC_COLOR, value=color)
    linnstrument.send(msg)


def save_pattern(linnstrument, pattern):
    """Save the pattern to one of the 3 slots"""
    msg = Message('control_change', control=LINN_CC_SAVE, value=pattern)
    linnstrument.send(msg)


def main():
    """Main function"""
    print("LinnStrument LED editor - v 1.0.0")
    print("---")
    outports = mido.get_output_names()
    outport_name = [s for s in outports if 'LinnStrument' in s][0]

    print(f"Opening {outport_name}...")
    with mido.open_output(outport_name) as linnstrument:
        print("Success!")

        for row in range(0, 8):
            # Each row will be a perfect fourth appart
            row_offset = row * ROW_OFFSET + START_OFFSET
            # Column 0 is the control keys, actual play area starts at column 1
            # Change the last index to 17 for the 128 pads version.
            for col in range(1, 26):
                scale_index = (col - 1 + row_offset) % len(EDO_19_TEMPLATE)
                set_color(linnstrument, col, row, EDO_19_TEMPLATE[scale_index])

        save_pattern(linnstrument, LinnSaveSlot.A_SHARP)


if __name__ == "__main__":
    main()
