import os
import time
import typer
import shutil
import requests
import markdown

from pathlib import Path
from timeit import timeit
from css_html_js_minify import html_minify

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


treeHtml = ""

SRCDIR = "./docsrc"
OUTDIR = "./docs"

template = requests.get("https://raw.githubusercontent.com/PaddeCraft/PaddeCraft.github.io/master/misc/doctemplate.html").text
docRepoName = ""

if not os.path.isdir(SRCDIR):
    print("ERROR: The source folder does not exist.")
    exit(1)

if os.path.isdir(OUTDIR):
    shutil.rmtree(OUTDIR)
os.makedirs(OUTDIR)


def generateMarkdown(md):
    return markdown.markdown(md,  extensions=['fenced_code', 'codehilite'])


def normalizePath(p):
    return p.replace(SRCDIR, "").replace(" ", "-").lower()


def getName(p):
    pth = p
    if not os.path.isfile(p):
        pth = os.path.join(p, "index.md")
    with open(pth, encoding="UTF-8") as f:
        for l in f.read().split("\n"):
            if l.split(" ")[0] == "#":
                return l[2:]
        print("No title (# Title) found in file " + pth)
        exit(1)


def getFileContent(p):
    pth = p
    if not os.path.isfile(p):
        pth = os.path.join(p, "index.md")
    with open(pth, encoding="UTF-8") as f:
        return f.read()


def index(dir):
    dirs = []
    for p in os.listdir(dir):
        pth = os.path.join(dir, p)
        if os.path.isdir(pth):
            dirs.append({"name": getName(os.path.join(pth, "index.md")),
                        "path": normalizePath(pth), "content": getFileContent(pth), "childs": index(pth)})
        elif os.path.basename(pth) == "index.md":
            if os.path.samefile(SRCDIR, dir):
                dirs.append({"name": getName(pth),
                            "path": normalizePath(pth[:-3]), "content": getFileContent(pth)})
            else:
                continue
        else:
            dirs.append({"name": getName(pth),
                        "path": normalizePath(pth[:-3]), "content": getFileContent(pth)})
    return dirs


def generateTreeUI(elem, withEnding=True):
    html = ""
    if "childs" in elem:
        parent = dict(elem)
        del parent["childs"]
        html += generateTreeUI(parent, False)
        html += "<ul>"
        for e in elem["childs"]:
            html += generateTreeUI(e)
        html += "</ul>"
        return html
    else:
        return "<li><a href='/" + docRepoName + "/docs" + elem["path"] + (".html" if withEnding else "") + "'><span>" + elem["name"] + "</span></a></li>"


def convert(elem):
    if "childs" in elem:
        # Modify parent and convert it
        parent = dict(elem)
        parent["path"] = os.path.join(parent["path"], "index")
        del parent["childs"]
        convert(parent)

        # Convert childs
        for e in elem["childs"]:
            convert(e)
    else:
        print("Generating ", elem["path"][1:] + "...")
        html = str(template)
        html = html.replace("##LIST##", treeHtml)
        html = html.replace("##CONTENT##", generateMarkdown(elem["content"]))
        pth = os.path.join(OUTDIR, elem["path"][1:] + ".html")
        Path(os.path.split(pth)[0]).mkdir(parents=True, exist_ok=True)
        with open(pth, encoding="UTF-8", mode="w+") as f:
            f.write(html)


# Main code
def build():
    global treeHtml
    print("Indexing...")
    fileTree = index(SRCDIR)
    print("Done.\nGenerating table of contents...")
    treeHtml = "<ul>"
    for e in fileTree:
        treeHtml += generateTreeUI(e)
    treeHtml += "</ul>"
    print("Done.\n\nGenerating pages...")
    for e in fileTree:
        convert(e)
    print("Done.")


def main(daemon: bool = False, reponame: str = ""):
    def buildProcess():
        print("\nRendered documentation in " +
              str(round(timeit(build, number=1) * 1000, 4)) + "ms.")

    def onNeedToUpdate(event):
        print(
            f"\n\nChange detected, regenerating docs...\n")
        buildProcess()
    # Set variable
    global docRepoName
    docRepoName = reponame
    # Run once with or without daemon, to initialize
    buildProcess()
    # Start daemon if wanted
    if daemon:
        eventHandler = PatternMatchingEventHandler(
            ["*.md"], None, False, False)
        eventHandler.on_any_event = onNeedToUpdate
        observer = Observer()
        observer.schedule(eventHandler, SRCDIR, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nDetected KeyboardInterrupt, exitting...")
            observer.stop()
            observer.join()


if __name__ == "__main__":
    typer.run(main)
