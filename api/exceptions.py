# -*- coding: utf-8 -*-

class NoSuchChild(Exception):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "NoSuchChild #%s" % self.id
