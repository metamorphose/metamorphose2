# -*- coding: utf-8 -*-

# Copyright (C) 2006-2010 ianaré sévi <ianare@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# Contributions:
#
# 2007-01-17
#  _to_alpha function by Gustavo Niemeyer (gustavo@niemeyer.net)


from __future__ import print_function
import wx
import os
import re
import sys
import EXIF
import roman
import time
import locale
import calendar
import utils

from mutagen.asf import ASF
from mutagen.apev2 import APEv2File
from mutagen.flac import FLAC
from mutagen.id3 import ID3FileType
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.oggflac import OggFLAC
from mutagen.oggspeex import OggSpeex
from mutagen.oggtheora import OggTheora
from mutagen.oggvorbis import OggVorbis
from mutagen.trueaudio import TrueAudio
from mutagen.wavpack import WavPack
from mutagen.mp4 import MP4
from mutagen.musepack import Musepack
from mutagen.monkeysaudio import MonkeysAudio
from mutagen.optimfrog import OptimFROG

# Metadata tag translations

AUDIO_INFO = {
    _('title') : "title",
    _('version') : "version",
    _('album') : "album",
    _('track number') : "tracknumber",
    _('artist') : "artist",
    _('genre') : "genre",
    _('performer') : "performer",
    _('date') : "date",
    _('author') : "author",
    _('composer') : "composer",
    _('conductor') : "conductor",
    _('lyricist') : "lyricist",
    _('disc number') : "discnumber",
    _('language') : "language",
    _('encoded by') : "encodedby",
    _('comment') : 'comment',
}

IMAGE_INFO ={
    _(u"width") : u"EXIF ExifImageWidth",
    #_(u"date taken") : u'EXIF DateTimeOriginal',
    #_(u"date modified") : u'Image DateTime',
    _(u"height") : u"EXIF ExifImageLength",
    _(u"exposure") : u"EXIF ExposureTime",
    _(u"F-stop") : u"EXIF FNumber",
    _(u"flash") : u"EXIF Flash",
    _(u"focal-length") : u"EXIF FocalLength",
    _(u"ISO") : u"EXIF ISOSpeedRatings",
    _(u"shutter-speed") : u"EXIF ShutterSpeedValue",
    _(u"copyright") : u"Image Copyright",
    _(u"make") : u"Image Make",
    _(u"model") : u"Image Model",
    _(u"orientation") : u"Image Orientation",
    _(u"unit") : u"Image ResolutionUnit",
    _(u"X-resolution") : u"Image XResolution",
    _(u"Y-resolution") : u"Image YResolution",
    _(u"X-res") : u"Image XResolution",
    _(u"Y-res") : u"Image YResolution",
    _(u"software") : u"Image Software"
}

[wxID_PANEL, wxID_PANELID3, wxID_PANELID3SELECT, wxID_PANELINSDATE,
 wxID_PANELINS_NUM, wxID_PANELINSTIME, wxID_PANELSTATICTEXT1,
 wxID_PANELEXIF, wxID_PANELEXIFSELECT, wxID_PANELFOLDER,
 wxID_PANELFOLDERDEPTH
] = [wx.NewId() for __init_ctrls in range(11)]

class Panel(wx.Panel):
    """"
    Helper panel to some of the operations panels.
    It allows the usage of buttons to insert sub-operations,
    and contains the associated sub-operations.
    """

    def __init_sizer(self):

        mainSizer = self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.staticText1,0,wx.TOP|wx.LEFT,5)

        buttonSizer = self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add(self.ins_num,0,wx.LEFT|wx.ALIGN_CENTER,4)
        buttonSizer.Add(self.insDate,0,wx.LEFT|wx.ALIGN_CENTER,8)
        buttonSizer.Add(self.insTime,0,wx.LEFT|wx.ALIGN_CENTER,8)
        buttonSizer.Add(self.id3select,0,wx.LEFT|wx.ALIGN_CENTER,8)
        buttonSizer.Add(self.EXIFselect,0,wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER,8)
        buttonSizer.Add(self.folder,0,wx.RIGHT|wx.ALIGN_CENTER,2)
        buttonSizer.Add(self.folderDepth,0,wx.RIGHT|wx.ALIGN_CENTER,4)
        mainSizer.Add(buttonSizer,0,wx.EXPAND|wx.TOP,2)
        self.SetSizerAndFit(mainSizer)


    def __init_ctrls(self, prnt, Name):
        wx.Panel.__init__(self, id=wxID_PANEL, name=Name, parent=prnt,
              style=wx.TAB_TRAVERSAL,)

        self.staticText1 = wx.StaticText(id=wxID_PANELSTATICTEXT1,
              label=_(u"Insert a special operation:"), name='staticText1',
              parent=self, style=0)

        self.ins_num = wx.Button(id=wxID_PANELINS_NUM,
              label=_(u"numbering"), name=u'ins_num', parent=self, style=wx.BU_EXACTFIT)
        self.ins_num.SetToolTipString(_(u"Insert enumerating sequence. Use the 'Numbering settings'\npanel to change settings"))
        self.ins_num.Bind(wx.EVT_BUTTON, self._on_number_button,
              id=wxID_PANELINS_NUM)

        self.insDate = wx.Button(id=wxID_PANELINSDATE, label=_(u"date"),
              name=u'insDate', parent=self, style=wx.BU_EXACTFIT)
        self.insDate.SetToolTipString(_(u"Insert date. Use the 'Date / Time settings' panel to\nchange settings"))
        self.insDate.Bind(wx.EVT_BUTTON, self._on_date_button,
              id=wxID_PANELINSDATE)

        self.insTime = wx.Button(id=wxID_PANELINSTIME, label=_(u"time"),
              name=u'insTime', parent=self, style=wx.BU_EXACTFIT)
        self.insTime.SetToolTipString(_(u"Insert time. Use the 'Date / Time settings' panel to\nchange settings"))
        self.insTime.Bind(wx.EVT_BUTTON, self._on_time_button,
              id=wxID_PANELINSTIME)

        self.id3select = wx.Choice(choices=[
            _(u"audio info"),
            _('artist'),
            _('album'),
            _('disc number'),
            _('track number'),
            _('title'),
            _('genre'),
            _('performer'),
            _('date'),
            _('author'),
            _('composer'),
            _('conductor'),
            _('lyricist'),
            _('comment'),
            #_('version'),
            #_('language'),
            #_('encoded by'),
            ],
              id=wxID_PANELID3SELECT, name=u'id3select', parent=self)
        self.id3select.SetSelection(0)
        self.id3select.SetToolTipString(_(u"Insert id3 tag information from mp3 file"))
        self.id3select.Bind(wx.EVT_CHOICE, self._on_id3, id=wxID_PANELID3SELECT)

        self.EXIFselect = wx.Choice(choices=[
              _(u"image info"),
              #_(u"date taken"),
              #_(u"date modified"),
              _(u"width"),
              _(u"height"),
              _(u"width")+u":x:"+_(u"height"),
              _(u"X-resolution"),
              _(u"Y-resolution"),
              _(u"X-res")+u":x:"+_(u"Y-res"),
              _(u"orientation"),
              _(u"exposure"),
              _(u"F-stop"),
              _(u"flash"),
              _(u"focal-length"),
              _(u"ISO"),
              _(u"shutter-speed"),
              _(u"copyright"),
              _(u"make"),
              _(u"model"),
              _(u"unit"),
              _(u"software")],
              id=wxID_PANELEXIFSELECT, name=u'EXIFselect', parent=self,
              size=wx.Size(128, -1))
        self.EXIFselect.SetSelection(0)
        self.EXIFselect.SetToolTipString(_(u"Insert Exif tag information from tiff or jpeg file.\nUse the date button to insert Exif date"))
        self.EXIFselect.Bind(wx.EVT_CHOICE, self._on_exif, id=wxID_PANELEXIFSELECT)

        self.folder = wx.Button(id=wxID_PANELFOLDER, label=_(u"folder:"),
            name=u'folder', parent=self, style=wx.BU_EXACTFIT)
        self.folder.SetToolTipString(_(u"Insert parent folder name"))
        self.folder.Bind(wx.EVT_BUTTON, self._on_folder_button, id=wxID_PANELFOLDER)

        self.folderDepth = wx.SpinCtrl(id=wxID_PANELFOLDERDEPTH,
              initial=1, max=999, min=1, name=u'folderDepth',
              parent=self, pos=wx.Point(200, 104), size=wx.Size(50, -1),
              value='1', style=wx.SP_ARROW_KEYS)
        self.folderDepth.SetValue(1)
        self.folderDepth.SetToolTipString(_(u"How far back to get folder"))


    def __init__(self, prnt, main_window, name=u'opButtonsPanel'):
        global main
        main = main_window
        self.parent = prnt
        self.__init_ctrls(prnt, name)

        # adjust button sizes
        utils.adjust_exact_buttons(self)

        self.__init_sizer()
        self.counter = 0
        self.auxCount = 0

#### BUTTONS ##################################################################
    def _insert_text(self,txt):
        if self.parent.activatedField:
            txt = u":" + txt + u":"
            iPoint = self.parent.activatedField.GetInsertionPoint()
            self.parent.activatedField.WriteText(txt)
            self.parent.activatedField.SetFocus()
            self.parent.activatedField.SetInsertionPoint(iPoint + len(txt))

    def _on_number_button(self, event):
        self._insert_text(_(u"numb"))

    def _on_date_button(self, event):
        self._insert_text(_(u"date"))

    def _on_time_button(self, event):
        self._insert_text(_(u"time"))

    def _on_id3(self, event):
        if self.id3select.GetSelection() != 0:
            self._insert_text(self.id3select.GetStringSelection())
            self.id3select.SetSelection(0)

    def _on_exif(self, event):
        if self.EXIFselect.GetSelection() != 0:
            self._insert_text(self.EXIFselect.GetStringSelection())
            self.EXIFselect.SetSelection(0)

    def _on_folder_button(self, event):
        self._insert_text(_(u"folder%s")%self.folderDepth.GetValue())


#### FOLDER ###################################################################
    def _add_folder(self,file, depth):
        splitPath = file.split(os.sep)
        try:
            folder = splitPath[-(int(depth)+1)]
        except (ValueError,IndexError):
            return ''
        else:
            return folder


#### NUMBERING ################################################################
    def _to_alpha(self,i):
        s = ''
        while i:
            i -= 1
            q, m = divmod(i, 26)
            s = chr(97+m)+s
            i = q
        return s

    def enumber(self, file, operation):
        numberStyle = operation.numberingPanel.Style
        numberParams = operation.numberingPanel.Params
        start = numberParams[0]
        count = numberParams[1]
        reset = numberParams[2]
        dirReset = numberParams[3]
        countByDir = numberParams[4]
        repeat = numberParams[5]
        maxNumb = numberParams[6]

        # XXX TODO incorporate into params
        incrementOnDiff = operation.numberingPanel.incrementOnDiff.GetValue()

        lastDir = main.lastDir
        curDir = main.curDir
        lastName = main.lastName
        curName = main.curName

        #print lastName, curName

        maxNumb = abs((len(main.items) + (start-1))*count)
        if repeat > 0:
            maxNumb = maxNumb / (repeat+1)

        # to reset count by directory
        if lastDir != curDir and lastDir is not False and dirReset:
            self.counter = 0
        if lastDir != curDir and lastDir is not False and countByDir:
            self.counter += 1
        # to reset by identical name
        if incrementOnDiff and curName is not False and lastName != curName:
            self.counter = 0
            #if True:
            #    return u''


        # calculate current number based on user settings:
        i = start + (self.counter*int(count))

        # numerical counting:
        if numberStyle[0] == u'digit':
            padChar = unicode(numberStyle[1])
            # padding enabled and non-empty pad charcter:
            if numberStyle[3] and padChar:
                if numberStyle[2] == u'auto':
                    padWidth = len(unicode(maxNumb))
                    y = unicode(i).rjust(padWidth, padChar)
                else:
                    y = unicode(i).rjust(int(numberStyle[2]), padChar)
            # no padding:
            else:
                y = i

        # alphabetical numbering:
        elif numberStyle[0] == u'alpha':
            i = abs(i)

            if i == 0:
                i = 1
            y = self._to_alpha(i)
            # uppercase
            if numberStyle[1]:
                y = y.upper()

        # roman numerals
        elif numberStyle[0] == u'roman':
            try:
                y = roman.toRoman(i)
                if not numberStyle[1]:
                    y = y.lower()
            except:
                if main.bad.count(main.ec) < 1:
                    main.bad.append(main.ec)
                    main.errorLog.insert(0,(main.ec,file,
                                            _(u"Roman numeral error: %s")%sys.exc_info()[1],
                                            u'bad'))
                y = ""

        def increment_reset_count():
            # see if count is at reset level:
            if  self.counter == reset and self.counter != 0:
                self.counter = 0
            elif not countByDir:
                self.counter += 1

        # repeat the same number
        if repeat > 0:
            if self.auxCount == repeat:
                increment_reset_count()
                self.auxCount = 0
            elif self.auxCount < repeat:
                self.auxCount += 1
            else:
                self.auxCount = 0
        else:
            increment_reset_count()

        return unicode(y)


#### DATE AND TIME ############################################################
    def _get_exif_date(self, path, tag):
        ext = os.path.splitext(path)[1][1:].lower()
        if re.match('tif|tiff|jpg|jpeg|jtif|thm', ext, re.IGNORECASE):
            try:
                file = open(path,'rb')
            except IOError:
                utils.add_to_errors(main,path,_(u"Could not open file!"))
            else:
                tags = EXIF.process_file(file, details=False, stop_tag=tag)
                # see if the tag exists
                if tags.has_key(tag):
                    try:
                        itemDateTime = str(tags[tag])
                        itemDateTime = re.compile(r'\D').split(itemDateTime)
                        itemDateTime = map(int, itemDateTime)
                    except ValueError, err:
                        utils.add_to_warnings(main,path,_(u"Exif error: %s")%err)
                        return False

                    # attempt to convert tag's text to a date
                    try:
                        dayWeek = calendar.weekday(itemDateTime[0],
                                                   itemDateTime[1],
                                                   itemDateTime[2])
                    # invalid date
                    except ValueError, err:
                        utils.add_to_warnings(main,path,_(u"Exif error: %s")%err)
                    else:
                        itemDateTime.extend([dayWeek, 1, 0])
                        return itemDateTime
                # date tag doesn't exist
                else:
                    utils.add_to_warnings(main,path,_(u"Could not read Exif tag"))
                    return False


    def _date_time(self, op, path, operation):
        dateTimePanel = operation.dateTimePanel
        dateTime = dateTimePanel.dateTime
        dateTime[1] = dateTimePanel.dateTestDisplay.GetLabel()
        dateTime[2] = dateTimePanel.timeTestDisplay.GetLabel()

        # user specified date/time
        if not dateTime[0]:
            return dateTime[op+1]

        # get date/time from item
        else:
            itemTimeType = dateTimePanel.itemTimeType.GetSelection()
            if itemTimeType == 0:
                try: itemDateTime = time.localtime(os.path.getctime(path))
                except WindowsError: return ''
            elif itemTimeType == 1:
                try: itemDateTime = time.localtime(os.path.getmtime(path))
                except WindowsError: return ''
            elif itemTimeType == 2:
                try: itemDateTime = time.localtime(os.path.getatime(path))
                except WindowsError: return ''
            elif itemTimeType == 3:
                itemDateTime = self._get_exif_date(path, 'EXIF DateTimeOriginal')
            elif itemTimeType == 4:
                itemDateTime = self._get_exif_date(path, 'Image DateTime')

            if itemDateTime:
                return utils.udate(main, dateTime[op+1],itemDateTime)
            else:
                return ''


#### IMAGE METADATA ############################################################
    def get_image_tag(self, path, EXIFtags, command):
        tag = IMAGE_INFO[command]

        if EXIFtags.has_key(tag):
            '''
            if tag == u'EXIF DateTimeOriginal':
                print self._get_exif_date(path, tag)
                itemDateTime = self._get_exif_date(path, tag)
            elif tag == u'Image DateTime':
                itemDateTime = self._get_exif_date(path, tag)
            else:
            '''
            return unicode(EXIFtags[tag])
        else:
            utils.add_to_warnings(main, path, _(u"Could not read Exif tag"))


#### AUDIO METADATA ############################################################
    # (based on 'File' function from mutagen/__init__.py)
    def _get_audio_metadata(self, filename, options=None):
        """Guess the type of the file and try to open it.

        The file type is decided by several things, such as the first 128
        bytes (which usually contains a file type identifier), the
        filename extension, and the presence of existing tags.

        If no appropriate type could be found, None is returned.
        """

        if options is None:
            options = [MP3, TrueAudio, OggTheora, OggSpeex, OggVorbis, OggFLAC,
                       FLAC, APEv2File, MP4, ID3FileType, WavPack, Musepack,
                       MonkeysAudio, OptimFROG, ASF]

        if not options:
            return None

        try:
            fileobj = file(filename, "rb")
        except IOError:
            utils.add_to_errors(main,filename,_(u"Could not open file!"))
            return None

        try:
            header = fileobj.read(128)
            # Sort by name after score. Otherwise import order affects
            # Kind sort order, which affects treatment of things with
            # equals scores.
            results = [(Kind.score(filename, fileobj, header), Kind.__name__)
                       for Kind in options]
        finally:
            fileobj.close()
        results = zip(results, options)
        results.sort()
        (score, name), Kind = results[-1]
        if score > 0:
            if Kind.__name__ == 'MP3':
                Kind = EasyID3
            try:
                audioMetadata = Kind(filename)
            except:
                utils.add_to_errors(main,filename,_(u"Could not read audio metadata"))
                return None
            if main.debug:
                print(audioMetadata)
            return audioMetadata
        else:
            utils.add_to_warnings(main,filename,_(u"Could not determine audio file type"))
            return None


    def get_audio_tag(self, audioMetadata, command):
        tag = AUDIO_INFO[command]
        print(tag)
        path = audioMetadata.filename
        if audioMetadata.has_key(tag):
            value = audioMetadata[tag][0]
            encoding = main.prefs.get('encodingSelect')
            if str(encoding) != str(locale.getlocale()[1]):
                try:
                    # incorrect encodings should default to latin-1
                    # allow forcing an encoding type from preferences
                    value = value.encode('latin-1').decode(encoding)
                except:
                    utils.add_to_warnings(main, path, _(u"Invalid encoding specified: %s")%encoding)
            if tag == "tracknumber" and len(value) == 1:
                value = "0" + value
            return value
        else:
            utils.add_to_warnings(main, path, _(u"Could not read tag: %s")%command)
            return False


#### PARSE INPUT AND FORMAT ###################################################
    
    def parse_input(self, text, file, operation):
        """
        Parse the active fields for sub operations and return
        the corresponding result in place.
        """
        ext = os.path.splitext(file)[1][1:]
        # possible special operations:
        commands = [_(u"numb"),_(u"date"),_(u"time"),_(u"folder")]

        # audio
        audioInfoStart = len(commands)
        for i in AUDIO_INFO.keys():
            commands.append(i)
        audioInfoEnd = len(commands)

        # Exif
        for i in IMAGE_INFO.keys():
            commands.append(i)

        parsedText = u''

        # any text in between this character will be considered an operation:
        text = text.strip(u':').split(u':')

        isImage = re.match('tif|tiff|jpg|jpeg|jtif|thm', ext, re.IGNORECASE)
        isAudio = re.match('ape|asf|flac|m4a|mp3|mp4|ogg', ext, re.IGNORECASE)
        audioMetadata = False

        # process here to load Exif metadata only once
        if isImage:
            for segment in text:
                if segment in commands[10:]:
                    file_rb = open(file, 'rb')
                    imageMetadata = EXIF.process_file(file_rb, details=False)
                    break

        # process here to load audio metadata only once
        elif isAudio:
            for segment in text:
                if segment in commands[audioInfoStart:audioInfoEnd]:
                    audioMetadata = self._get_audio_metadata(file)
                    break

        # execute functions based on user input:
        for segment in text:
            value = False
            # numbering
            if segment == commands[0]:
                value = self.enumber(file,operation)
            # date
            elif segment == commands[1]:
                value = self._date_time(0,file,operation)
            # time
            elif segment == commands[2]:
                value = self._date_time(1,file,operation)
            # folder name
            elif segment[:len(commands[3])] == commands[3]:
                value = self._add_folder(file, segment[len(commands[3]):])
            # audio
            elif isAudio and audioMetadata and segment in commands[audioInfoStart:audioInfoEnd]:
                value = self.get_audio_tag(audioMetadata, segment)
            # EXIF
            elif isImage and segment in commands[audioInfoEnd+1:]:
                value = self.get_image_tag(file, imageMetadata, segment)
            # if segment doesn't match a command, reprint segment:
            else:
                parsedText += segment

            if value:
                parsedText += value

        return parsedText
