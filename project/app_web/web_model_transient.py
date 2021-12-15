class WebPageContent:
    def __init__(
        self, default_title, default_subtitle=None, default_subtitle_info=None
    ):
        self.title = default_title
        self.subtitle = default_subtitle
        self.subtitle_info = default_subtitle_info
        if self.subtitle is None:
            self.subtitle = """Lorem ipsum dolor sit amet, consetetur sadipscing elitr,
                sed diam."""
        if self.subtitle_info is None:
            self.subtitle_info = """Lorem ipsum dolor sit amet, consetetur sadipscing
            elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna
            aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo
            dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus
            est Lorem ipsum dolor sit amet."""
