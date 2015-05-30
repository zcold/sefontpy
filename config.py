# coding: utf-8

# Assign this shadow size even if
# a font bitmap set has no shadow to keep location consistency.
shadow_size = 3

def construct_color(r, g, b) :
  rx = hex(r).split('x')[1]
  if len(rx) == 1 :
    rx = '0' + rx
  gx = hex(g).split('x')[1]
  if len(gx) == 1 :
    gx = '0' + rx
  bx = hex(b).split('x')[1]
  if len(gx) == 1 :
    gx = '0' + rx
  return '#' + rx + gx + bx

blue = construct_color(214, 244, 255)
darkblue = construct_color(118, 200, 241)
green = construct_color(101, 181, 91)
red = construct_color(228, 63, 63)
white = construct_color(255, 255, 255)
grey = construct_color(110, 111, 115)
black = construct_color(0, 0, 0)
shadow_color = construct_color(50, 50, 50)

config = {

  'Do not delete this configure file.' : ''

  # The base folder of this font map generator.
  , 'base folder'
  : './'

  # The folder stores all TrueType font (.ttf) files.
  # The specified folder is relative to this configure file.
  # Absolute folder will be base folder + font folder.
  , 'font folder'
  : 'fonts'

  # The Space Engineers (SE) installation path.
  , 'space engineer base folder'
  : 'C:\Program Files (x86)\Steam\SteamApps\common\SpaceEngineers'

  # Font size in SE
  , 'font size'
  : 33

  # The font priority list, from high to low.
  # The bitmap of each character
  #   is given by the TrueType font (.tff)
  #   who has a valid bitmap and a highest priority.
  , 'font priority list'
  : [ ]

  # The width of the result .dds image.
  , 'image width'
  : 1024

  # The width of the result .dds image
  , 'image height'
  : 1024

  # output .dds file name prefix
  , 'output dds prefix'
  : 'FontDataExtra-'

  # Original dds file names.
  # They are used when
  # the user wants to keep the original font bitmaps
  # and only construct the characters that
  # are not included in the original font bitmaps.
  , 'original dds file names'
  : [ 'FontData-0.dds' ]

  # Predefined colors
  , 'predefined colors'
  : { 'blue': {
        'output' : True,
        'color': blue,
        'shadow_color': shadow_color,
        'shadow_size': shadow_size,
        'shadow' : False },

      'darkblue': {
        'output' : True,
        'color': darkblue,
        'shadow_color': shadow_color,
        'shadow_size': shadow_size,
        'shadow' : False },

      'green': {
        'output' : True,
        'color': green,
        'shadow_color': shadow_color,
        'shadow_size': shadow_size,
        'shadow' : False },

      'red': {
        'output' : True,
        'color': red,
        'shadow_color': shadow_color,
        'shadow_size': shadow_size,
        'shadow' : False },

      'white': {
        'output' : True,
        'color': white,
        'shadow_color': shadow_color,
        'shadow_size': shadow_size,
        'shadow' : False },

      'grey': {
        'output' : True,
        'color': grey,
        'shadow_color': shadow_color,
        'shadow_size': shadow_size,
        'shadow' : False },

      'white_shadow': {
        'output' : True,
        'color': white,
        'shadow_color': shadow_color,
        'shadow_size': shadow_size,
        'shadow' : True }
    }

  # Left Side Bearing, lsb
  #
  # illusion:
  #
  # |<  last  >|         |<  this  >|
  # |<  char  >|         |<  char  >|
  # |< bitmap >||< lsb >||< bitmap >|
  #
  , 'lsb'
  : -1

  # font map xml template file
  , 'xml template'
  : 'xml_template.xml'

  # font map xml file name
  , 'xml file name'
  : 'FontData.xml'

  # font place holder north margin
  , 'north margin'
  : 0

  # font place holder west margin
  , 'west margin'
  : 0

  # font place holder south margin
  , 'south margin'
  : 0

  # font place holder east margin
  , 'east margin'
  : 0

  # keep original font map
  , 'keep original font map'
  : True

  , 'text file folder'
  : 'text_files'

  , 'unsupported folder'
  : 'unsupported'

  , 'backup folder'
  : 'backup'

  , 'output folder'
  : 'output'

}
