from .base_view import ClassView


def get_model_value(instance, field):
    try:
        value = getattr(instance, field)
    except Exception:
        if field.find('__') > 0:
            fields = field.split('__')
        elif field.find('.') > 0:
            fields = field.split('.')
        else:
            raise Exception()
        value = instance
        for field in fields:
            value = getattr(value, field)
            if value is None:
                return None
    return value


class ModelListView(ClassView):
    fields = None

    has_pagination = True

    default_per_page = 10

    def __init__(self, request):
        ClassView.__init__(self, request)

        get = request.GET.get

        self.per_page = get("per_page", self.default_per_page)
        self.per_page = int(self.per_page)

        self.page = get("page", 1)
        self.page = int(self.page)

        self.search = get("search", "")
        self.sort_param = get("sort", None)

        self.data = {}
        self.json_string = None

        self.validate_fields()

    def validate_fields(self):
        fields = self.fields
        if type(fields) not in (list, tuple):
            raise Exception("Fields format is not valid.")

        new_fields = []
        for field in fields:
            if type(field) in (list, tuple):
                if len(field) > 2:
                    raise Exception("Fields format is not valid.")

                field, json_key = field
            else:
                field, json_key = field, field

            new_fields.append((field, json_key))

        self.fields = new_fields

    def get_query(self):
        raise NotImplementedError()

    def to_json(self, record):
        fields = self.fields
        data = {}

        for field, json_key in fields:
            fn = getattr(self, 'render_' + field, None)
            if fn is not None:
                value = fn(record)
            else:
                value = get_model_value(record, field)
            data[json_key] = value

        return data

    # noinspection PyBroadException
    def sort(self, query):
        sort = self.sort_param
        if not sort:
            return query

        try:
            param, asc = sort.split("|")
            if asc != "asc":
                param = "-" + param
            return query.order_by(param)
        except Exception:
            return query

    def get_count(self, query):
        from django.db.models.query import QuerySet

        if type(query) is QuerySet:
            return query.count()

        return len(query)

    def process(self, request):
        query = self.get_query()
        fields = [a for a, b in self.fields]

        if len(fields) > 0:
            query = query.only(*fields)

        query = self.sort(query)
        if self.has_pagination:
            data = self.paginate(query)
        else:
            data = [self.to_json(record) for record in query]

        self.add("status", True)
        self.add('total', self.get_count(query))
        self.add("data", data)

    def paginate(self, query):
        from django.core.paginator import Paginator

        if not self.has_pagination:
            return

        paginator = Paginator(query, self.per_page)

        page = paginator.page(self.page)
        records = page.object_list
        data = [self.to_json(record) for record in records]

        self.add("last_page", paginator.num_pages)
        self.add("from", page.start_index())
        self.add("current_page", self.page)
        self.add("per_page", self.per_page)
        self.add("to", page.end_index())

        return data

