import collections

class Simulation:

    def __init__(self, filename: str):
        self.data = parse_input_file('maps/{0}.in'.format(filename))
        self.drones = []

        self.init_drones()

    def init_drones(self):
        for i in range(self.data.drone_count):
            self.drones.append(Drone(i, self))

    def simulate(self):
        warehouse = self.data.get_warehouse_by_id(0)
        # commands_info.append({
        #     "coords": coords,
        #     "nb_items": nb_items, 10 item dans la commande
        #     "items_qty": dict_items_qty {'itemId', 5}
        # })
        # print(self.data.max_drone_load)
        travels = {}
        for order_id, order in enumerate(self.data.commands_info):
            items = order['items_qty']
            total_weight = 0
            for id, qty in items.items():
                weight = self.data.get_weight(id)
                total_weight += weight * qty

            if total_weight != 0:
                travel_count = ((total_weight-1) // self.data.max_drone_load)+1
                if travel_count not in travels:
                    travels[travel_count] = []

                travels[travel_count].append(order_id)

        travels = dict(collections.OrderedDict(sorted(travels.items())))

        drone_path = {}
        for i in range(len(self.drones)):
            drone_path[i] = []

        for ind in travels.keys():
            while len(travels[ind]) > 0:
                for i, drone in enumerate(self.drones):
                    if len(travels[ind]) == 0:
                        break

                    for j in range(ind):
                        drone_path[i].append(travels[ind][0])

                    del travels[ind][0]

        for i in range(len(self.drones)):
            self.drones[i].fromPath(drone_path[i])


class Drone:
    LOAD_SIGN = 'L'
    UNLOAD_SIGN = 'U'
    DELIVER_SIGN = 'D'
    WAIT_SIGN = 'W'

    def __init__(self, drone_id, position: tuple, simulation):
        self.id = drone_id
        self.simulation = simulation
        self.commands = []
        self.position = position

    def fromPath(self, path: list):
        for order_id in path:
            total_weight = 0
            drone_load = {}

            order = self.simulation.data.get_command(order_id)
            for item_id, qty in order['items_qty'].items():  # On load
                if qty > 0:
                    order_weight = self.simulation.data.get_weight(item_id) * qty
                    futur_weight = order_weight + total_weight
                    if futur_weight < self.simulation.data.max_drone_load:
                        total_weight = futur_weight

                        warehouses = self.simulation.data.get_warehouse_by_item_id(item_id, qty)
                        if len(warehouses) > 0:
                            for warehouse_id in warehouses:
                                warehouse_qty = self.simulation.data.get_qty_in_warehouse(warehouse_id, item_id)
                                if warehouse_qty < qty:
                                    qty = warehouse_qty

                                self.load(warehouse_id, item_id, qty)
                                if order_id not in drone_load:
                                    drone_load[order_id] = []

                                drone_load[order_id].append((item_id, qty))
                                self.simulation.data.remove_item_from_order(warehouse_id, order_id, item_id, qty)
                    else:
                        break

            for order_id, l in drone_load.items():  # On deliver
                for t in l:
                    self.deliver(order_id, t[0], t[1])

            self.position =

    def append_cmd(self, cmd: str):
        self.commands.append("{0}\n".format(cmd))

    def get_commands(self) -> str:
        return "".join(self.commands)

    def get_commands_count(self) -> int:
        return len(self.commands)

    def load(self, warehouse_id, item_id, item_qty):
        cmd = "{0} {1} {2} {3} {4}".format(self.id, Drone.LOAD_SIGN, warehouse_id, item_id, item_qty)
        self.append_cmd(cmd)

    def unload(self, warehouse_id, item_id, item_qty):
        cmd = "{0} {1} {2} {3} {4}".format(self.id, Drone.UNLOAD_SIGN, warehouse_id, item_id, item_qty)
        self.append_cmd(cmd)

    def deliver(self, cmd_id, item_id, item_qty):
        cmd = "{0} {1} {2} {3} {4}".format(self.id, Drone.DELIVER_SIGN, cmd_id, item_id, item_qty)
        self.append_cmd(cmd)

    def wait(self, time):
        cmd = "{0} {1} {2}".format(self.id, Drone.DELIVER_SIGN, time)
        self.append_cmd(cmd)


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

    def get_weight(self, item_id):
        return self.products_weight[item_id]

    def get_warehouse_by_id(self, warehouse_id):
        return self.warehouse_info[warehouse_id]

    def get_qty_in_warehouse(self, warehouse_id, item_id):
        return self.warehouse_info[warehouse_id]['qty'][item_id]

    def get_warehouse_position(self, warehouse_id) -> tuple:
        return self.warehouse_info[warehouse_id]['coords']

    def get_warehouse_by_item_id(self, item_id, qty):
        # warehouse_info.append({
        #     "coords": coords,
        #     "qty": qty_each_item
        # })
        total_qty = 0
        warehouses = []
        for i in range(len(self.warehouse_info)):
            warehouse_qty = self.warehouse_info[i]['qty'][item_id]
            if warehouse_qty > 0:
                if warehouse_qty >= qty:
                    return [i]

                total_qty += qty
                warehouses.append(i)

                if total_qty >= qty:
                    break

        return warehouses

    def get_warehouse_id_with_coords(self, coords: tuple):
        for i in range(len(self.warehouse_info)):
            if coords == self.warehouse_info[i]['coords']:
                return i
        return -1

    def remove_item_from_order(self, warehouse_id, order_id, item_id, qty):
        self.warehouse_info[warehouse_id]['qty'][item_id] -= qty
        self.commands_info[order_id]['items_qty'][item_id] -= qty

    def get_warehouse_item_qty(self, warehouse_id, item_id):
        return self.warehouse_info[warehouse_id]['qty'][item_id]

    def get_command(self, cmd_id):
        return self.commands_info[cmd_id]

    def get_item_quantity(self, warehouse_id, item_id):
        return self.warehouse_info[warehouse_id]['qty'][item_id]

    def get_command_coords(self, cmd_id):
        return self.commands_info[cmd_id]['coords']

    def get_command_nb_items(self, cmd_id):
        return self.commands_info[cmd_id]['nb_items']

    def get_command_item_qty(self, cmd_id, item_id):
        return self.commands_info[cmd_id]['items_qty'][str(item_id)]


def parse_input_file(filename: str) -> cmd_responses:
    file = open(filename, 'r')
    lines = file.readlines()

    first_line = lines[0].split(" ")

    line_count = int(first_line[0])
    col_count = int(first_line[1])
    drone_count = int(first_line[2])
    simulation_duration = int(first_line[3])
    max_drone_load = int(first_line[4])

    product_count = int(lines[1])

    third_line = lines[2].split(" ")
    products_weight = []
    for element in third_line:
        products_weight.append(int(element))

    warehouse_count = int(lines[3])
    warehouse_info = []
    line_index = 3 + warehouse_count * 2
    for i in range(4, line_index, 2):
        coords_string = lines[i].split(" ")
        coords = (int(coords_string[0]), int(coords_string[1]))
        qty_each_item = []
        for element in lines[i+1].split(" "):
            qty_each_item.append(int(element))

        warehouse_info.append({
            "coords": coords,
            "qty": qty_each_item
        })

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

        dict_items_qty = dict(collections.Counter(items))
        commands_info.append({
            "coords": coords,
            "nb_items": nb_items,
            "items_qty": dict_items_qty  # {'itemId': qty }
        })

    return cmd_responses(line_count, col_count, drone_count, simulation_duration, max_drone_load, product_count,
                         products_weight, warehouse_count, warehouse_info, cmd_count, commands_info)


def write_output_file(filename: str, drones: list):
    output = open(filename, "w")

    orders_to_exe = 0
    cmd_lines = []
    for drone in drones:
        orders_to_exe += drone.get_commands_count()
        cmd_lines.append(drone.get_commands())

    header = [(str(orders_to_exe) + '\n')]

    output.writelines(header + cmd_lines)


if __name__ == "__main__":
    # s = Simulation('busy_day')
    # s = Simulation('mother_of_all_warehouses')
    s = Simulation('redundancy')
    s.simulate()
    write_output_file('test.txt', s.drones)
    pass
