import sys

import colored


DEFAULT_FORMAT = {
    "width": 0,
    "align": "left",
    "fill": "",
    "color": lambda x: "default",
    "bold": False
}

ALIGN = {
    "left": "<",
    "default": "<",
    "right": ">",
    "center": "^"
}


def clicolumn(txt, opts=DEFAULT_FORMAT, title=False):
    align = opts.get("align").lower()
    if hasattr(opts.get("color"), "__call__"):
        c = opts.get("color")(txt)
    else:
        c = opts.get("color")

    c = c.lower()
    if (c not in colored._ALL) or title:
        c = "default"

    if align not in ALIGN:
        align = "default"

    align = ALIGN[align]
    width = opts.get("width", 0)
    fill = opts.get("fill", "")

    raw_txt = "{0:{fill}{align}{width}}".format(txt,
                                                fill=fill,
                                                align=align,
                                                width=width)
    if opts.get("bold"):
        return colored.bold(getattr(colored, c)(raw_txt))
    else:
        return getattr(colored, c)(raw_txt)


class CliTable(object):
    def __init__(self, num_cols, autowidth=True, space=" ", bold=False,
                 title_row=True, underline=True,
                 row_color_func=lambda x: "default"):
        self.num_cols = num_cols
        self.cols_format = [DEFAULT_FORMAT] * num_cols
        self.rows = []
        self.title_row_values = []
        self.max_lengths = [0] * num_cols
        self.autowidth = autowidth
        self.space = space
        self.bold = bold
        self.title_row = title_row
        self.underline = underline
        self.row_color_func = row_color_func

    def format_column(self, col, width=0, align="left",
                      fill="", color=lambda x: "default"):
        self.cols_format[col - 1] = {
            "width": width,
            "align": align,
            "fill": fill,
            "color": color
        }

    def set_max(self, values):
        if not self.autowidth:
            return

        for idx, v in enumerate(values):
            v = str(v)
            if self.max_lengths[idx] < len(v):
                self.max_lengths[idx] = len(v)

    def add_title_row(self, *values):
        self.set_max(values)
        self.title_row_values = values

    def add_row(self, *values):
        self.set_max(values)
        self.rows.append(values)

    def display(self):
        if self.rows:
            # Print Title Row and Underline using hyphen
            if self.title_row_values:
                title_row_out = []
                total_length = 0
                for idx, col in enumerate(self.title_row_values):
                    total_length += self.max_lengths[idx]
                    self.cols_format[idx]["width"] = self.max_lengths[idx]
                    self.cols_format[idx]["bold"] = self.bold
                    title_row_out.append(
                        clicolumn(col, DEFAULT_FORMAT, title=True)
                    )
                sys.stdout.write("{0}\n".format(self.space.join(
                    title_row_out)))
                if self.underline:
                    hyphen_width = (len(self.space) * (self.num_cols - 1) +
                                    total_length)
                    sys.stdout.write("{0}\n".format("-" * hyphen_width))

        for row in self.rows:
            row_out = []
            for idx, col in enumerate(row):
                if self.autowidth:
                    self.cols_format[idx]["width"] = self.max_lengths[idx]

                row_out.append(
                    clicolumn(col, self.cols_format[idx])
                )

            row_color = self.row_color_func(row_out)
            row_color = row_color.lower()
            if (row_color not in colored._ALL):
                row_color = "default"

            out = "{0}\n".format(self.space.join(row_out))
            sys.stdout.write(getattr(colored, row_color)(out))
