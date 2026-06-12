import sys
from cli.packages import tag_ops
from cli.packages import normalize_ops, score_pr
from cli.packages.config import load_config
from cli.packages import doctor_ops, field_ops, help


def preflight():
    config = load_config()

    # --- Doctor ---
    if config["doctor"]["auto_run"]:
        problems = doctor_ops.run()

        if problems and config["doctor"]["fail_on_error"]:
            print("Aborting due to validation errors.")
            exit(1)

    # --- Normalize ---
    if config["normalize"]["auto_run"]:
        normalize_ops.normalize_all()


def main():
    # preflight()

    args = sys.argv[1:]

    if not args or args[0] in ["help", "--help", "-h"]:
        help.show_help()
        return
    

    if args[0] == "tag":
        if args[1] == "mv":
            tag_ops.rename_tag(args[2], args[3])
        elif args[1] == "rm":
            tag_ops.remove_tag(args[2])

    elif args[0] == "field":
        if args[1] == "mv":
            field_ops.rename_field(args[2], args[3])
        elif args[1] == "add":
            name = args[2]
            default = args[3] if len(args) > 3 else ""
            field_ops.add_field(name, default)
        elif args[1] == "update":
            field_ops.update_field(args[2], args[3], args[4])

    elif args[0] == "packages":
        if args[1] == "score_pr":
            reset = "--reset" in args
            score_pr.run(reset=reset)

        elif args[1] == "score_2":
            print("score_2 not implemented")

        elif args[1] == "score_3":
            print("score_3 not implemented")

        else:
            print('Unknow score method')

    elif args[0] == "normalize":
        normalize_ops.normalize_all()

    else:
        print("Unknown command")
    
if __name__ == "__main__":
    main()
