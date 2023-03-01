from functools import wraps


def paginate_content():
    default_range = "0-9"

    def wrap(func):
        """Wrapper for header parser"""

        @wraps(func)
        def header_parser(self, request):
            """Request header parser"""

            if "Range" in request.headers:
                range_ = request.headers.get("Range", "0-9")
            else:
                range_ = default_range

            self.pagination_start, self.pagination_end = [
                int(x) for x in range_.split("-")
            ]

            return func(self, request)

        return header_parser

    return wrap
