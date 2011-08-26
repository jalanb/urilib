import re
import urilib.regex
import urilib.tools

class URI(object):
    scheme   = None
    hier_part= None
    query    = None
    fragment = None
    path     = None
    authority= None

    def __init__(self, uri):
        self.uri = uri
        self._parse()

    def _parse_regex(self):
        ''' Simple URI parser using a regex from the appendix of RFC 3986 '''
        uri_regex     = re.compile(urilib.regex.simple_uri_regex)
        match         = uri_regex.match(self.uri)
        if match is not None:
            self.scheme    = match.group(2)
            self.hier_part = match.group(3)
            self.authority = match.group(5)
            self.path      = match.group(6)
            self.query     = match.group(8)
            self.fragment  = match.group(10)

    def _parse_lexer(self):
        ''' Coming soo to a package near you... '''

    def __str__(self):
        ''' Return the full URI '''
        str = ''
        if self.scheme is not None:
            str += '%s:' % self.scheme
        if self.authority is not None:
            str += '//%s' % self.authority
        if self.path is not None:
            str += self.path
        if self.query is not None:
            str += '?%s' % self.query
        if self.fragment is not None:
            str += '#%s' % self.fragment
        return str

URI._parse = URI._parse_regex

class Query(dict):
    def __init__(self, query=None, separator='&'):
        if type(separator) != str:
            raise ValueError('Expected separator to be a string, got %s' % str(type(separator)))
        self.separator = separator

        if query is None:
            dict.__init__(self)
        elif type(query) is dict:
            dict.__init__(self, query)
        else:
            dict.__init__(self)
            self.split_query_string(query)

    def __str__(self):
        self.separator.join([
            '='.join(param, value)
                for param,values in self.iteritems()
                    for value in values
        ])

    def del_by_name_value(self, name, value, max=None):
        count = 0
        for i, v in enumerate(self[name]):
            if v == value:
                del self[name][i]
                count += 1
                if max is not None and count >= max:
                    return

    def split_query_string(self, query):
        for pair in query.split(self.separator):
            if pair == '':
                continue
            k,v = pair.split('=')
            if k in self:
                self[k].append(v)
            else:
                self[k] = [v]

class URL(URI):
    query_separator = '&'

    def get_query_as_dict(self):
        return dict(
            kvpair.split('=')
                for kvpair in self.query.split(self.query_separator)
        )

    def set_query_from_dict(self, d):
        self.query = self.query_separator.join(
            [ '%s=%s' % (k,v) for k,v in d.iteritems() ]
        )

class URIParseError(Exception):
    ''' An exception during processing of a URI '''
