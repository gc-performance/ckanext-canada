# -*- coding: UTF-8 -*-
from ckanapi import LocalCKAN, ValidationError

import pytest
from ckanext.canada.tests.fixtures import prepare_dataset_type_with_resource

from ckanext.recombinant.tables import get_chromo


@pytest.mark.usefixtures('clean_db', 'prepare_dataset_type_with_resources')
@pytest.mark.parametrize(
    'prepare_dataset_type_with_resources',
    [{'dataset_type': 'ati'}],
    indirect=True)
class TestAti(object):
    def test_example(self, request):
        lc = LocalCKAN()
        record = get_chromo('ati')['examples']['record']
        lc.action.datastore_upsert(
            resource_id=request.config.cache.get("resource_id", None),
            records=[record])


    def test_blank(self, request):
        lc = LocalCKAN()
        with pytest.raises(ValidationError) as ve:
            lc.action.datastore_upsert(
                resource_id=request.config.cache.get("resource_id", None),
                records=[{}])
        err = ve.value.error_dict
        expected = {
            u'key': [u'fields "request_number" are missingfields "request_number" are missing but needed as key']
            }
        assert err == expected


@pytest.mark.usefixtures('clean_db', 'prepare_dataset_type_with_resources')
@pytest.mark.parametrize(
    'prepare_dataset_type_with_resources',
    [{
        'dataset_type': 'ati',
        'resource_key': 1,
    }],
    indirect=True)
class TestAtiNil(object):
    def test_example(self, request):
        lc = LocalCKAN()
        record = get_chromo('ati-nil')['examples']['record']
        lc.action.datastore_upsert(
            resource_id=request.config.cache.get("resource_id", None),
            records=[record])


    def test_blank(self, request):
        lc = LocalCKAN()
        with pytest.raises(ValidationError) as err:
            lc.action.datastore_upsert(
                resource_id=request.config.cache.get("resource_id", None),
                records=[{}])
        assert err is not None
