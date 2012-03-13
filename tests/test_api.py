#!/usr/bin/env python

import os
import pytest
import datetime

import api.child
from common.log import logger
import db.schema as schema
from common.config import core_config

log = logger("test")
class TestChild:
    def setup_class(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_file = os.path.join(base_path, 'conf', 'klp.ini')
        
        cfg = core_config(config_file)
        self.meta, self.session, self.engine = schema.init_model(cfg['dburi'])

        
    @pytest.mark.parametrize(('name', 'dob', 'sex'),
                              [ ('child 0', datetime.date(2012, 3, 13), 'male'),
                                ('child 1', datetime.date(2013, 3, 13), 'female'),
                                ('child 2', datetime.date(1979, 3, 13), 'tg') ])
    def test_create_child(self, name, dob, sex):
        """
        Create a child
        """
        cid = api.child.create(self.session, name, dob, sex)
        assert cid, "Child not created"
        self.session.commit()

    @pytest.mark.parametrize(('id'), range(13, 15))
    def test_delete_child(self, id):
        """
        Delete a child
        """
        api.child.delete(self.session, id)
        c = api.child.get(self.session, id)

        assert c.deleted, "Child not deleted"
