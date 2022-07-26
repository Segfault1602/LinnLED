# LinnLED

LinnLED is a simple python script to help setting custom LED patterns on the LinnStrument.

## Important Notes

Right now, the script is hardcoded to push a custom 19 EDO light pattern to the LinnStrument and saves it to the A# custom memory slot. The script also assumes that the **200** pads version of the LinnStrument is used.

That being said, the script should be simple enough to allow any one with a basic understanding of Python to modify this script to suit their needs.

## Dependencies

The script uses [Mido](https://mido.readthedocs.io/en/latest/#) to communicate with the LinnStrument through MIDI messages. The library is easily installable using pip:
```
pip install mido
```
