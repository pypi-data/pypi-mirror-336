#!/usr/bin/env python3

import os
import configparser
from lbkit.tools import Tools

tools = Tools("EnvDetector")
log = tools.log


class LbkitComponent(object):
    def __init__(self, folder, config: configparser.ConfigParser):
        self.folder = os.path.realpath(folder)
        self.config = config


class LbkitManifest(object):
    def __init__(self, folder, config: configparser.ConfigParser):
        self.folder = os.path.realpath(folder)
        self.config = config


class EnvDetector(object):
    def __init__(self):
        """初始化"""
        self.component: LbkitComponent = None
        self.manifest: LbkitManifest = None
        self.cwd = os.getcwd()
        """探测环境"""
        cwd = self.cwd
        while cwd != "/":
            if os.path.isfile(os.path.join(cwd, "manifest.yml")):
                self.manifest = LbkitManifest(cwd, None)
                return
            if os.path.isfile(os.path.join(cwd, "metadata/package.yml")):
                self.component = LbkitComponent(cwd, None)
                return
            cwd = os.path.dirname(cwd)
