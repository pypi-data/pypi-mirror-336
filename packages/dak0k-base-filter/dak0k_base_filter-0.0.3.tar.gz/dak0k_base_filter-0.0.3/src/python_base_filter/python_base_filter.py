import json
from datetime import datetime

from django.db.models import Q


class BaseFilter:
    def __init__(self, queryset, params):
        self.queryset = queryset
        self.params = params

    def apply_filters(self):
        filters = self.get_filters()
        for field, value in filters.items():
            if value:
                self.queryset = self.filter_by_field(field, value)

        global_filter_q = self.get_global_filter()
        if global_filter_q:
            self.queryset = self.queryset.filter(global_filter_q)

        sorting_list = self.get_sorting()
        if sorting_list:
            order_fields = []
            for (field_id, desc) in sorting_list:
                order_fields.append("-" + field_id if desc else field_id)
            self.queryset = self.queryset.order_by(*order_fields)

        return self.queryset

    def get_filters(self):
        """Retrieve and parse filters from request parameters"""
        filters_str = self.params.get('filters', '[]')
        try:
            filters_data = json.loads(filters_str)
        except json.JSONDecodeError:
            filters_data = []

        transformed_filters = {}
        for item in filters_data:
            field_id = item.get('id')
            value = item.get('value')
            if field_id:
                field_id = field_id.replace('.', '__')
            transformed_filters[field_id] = value

        return transformed_filters

    def get_sorting(self):
        """Retrieve and parse sorting as a list of (field, desc) from request parameters"""
        sorting_str = self.params.get('sorting', '[]')
        try:
            sorting_list = json.loads(sorting_str)
        except json.JSONDecodeError:
            sorting_list = []

        results = []
        for item in sorting_list:
            field_id = item.get('id')
            field_id = field_id.replace('.', '__') if field_id else None

            desc = item.get('desc', False)
            if field_id:
                results.append((field_id, desc))
        return results

    def get_global_filter(self):
        global_filter = self.params.get('globalFilter')
        if not global_filter:
            return None

        try:
            global_filter = json.loads(global_filter)
        except json.JSONDecodeError:
            global_filter = str(global_filter)

        if not global_filter:
            return None

        search_value = str(global_filter)
        search_query = Q()

        model = self.queryset.model
        text_fields = [field.name for field in model._meta.fields if
                       hasattr(field, 'get_internal_type') and field.get_internal_type() in ['CharField', 'TextField']]

        for field in text_fields:
            search_query |= Q(**{f"{field}__icontains": search_value})

        return search_query

    def filter_by_field(self, field, value):
        """Filter queryset based on the field and value"""
        if isinstance(value, list) and len(value) == 2:
            return self.filter_by_range(field, value)
        return self.filter_by_exact_match(field, value)

    def filter_by_exact_match(self, field, value):
        """Handles exact matches and partial text search"""
        if isinstance(value, str):
            return self.queryset.filter(**{f"{field}__icontains": value})
        return self.queryset.filter(**{field: value})

    def filter_by_range(self, field, value):
        """Handles date range filtering"""
        try:
            start_date = datetime.strptime(value[0], "%Y-%m-%d").date()
            end_date = datetime.strptime(value[1], "%Y-%m-%d").date()
            return self.queryset.filter(**{f"{field}__range": [start_date, end_date]})
        except ValueError:
            return self.queryset