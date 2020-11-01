from __future__ import unicode_literals

import collections
import os
import urllib
import humanfriendly
import re
import time
import requests

from octoprint.printer import InvalidFileLocation, InvalidFileType

from octoprint_discordremote.command_plugins import plugin_list
from octoprint_discordremote.embedbuilder import EmbedBuilder, success_embed, error_embed, info_embed, upload_file


class Command:
    def __init__(self, plugin):
        assert plugin
        self.plugin = plugin
        self.command_dict = collections.OrderedDict()
        self.command_dict['connect'] = {'cmd': self.connect, 'params': "[port] [baudrate]",
                                        'description': "Connect to a printer."}
        self.command_dict['disconnect'] = {'cmd': self.disconnect, 'description': "Disconnect from a printer."}
        self.command_dict['print'] = {'cmd': self.start_print, 'params': "{filename}", 'description': "Print a file."}
        self.command_dict['files'] = {'cmd': self.list_files,
                                      'description': "List all files and respective download links."}
        self.command_dict['abort'] = {'cmd': self.cancel_print, 'description': "Abort a print."}
        self.command_dict['snapshot'] = {'cmd': self.snapshot, 'description': "Take a snapshot with the camera."}
        self.command_dict['status'] = {'cmd': self.status, 'description': "Get the current printer status."}
        self.command_dict['help'] = {'cmd': self.help, 'description': "Print this help."}
        self.command_dict['pause'] = {'cmd': self.pause, 'description': "Pause current print."}
        self.command_dict['resume'] = {'cmd': self.resume, 'description': "Resume current print."}
        self.command_dict['timelapse'] = {'cmd': self.timelapse,
                                          'description': "List all timelapses and respective download links."}
        self.command_dict['mute'] = {'cmd': self.mute,
                                     'description': "Mute notifications."}
        self.command_dict['unmute'] = {'cmd': self.unmute,
                                       'description': "Unmute notifications."}
        self.command_dict['gcode'] = {'cmd': self.gcode, 'params': '{GCODE}',
                                      'description': "Send a set of GCODE commands directly to the printer. GCODE lines seperated by \';\'"}
        self.command_dict['getfile'] = {'cmd': self.getfile, 'params': "{filename}",
                                        'description': "Get a gcode file and upload to discord."}
        self.command_dict['gettimelapse'] = {'cmd': self.gettimelapse, 'params': "{filename}",
                                             'description': "Get a timelapse file and upload to discord."}

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

    
