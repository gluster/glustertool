from glustertool.utils import clitable

# Number of Gluster patches per Year
# git log --after={2010-12-31} --before={2012-01-01} --oneline
# | wc -l # YEAR 2011
data = ((2011, 1181),
        (2012, 1129),
        (2013, 972),
        (2014, 1165),
        (2015, 1732))


def format_patches(value):
    if int(value) > 1000:
        return "green"
    else:
        return "yellow"

table = clitable.CliTable(num_cols=2,
                          autowidth=True,
                          title_row=True,
                          underline=True,
                          space="    ")
table.format_column(2, align="right", color=format_patches)
table.add_title_row("YEAR", "PATCHES")
for row in data:
    table.add_row(row[0], row[1])

table.display()
