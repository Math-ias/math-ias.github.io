import leather 

leather.theme.axis_title_color = "#000000"
leather.theme.axis_title_font_size = 15
leather.theme.axis_title_gap = 30
leather.theme.background_color = "#ffffff"
leather.theme.default_chart_height = 350
leather.theme.default_chart_width = 600
leather.theme.axis_title_font_family = "monospace"
leather.theme.default_dot_radius = 7
leather.theme.default_line_width = 7
leather.theme.label_color = "#000000"
leather.theme.tick_color = "#000000"
leather.theme.tick_font_size = 15
leather.theme.tick_size = 3
leather.theme.tick_font_family = "monospace"
leather.theme.tick_width = 1
leather.theme.title_color = "#000000"
leather.theme.title_font_size = 15
leather.theme.zero_color = "#000000"
leather.theme.title_font_family = "monospace"

with open(".7.txt", "r") as fp:
    positions = list(map(lambda position: int(position), ",".join(fp.readlines()).split(",")))

chart_one = leather.Chart("Total Cost VS Chosen Center (Pt 1)")
chart_two = leather.Chart("Total Cost VS Chosen Center (Pt 2)")

part_one_points = []
part_two_points = []

for center in range(min(positions), max(positions) + 1):
    part_one_points.append(
        (center,
        sum(map(lambda position: abs(position - center), positions))/1000)
    )
    part_two_points.append(
        (center,
        sum(map(lambda position: ((position - center)**2 + abs(position - center)) >> 1, positions))/1000000)
    )

chart_one.add_line(part_one_points)
chart_one.add_x_axis(name="Center")
chart_one.add_y_axis(name="Total Cost (thousands)")
chart_two.add_line(part_two_points)
chart_two.add_x_axis(name="Center")
chart_two.add_y_axis(name="Total Cost (millions)")
print(chart_one.to_svg())
print(chart_two.to_svg())
