import collections

class cmd_responses:

    def __init__(self, line_count, col_count, drone_count, simulation_duration, max_drone_load, product_count,
                 products_weight, warehouse_count, warehouse_info, cmd_count, commands_info):
        self.line_count = line_count
        self.col_count = col_count
        self.drone_count = drone_count
        self.simulation_duration = simulation_duration
        self.max_drone_load = max_drone_load
        self.product_count = product_count
        self.products_weight = products_weight
        self.warehouse_count = warehouse_count
        self.warehouse_info = warehouse_info
        self.cmd_count = cmd_count
        self.commands_info = commands_info


def parse_input_file(filename: str) -> cmd_responses:
    file = open(filename, 'r')
    lines = file.readlines()

    line_count = 0
    col_count = 0
    drone_count = 0
    simulation_duration = 0
    max_drone_load = 0

    first_line = lines[0].split(" ")

    line_count = int(first_line[0])
    col_count = int(first_line[1])
    drone_count = int(first_line[2])
    simulation_duration = int(first_line[3])
    max_drone_load = int(first_line[4])

    # print(line_count, col_count, drone_count, simulation_duration, max_drone_load)

    product_count = int(lines[1])

    third_line = lines[2].split(" ")
    products_weight = []
    for element in third_line:
        products_weight.append(int(element))

    # print(products_weight[:10])

    warehouse_count = int(lines[3])
    warehouse_info = []
    line_index = 3 + warehouse_count * 2
    for i in range(4, line_index, 2):
        coords_string = lines[i].split(" ")
        coords = (int(coords_string[0]), int(coords_string[1]))
        qty = []
        for element in lines[i+1].split(" "):
            qty.append(int(element))

        warehouse_info.append({
            "coords": coords,
            "qty": qty
        })

    # print(warehouse_info[:2][1])

    line_index += 1
    cmd_count = int(lines[line_index])
    line_index += 1
    commands_info = []
    for i in range(line_index, line_index + cmd_count * 3, 3):
        coords_string = lines[i].split(" ")
        coords = (int(coords_string[0]), int(coords_string[1]))

        nb_items = int(lines[i+1])
        items = []
        for element in lines[i+2].split(" "):
            items.append(int(element))

        dict_items_qty = collections.Counter(items)
        commands_info.append({
            "coords": coords,
            "nb_items": nb_items,
            "items_qty": dict_items_qty
        })

    # print(commands_info[-1])
    return cmd_responses(line_count, col_count, drone_count, simulation_duration, max_drone_load, product_count,
                         products_weight, warehouse_count, warehouse_info, cmd_count, commands_info)


def format_line_to_output(string: str) -> str:
    return "{0}\n".format(string)


def write_output_file(filename: str, drones: list):
    output = open(filename, "w")
    orders_to_exe = format_line_to_output("0")
    lines = [format_line_to_output(orders_to_exe)]

    for i, drone in enumerate(drones):
        cmd = "{0} {1}".format(i, drone.commandes)
        lines.append(format_line_to_output(cmd))

    output.writelines(lines)


if __name__ == "__main__":
    # rep = parse_input_file('maps/busy_day.in')
    write_output_file('output_text.txt')
    print("Code here people :)")
