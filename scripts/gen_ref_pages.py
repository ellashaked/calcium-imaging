from pathlib import Path
import shutil
import mkdocs_gen_files

root = Path(__file__).parent.parent
src = root / "src"

# Copy README.md to docs/index.md
# readme_src = root / "README.md"
# readme_dest = Path("index.md")
# shutil.copyfile(readme_src, Path(mkdocs_gen_files.config["docs_dir"]) / readme_dest)

nav = mkdocs_gen_files.Nav()

nav[("Home",)] = "index.md"

for path in sorted(src.rglob("*.py")):
    mod = path.relative_to(src).with_suffix("")
    parts = tuple(mod.parts)
    if parts[-1] in ("__init__", "__main__"):
        continue
    
    dest = Path("api_reference", *parts).with_suffix(".md")

    nav[parts] = dest.as_posix()
    with mkdocs_gen_files.open(dest, "w") as fd:
        fd.write(f"::: {' '.join(parts).replace(' ', '.')}")
    mkdocs_gen_files.set_edit_path(dest, path.relative_to(root))

with mkdocs_gen_files.open("SUMMARY.md", "w") as fd:
    fd.writelines(nav.build_literate_nav())