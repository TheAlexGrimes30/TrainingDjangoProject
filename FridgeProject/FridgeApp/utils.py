class TitleMixin:
    title = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context

class FridgeFilterMixin:
    def get_filter_fridge_data(self, queryset):
        brand = self.request.GET.get('brand', '')
        model = self.request.GET.get('model', '')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        min_capacity = self.request.GET.get('min_capacity')
        max_capacity = self.request.GET.get('max_capacity')

        if brand:
            queryset = queryset.filter(brand__icontains=brand)

        if model:
            queryset = queryset.filter(model__icontains=model)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if min_capacity:
            queryset = queryset.filter(capacity__gte=min_capacity)

        if max_capacity:
            queryset = queryset.filter(capacity__lte=max_capacity)

        return queryset

class FridgeContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context['query_params'] = query_params.urlencode()
        context['filters'] = self.request.GET
        return context