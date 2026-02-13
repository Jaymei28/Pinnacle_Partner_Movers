from django.utils.cache import add_never_cache_headers


class DisableAdminCachingMiddleware:
    """
    Middleware to disable caching for Django admin pages.
    This prevents browsers from caching admin pages which can cause
    stale data to be displayed when clicking on items.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Only apply to admin URLs
        if request.path.startswith('/admin/'):
            add_never_cache_headers(response)
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response
