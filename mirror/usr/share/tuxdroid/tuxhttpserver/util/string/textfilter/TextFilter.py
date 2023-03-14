# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import sys
import os
import re
import chardet.chardet

class TextFilter(object):

    def __init__(self, filter_path):
        self.filter_path = filter_path
        self.__parse()

    def __parse(self):
        if not os.path.isfile(self.filter_path):
            return
        f = open(self.filter_path, 'r')
        filter_code = f.read()
        f.close()
        global pattern_name
        pattern_name = ""
        global pattern_description
        pattern_description = ""
        global pattern_author
        pattern_author = ""
        global pattern_version
        pattern_version = ""
        global pattern_languages
        pattern_languages = ['ALL',]
        global pattern_define
        pattern_define = []
        exec str(filter_code) in globals()
        self.name = pattern_name
        self.description = pattern_description
        self.author = pattern_author
        self.version = pattern_version
        self.languages = pattern_languages
        self.__re_patterns = []
        for pattern in pattern_define:
            if len(pattern) == 3:
                new_pattern = ['', '']
                new_pattern[1] = pattern[2]
                if pattern[0] == 'replace':
                    new_pattern[0] = r'\b' + pattern[1] + r'\b'
                else:
                    new_pattern[0] = pattern[1]
                new_pattern[0] = unicode(new_pattern[0], "latin1")
                self.__re_patterns.append(new_pattern)

    def apply(self, text):
        for pattern in self.__re_patterns:
            text = re.sub(pattern[0], pattern[1], text)
        return text

class TextFilterContainer(object):

    def __init__(self):
        self.__filters = {
            'ALL' : [],
            'ar_ALL' : [],
            'nl_BE' : [],
            'en_GB' : [],
            'da_ALL' : [],
            'fr_ALL' : [],
            'de_ALL' : [],
            'it_ALL' : [],
            'nl_NL' : [],
            'no_ALL' : [],
            'pt_ALL' : [],
            'es_ALL' : [],
            'sv_ALL' : [],
            'en_US' : []
        }

    def __completeLanguage(self, language):
        if self.__filters.has_key(language):
            return language
        for lang in self.__filters.keys():
            if lang.find(language) == 0:
                return lang
        return None

    def insert_filter(self, text_filter):
        try:
            languages = text_filter.languages
        except:
            return
        for language in languages:
            if self.__filters.has_key(language):
                self.__filters[language].append(text_filter)

    def load_directory(self, dir_path):
        re_tpf = re.compile(r'.tpf$')
        if os.path.isdir(dir_path):
            list_dir = os.listdir(dir_path)
            for element in list_dir:
                filename = os.path.join(dir_path, element)
                if os.path.isfile(filename):
                    if re_tpf.search(filename) != None:
                        new_filter = TextFilter(filename)
                        self.insert_filter(new_filter)

    def __ascii_decode(self, html_source):
        def hex_to_char(hexa_re):
            val = str(hexa_re.group(1))
            return chr(int(val))
        rex = re.compile(r'&#([0-9a-hA-H][0-9a-hA-H]);', re.UNICODE)
        return rex.sub(hex_to_char, html_source)

    def apply(self, text, language):
        language = self.__completeLanguage(language)
        filters = self.__filters['ALL']
        for _filter in filters:
            text = _filter.apply(text)
        if (language != None) and (language != 'ALL'):
            filters = self.__filters[language]
            for _filter in filters:
                text = _filter.apply(text)
        text = self.__ascii_decode(text)
        return text