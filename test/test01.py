#!/usr/bin/python
# vim: set ts=2 expandtab:
"""
Module: test01.py
Desc: Test to draw info out of poker image.
Author: John O'Neil
Email: oneil.john@gmail.com
DATE: Saturday, Sept 21st 2014

  Simple test to draw info from poker image.
  Image and required info is in /test subfolder.

"""

import os
import sys
import subimage.find_by_ar as ar
import subimage.find_subimage as si
import cv2

def contains_subimage(img, subimage_filename):
  subimage = cv2.imread(subimage_filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)
  hits = si.find_subimages(img, subimage, confidence=0.70)
  if hits:
    return True
  return False

def get_suit(img):
  if contains_subimage(img, 'heart.png'):
    return 'heart'
  if contains_subimage(img, 'diamond.png'):
    return 'diamond'
  if contains_subimage(img, 'club.png'):
    return 'club'
  if contains_subimage(img, 'spade.png'):
    return 'spade'
  return 'unknown'

def get_value(img):
  if contains_subimage(img, '2.png'):
    return '2'
  if contains_subimage(img, '6.png'):
    return '6'
  if contains_subimage(img, '7.png'):
    return '7'
  if contains_subimage(img, '8.png'):
    return '8'
  if contains_subimage(img, 'a.png'):
    return 'ace'
  #hmm. Jack requires confidence level 0.7 to detect. Don't quite know why.
  if contains_subimage(img, 'j.png'):
    return 'jack'
  if contains_subimage(img, 'k.png'):
    return 'king'
  return 'unknown'


def main():
  if not os.path.exists('poker.jpg'):
    print 'ERROR: This is a simple test meant to be run on local files. Please run from the subimage/test directory.'
    sys.exit(-1)

  img = cv2.imread('poker.jpg', cv2.CV_LOAD_IMAGE_GRAYSCALE)
  cards = ar.find_by_ar(img, 0.7, 0.02,min_height=100,min_width=50)
  if not cards:
    print 'Sorry, couldn\'t find any cards in the provided image.'
    sys.error(-1)
  for card in cards:
    #try to find what suit this card is
    subsection = img[card.box]
    subsection = subsection * card.mask
    suit = get_suit(subsection)
    value = get_value(subsection)
    print 'Card found at ' + str(card.x) +','+ str(card.y)+': ' + suit + ' ' + value 


if __name__ == '__main__':
  main()
