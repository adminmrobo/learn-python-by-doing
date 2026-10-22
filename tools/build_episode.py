"""편 원고(tools/epN_content.py)를 실제로 실행해서 docs/epN/*.md, 그림, 노트북을 만든다.
usage: python tools/build_episode.py 1

원고 문장 안의 ⟦식⟧ 또는 ⟦식|형식⟧ 은 실행이 끝난 이름(ns)으로 계산해 채운다.
예) ⟦len(sales)|,⟧ → 14,237   ⟦pl['profit'].max()/1e4|.0f⟧ → 193
"""
import contextlib, importlib.util, io, json, os, re, shutil, sys, tempfile, warnings, zipfile
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAT = re.compile(r"⟦(.+?)⟧")

def fill(text, ns):
    def one(m):
        expr, _, fmt = m.group(1).partition("|")
        v = eval(expr, ns)
        return format(v, fmt) if fmt else str(v)
    return PAT.sub(one, text) if text else text

def render(x, ns):
    """절 원고 안의 모든 문자열(코드 제외)을 지금 상태로 채운다."""
    if isinstance(x, str): return fill(x, ns)
    if isinstance(x, (list, tuple)): return type(x)(render(v, ns) for v in x)
    if isinstance(x, dict): return {k: (v if k in ("code", "run", "prefix") else render(v, ns)) for k, v in x.items()}
    return x

def say(who, text, state=None):
    st = f' data-state="{state}"' if state else ""
    return f'<div class="say" data-who="{who}"{st}>{text}</div>'

def main(n):
    spec = importlib.util.spec_from_file_location("content", os.path.join(ROOT, "tools", f"ep{n}_content.py"))
    C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
    out_dir = os.path.join(ROOT, "docs", f"ep{n}"); img_dir = os.path.join(out_dir, "img")
    shutil.rmtree(out_dir, ignore_errors=True); os.makedirs(img_dir)
    work = tempfile.mkdtemp(); cwd = os.getcwd(); os.chdir(work)
    zipfile.ZipFile(os.path.join(ROOT, "docs", "data", C.ZIP)).extractall()
    ns = {"__name__": "__main__"}
    plt.rcParams.update(matplotlib.rcParamsDefault)
    results = []   # (section, [(code, output, [imgs])])
    for sec in C.SECTIONS:
        cells = []
        for k, cell in enumerate(sec["cells"]):
            code = cell["code"].strip("\n")
            run = cell.get("run", code)          # Colab 전용 셀은 로컬에서 대신 돌릴 코드
            imgs = []
            def show(*a, **kw):
                for num in plt.get_fignums():
                    name = f"{sec['slug']}-{k}{'' if not imgs else '-' + str(len(imgs))}.png"
                    plt.figure(num).savefig(os.path.join(img_dir, name), dpi=80, bbox_inches="tight", facecolor="white")
                    imgs.append("img/" + name)
                plt.close("all")
            plt.show = show
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), warnings.catch_warnings():
                warnings.simplefilter("ignore")
                exec(compile(run, f"{sec['id']}#{k}", "exec"), ns)
            if plt.get_fignums(): show()
            outp = cell.get("prefix", "") + buf.getvalue().rstrip("\n")
            cells.append((code, outp, imgs))
        results.append((render(sec, ns), cells))   # 문장은 이 절까지 실행한 상태로 채운다
    os.chdir(cwd)

    # ---------- 편 개요 ----------
    rows = "\n".join(f"| [{s['id']} {s['title']}]({s['slug']}.md) | {s['short']} |" for s in C.SECTIONS)
    head = "\n".join(say(*t) for t in C.HEAD_TALK)
    open(os.path.join(out_dir, "index.md"), "w").write(fill(f"""# {C.TITLE}

{C.INTRO}

{head}

| 절 | 할 일 |
|---|---|
{rows}

<a class="colab" data-nb="ep{n}.ipynb">▶ {n}편 노트북을 Colab 에서 열기</a>

!!! tip "준비물"
    [{C.ZIP}](../data/{C.ZIP}) 하나. 0-3 처럼 압축을 풀지 않고 그대로 올린다.

| 파일 | 내용 |
|---|---|
{C.FILES}
""", ns))

    # ---------- 절 페이지 ----------
    for i, (sec, cells) in enumerate(results):
        md = [f"# {sec['id']} {sec['title']}", "", '!!! abstract "이 절에서 할 일"', "    " + fill(sec["goal"], ns), ""]
        if sec.get("intro"): md += [fill(sec["intro"], ns), ""]
        for k, (code, outp, imgs) in enumerate(cells):
            cell = sec["cells"][k]
            if cell.get("before"): md += [fill(cell["before"], ns), ""]
            md += ["```python", code, "```", ""]
            if outp: md += ['```text title="실행 결과"', outp, "```", ""]
            for im in imgs: md += [f"![{cell.get('alt', sec['title'])}]({im})", ""]
            if cell.get("after"): md += [fill(cell["after"], ns), ""]
        for t in sec.get("talk", []):
            md.append(say(t[0], fill(t[1], ns), fill(t[2], ns) if len(t) > 2 else None))
        if sec.get("talk"): md.append("")
        if sec.get("read"): md += ['!!! info "읽는 법"', "    " + fill(sec["read"], ns), ""]
        if sec.get("warn"): md += [f'!!! warning "{sec["warn"][0]}"', "    " + fill(sec["warn"][1], ns), ""]
        if sec.get("try"): md += ['!!! tip "바꿔 보기"', "    " + fill(sec["try"], ns), ""]
        md += [f'<label class="done"><input type="checkbox" data-step="{sec["id"]}"> {sec["id"]} 끝냈어요</label>', ""]
        if i == len(results) - 1:
            md += ['<div class="outro" markdown>', f"{n}편 정리", ""]
            md += [say(t[0], fill(t[1], ns), t[2] if len(t) > 2 else None) for t in C.OUTRO]
            md += ["", C.NEXT, "</div>", ""]
        open(os.path.join(out_dir, sec["slug"] + ".md"), "w").write("\n".join(md))

    # ---------- 노트북 ----------
    def mdc(t): return {"cell_type": "markdown", "metadata": {}, "source": t}
    def cc(t): return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": t}
    nb = [mdc(f"# {C.TITLE}\n**쉽게 따라 해 보면서 배우는 파이썬**\n\n위에서부터 한 셀씩 `Shift + Enter`. 설명은 사이트의 {n}편 페이지에 있다.")]
    for sec, cells in results:
        nb.append(mdc(f"## {sec['id']} {sec['title']}"))
        nb += [cc(code) for code, _, _ in cells]
    os.makedirs(os.path.join(ROOT, "docs", "notebooks"), exist_ok=True)
    json.dump({"cells": nb, "metadata": {"colab": {"provenance": []}, "kernelspec": {"name": "python3", "display_name": "Python 3"},
               "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 0},
              open(os.path.join(ROOT, "docs", "notebooks", f"ep{n}.ipynb"), "w"), ensure_ascii=False, indent=1)

    # ---------- mkdocs.yml 목차 ----------
    y = open(os.path.join(ROOT, "mkdocs.yml")).read()
    nav = f"  - {C.TITLE}:\n      - ep{n}/index.md\n" + "".join(f"      - '{s['id']} {s['title']}': ep{n}/{s['slug']}.md\n" for s in C.SECTIONS)
    y = re.sub(rf"  - {n}편 [^\n]*\n(      - [^\n]*\n)*", nav, y, count=1)
    open(os.path.join(ROOT, "mkdocs.yml"), "w").write(y)
    print(f"ep{n}: {len(results)} sections, {sum(len(c[2]) for _, cs in results for c in cs)} images")

if __name__ == "__main__":
    main(int(sys.argv[1]))
