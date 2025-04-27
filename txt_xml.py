import re


def parse_struct_block(start_line, lines_iter):
    struct_match = re.match(r"\s*(\w+)\s+Struct\{(\d+)\}", start_line)
    if not struct_match:
        return ""

    block_name = struct_match.group(1)
    struct_count = int(struct_match.group(2))

    xml = f"    <{block_name}>\n"

    for _ in range(struct_count):
        line = next(lines_iter).strip()
        param_match = re.match(r">>> \d+\.(\w+)\s*=\s*(.+)", line)
        if param_match:
            param_name = param_match.group(1)
            values = param_match.group(2).split()
            for val in values:
                xml += f"      <{param_name}>{val}</{param_name}>\n"

    xml += f"    </{block_name}>\n"
    return xml


def parse_simple_kv_line(line):
    # Match like: paramName    value
    match = re.match(r"\s*(\w+)\s+(\S+)", line)
    if match:
        param_name = match.group(1)
        value = match.group(2)
        return f"    <{param_name}>{value}</{param_name}>\n"
    return ""


def convert_line_to_xml(line, lines_iter):
    match = re.search(r"ENodeBFunction=(\d+),EUtranCellFDD=(\w+)", line)
    if not match:
        return None


    xml_output = f"""
<ENodeBFunction xmlns="urn:com:ericsson:ecim:Lrat">
  <eNodeBFunctionId>1</eNodeBFunctionId>
"""

    # Process lines until separator
    for next_line in lines_iter:
        if "Struct{" in next_line:
            xml_output += parse_struct_block(next_line, lines_iter)
        elif re.match(r"\s*(\w+)\s+(\S+)", next_line):
            xml_output += parse_simple_kv_line(next_line)
        elif re.match(r"\s*=+", next_line):
            break

    # Append this at the end so we don't skip Structs above it
    xml_output += f""

    xml_output += """  </EUtranCellFDD>
</ENodeBFunction>
"""
    return xml_output


# Run the parser
with open("source.txt", "r") as infile:
    lines = infile.readlines()
    lines_iter = iter(lines)

    for line in lines_iter:
        if "ENodeBFunction=" in line and "EUtranCellFDD=" in line:
            xml_result = convert_line_to_xml(line, lines_iter)
            if xml_result:
                print(xml_result)
