import re

exclude_params = ["reservedBy"]


def extract_clean_fdn_blocks(text):
    text = text.replace("\r\n", "\n")  # Normalize line endings

    # Match blocks: FDN line ending with EUtranCellFDD=" and lines below it, until empty line
    pattern = re.compile(
        r'(FDN\s*:\s*".*?ENodeBFunction=1,EUtranCellFDD=[^",]+?"\n(?:[^\n]*\n)*?)\n',
        re.MULTILINE,
    )

    blocks = pattern.findall(text)

    filtered_blocks = []
    for block in blocks:
        fdn_line = block.splitlines()[0]

        # Convert line to lowercase for case-insensitive matching
        fdn_lower = fdn_line.lower()

        # Only keep the block if none of the excluded parameters appear as ",param=" in FDN line
        if not any(f",{param.lower()}=" in fdn_lower for param in exclude_params):
            filtered_blocks.append(block)

    return filtered_blocks


# Example usage
with open("cmedit_export_2.txt", "r", encoding="utf-8") as f:
    content = f.read()

matches = extract_clean_fdn_blocks(content)

for i, block in enumerate(matches, 1):
    print(block)
