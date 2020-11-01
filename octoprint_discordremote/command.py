from __future__ import unicode_literals

import collections
import os
import urllib
import humanfriendly
import re
import time
import requests
import random

from octoprint.printer import InvalidFileLocation, InvalidFileType

from octoprint_discordremote.command_plugins import plugin_list
from octoprint_discordremote.embedbuilder import EmbedBuilder, success_embed, error_embed, info_embed, upload_file


class Command:
    def __init__(self, plugin):
        assert plugin
        self.plugin = plugin
        self.command_dict = collections.OrderedDict()
        self.command_dict['yellow'] = {'cmd':self.sus, 'description':"Yellow"}
        self.command_dict['red'] = {'cmd':self.sus, 'description':"Yellow"}
        self.command_dict['green'] = {'cmd':self.sus, 'description':"Yellow"}
        self.command_dict['orange'] = {'cmd':self.sus, 'description':"Yellow"}
        self.command_dict['black'] = {'cmd':self.sus, 'description':"Yellow"}
        self.command_dict['white'] = {'cmd':self.sus, 'description':"Yellow"}

        # Load plugins
        for command_plugin in plugin_list:
            command_plugin.setup(self, plugin)

    

    def list_files(self):
        port = self.plugin.get_port()
        baseurl = self.plugin.get_settings().get(["baseurl"])
        if baseurl is None or baseurl == "":
            baseurl = "%s:%s" % (self.plugin.get_ip_address(), port)

        builder = EmbedBuilder()
        builder.set_title('Files and Details')
        builder.set_author(name=self.plugin.get_printer_name())
        file_list = self.get_flat_file_list()
        for details in file_list:
            description = ''
            title = ''
            try:
                title = details['path'].lstrip('/')
            except:
                pass

            try:
                description += 'Location: %s\n' % details['location']
            except:
                pass

            try:
                estimated_print_time = humanfriendly.format_timespan(details['analysis']['estimatedPrintTime'],
                                                                     max_units=2)
                description += 'Estimated Print Time: %s\n' % estimated_print_time
            except:
                pass

            try:
                average_print_time = humanfriendly.format_timespan(
                    details['statistics']['averagePrintTime']['_default'], max_units=2)
                description += 'Average Print Time: %s\n' % average_print_time
            except:
                pass

            try:
                filament_required = humanfriendly.format_length(
                    details['analysis']['filament']['tool0']['length'] / 1000)
                description += 'Filament Required: %s\n' % filament_required
            except:
                pass

            try:
                url = "http://" + baseurl + "/downloads/files/" + details['location'] + "/" + details['path'].lstrip('/')
                description += 'Download Path: %s\n' % url
            except:
                pass

            builder.add_field(title=title, text=description)

        return None, builder.get_embeds()
    def sus(self,n):
        builder = EmbedBuilder()
        builder.set_title(n)
        x=random.randint(0,9)
        if x==0:
            builder.add_field(title=n, text="is sus")
        else
            builder.add_field(title=n, text="is sus")
        return None, builder.get_embeds()

    
