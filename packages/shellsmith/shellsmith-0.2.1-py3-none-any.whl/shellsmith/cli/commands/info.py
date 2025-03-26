import shellsmith
from shellsmith import services


def info():
    print("ℹ️ Showing all shells")
    print_shells_tree()
    print_unreferenced_submodels()
    print_dangling_submodel_refs()


def print_unreferenced_submodels():
    submodel_ids = services.find_unreferenced_submodels()

    if submodel_ids:
        print()
        print("⚠️ Unreferenced Submodels:")
        for submodel_id in submodel_ids:
            submodel = shellsmith.get_submodel(submodel_id)
            id_short = submodel.get("idShort", "<no idShort>")
            print(f"- {id_short} ({submodel_id})")


def print_shells_tree():
    shells = shellsmith.get_shells()
    for shell in shells:
        shell_id = shell['id']
        shell_id_short = shell.get('idShort', "<no idShort>")
        print(f"{shell_id_short}: {shell_id}")

        submodels = services.get_shell_submodels(shell_id)

        for i, submodel in enumerate(submodels):
            is_last = i == len(submodels) - 1
            prefix = "└──" if is_last else "├──"
            submodel_id = submodel['id']
            submodel_id_short = submodel.get('idShort', "<no idShort>")
            print(f"{prefix} {submodel_id}: {submodel_id_short}")


def print_dangling_submodel_refs():
    dangling = services.find_dangling_submodel_refs()

    if dangling:
        print()
        print("⚠️ Dangling Submodel References:")
        for shell_id, submodel_ids in dangling.items():
            shell = shellsmith.get_shell(shell_id)
            shell_id_short = shell.get('idShort', "<no idShort>")
            print(f"- {shell_id_short}: {shell_id}")
            for submodel_id in submodel_ids:
                print(f"  └── {submodel_id}")
