# -*- coding: utf-8 -*-
from django.utils.html import conditional_escape
from django.utils.encoding import force_text
from django.utils.functional import Promise
from django.core.serializers.json import DjangoJSONEncoder


class SafeJSONEncoder(DjangoJSONEncoder):
    def _recursive_escape(self, o, esc=conditional_escape):
        if isinstance(o, dict):
            return type(o)((esc(k), self._recursive_escape(v)) for (k, v) in o.iteritems())
        if isinstance(o, (list, tuple)):
            return type(o)(self._recursive_escape(v) for v in o)
        try:
            return type(o)(esc(o))
        except ValueError:
            return self.default(o)

    def encode(self, o):
        value = self._recursive_escape(o)
        return super(SafeJSONEncoder, self).encode(value)

    def default(self, o):
        if isinstance(o, Promise):
            return force_text(o)
        return super(SafeJSONEncoder, self).default(o)
