#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# python
# -----------------------------------------------------------------------------
# python version is: 3.5.3
# -----------------------------------------------------------------------------
import sys
print('python version is: ' + sys.version)

# -----------------------------------------------------------------------------
# to do
# -----------------------------------------------------------------------------
todo = [
"extract metadata from mp4 and other video format",
"extract metadata from mp3 and other audio format",
"extract metadata from epub and other electronic books format",
"done! : extract metadata from srt and other subtitles format to get the language",
"find duplicate files",
"find orphean files (i.e.: srt without mp4, idx without sub, etc)"
]


# -----------------------------------------------------------------------------
# import
# -----------------------------------------------------------------------------
import string
import struct
import os
import hashlib
import time
import magic
import shutil
import operator
from math import sqrt


#------------------------------------------------------------------------------
# name:     defktlg_filepaths
# version:  1.0
# date:     20170603
#--------
# param_media_name :     path to the media
#--------
# return list of full path of all files on a media
#------------------------------------------------------------------------------
def defktlg_filepaths(param_media_name):

    #get all full path file in the media into tmp_paths list
    tmp_paths = []
    for root, directories, files in os.walk(ktlg_path_media + "/" + param_media_name):
        for file in files:
            tmp_path = os.path.join(root, file)
            tmp_paths.append(tmp_path)

    #inventaire des fichiers
    tmp_paths.sort()
    tmp_paths_undef = []

    #explose le contenu du media en categories/fichiers definies dans cfg
    for category, filetypes in ktlg_dico_filetypes.items():

        output_category = open(ktlg_path_xml + "/" + ktlg_media_id + "/" + category + ".data", "w")

        for filetype in filetypes:

            tmp_paths_undef.clear()
            tmp_paths_undef = list(tmp_paths)
            tmp_paths.clear()

            for file in tmp_paths_undef:
                if file.lower().endswith("." + filetype.lower()):
                    output_category.write("%s\n" % file)
                else:
                    tmp_paths.append(file)

        output_category.close()

    # output tous les fichiers inconnus
    tmp_paths_undef = []
    for file in tmp_paths:

        tmp_file = os.path.split(file)[1]
        tmp_filetype = os.path.splitext(tmp_file)[1]

        tmp_paths_undef.append(tmp_filetype.lower() + ' -> ' + file)
    tmp_paths_undef.sort()

    output_category = open(ktlg_path_xml + "/" + ktlg_media_id + "/undef.data", "w")
    for file in tmp_paths_undef:
        output_category.write("%s\n" % file)
    output_category.close()

    return 1

#------------------------------------------------------------------------------
# name:     defktlg_createdir
# version:  1.0
# date:     20170602
#--------
# param_dir : path of the folder to create
#--------
# create a directory in param_dir (if not exists)
#------------------------------------------------------------------------------
def defktlg_createdir(param_dir):
    if not os.path.isdir(param_dir):
        os.mkdir(param_dir)
    return param_dir

#------------------------------------------------------------------------------
# name:     defktlg_cfg
# version:  1.1
# date:     20170602
#--------
# param_type :  type of data to extract from configuration file
#--------
# Create the config file if it does not exists
# get the data from the config file
#------------------------------------------------------------------------------
def defktlg_cfg(param_type):

    if not os.path.isfile(ktlg_path_cfg + "/katalog.cfg"):
        tmp_file = open(ktlg_path_cfg + "/katalog.cfg", "w")
        #filetype the program is able to manage.
        #audio:     mp3 / Podcasts
        #books:     ePubs
        #subtitles: subtitles for video
        #video:     Movies, series, documentaries, conferences
        #special:   Covers for mp3/mp4/epub, etc...
        tmp_file.write("filetype:audio:mp3,ac3\n")
        tmp_file.write("filetype:books:epub,pdf\n")
        tmp_file.write("filetype:special:kid,card,jpg,txt\n")
        tmp_file.write("filetype:subtitles:srt,idx,sub\n")
        tmp_file.write("filetype:video:mp4,avi,mkv,rmvb,ts,flv,m4v\n")
        #definition for the VIDEO. XML/sql at once
        tmp_file.write("xml:video:movie_ID,             int(10) unsigned NOT NULL AUTO_INCREMENT\n")
        tmp_file.write("xml:video:movie_path,           varchar(128) NOT NULL\n")
        tmp_file.write("xml:video:movie_file,           varchar(128) NOT NULL\n")
        tmp_file.write("xml:video:movie_filetype,       varchar(8) NOT NULL\n")
        tmp_file.write("xml:video:movie_filesize,       bigint(20) unsigned DEFAULT NULL\n")
        tmp_file.write("xml:video:movie_source,         varchar(16) DEFAULT NULL\n")
        tmp_file.write("xml:video:movie_time,           time DEFAULT NULL\n")
        tmp_file.write("xml:video:movie_width,          smallint(5) unsigned DEFAULT NULL\n")
        tmp_file.write("xml:video:movie_height,         smallint(5) unsigned DEFAULT NULL\n")
        tmp_file.write("xml:video:movie_lang_vo,        varchar(16) NOT NULL\n")
        tmp_file.write("xml:video:movie_vo_subtitles,   varchar(16) NOT NULL\n")
        tmp_file.write("xml:video:movie_fr_subtitles,   varchar(16) NOT NULL\n")
        tmp_file.write("xml:video:movie_rating,         tinyint(5) unsigned DEFAULT NULL\n")
        tmp_file.write("xml:video:serie_name,           varchar(64) NOT NULL\n")
        tmp_file.write("xml:video:movie_season,         tinyint(3) unsigned DEFAULT NULL\n")
        tmp_file.write("xml:video:movie_episode,        tinyint(3) unsigned DEFAULT NULL\n")
        tmp_file.write("xml:video:movie_title_vo,       varchar(64) NOT NULL\n")
        tmp_file.write("xml:video:movie_subtitle_vo,    varchar(64) NOT NULL\n")
        tmp_file.write("xml:video:movie_title_fr,       varchar(64) NOT NULL\n")
        tmp_file.write("xml:video:movie_subtitle_fr,    varchar(64) NOT NULL\n")
        tmp_file.write("xml:video:movie_year,           year(4) DEFAULT NULL\n")
        tmp_file.write("xml:video:movie_country,        varchar(32) NOT NULL\n")
        tmp_file.write("xml:video:movie_type,           varchar(32) NOT NULL\n")
        tmp_file.write("xml:video:movie_genre,          varchar(32) NOT NULL\n")
        tmp_file.write("xml:video:movie_subgenre,       varchar(32) NOT NULL\n")
        tmp_file.write("xml:video:movie_comment,        varchar(64) NOT NULL\n")
        tmp_file.write("xml:video:movie_jpg,            varchar(128) NOT NULL\n")
        #ISO code for languages in sub/idx files
        tmp_file.write("iso639:aa,Afar\n")
        tmp_file.write("iso639:ab,Abkhazian\n")
        tmp_file.write("iso639:ae,Avestan\n")
        tmp_file.write("iso639:af,Afrikaans\n")
        tmp_file.write("iso639:am,Amharic\n")
        tmp_file.write("iso639:an,Aragonese\n")
        tmp_file.write("iso639:ar,Arabic\n")
        tmp_file.write("iso639:as,Assamese\n")
        tmp_file.write("iso639:ay,Aymara\n")
        tmp_file.write("iso639:az,Azerbaijani\n")
        tmp_file.write("iso639:ba,Bashkir\n")
        tmp_file.write("iso639:be,Belarusian\n")
        tmp_file.write("iso639:bg,Bulgarian\n")
        tmp_file.write("iso639:bh,Bihari\n")
        tmp_file.write("iso639:bi,Bislama\n")
        tmp_file.write("iso639:bn,Bengali\n")
        tmp_file.write("iso639:bo,Tibetan\n")
        tmp_file.write("iso639:br,Breton\n")
        tmp_file.write("iso639:bs,Bosnian\n")
        tmp_file.write("iso639:ca,Catalan\n")
        tmp_file.write("iso639:ce,Chechen\n")
        tmp_file.write("iso639:ch,Chamorro\n")
        tmp_file.write("iso639:co,Corsican\n")
        tmp_file.write("iso639:cs,Czech\n")
        tmp_file.write("iso639:cu,Slavonic\n")
        tmp_file.write("iso639:cv,Chuvash\n")
        tmp_file.write("iso639:cy,Welsh\n")
        tmp_file.write("iso639:da,Danish\n")
        tmp_file.write("iso639:de,German\n")
        tmp_file.write("iso639:dv,Divehi\n")
        tmp_file.write("iso639:dz,Dzongkha\n")
        tmp_file.write("iso639:el,Greek\n")
        tmp_file.write("iso639:en,English\n")
        tmp_file.write("iso639:eo,Esperanto\n")
        tmp_file.write("iso639:es,Spanish\n")
        tmp_file.write("iso639:et,Estonian\n")
        tmp_file.write("iso639:eu,Basque\n")
        tmp_file.write("iso639:fa,Persian\n")
        tmp_file.write("iso639:fi,Finnish\n")
        tmp_file.write("iso639:fj,Fijian\n")
        tmp_file.write("iso639:fo,Faroese\n")
        tmp_file.write("iso639:fr,French\n")
        tmp_file.write("iso639:fy,Western Frisian\n")
        tmp_file.write("iso639:ga,Irish\n")
        tmp_file.write("iso639:gd,Gaelic\n")
        tmp_file.write("iso639:gl,Galician\n")
        tmp_file.write("iso639:gn,Guarani\n")
        tmp_file.write("iso639:gu,Gujarati\n")
        tmp_file.write("iso639:gv,Manx\n")
        tmp_file.write("iso639:ha,Hausa\n")
        tmp_file.write("iso639:he,Hebrew\n")
        tmp_file.write("iso639:hi,Hindi\n")
        tmp_file.write("iso639:ho,Hiri Motu\n")
        tmp_file.write("iso639:hr,Croatian\n")
        tmp_file.write("iso639:ht,Haitian\n")
        tmp_file.write("iso639:hu,Hungarian\n")
        tmp_file.write("iso639:hy,Armenian\n")
        tmp_file.write("iso639:hz,Herero\n")
        tmp_file.write("iso639:ia,Interlingua\n")
        tmp_file.write("iso639:id,Indonesian\n")
        tmp_file.write("iso639:ie,Interlingue\n")
        tmp_file.write("iso639:ii,Sichuan Yi\n")
        tmp_file.write("iso639:ik,Inupiaq\n")
        tmp_file.write("iso639:io,Ido\n")
        tmp_file.write("iso639:is,Icelandic\n")
        tmp_file.write("iso639:it,Italian\n")
        tmp_file.write("iso639:iu,Inuktitut\n")
        tmp_file.write("iso639:ja,Japanese\n")
        tmp_file.write("iso639:jv,Javanese\n")
        tmp_file.write("iso639:ka,Georgian\n")
        tmp_file.write("iso639:ki,Kikuyu\n")
        tmp_file.write("iso639:kj,Kuanyama\n")
        tmp_file.write("iso639:kk,Kazakh\n")
        tmp_file.write("iso639:kl,Kalaallisut\n")
        tmp_file.write("iso639:km,Khmer\n")
        tmp_file.write("iso639:kn,Kannada\n")
        tmp_file.write("iso639:ko,Korean\n")
        tmp_file.write("iso639:ks,Kashmiri\n")
        tmp_file.write("iso639:ku,Kurdish\n")
        tmp_file.write("iso639:kv,Komi\n")
        tmp_file.write("iso639:kw,Cornish\n")
        tmp_file.write("iso639:ky,Kirghiz\n")
        tmp_file.write("iso639:la,Latin\n")
        tmp_file.write("iso639:lb,Luxembourgish\n")
        tmp_file.write("iso639:li,Limburgan\n")
        tmp_file.write("iso639:ln,Lingala\n")
        tmp_file.write("iso639:lo,Lao\n")
        tmp_file.write("iso639:lt,Lithuanian\n")
        tmp_file.write("iso639:lv,Latvian\n")
        tmp_file.write("iso639:mg,Malagasy\n")
        tmp_file.write("iso639:mh,Marshallese\n")
        tmp_file.write("iso639:mi,Maori\n")
        tmp_file.write("iso639:mk,Macedonian\n")
        tmp_file.write("iso639:ml,Malayalam\n")
        tmp_file.write("iso639:mn,Mongolian\n")
        tmp_file.write("iso639:mo,Moldavian\n")
        tmp_file.write("iso639:mr,Marathi\n")
        tmp_file.write("iso639:ms,Malay\n")
        tmp_file.write("iso639:mt,Maltese\n")
        tmp_file.write("iso639:my,Burmese\n")
        tmp_file.write("iso639:na,Nauru\n")
        tmp_file.write("iso639:nb,Norwegian Bokmal\n")
        tmp_file.write("iso639:nd,Ndebele\n")
        tmp_file.write("iso639:ne,Nepali\n")
        tmp_file.write("iso639:ng,Ndonga\n")
        tmp_file.write("iso639:nl,Dutch\n")
        tmp_file.write("iso639:nn,Norwegian Nynorsk\n")
        tmp_file.write("iso639:no,Norwegian\n")
        tmp_file.write("iso639:nr,Ndebele\n")
        tmp_file.write("iso639:nv,Navaho\n")
        tmp_file.write("iso639:ny,Nyanja\n")
        tmp_file.write("iso639:oc,Occitan\n")
        tmp_file.write("iso639:om,Oromo\n")
        tmp_file.write("iso639:or,Oriya\n")
        tmp_file.write("iso639:os,Ossetian\n")
        tmp_file.write("iso639:pa,Panjabi\n")
        tmp_file.write("iso639:pi,Pali\n")
        tmp_file.write("iso639:pl,Polish\n")
        tmp_file.write("iso639:ps,Pushto\n")
        tmp_file.write("iso639:pt,Portuguese\n")
        tmp_file.write("iso639:qu,Quechua\n")
        tmp_file.write("iso639:rm,Raeto-Romance\n")
        tmp_file.write("iso639:rn,Rundi\n")
        tmp_file.write("iso639:ro,Romanian\n")
        tmp_file.write("iso639:ru,Russian\n")
        tmp_file.write("iso639:rw,Kinyarwanda\n")
        tmp_file.write("iso639:sa,Sanskrit\n")
        tmp_file.write("iso639:sc,Sardinian\n")
        tmp_file.write("iso639:sd,Sindhi\n")
        tmp_file.write("iso639:se,Northern Sami\n")
        tmp_file.write("iso639:sg,Sango\n")
        tmp_file.write("iso639:si,Sinhala\n")
        tmp_file.write("iso639:sk,Slovak\n")
        tmp_file.write("iso639:sl,Slovenian\n")
        tmp_file.write("iso639:sm,Samoan\n")
        tmp_file.write("iso639:sn,Shona\n")
        tmp_file.write("iso639:so,Somali\n")
        tmp_file.write("iso639:sq,Albanian\n")
        tmp_file.write("iso639:sr,Serbian\n")
        tmp_file.write("iso639:ss,Swati\n")
        tmp_file.write("iso639:st,Sotho\n")
        tmp_file.write("iso639:su,Sundanese\n")
        tmp_file.write("iso639:sv,Swedish\n")
        tmp_file.write("iso639:sw,Swahili\n")
        tmp_file.write("iso639:ta,Tamil\n")
        tmp_file.write("iso639:te,Telugu\n")
        tmp_file.write("iso639:tg,Tajik\n")
        tmp_file.write("iso639:th,Thai\n")
        tmp_file.write("iso639:ti,Tigrinya\n")
        tmp_file.write("iso639:tk,Turkmen\n")
        tmp_file.write("iso639:tl,Tagalog\n")
        tmp_file.write("iso639:tn,Tswana\n")
        tmp_file.write("iso639:to,Tonga\n")
        tmp_file.write("iso639:tr,Turkish\n")
        tmp_file.write("iso639:ts,Tsonga\n")
        tmp_file.write("iso639:tt,Tatar\n")
        tmp_file.write("iso639:tw,Twi\n")
        tmp_file.write("iso639:ty,Tahitian\n")
        tmp_file.write("iso639:ug,Uighur\n")
        tmp_file.write("iso639:uk,Ukrainian\n")
        tmp_file.write("iso639:ur,Urdu\n")
        tmp_file.write("iso639:uz,Uzbek\n")
        tmp_file.write("iso639:vi,Vietnamese\n")
        tmp_file.write("iso639:vo,Volapuk\n")
        tmp_file.write("iso639:wa,Walloon\n")
        tmp_file.write("iso639:wo,Wolof\n")
        tmp_file.write("iso639:xh,Xhosa\n")
        tmp_file.write("iso639:yi,Yiddish\n")
        tmp_file.write("iso639:yo,Yoruba\n")
        tmp_file.write("iso639:za,Zhuang\n")
        tmp_file.write("iso639:zh,Chinese\n")
        tmp_file.write("iso639:zu,Zulu\n")
        #theorical frequency to guess the language of a SRT file
        tmp_file.write("frequency:   :    en ,    fr ,    de ,    es ,    it ,    pt \n")
        tmp_file.write("frequency: a :  8.34 ,  8.13 ,  5.58 , 11.72 , 10.85 , 12.21 \n")
        tmp_file.write("frequency: b :  1.54 ,  0.93 ,  1.96 ,  1.49 ,  1.05 ,  1.01 \n")
        tmp_file.write("frequency: c :  2.73 ,  3.15 ,  3.16 ,  3.87 ,  4.30 ,  3.35 \n")
        tmp_file.write("frequency: d :  4.14 ,  3.55 ,  4.98 ,  4.67 ,  3.39 ,  4.21 \n")
        tmp_file.write("frequency: e : 12.60 , 15.10 , 16.93 , 13.72 , 11.49 , 13.19 \n")
        tmp_file.write("frequency: f :  2.03 ,  0.96 ,  1.49 ,  0.69 ,  1.01 ,  1.07 \n")
        tmp_file.write("frequency: g :  1.92 ,  0.97 ,  3.02 ,  1.00 ,  1.65 ,  1.08 \n")
        tmp_file.write("frequency: h :  6.11 ,  1.08 ,  4.98 ,  1.18 ,  1.43 ,  1.22 \n")
        tmp_file.write("frequency: i :  6.71 ,  6.94 ,  8.02 ,  5.25 , 10.18 ,  5.49 \n")
        tmp_file.write("frequency: j :  0.23 ,  0.71 ,  0.24 ,  0.52 ,  0    ,  0.30 \n")
        tmp_file.write("frequency: k :  0.87 ,  0.16 ,  1.32 ,  0.11 ,  0    ,  0.13 \n")
        tmp_file.write("frequency: l :  4.24 ,  5.68 ,  3.60 ,  5.24 ,  5.70 ,  3.00 \n")
        tmp_file.write("frequency: m :  2.53 ,  3.23 ,  2.55 ,  3.08 ,  2.87 ,  5.07 \n")
        tmp_file.write("frequency: n :  6.80 ,  6.42 , 10.53 ,  6.83 ,  7.02 ,  5.02 \n")
        tmp_file.write("frequency: o :  7.70 ,  5.27 ,  2.24 ,  8.44 ,  9.97 , 10.22 \n")
        tmp_file.write("frequency: p :  1.66 ,  3.03 ,  0.67 ,  2.89 ,  2.96 ,  3.01 \n")
        tmp_file.write("frequency: q :  0.09 ,  0.89 ,  0.02 ,  1.11 ,  0.45 ,  1.10 \n")
        tmp_file.write("frequency: r :  5.68 ,  6.43 ,  6.89 ,  6.41 ,  6.19 ,  6.73 \n")
        tmp_file.write("frequency: s :  6.11 ,  7.91 ,  6.42 ,  7.20 ,  5.48 ,  7.35 \n")
        tmp_file.write("frequency: t :  9.37 ,  7.11 ,  5.79 ,  4.60 ,  6.97 ,  5.07 \n")
        tmp_file.write("frequency: u :  2.85 ,  6.05 ,  3.83 ,  4.55 ,  3.16 ,  4.46 \n")
        tmp_file.write("frequency: v :  1.06 ,  1.83 ,  0.84 ,  1.05 ,  1.75 ,  1.72 \n")
        tmp_file.write("frequency: w :  2.34 ,  0.04 ,  1.78 ,  0.04 ,  0    ,  0.05 \n")
        tmp_file.write("frequency: x :  0.20 ,  0.42 ,  0.05 ,  0.14 ,  0    ,  0.28 \n")
        tmp_file.write("frequency: y :  2.04 ,  0.19 ,  0.05 ,  1.09 ,  0    ,  0.04 \n")
        tmp_file.write("frequency: z :  0.06 ,  0.21 ,  1.21 ,  0.47 ,  0.85 ,  0.45 \n")
        tmp_file.write("frequency: á :  0    ,  0    ,  0    ,  0.44 ,  0    ,  0.41 \n")
        tmp_file.write("frequency: â :  0    ,  0.03 ,  0    ,  0    ,  0    ,  0    \n")
        tmp_file.write("frequency: à :  0    ,  0.54 ,  0    ,  0    ,  0.15 ,  0.04 \n")
        tmp_file.write("frequency: ä :  0    ,  0    ,  0.54 ,  0    ,  0    ,  0    \n")
        tmp_file.write("frequency: ã :  0    ,  0    ,  0    ,  0    ,  0    ,  0.83 \n")
        tmp_file.write("frequency: ç :  0    ,  0    ,  0    ,  0    ,  0    ,  0.40 \n")
        tmp_file.write("frequency: é :  0    ,  2.13 ,  0    ,  0.36 ,  0.06 ,  0.52 \n")
        tmp_file.write("frequency: ê :  0    ,  0.24 ,  0    ,  0    ,  0    ,  0.36 \n")
        tmp_file.write("frequency: è :  0    ,  0.35 ,  0    ,  0    ,  0.42 ,  0    \n")
        tmp_file.write("frequency: ë :  0    ,  0.01 ,  0    ,  0    ,  0    ,  0    \n")
        tmp_file.write("frequency: í :  0    ,  0    ,  0    ,  0.70 ,  0    ,  0    \n")
        tmp_file.write("frequency: ì :  0    ,  0    ,  0    ,  0    ,  0.09 ,  0.18 \n")
        tmp_file.write("frequency: î :  0    ,  0.03 ,  0    ,  0    ,  0    ,  0    \n")
        tmp_file.write("frequency: ï :  0    ,  0    ,  0    ,  0    ,  0    ,  0    \n")
        tmp_file.write("frequency: ñ :  0    ,  0    ,  0    ,  0.17 ,  0    ,  0    \n")
        tmp_file.write("frequency: ó :  0    ,  0    ,  0    ,  0.76 ,  0    ,  0    \n")
        tmp_file.write("frequency: ô :  0    ,  0.07 ,  0    ,  0    ,  0    ,  0.01 \n")
        tmp_file.write("frequency: ò :  0    ,  0    ,  0    ,  0    ,  0.11 ,  0.17 \n")
        tmp_file.write("frequency: ö :  0    ,  0    ,  0.30 ,  0    ,  0    ,  0    \n")
        tmp_file.write("frequency: õ :  0    ,  0    ,  0    ,  0    ,  0    ,  0.04 \n")
        tmp_file.write("frequency: œ :  0    ,  0.01 ,  0    ,  0    ,  0    ,  0    \n")
        tmp_file.write("frequency: ß :  0    ,  0    ,  0.37 ,  0    ,  0    ,  0    \n")
        tmp_file.write("frequency: ú :  0    ,  0    ,  0    ,  0.12 ,  0    ,  0.11 \n")
        tmp_file.write("frequency: û :  0    ,  0.05 ,  0    ,  0    ,  0    ,  0    \n")
        tmp_file.write("frequency: ù :  0    ,  0.02 ,  0    ,  0    ,  0.12 ,  0    \n")
        tmp_file.write("frequency: ü :  0    ,  0.02 ,  0.65 ,  0.02 ,  0    ,  0    \n")
        tmp_file.close()

    tmp_dico = {}
    cols = 0

    with open(ktlg_path_cfg + "/katalog.cfg", "r") as tmp_file:
        for tmp_line in tmp_file:
            tmp_line = tmp_line.rstrip('\n\r')
            if len(tmp_line) > 1:

                tmp_header = tmp_line.split(':')

                # Get the filetype management
                if param_type == 'filetype':
                    if tmp_header[0] == 'filetype':
                        tmp_dico[tmp_header[1]] = tmp_header[2].lower().split(',')

                # get the xml/sql definition
                if param_type == 'video':
                    if tmp_header[0] == 'xml':
                        if tmp_header[1] in ['video', 'audio', 'books', 'subtitles']:
                            tmp_data = tmp_header[2].split(',')
                            tmp_xml = tmp_data[0].strip(' \t')
                            tmp_sql = tmp_data[1].strip(' \t')
                            tmp_dico[tmp_xml] = tmp_sql

                # get the iso language names
                if param_type == 'iso639':
                    if tmp_header[0] == 'iso639':
                        tmp_data = tmp_header[1].split(',')
                        tmp_dico[tmp_data[0]] = tmp_data[1]

                # Get the theorical frecency
                if param_type == 'frequency':
                    if tmp_header[0] == 'frequency':
                        #if header of frequency, get the country codes
                        if tmp_header[1].strip() == "":
                            tmp_dico['total'] = []                              #all the letters
                            tmp_dico['country'] = []                            #all the country
                            countrycodes = tmp_header[2].replace(" ", "").split(',')
                            cols = len(countrycodes)
                            for col in range(0, cols):
                                tmp_dico[countrycodes[col]] = {}                #all the letters:values
                        #otherwise fill the dico with letter/value per country
                        else:
                            letter = tmp_header[1].strip()
                            vals = tmp_header[2].split(',')
                            for col in range(0, cols):
                                if countrycodes[col] not in tmp_dico['country']:
                                    tmp_dico['country'].append(countrycodes[col])
                                if col == 0:
                                    tmp_dico['total'].append(letter)
                                tmp_dico[countrycodes[col]][letter] = float(vals[col])

    tmp_file.close()
    return tmp_dico

#------------------------------------------------------------------------------
# name:     defktlg_mediaid
# version:  1.0
# date:     20170603
#--------
# param_media_name : media name
#--------
# create unique ID for a media
#------------------------------------------------------------------------------
def defktlg_media_id(param_media_name):
    if not os.path.isdir(ktlg_path_media + "/" + param_media_name + "/Katalog"):
        os.mkdir(ktlg_path_media + "/" + param_media_name + "/Katalog")
        tmp_idfile = open(ktlg_path_media + "/" + param_media_name + "/Katalog/media.kid", "w")
        tmp_id = param_media_name + str(time.time())
        tmp_id = hashlib.md5(tmp_id.encode("utf")).hexdigest()
        tmp_idfile.write("%s\n" % tmp_id)
        tmp_idfile.close()

    tmp_id = ""

    #creer le fichier ID sur le media
    with open(ktlg_path_media + "/" + param_media_name + "/Katalog/media.kid", "r") as tmp_idfile:
        for tmp_line in tmp_idfile:
            tmp_line = tmp_line.lower().rstrip('\n\r')
            if len(tmp_line) > 1:
                tmp_id = str(tmp_line)
    tmp_idfile.close()

    #creer le dossier dans le dossier XML
    if not os.path.isdir(ktlg_path_xml + "/" + tmp_id):
        os.mkdir(ktlg_path_xml + "/" + tmp_id)

    return tmp_id

#------------------------------------------------------------------------------
# name:     defktlg_filepaths
# version:  4.1
# date:     20170609
#--------
# param_full_path :  path to the file
# param_md5type : real MD5 or fake MD5
#--------
# get all content of a media
#------------------------------------------------------------------------------
def defktlg_md5(param_full_path, param_md5type):

    tmp_checksum = hashlib.md5()

    # if file is less than 1 Mo then get the real MD5
    #if os.stat(param_full_path).st_size < 1048576:
    if param_md5type == 'real':
        #slice file to avoid memory error.
        tmp_readsize = 3072
        with open(param_full_path, 'rb') as tmp_file:
            for chunk in iter(lambda: tmp_file.read(3072), b""):
                tmp_checksum.update(chunk)
            tmp_checksum = tmp_checksum.hexdigest()

    # if file is greater than 1 Mo then get the fake MD5
    else:
        tmp_readsize = 3072  #1024-2048-3072-4096
        with open(param_full_path, 'rb') as tmp_file:
            tmp_data = tmp_file.read(tmp_readsize)
            tmp_checksum.update(tmp_data)
            tmp_data = tmp_file.read(tmp_readsize)
            tmp_checksum = tmp_checksum.hexdigest()

    return tmp_checksum

#------------------------------------------------------------------------------
# name:     defktlg_filepaths
# version:  4.1
# date:     20170609
#--------
# param_full_path :  path to the file
# param_md5type : real MD5 or fake MD5
#--------
# get all content of a media
#------------------------------------------------------------------------------
def defktlg_lang(param_full_path):

    tmp_encod = 'undef' #initialisation du return de la fonction
    tmp_lang = 'undef'  #initialisation du return de la fonction

    #get file path info
    folder = os.path.split(param_full_path)[0]
    file = os.path.split(param_full_path)[1]
    filename = os.path.splitext(file)[0]
    filetype = os.path.splitext(file)[1]

    #magic gives then encoding of a file
    #https://github.com/ahupp/python-magic
    m = magic.open(magic.MAGIC_MIME)
    m.load()
    tmp_magic = m.file(param_full_path)
    tmp_encod = tmp_magic.split("; charset=")[1]

    #convert encoding names from magic to python
    py_encode = {'utf-8': 'utf8', 'us-ascii': 'ascii', 'iso-8859-1': 'latin1', 'utf-16le': 'utf-16le'}

    #if encoding in unknown-8bit let's bet it's Latin-1 Supplement
    #convert from Latin-1 Supplement to UTF-8
    #http://www.unicodemap.org/range/2/Latin-1_Supplement/
    if tmp_encod == 'unknown-8bit':
        #backup the file
        shutil.copy(param_full_path, param_full_path + ".ktabackup")

        #create an utf-8 copy
        tmp_file = open(param_full_path, "w", encoding='utf8')
        with open(param_full_path + ".ktabackup", 'r', encoding='latin1') as subt_file:
            #Latin-1 Supplement
            for line in subt_file:
                line_o = line
                line = line.replace(u"\u0080", '€')
                line = line.replace(u"\u0081", ' ')
                line = line.replace(u"\u0082", ',')
                line = line.replace(u"\u0083", 'ƒ')
                line = line.replace(u"\u0084", '"')
                line = line.replace(u"\u0085", '…')
                line = line.replace(u"\u0086", '†')
                line = line.replace(u"\u0087", '‡')
                line = line.replace(u"\u0088", 'ˆ')
                line = line.replace(u"\u0089", '‰')
                line = line.replace(u"\u008A", 'Š')
                line = line.replace(u"\u008B", '‹')
                line = line.replace(u"\u008C", 'Œ')
                line = line.replace(u"\u008D", ' ')
                line = line.replace(u"\u008E", 'Ž')
                line = line.replace(u"\u008F", ' ')
                line = line.replace(u"\u0090", ' ')
                line = line.replace(u"\u0091", "'")
                line = line.replace(u"\u0092", "'")
                line = line.replace(u"\u0093", '"')
                line = line.replace(u"\u0094", '"')
                line = line.replace(u"\u0095", '•')
                line = line.replace(u"\u0096", '–')
                line = line.replace(u"\u0097", '—')
                line = line.replace(u"\u0098", '˜')
                line = line.replace(u"\u0099", '™')
                line = line.replace(u"\u009A", 'š')
                line = line.replace(u"\u009B", '›')
                line = line.replace(u"\u009C", 'œ')
                line = line.replace(u"\u009D", ' ')
                line = line.replace(u"\u009E", 'ž')
                line = line.replace(u"\u009F", 'Ÿ')
                line = line.replace(u"\u00A0", ' ')
                line = line.replace(u"\u00A1", '¡')
                line = line.replace(u"\u00A2", '¢')
                line = line.replace(u"\u00A3", '£')
                line = line.replace(u"\u00A4", '¤')
                line = line.replace(u"\u00A5", '¥')
                line = line.replace(u"\u00A6", '¦')
                line = line.replace(u"\u00A7", '§')
                line = line.replace(u"\u00A8", '¨')
                line = line.replace(u"\u00A9", '©')
                line = line.replace(u"\u00AA", 'ª')
                line = line.replace(u"\u00AB", '«')
                line = line.replace(u"\u00AC", '¬')
                line = line.replace(u"\u00AD", ' ')
                line = line.replace(u"\u00AE", '®')
                line = line.replace(u"\u00AF", '¯')
                line = line.replace(u"\u00B0", '°')
                line = line.replace(u"\u00B1", '±')
                line = line.replace(u"\u00B2", '²')
                line = line.replace(u"\u00B3", '³')
                line = line.replace(u"\u00B4", '´')
                line = line.replace(u"\u00B5", 'µ')
                line = line.replace(u"\u00B6", '¶')
                line = line.replace(u"\u00B7", '·')
                line = line.replace(u"\u00B8", '¸')
                line = line.replace(u"\u00B9", '¹')
                line = line.replace(u"\u00BA", 'º')
                line = line.replace(u"\u00BB", '»')
                line = line.replace(u"\u00BC", '¼')
                line = line.replace(u"\u00BD", '½')
                line = line.replace(u"\u00BE", '¾')
                line = line.replace(u"\u00BF", '¿')
                line = line.replace(u"\u00C0", 'À')
                line = line.replace(u"\u00C1", 'Á')
                line = line.replace(u"\u00C2", 'Â')
                line = line.replace(u"\u00C3", 'Ã')
                line = line.replace(u"\u00C4", 'Ä')
                line = line.replace(u"\u00C5", 'Å')
                line = line.replace(u"\u00C6", 'Æ')
                line = line.replace(u"\u00C7", 'Ç')
                line = line.replace(u"\u00C8", 'È')
                line = line.replace(u"\u00C9", 'É')
                line = line.replace(u"\u00CA", 'Ê')
                line = line.replace(u"\u00CB", 'Ë')
                line = line.replace(u"\u00CC", 'Ì')
                line = line.replace(u"\u00CD", 'Í')
                line = line.replace(u"\u00CE", 'Î')
                line = line.replace(u"\u00CF", 'Ï')
                line = line.replace(u"\u00D0", 'Ð')
                line = line.replace(u"\u00D1", 'Ñ')
                line = line.replace(u"\u00D2", 'Ò')
                line = line.replace(u"\u00D3", 'Ó')
                line = line.replace(u"\u00D4", 'Ô')
                line = line.replace(u"\u00D5", 'Õ')
                line = line.replace(u"\u00D6", 'Ö')
                line = line.replace(u"\u00D7", '×')
                line = line.replace(u"\u00D8", 'Ø')
                line = line.replace(u"\u00D9", 'Ù')
                line = line.replace(u"\u00DA", 'Ú')
                line = line.replace(u"\u00DB", 'Û')
                line = line.replace(u"\u00DC", 'Ü')
                line = line.replace(u"\u00DD", 'Ý')
                line = line.replace(u"\u00DE", 'Þ')
                line = line.replace(u"\u00DF", 'ß')
                line = line.replace(u"\u00E0", 'à')
                line = line.replace(u"\u00E1", 'á')
                line = line.replace(u"\u00E2", 'â')
                line = line.replace(u"\u00E3", 'ã')
                line = line.replace(u"\u00E4", 'ä')
                line = line.replace(u"\u00E5", 'å')
                line = line.replace(u"\u00E6", 'æ')
                line = line.replace(u"\u00E7", 'ç')
                line = line.replace(u"\u00E8", 'è')
                line = line.replace(u"\u00E9", 'é')
                line = line.replace(u"\u00EA", 'ê')
                line = line.replace(u"\u00EB", 'ë')
                line = line.replace(u"\u00EC", 'ì')
                line = line.replace(u"\u00ED", 'í')
                line = line.replace(u"\u00EE", 'î')
                line = line.replace(u"\u00EF", 'ï')
                line = line.replace(u"\u00F0", 'ð')
                line = line.replace(u"\u00F1", 'ñ')
                line = line.replace(u"\u00F2", 'ò')
                line = line.replace(u"\u00F3", 'ó')
                line = line.replace(u"\u00F4", 'ô')
                line = line.replace(u"\u00F5", 'õ')
                line = line.replace(u"\u00F6", 'ö')
                line = line.replace(u"\u00F7", '÷')
                line = line.replace(u"\u00F8", 'ø')
                line = line.replace(u"\u00F9", 'ù')
                line = line.replace(u"\u00FA", 'ú')
                line = line.replace(u"\u00FB", 'û')
                line = line.replace(u"\u00FC", 'ü')
                line = line.replace(u"\u00FD", 'ý')
                line = line.replace(u"\u00FE", 'þ')
                line = line.replace(u"\u00FF", 'ÿ')
                line = line.replace("`", "'")
                line = line.replace("â™ª", '♪')
                tmp_file.write(line)
                if line != line_o:
                    print(line_o + line)
        tmp_file.close
        tmp_encod = 'utf-8'

    #Now let's try to guess the language
    if tmp_encod in py_encode:

        if filetype == '.idx':
            with open(param_full_path, 'r', encoding=py_encode.get(tmp_encod)) as subt_file:
                #VobSub version
                vobsub = 0
                for line in subt_file:
                    #get the VobSub version
                    if line.find("# VobSub index file, v") != -1:
                        vobsub = int(line[22:24])
                    #if vobsub version is known get the lang
                    if vobsub in [7]:
                        if line.find("id: ") != -1 and line.find("index: 0") != -1:
                            tmp_lang = line[4:6]
                            break

        if filetype == '.srt':
            with open(param_full_path, 'r', encoding=py_encode.get(tmp_encod)) as subt_file:
                SRT_data = ""
                SRT_sample = ""                                                 #pour d'identifier manuellement la langue si nécessaire
                for line in subt_file:
                    line = line.replace('\n', ' ')
                    #delete tags
                    for (opentag, closetag) in [('www.','.com'),('{','}'),('[',']'),('<','>')]:
                        i0 = len(line)
                        while i0 != -1:
                            i0 = line.rfind(opentag,0,i0)
                            i1 = line.find(closetag,i0)
                            if i1 != -1:
                                line = line[:i0]+line[i1+len(closetag):]
                            else:
                                i0 = max(-1,i0-1)
                    #clean HTML
                    dicoHTML={'&nbsp;':' '}
                    for entity in dicoHTML:
                        line=line.replace(entity, dicoHTML[entity])
                    # clean diactritics
                    diactritics = ('\\/\'’"“”.:;…,¿¡?!<«([{|¦}])»>_–¬—^~´`¨*=#%±+-÷¾½¼¹²³£$€&µ¤°©@™ª§★♫♪0123456789¶')
                    for char in diactritics:
                        line = line.replace(char, ' ')                          #clean diacritics

                    # lower case for accents
                    line = line.lower()

                    if len(line) > 0:
                        SRT_data = SRT_data + line

            #copy for dictionnary identification
            SRT_sample = SRT_data
            SRT_data = SRT_data.replace(' ', '')

            #traitement du SRT pour en trouver la langue
            #|
            SRT_hz = {}
            SRT_len = len(SRT_data)

            #calcule de la frequence de chaque lettre
            for x in ktlg_alpha['total']:
                SRT_hz[x] = float(SRT_data.count(x))*100
                SRT_data = SRT_data.replace(x, '')

            SRT_len = SRT_len - len(SRT_data)                                   #tient compte des caracteres residuels
            for x in SRT_hz:
                SRT_hz[x] = SRT_hz[x]/SRT_len

            #distance euclidienne
            #Retourne un vecteur R=[d(X,ENG),d(X,FR),...]
            LANGs = ktlg_dico_langs['country']
            R=[]
            for L in LANGs:
                R.append(0)
            for L in LANGs:
                d = 0
                for letter in ktlg_alpha['total']:
                    d+=(ktlg_freq[L][letter]-SRT_hz[letter])**2
                R[LANGs.index(L)] = round(sqrt(d), 3)

            m = min(R)
            tmp_lang = LANGs[R.index(m)]


            #recherche de la langue par dictionnaire lorsque la distance euclidienne est douteuse
            if m > 4.5:

                for i in range(1, 32):
                    SRT_sample = SRT_sample.replace('  ', ' ')

                SRT_sample = SRT_sample.split()
                SRT_words = {'_tot_': len(SRT_sample)}

                for word in SRT_sample:
                    if word not in SRT_words.keys():
                        SRT_words[word] = SRT_sample.count(word)

                hunspell_result = {}
                for L in ['en', 'fr']:
                    word_in = 0
                    word_out = 0
                    for word, occur in SRT_words.items():
                        if word in hunspell[L]:
                            word_in += occur
                        else:
                            if word != '_tot_':
                                word_out += occur

                    hunspell_result[L] = (word_in*100)/SRT_words['_tot_']

                if max(hunspell_result.values()) > (2/3*100):
                    for k, v in hunspell_result.items():
                        if v == max(hunspell_result.values()):
                            tmp_lang = k
                else:
                    tmp_lang = 'undef'

            #for blabla in SRT_extract:
            #    print(blabla)



    #-------------------------------------
    if tmp_lang in ktlg_dico_ccode.keys():
        tmp_lang = ktlg_dico_ccode[tmp_lang]
    else:
        tmp_lang = 'Unknow'

    return tmp_encod, tmp_lang
    #-------------------------------------

# -----------------------------------------------------------------------------
# initialisations
# -----------------------------------------------------------------------------
ktlg_path_media = "/media/" + os.environ.get('USERNAME')

ktlg_path_ktlg = defktlg_createdir("/home/" + os.environ.get('USERNAME') + "/Katalog")
ktlg_path_cfg = defktlg_createdir(ktlg_path_ktlg + "/cfg")
ktlg_path_xml = defktlg_createdir(ktlg_path_ktlg + "/xml")


# {
#   'video': ['mp4', 'avi', 'mkv', 'rmvb', 'ts', 'flv', 'm4v'],
#   'audio': ['mp3', 'ac3'], 'books': ['epub', 'pdf'],
#   'ignore': ['ini', 'inf', 'xls', 'xlsx', 'trashinfo', 'ico', 'zip', 'nfo', 'xlsm', 'psd', '7z', 'rar', 'dat', 'id'],
#   'special': ['card', 'jpg', 'txt'],
#   'subtitles': ['srt', 'idx', 'sub']
# }
ktlg_dico_filetypes = defktlg_cfg('filetype')

# {
#   'movie_filesize': 'bigint(20) unsigned DEFAULT NULL',
#   'movie_path': 'varchar(128) NOT NULL',
#   'movie_vo_subtitles': 'varchar(16) NOT NULL',
#   'movie_title_vo': 'varchar(64) NOT NULL',
#   'movie_year': 'year(4) DEFAULT NULL',
#   'movie_subgenre': 'varchar(32) NOT NULL',
#   'movie_title_fr': 'varchar(64) NOT NULL',
#   'movie_lang_vo': 'varchar(16) NOT NULL',
#   'movie_file': 'varchar(128) NOT NULL',
#   'movie_height': 'smallint(5) unsigned DEFAULT NULL',
#   'movie_filetype': 'varchar(8) NOT NULL',
#   'movie_time': 'time DEFAULT NULL',
#   'movie_country': 'varchar(32) NOT NULL',
#   'movie_jpg': 'varchar(128) NOT NULL',
#   'movie_subtitle_fr': 'varchar(64) NOT NULL',
#   'movie_ID': 'int(10) unsigned NOT NULL AUTO_INCREMENT',
#   'movie_type': 'varchar(32) NOT NULL',
#   'movie_season': 'tinyint(3) unsigned DEFAULT NULL',
#   'movie_fr_subtitles': 'varchar(16) NOT NULL',
#   'movie_comment': 'varchar(64) NOT NULL',
#   'movie_subtitle_vo': 'varchar(64) NOT NULL',
#   'movie_genre': 'varchar(32) NOT NULL',
#   'movie_rating': 'tinyint(5) unsigned DEFAULT NULL',
#   'movie_width': 'smallint(5) unsigned DEFAULT NULL',
#   'serie_name': 'varchar(64) NOT NULL',
#   'movie_source': 'varchar(16) DEFAULT NULL',
#   'movie_episode': 'tinyint(3) unsigned DEFAULT NULL'
# }
ktlg_dico_video = defktlg_cfg('video')

#ktlg_dico_audio = defktlg_cfg_v1_1('audio')
#print(ktlg_dico_audio)

#ktlg_dico_books = defktlg_cfg_v1_1('books')
#print(ktlg_dico_books)

#ktlg_dico_subti = defktlg_cfg_v1_1('subtitles')
#print(ktlg_dico_subti)

#identify the vobsub idx/sub language
ktlg_dico_ccode = defktlg_cfg('iso639')

#theorical frecencies used to identifiy the language of SRT files
#ktlg_alpha['en'] = ['a', 'b', 'c', ... ... ... , 'ú', 'û', 'ù', 'ü']
#ktlg_freq['en'] = {'ó': 0.0, 'p': 3.01, 'u': 4.46, ... ... ..., 'y': 0.04, 'x': 0.28, 'è': 0.0}
ktlg_dico_langs = defktlg_cfg('frequency')
ktlg_alpha = {}
ktlg_freq = {}
ktlg_alpha['total'] = ktlg_dico_langs['total']
for lang in ktlg_dico_langs['country']:
    ktlg_alpha[lang] = ktlg_alpha['total']
    ktlg_freq[lang] = ktlg_dico_langs[lang]



# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
#identifie tous les disk dans media
ktlg_media_list = os.listdir(ktlg_path_media)

#pour chaque disk
for ktlg_media in ktlg_media_list:

    #identification du media
    print('media ID')
    ktlg_media_id = defktlg_media_id(ktlg_media)

    #inventaire des fichiers du media et creation des fichiers DATA
    print('Catalogue / data files')
    defktlg_filepaths(ktlg_media)

    #--------------------------------------------
    #traitement des soustitres
    #--------------------------------------------
    print('subtitles XML file')
    with open(ktlg_path_xml + "/" + ktlg_media_id + "/subtitles.data") as tmp_file:
        subtitles = tmp_file.read().splitlines()
        subtitles.sort()

    xml_path = defktlg_createdir(ktlg_path_xml + "/" + ktlg_media_id)

    if len(subtitles) > 0:

        #load dictionnary en_US
        hunspell = {}
        hunspell['en'] = []
        with open(ktlg_path_cfg + "/en_US.dic.modif", 'r', encoding='utf-8') as hunfile:
            for word in hunfile:
                hunspell['en'].append(word.lower().replace('\n', ''))

        #load dictionnary fr_FR
        hunspell['fr'] = []
        with open(ktlg_path_cfg + "/fr_FR_Classic.dic.modif", 'r', encoding='utf-8') as hunfile:
            for word in hunfile:
                hunspell['fr'].append(word.lower().replace('\n', ''))

        #if not os.path.isfile(xml_path + "/" + "subtitles.xml"):
        xml_file = open(xml_path + "/" + "subtitles.xml", "w")

        zz = 0
        for file_fullpath in subtitles:

            #if zz > 30:
            #    break

            zz+=1
            #print(str(zz) + " >> " + file_fullpath)

            folder = os.path.split(file_fullpath)[0]
            file = os.path.split(file_fullpath)[1]
            filename = os.path.splitext(file)[0]
            filetype = os.path.splitext(file)[1]

            xml_file.write("<subtitle>\n")

            xml_file.write("\t<subtitle_path>" + folder + "</subtitle_path>\n")

            xml_file.write("\t<subtitle_file>" + file + "</subtitle_file>\n")

            xml_file.write("\t<subtitle_filetype>" + filetype + "</subtitle_filetype>\n")

            size = os.stat(file_fullpath).st_size
            xml_file.write("\t<subtitle_filesize>" + str(size) + "</subtitle_filesize>\n")

            encoding, languess = defktlg_lang(file_fullpath)
            xml_file.write("\t<subtitle_encode>" + encoding + "</subtitle_encode>\n")
            xml_file.write("\t<subtitle_lang>" + languess + "</subtitle_lang>\n")

            xml_file.write("\t<subtitle_rating></subtitle_rating>\n")

            #ID is the last because langage function could change the encoding if needed
            ID = defktlg_md5(file_fullpath, 'real')
            xml_file.write("\t<subtitle_id>" + ID + "</subtitle_id>\n")

            xml_file.write("</subtitle>\n")
        xml_file.close()
