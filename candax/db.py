# -*- coding: utf-8 -*-

import riak
import functools
import tornado.gen
import logging
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

MAX_WORKERS = 10
LOGGER = logging.getLogger(__name__)

def threadexecute(f):
    @functools.wraps(f)
    @tornado.gen.coroutine
    def wrapper(self, *args, **kwargs):
        resp = yield self.executor.submit(f, self, *args, **kwargs)
        return resp
    return wrapper

class RiakDB:
    instance = None
    def __init__(self, riak_url):
        url = urlparse(riak_url)
        self.client = riak.RiakClient(
            protocol=url.scheme, host=url.hostname, pb_port=url.port,
            http_port=url.port)
        self.executor = ThreadPoolExecutor(MAX_WORKERS)

    @threadexecute
    def insert(self, bucket, d):
        bucket = self.client.bucket(bucket)
        obj = bucket.new(d['key'], data=d)
        obj.store()
        return d

    @threadexecute
    def get_all(self, bucket):
        bucket = self.client.bucket(bucket)
        return [bucket.get(key).data for key in bucket.get_keys()]

    @threadexecute
    def get(self, bucket, key):
        bucket = self.client.bucket(bucket)
        return bucket.get(key).data

    @threadexecute
    def update(self, bucket, d):
        bucket = self.client.bucket(bucket)
        obj = bucket.get(d['key'])
        obj.data = d
        obj.store()
        return bucket.get(d['key']).data

    @threadexecute
    def delete(self, bucket, key):
        bucket = self.client.bucket(bucket)
        obj = bucket.get(key)
        ret = obj.data
        obj.delete()
        return ret
