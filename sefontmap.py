# coding: utf-8
# The MIT License (MIT)
  # Copyright (c) 2014 by Shuo Li (contact@shuo.li)
  #
  # Permission is hereby granted, free of charge, to any person obtaining a
  # copy of this software and associated documentation files (the "Software"),
  # to deal in the Software without restriction, including without limitation
  # the rights to use, copy, modify, merge, publish, distribute, sublicense,
  # and/or sell copies of the Software, and to permit persons to whom the
  # Software is furnished to do so, subject to the following conditions:
  #
  # The above copyright notice and this permission notice shall be included in
  # all copies or substantial portions of the Software.
  #
  # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
  # FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
  # DEALINGS IN THE SOFTWARE.

__author__ = 'Shuo Li <contact@shuol.li>'
__version__= '2014-09-27-12:42'

import timeit
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from os import listdir
from os.path import isfile, join

import copy
import re
import shutil

import xml.etree.ElementTree as ET

import jinja2
# from fontTools.ttLib import TTFont

import PIL
from PIL import ImageFont, ImageDraw

if 'define constants' :

  def file_names_in_folder(folder) :

    abs_folder = os.path.abspath(folder)
    return [ f for f in listdir(abs_folder)
              if isfile(join(abs_folder,f)) ]

  def get_default_image() :
    return PIL.Image.new( 'RGBA', (image_width, image_height) )

  if isfile('config.py') :
    config_module = __import__( 'config' )
    config = config_module.config
  else :
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
      : 28

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

  keep_original = bool(config['keep original font map'])

  output_dds_prefix = str(config['output dds prefix'])
  original_dds_file_names = config['original dds file names']
  se_folder = str(config['space engineer base folder'])
  font_size = int(config['font size'])
  base_folder = str(config['base folder'])
  font_folder = base_folder + str(config['font folder'])
  font_folder = os.path.abspath(font_folder)
  output_folder = base_folder + str(config['output folder'])
  output_folder = os.path.abspath(output_folder)

  font_priority_list = config['font priority list']
  font_priority_list = []
  font_files_in_folder = file_names_in_folder(font_folder)

  font_files = [ join(font_folder, f) for f in list(font_priority_list)]

  for f in font_files_in_folder :
    if f not in font_priority_list :
      font_files.append(join(font_folder, f))

  fonts = [ { 'face' : 'freetype.Face(f)',
              'font' : ImageFont.truetype(f, font_size),
              'font_size' : font_size,
              'file_name' : os.path.basename(f)}
            for f in font_files ]

  unsupported_folder = config['unsupported folder']

  image_width = int(config['image width'])
  image_height = int(config['image height'])


  color_dict = config['predefined colors']

  lsb = config['lsb']

  xml_template_name = str(config['xml template'])
  xml_file_name = str(config['xml file name'])

  north_margin = int(config['north margin'])
  west_margin = int(config['west margin'])
  south_margin = int(config['south margin'])
  east_margin = int(config['east margin'])

  text_file_folder =  os.path.abspath(str(config['text file folder']))

  backup_folder = str(config['backup folder'])

if 'define classes' :

  class location() :

    '''
      Location class
    '''

    def __init__(self, x, y) :
      self.x = x
      self.y = y

    def clone(self) :
      return location(x, y)

    def __str__(self) :
      return '(%s, %s)' % (self.x, self.y)


    def add_sub_action(self, another_location, mode = '+') :

      def add_sub(a, b, mode = '+') :
        if mode == '+' :
          return a + b
        if mode == '-' :
          return a - b

        raise NotImplementedError()

      if isinstance(another_location, location) :
        return location(
          add_sub( self.x,
                   another_location.x,
                   mode),
          add_sub( self.y,
                   another_location.y,
                   mode))

      if isinstance(another_location, tuple) \
        or isinstance(another_location, list) :
          if len(another_location) == 2 :
            return location(
              add_sub( self.x,
                       int(another_location[0]),
                       mode),
              add_sub( self.y,
                       int(another_location[1]),
                       mode))

      if isinstance(another_location, dict) :
        if 'x' in another_location.keys() and 'y' in another_location.keys() :
          return location(
              add_sub( self.x,
                       int(another_location['x']),
                       mode),
              add_sub( self.y,
                       int(another_location['y']),
                       mode))

      raise NotImplementedError()

    def __add__(self, another_location) :
      return self.add_sub_action(another_location, mode = '+')

    def __sub__(self, another_location) :
      return self.add_sub_action(another_location, mode = '-')

  class char() :

    '''
      Character class
    '''

    def __init__(self, content) :

      self.content = content

    def map(self, color, fonts,
      north_margin = north_margin,
      west_margin = west_margin,
      south_margin = south_margin,
      east_margin = east_margin,
      unsupported = {}) :

      def haschar(font, one_character, unsupported = {}) :

        '''
          Return if a font has a character.
        '''
        return True
        # ttf_face = font['face']
        # font_file_name = font['file_name']

        # ttf_face.set_char_size( 48*64 )
        # ttf_face.load_char(one_character)

        # a = copy.deepcopy(ttf_face.glyph.bitmap.buffer)
        # b = []
        # if font_file_name in unsupported.keys() :
        #   if one_character in unsupported[ font_file_name ] :
        #     return False

        #   ttf_face.load_char(unsupported[ font_file_name ][0])
        #   b = copy.deepcopy(ttf_face.glyph.bitmap.buffer)

        # return a != b

      self.color = color

      self.font = None

      for f in fonts :

        if haschar(f, one_character = self.content,
          unsupported = unsupported) :

          self.font = f['font']
          self.font_size = f['font_size']
          break

      if self.font == None :
        print 'Warning! No font file has \'%s\'.' % self.content
        self.font = fonts[0]['font']
        self.font_size = f['font_size']

      self.width, self.height = self.font.getsize(self.content)

      self.shadow_size = color['shadow_size']
      self.width += (self.shadow_size * 2)
      self.height += (self.shadow_size * 2)
      self.size = (self.width, self.height)

      self.holder_height = north_margin + self.font_size + south_margin
      self.holder_height += (self.shadow_size * 4)

      self.holder_width = west_margin + self.width + east_margin
      self.holder_size = (self.holder_width, self.holder_height)

    def locate(self, code, image_location, image_index, left_sep) :

      self.code = code
      self.image_location = image_location
      self.image_index = image_index
      self.left_sep = left_sep

    def attribute(self) :
      return { 'content' : escape(self.content),
               'code' : get_code_string(self.code),
               'image_index' : self.image_index,
               'x' : self.image_location.x,
               'y' : self.image_location.y + self.shadow_size,
               'width' : self.width-1,
               'height' : self.holder_height - (self.shadow_size*2),
               'advance_width' : self.width - (self.shadow_size*2),
               'left_sep' : self.left_sep }

if 'define misc. functions' :

  def cleanup(folder_paths, file_names = [], remove_ext_name = ['.pyc', '.png']) :

    for folder_path in folder_paths :
      for f in file_names :
        os.remove(join(os.path.abspath(folder_path), f))

      for f in file_names_in_folder(folder_path) :
        for ext_name in remove_ext_name :
          if f.endswith(ext_name) :
            os.remove(join(folder_path, f))


  def distinct(string_list) :

    one_list = ''
    for s in string_list :
      one_list += s
      one_list = list(set(one_list))
    return one_list

  def save_dds(pillow_image, index = 0, output_folder = './'):
    output_folder = os.path.abspath(output_folder)
    temp_file_path = join(output_folder, 'temp_%s.png' % index)
    output_file_path = join(output_folder, '%s%s.dds' % (output_dds_prefix, index))
    pillow_image.save(temp_file_path)
    os.system(r'.\nvtt\nvcompress.exe -nocuda -bc3 %s %s' \
      % (temp_file_path, output_file_path ))
    os.remove(temp_file_path)

  def compute_location(one_char, draw_location, target_images) :

    (w, h) = target_images[-1].size

    # to the next line
    if draw_location.x + one_char.holder_width >= w :
      draw_location.y += one_char.holder_height
      draw_location.x = 0

    # to the next image
    if draw_location.y + one_char.holder_height >= h :
      target_images.append(get_default_image())
      draw_location.y = 0

    return draw_location, target_images

  def draw_one_char_to_image(one_char, draw_location, target_image, west_margin, south_margin) :

    '''
      Draw one char on one image
    '''

    def draw_once(draw, color, xshift, yshift,) :
      draw.text( ( draw_location.x + xshift,
                   draw_location.y + yshift),
                 one_char.content,
                 font = one_char.font,
                 fill = color )

    draw = ImageDraw.Draw(target_image)

    if one_char.color['shadow'] == True :
      for i in xrange(one_char.shadow_size) :
        draw_once(draw, one_char.color['shadow_color'], +i, +i)
        draw_once(draw, one_char.color['shadow_color'], one_char.shadow_size + 1 + i, +i)
        draw_once(draw, one_char.color['shadow_color'], +i, one_char.shadow_size + 1 + i)
        draw_once(draw, one_char.color['shadow_color'],
          one_char.shadow_size + 1 + i, one_char.shadow_size + 1 + i)

    draw_once(draw, one_char.color['color'], one_char.shadow_size, one_char.shadow_size)

    return draw_location + (one_char.holder_width, 0), target_image

  def write_char_to_image( one_char, draw_location, code,
      image_start_index,
      target_images = [ get_default_image() ] ) :

    if not isinstance(target_images, list) :
      target_images = [ target_images ]

    # compute char bitmap location
    draw_location, target_images \
    = compute_location(one_char, draw_location, target_images)

    one_char.locate(code, draw_location, image_start_index + len(target_images) - 1, lsb)

    # draw one char
    loc, target_images[-1] \
    = draw_one_char_to_image( one_char, draw_location, target_images[-1],
        west_margin, south_margin)

    return one_char, loc, target_images

  def save_images(images, output_folder) :
    i = 0
    for image in images :
      save_dds(image, i, output_folder)
      i += 1

  def get_code_string(decimal_code) :
    return hex(decimal_code).split('x')[1]

  def escape(input_string) :

    html_escape_table = {
      unicode('&'): unicode("&amp;"),
      unicode('"'): unicode("&quot;"),
      unicode("'"): unicode("&apos;"),
      unicode(">"): unicode("&gt;"),
      unicode("<"): unicode("&lt;") }

    input_string = unicode(input_string)

    if input_string in html_escape_table.keys() :
      return html_escape_table[ input_string ]

    return input_string

  def get_char_list(xml_file_name) :

    tree = ET.parse(xml_file_name)
    root = tree.getroot()

    glyphs = [ child for child in root if child.tag.endswith('glyphs') ][0]
    max_code = max([ int('0x' + glyph.attrib['code'], 16) for glyph in glyphs ])
    return [ glyph.attrib['ch'] for glyph in glyphs ], max_code

  def get_original_xml_attributes(xml_file_name) :

    tree = ET.parse(xml_file_name)
    root = tree.getroot()

    glyphs = [ child for child in root if child.tag.endswith('glyphs') ][0]
    kernpairs = [ child for child in root if child.tag.endswith('kernpairs') ][0]

    glyphs_attribute_list = [ {
      'content' : escape(glyph.attrib['ch']),
      'code' : glyph.attrib['code'],
      'bm' : glyph.attrib['bm'],
      'origin' : glyph.attrib['origin'],
      'size' : glyph.attrib['size'],
      'aw' : glyph.attrib['aw'],
      'lsb' : glyph.attrib['lsb'] }
      for glyph in glyphs ]

    kernpair_attribute_list = [ {
      'left' : escape(kernpair.attrib['left']),
      'right' : escape(kernpair.attrib['right']),
      'adjust' : kernpair.attrib['adjust'] }
      for kernpair in kernpairs ]

    return glyphs_attribute_list, kernpair_attribute_list

  def write_text_to_image(text, color, unsupported, start_code, output_folder = output_folder,
    image_start_index = 0,
    north_margin = north_margin,
    west_margin = west_margin,
    south_margin = south_margin,
    east_margin = east_margin) :

    draw_location = location(0, 0)
    target_images = [ get_default_image() ]
    current_code = start_code
    char_list = []
    for c in text :

      # create a char object
      one_char = char(content = c)

      # map a char to a bitmap
      one_char.map( color = color, fonts = fonts,
        north_margin = north_margin,
        west_margin = west_margin,
        south_margin = south_margin,
        east_margin = east_margin,
        unsupported = unsupported )

      one_char, draw_location, target_images \
      = write_char_to_image( one_char = one_char,
          draw_location = draw_location,
          code = current_code,
          image_start_index = image_start_index,
          target_images = target_images )

      char_list.append(one_char)
      current_code += 1

    save_images(target_images, output_folder)

    return char_list, target_images

  def produce_xml(char_list, target_images, output_folder,
    keep_original, original_xml_file_name) :

    env = jinja2.Environment()
    env.loader = jinja2.FileSystemLoader('./')

    template = env.get_template(xml_template_name)

    xml_file = open(join(output_folder, xml_file_name), 'w+')

    char_attribute_list = [ c.attribute() for c in char_list ]

    dds_files = []
    glyphs_attribute_list = []
    kernpair_attribute_list = []

    image_index = 0

    if keep_original == True :
      for n in original_dds_file_names :
        dds_files.append( { 'index' : image_index, 'name': n } )
        image_index += 1

      glyphs_attribute_list, kernpair_attribute_list = \
      get_original_xml_attributes(original_xml_file_name)

    dds_files += [ { 'index' : i + image_index, 'name': '%s%s.dds' % (output_dds_prefix, i) }
                  for i in xrange(len(target_images)) ]

    xml_file.write( template.render(
      char_attribute_list = char_attribute_list,
      dds_files = dds_files,
      glyphs_attribute_list = glyphs_attribute_list,
      kernpair_attribute_list = kernpair_attribute_list ) )

  def get_original_text(base_folder, backup_folder, xml_file_name) :

    original_xml_file_name = join(backup_folder, 'red\\' + xml_file_name)
    original_xml_file_name_copy = join(base_folder, 'original_' + xml_file_name)
    shutil.copy2(original_xml_file_name, original_xml_file_name_copy)

    return get_char_list(xml_file_name = original_xml_file_name_copy)

  def backup_se_font_map(se_folder, backup_folder) :

    if not os.path.exists(backup_folder) :
      shutil.copytree(join(se_folder, 'Content\\Fonts'), backup_folder )
    else :
      if not os.listdir(backup_folder) :
        os.rmdir(backup_folder )
        shutil.copytree(join(se_folder, 'Content\\Fonts'), backup_folder )

  def include_text_files(base_folder, text_file_folder) :

    text_files = file_names_in_folder(text_file_folder)
    text_mod_files = [ f for f in text_files if f.endswith('.py') ]
    for f in text_files :
      shutil.copy2(join(text_file_folder, f), join(base_folder, f))
    text_file_modules = [ __import__( f.split('.')[0]) for f in text_mod_files ]

    result = []
    for m in text_file_modules :
      result += distinct(m.text)
    return text_files, distinct(result)

  def check_unsupported_files (base_folder, unsupported_folder) :

    unsupported_files = file_names_in_folder(unsupported_folder)

    for f in unsupported_files :
      shutil.copy2(join(unsupported_folder, f), join(base_folder, f))

    unsupported_file_modules = [ __import__( f.split('.')[0]) for f in unsupported_files ]
    unsupported = {}

    for m in unsupported_file_modules :
      for key, value in m.unsupported_char.items() :
        unsupported[key] = value

    return unsupported_files, unsupported

start_time = timeit.default_timer()
backup_se_font_map(se_folder, backup_folder)
text_original, max_code = get_original_text(base_folder, backup_folder, xml_file_name)
text_files, text_in_files = include_text_files(base_folder, text_file_folder)
unsupported_files, unsupported = check_unsupported_files (base_folder, unsupported_folder)

if not os.path.exists(output_folder) :
  os.mkdir(output_folder)

if not keep_original :
  text = distinct(text_in_files + text_original)
  start_code = 0
else :
  text = list(set(text_in_files).symmetric_difference(text_original))
  start_code = max_code + 1

# generate font map
for c, v in color_dict.items() :

  if v['output'] == True :

    print 'Generate bitmap for %s ...' % c

    if os.path.exists(join(output_folder, c)) :
      shutil.rmtree(join(output_folder, c))

    if not os.path.exists(join(output_folder, c)) :
      os.mkdir(join(output_folder, c))

    if keep_original == True :

      for n in original_dds_file_names :
        shutil.copy2(
          join( backup_folder, c + '\\' + n),
          join( output_folder, c + '\\' + n) )

    original_xml_file_name \
    = os.path.abspath(join( backup_folder, c + '\\' + xml_file_name))

    print 'Done'
    print
    print 'Write bitmap to dds.'

    char_list, target_images \
    = write_text_to_image(
        text = text, color = v, unsupported = unsupported,
        start_code = copy.deepcopy(start_code),
        output_folder = join(output_folder, c),
        image_start_index = len(original_dds_file_names),
        north_margin = north_margin, west_margin = west_margin,
        south_margin = south_margin, east_margin = east_margin )

    print 'Done'
    print
    print 'Generate XML for %s ...'

    produce_xml(char_list, target_images, join(output_folder, c),
      keep_original, original_xml_file_name)

    print 'Done'

print 'All image and XMl generations done.'
print
print 'Cleaning up temp files...'

cleanup( folder_paths = [ base_folder ],
  file_names = text_files + unsupported_files,
  remove_ext_name = ['.pyc', '.png', '.csv', 'original_' + xml_file_name])

print 'Done'
print 'Total run time is %f.' % (timeit.default_timer() - start_time)
