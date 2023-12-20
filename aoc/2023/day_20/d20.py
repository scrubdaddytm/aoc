from collections import defaultdict
from aoc.cli import file_input
from math import lcm


def main() -> None:
    modules = {}
    module_memory = {}
    input_modules = defaultdict(list)

    with file_input() as file:
        while line := file.readline().strip():
            line = line.split(" -> ")
            destination_modules = line[1].split(",")
            destination_modules = [m.strip() for m in destination_modules]
            name = ""
            module_type = None
            if line[0] == "broadcaster":
                name = line[0]
                module_type = name
            else:
                name = line[0][1:]
                module_type = "flip-flop" if line[0][0] == "%" else "conjunction"
                module_memory[name] = False if module_type == "flip-flop" else {}
            modules[name] = (module_type, destination_modules)

            for destination_module in destination_modules:
                input_modules[destination_module].append(name)

    for module_name, module_info in modules.items():
        module_type = module_info[0]
        if module_type == "conjunction":
            for other_module in input_modules[module_name]:
                module_memory[module_name][other_module] = False

    pulse_count = {False: 0, True: 0}
    modules["button"] = ("button", ["broadcaster"])

    cycles = {}

    for idx in range(1, 5_001):
        queue = [("button", False, "blah")]
        while queue:
            module_name, pulse_type, input_module = queue.pop(0)

            if module_name not in modules:
                continue

            module_type, destinations = modules[module_name]
            next_pulse = None
            if module_name == "button" or module_name == "broadcaster":
                next_pulse = False
            elif module_type == "conjunction":
                module_memory[module_name][input_module] = pulse_type
                next_pulse = not all(module_memory[module_name].values())
                if not next_pulse and module_name not in cycles:
                    cycles[module_name] = idx
            elif not pulse_type:
                module_memory[module_name] = not module_memory[module_name]
                next_pulse = module_memory[module_name]

            if next_pulse is not None:
                for next_module in destinations:
                    # print(f"  {module_name} -{'high' if next_pulse else 'low'}-> {next_module}")
                    queue.append((next_module, next_pulse, module_name))
                    pulse_count[next_pulse] += 1
        if idx == 1000:
            print(f"Part 1: {pulse_count}: {pulse_count[False] * pulse_count[True]}")

    print(cycles)

    print(f"Part 2: {lcm(*list(cycles.values()))}")


if __name__ == "__main__":
    main()
