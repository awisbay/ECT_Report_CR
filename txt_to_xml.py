import re

EXCLUDED_PARAMETERS = {
    "ailgRef",
    # Add more excluded parameters if needed
}


def extract_value(value):
    """Extract the value inside parentheses if present, otherwise return value."""
    match = re.search(r"\(([^)]+)\)", value)
    if match:
        return match.group(1).strip()
    return value.strip()


def is_placeholder_or_empty(value):
    """Check for placeholder values like i[0] =, b[0] =, etc. or empty values."""
    value = value.strip()
    if not value:
        return True
    if re.match(r"^[bit]\[\d+\]\s*=?\s*$", value):
        return True
    return False


def loose_wrap_to_xml(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    xml_lines = ["<root>"]
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("="):
            i += 1
            continue

        if "Struct{" in line:
            struct_key = line.split()[0]
            struct_children = []
            i += 1
            while i < len(lines) and lines[i].strip().startswith(">>>"):
                struct_line = lines[i].strip()[4:]  # remove '>>> '
                if "=" in struct_line:
                    _, kv = struct_line.split(".", 1)
                    key, value = [s.strip() for s in kv.split("=", 1)]

                    if key in EXCLUDED_PARAMETERS or is_placeholder_or_empty(value):
                        i += 1
                        continue

                    # Handle multiple values
                    values = value.split()
                    for v in values:
                        if v.strip():
                            struct_children.append((key, extract_value(v)))
                i += 1

            if struct_children:
                struct_children.sort(key=lambda x: x[0])
                xml_lines.append(f"  <{struct_key}>")
                for key, value in struct_children:
                    xml_lines.append(f"    <{key}>{value}</{key}>")
                xml_lines.append(f"  </{struct_key}>")
        else:
            parts = line.split(None, 1)
            if len(parts) == 2:
                key, value = parts
                if key in EXCLUDED_PARAMETERS or is_placeholder_or_empty(value):
                    i += 1
                    continue

                values = value.split()
                for v in values:
                    if v.strip():
                        xml_lines.append(f"  <{key}>{extract_value(v)}</{key}>")
            else:
                xml_lines.append(f"  <line>{line}</line>")
            i += 1

    xml_lines.append("</root>")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines))

    print(f"✅ Loose XML saved to {output_path}")


# Example usage
loose_wrap_to_xml("source.txt", "loose_output.xml")
