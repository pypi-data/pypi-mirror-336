"""DataTables server-side for Flask-MongoEngine supports both DT 1.x and 2.x"""
import json
import re

from bson import ObjectId, json_util
from mongoengine.fields import (BooleanField, DecimalField,
                                EmbeddedDocumentField,
                                EmbeddedDocumentListField, FloatField,
                                IntField, ListField, LongField, ObjectIdField,
                                ReferenceField, SequenceField)
from mongoengine.queryset.visitor import Q, QCombination


class DataTables(object):
    # Class-level cache for field_type_dict per model
    _cached_field_type_dict = {}

    def __init__(self, model, request_args, embed_search={}, q_obj=[],
                 custom_filter={}, exclude_lst=[]):
        """
        :param model: The MongoEngine model.
        :param request_args: Passed as Flask request.values.get('args').
        :param embed_search: For specific search inside EmbeddedDocumentField.
        :param q_obj: Additional search queries in reference collections.
        :param custom_filter: Additional filters.
        :param exclude_lst: Fields to exclude for performance optimization.
        """
        self.model = model
        # Normalize request parameters to support both DT 1.x and 2.x.
        self.request_args = self.normalize_request_args(request_args)
        self.columns = self.request_args.get('columns')
        self.search_string = self.request_args.get('search', {}).get('value')
        self.embed_search = embed_search
        self.q_obj = q_obj
        self.custom_filter = custom_filter
        self.exclude_lst = exclude_lst

        # Cache field type dictionary per model to avoid recalculating
        if model not in DataTables._cached_field_type_dict:
            _num_types = {IntField, BooleanField, DecimalField, FloatField,
                          LongField, SequenceField}
            _embed_types = {EmbeddedDocumentField, EmbeddedDocumentListField}
            field_type_dict = {}
            for k, v in model._fields.items():
                if type(v) in _num_types:
                    field_type_dict[k] = 'number'
                elif type(v) in {ReferenceField}:
                    field_type_dict[k] = 'reference'
                elif type(v) in {ObjectIdField}:
                    field_type_dict[k] = 'objectID'
                elif type(v) in {ListField}:
                    field_type_dict[k] = 'list'
                elif type(v) in _embed_types:
                    field_type_dict[k] = 'embed'
                else:
                    field_type_dict[k] = 'other'
            DataTables._cached_field_type_dict[model] = field_type_dict
        self.field_type_dict = DataTables._cached_field_type_dict[model]

    @staticmethod
    def normalize_request_args(args):
        """
        Normalizes request parameters to support both DataTables 1.x and 2.x.
        Converts keys and value types to a unified format.
        """
        normalized = {}

        # Convert draw, start, length parameters.
        normalized["draw"] = args.get("draw")
        try:
            normalized["start"] = int(args.get("start", 0))
        except (ValueError, TypeError):
            normalized["start"] = 0
        try:
            length = int(args.get("length", 10))
        except (ValueError, TypeError):
            length = 10
        normalized["length"] = None if length == -1 else length

        # Normalize global search parameter.
        search = args.get("search")
        if isinstance(search, dict):
            normalized["search"] = search
        elif isinstance(search, str):
            normalized["search"] = {"value": search, "regex": False}
        else:
            normalized["search"] = {"value": "", "regex": False}

        # Normalize order (wrap in a list if it is a dictionary).
        order = args.get("order")
        if isinstance(order, dict):
            normalized["order"] = [order]
        elif isinstance(order, list):
            normalized["order"] = order
        else:
            normalized["order"] = []

        # Normalize columns.
        columns = args.get("columns")
        if columns and isinstance(columns, list) and len(columns) > 0:
            # If columns are provided as strings, convert them to objects.
            if isinstance(columns[0], str):
                normalized["columns"] = [
                    {"data": col, "searchable": True, "orderable": True,
                     "search": {"value": "", "regex": False}}
                    for col in columns
                ]
            else:
                normalized["columns"] = columns
        else:
            normalized["columns"] = []

        return normalized

    @property
    def total_records(self):
        if self.custom_filter:
            return str(self.model.objects(**self.custom_filter).count())
        return str(self.model.objects().count())

    @property
    def search_terms(self):
        return str(self.request_args.get("search")["value"]).split()

    @property
    def requested_columns(self):
        return [column["data"] for column in self.request_args.get("columns")]

    @property
    def draw(self):
        return self.request_args.get("draw")

    @property
    def start(self):
        return self.request_args.get("start")

    @property
    def limit(self):
        return self.request_args.get("length")

    @property
    def order_dir(self):
        """
        Returns '' for 'asc' or '-' for 'desc'.
        If no order is specified, defaults to 'asc'.
        """
        orders = self.request_args.get("order", [])
        if orders and isinstance(orders, list):
            _dir = orders[0].get("dir", "asc")
        else:
            _dir = "asc"
        _MONGO_ORDER = {'asc': '', 'desc': '-'}
        return _MONGO_ORDER.get(_dir, '')

    @property
    def order_column(self):
        """
        DataTables provides the index of the order column,
        but MongoDB requires the column name.
        If no order is specified, returns an empty string.
        """
        orders = self.request_args.get("order", [])
        if orders and isinstance(orders, list):
            order_index = orders[0].get("column", 0)
            requested_columns = self.requested_columns
            if len(requested_columns) > order_index:
                return requested_columns[order_index]
        return ""

    @property
    def dt_column_search(self):
        """
        Adds support for column-specific search.
        Reference: https://datatables.net/examples/api/multi_filter.html
        """
        _cols = []
        for column in self.request_args.get('columns'):
            _val = column.get('search', {}).get('value', '')
            _regex = column.get('search', {}).get('regex', False)
            _data = column.get('data')
            if _val == '':
                continue
            if not _regex:
                _cols.append(dict(column=_data, value=_val, regex=False))
            else:
                # Compile regex for case-insensitive search.
                _d = {_data: re.compile(_val, re.IGNORECASE)}
                self.custom_filter.update(**_d)
        return _cols

    def query_by_col_type(self, _q, col):
        """Builds a query depending on the field type."""
        if self.field_type_dict.get(col) == 'number':
            if _q.isdigit() and len(_q) < 19:
                return [Q(**{col: _q})]
            return []

        if self.field_type_dict.get(col) == 'objectID':
            if not ObjectId.is_valid(_q):
                return []

        if self.field_type_dict.get(col) == 'embed':
            if not self.embed_search:
                return []
            _em = []
            for field in self.embed_search.get(col)['fields']:
                _emb = f'{col}__{field}__icontains'
                _em.append(Q(**{_emb: _q}))
            return _em

        return [Q(**{col + '__icontains': _q})]

    @property
    def get_search_query(self):
        """Builds the search query."""
        queries = []
        _column_names = [d['data'] for d in self.columns if d.get(
            'data') in self.field_type_dict.keys() and d.get('searchable')]
        # Global search across all columns.
        if self.search_string:
            for col in _column_names:
                _q = self.search_string
                _obj = self.query_by_col_type(_q, col)
                queries += _obj

        # Column-specific search.
        _own_col_q = []
        for column_search in self.dt_column_search:
            col = column_search['column']
            term = column_search['value']
            _obj = self.query_by_col_type(term, col)
            _own_col_q += _obj

        if self.q_obj:
            queries.append(self.q_obj)

        _search_query = QCombination(QCombination.OR, queries)
        if _own_col_q:
            _own_col_q = QCombination(QCombination.AND, _own_col_q)
            _search_query = (_search_query & _own_col_q)

        if self.custom_filter:
            _search_query = (_search_query & Q(**self.custom_filter))

        return _search_query

    def results(self):
        """
        Executes the query and returns results.
        Note: The use of skip() may become a bottleneck for very large offsets.
        """
        _res = self.model.objects(self.get_search_query)
        _order_by = f'{self.order_dir}{self.order_column}'
        _results = _res.exclude(*self.exclude_lst).order_by(_order_by).skip(
            self.start).limit(self.limit).as_pymongo()

        # The double conversion via json_util.dumps and json.loads can be heavy
        # for large result sets. Consider using a custom encoder if performance
        # becomes an issue.
        data = json.loads(json_util.dumps(_results))
        return dict(data=data, count=_res.count())

    def get_rows(self):
        _res = self.results()
        # If no global search, use the cached total record count.
        rec_totals = self.total_records if self.search_string else _res.get(
            'count')
        return {'recordsTotal': rec_totals,
                'recordsFiltered': _res.get('count'),
                'draw': int(str(self.draw)),
                'data': _res.get('data')}
