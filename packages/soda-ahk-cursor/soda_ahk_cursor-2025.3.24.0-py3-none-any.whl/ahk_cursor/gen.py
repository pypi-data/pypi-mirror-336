from pathlib import Path

CURRENT = Path(__file__).resolve().parent
gen_dir = CURRENT.parent.joinpath("ahk_cursor_script")
script = gen_dir.joinpath("Cursor.ahk")


def gen():
    gen_dir.mkdir(exist_ok=True)

    content = CURRENT.joinpath("Cursor.template.ahk").read_text(encoding="utf8")
    content = content.replace("{resources}", str(CURRENT))

    script.write_text(content, encoding="utf8")
