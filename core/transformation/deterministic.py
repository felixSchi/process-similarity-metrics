import xml.etree.ElementTree as ET
import argparse
import sys
import os


# helper: namespace-agnostic local name
def _local_name(tag):
    return tag.split('}')[-1] if '}' in tag else tag


# find first descendant <label> and return its text
def _find_label(node):
    for desc in node.iter():
        if _local_name(desc.tag) == 'label' and desc.text:
            return desc.text.strip()
    return ""


# XML-Baum rekursiv analysieren und den Prozess als Text zusammenbauen
def parse_node(node, depth=0):
    text = ""
    indent = " " * depth  # Einrückung basierend auf der Tiefe des Knotens
    tag = _local_name(node.tag)

    # Einfacher Task
    if tag == "call":
        label = _find_label(node)
        text += f"{indent}Then, the task {label} is executed.\n"

    # Parallele Tasks
    elif tag == "parallel":
        text += f"{indent}Then, the following tasks are executed in parallel"
        parallel_branches = [child for child in node if _local_name(child.tag) == "parallel_branch"]
        for child in parallel_branches:
            # find call inside branch
            for c in child:
                if _local_name(c.tag) == 'call':
                    label = _find_label(c)
                    text += f", {indent}{label}"
        text += f"{indent}.\nAfter all parallel tasks are completed, the process continues.\n"

    # XOR / exclusive gateways
    elif tag in ("choose"):
        if tag == 'choose':
            text += f"{indent}Then, a decision takes place.\n"
            alternatives = [child for child in node if _local_name(child.tag) == 'alternative']
            for alt in alternatives:
                    condition = alt.attrib.get('condition', '').strip()

                    # gather call labels in order
                    labels = []
                    for c in alt:
                        if _local_name(c.tag) == 'call':
                            labels.append(_find_label(c))

                    if len(labels) == 0:
                        text += f"{indent}If {condition}, nothing happens.\n"
                    elif len(labels) == 1:
                        text += f"{indent}If {condition}, {labels[0]} is executed.\n"
                    else:
                        text += f"{indent}If {condition}, the following steps are executed:\n"
                        for i, lab in enumerate(labels):
                            if i == 0:
                                text += f"{indent}First, {lab}.\n"
                            elif i == len(labels) - 1:
                                text += f"{indent}Lastly, {lab}.\n"
                            else:
                                text += f"{indent}Then, {lab}.\n"

            text += f"{indent}After the exclusive task is completed, the process continues.\n"

    # For container/other nodes, recurse
    else:
        for child in node:
            text += parse_node(child, depth)

    return text


def convert_model_to_text(fpath):
    if not os.path.isfile(fpath):
        raise FileNotFoundError(f"Model file not found: {fpath}")

    tree = ET.parse(fpath)
    root = tree.getroot()

    # find inner description element that contains the runnable children
    workflow_root = None
    for elem in root.iter():
        if _local_name(elem.tag) == 'description' and len(list(elem)) > 0:
            first_child = list(elem)[0]
            if _local_name(first_child.tag) in ['call', 'parallel', 'choose']:
                workflow_root = elem
                break

    if workflow_root is None:
        raise ValueError(f"No valid workflow description found in: {fpath}")

    parts = []
    parts.append(f"--- {os.path.basename(fpath)} ---")
    parts.append("The process starts.")
    parts.append(parse_node(workflow_root))
    parts.append("After that, the process ends.")

    return "\n".join(parts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministischer M2T Generator (Visitor-Based)")
    parser.add_argument("-m", "--model", help="Path to a BPMN XML file. If omitted, all files in data/bpmn/ will be processed.")
    args = parser.parse_args()

    files = []
    if args.model:
        files = [args.model]
    else:
        # default: process all xml files in workspace data/bpmn
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'bpmn'))
        if not os.path.isdir(base):
            print(f"Konnte data/bpmn Verzeichnis nicht finden: {base}")
            sys.exit(1)
        for fn in os.listdir(base):
            if fn.lower().endswith('.xml'):
                files.append(os.path.join(base, fn))

    for fpath in files:
        try:
            out = convert_model_to_text(fpath)
            print(out)
        except Exception as e:
            print(f"Fehler beim Verarbeiten '{fpath}': {e}")
            continue
