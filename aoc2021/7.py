import leather 

leather.theme.axis_title_font_family = "monospace"
leather.theme.background_color="#ffffff"
leather.theme.tick_font_family = "monospace"
leather.theme.title_font_family = "monospace"

with open(".7.txt", "r") as fp:
    positions = list(map(lambda position: int(position), ",".join(fp.readlines()).split(",")))

chart_one = leather.Chart("Total Cost VS Chosen Center (Part One)")
chart_two = leather.Chart("Total Cost VS Chosen Center (Part Two)")

part_one_points = []
part_two_points = []

for center in range(min(positions), max(positions) + 1):
    part_one_points.append(
        (center,
        sum(map(lambda position: abs(position - center), positions)))
    )
    part_two_points.append(
        (center,
        sum(map(lambda position: ((position - center)**2 + abs(position - center)) >> 1, positions)))
    )

chart_one.add_line(part_one_points)
chart_one.add_x_axis(name="Center")
chart_one.add_y_axis(name="Total Cost")
chart_two.add_line(part_two_points)
chart_two.add_x_axis(name="Center")
chart_two.add_y_axis(name="Total Cost")
print(chart_one.to_svg())
print(chart_two.to_svg())

