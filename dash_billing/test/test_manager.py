import unittest2 as unittest
import mox
import logging
import sys
from django_openstack import api
from dash_billing.billing import manager
import stubout

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
h1 = logging.StreamHandler(sys.stdout)
logging.basicConfig(format=FORMAT)
LOG = logging.getLogger('notification_test')
LOG.addHandler(h1)

class TestManager(unittest.TestCase):
    def setUp(self):
        LOG.debug("setup")
        self.stubs = stubout.StubOutForTesting()

    def tearDown(self):
        self.stubs.UnsetAll()
        self.stubs.SmartUnsetAll()

    def test_add_instance_record(self):
        billing_manager = manager.BillingManager()

        def fake_add_record(tenant_id, amount, memo):
            LOG.debug("%s %s" % ( tenant_id,  amount))

        self.stubs.Set(billing_manager, '_add_record', fake_add_record)
        billing_manager._add_record_for_active_instance()


    def test_create_record(self):
        billing_manager = manager.BillingManager()

        def fake_add_record(tenant_id, amount, memo):
            LOG.debug("%s %s" % ( tenant_id,  amount))

        self.stubs.Set(billing_manager, '_add_record', fake_add_record)
        message = {'payload':{'project_id':"fake"}}
        billing_manager.compute_instance_create(message)


