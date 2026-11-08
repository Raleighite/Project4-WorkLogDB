# Source Floorplan

Open [the offline map](index.html) after downloading it. GitHub may show HTML source rather than execute it. Use **Start here**, **Flows**, search and the details-panel toggle to read the architecture. On narrow screens the fit-to-view overview can be small; readable details/tour prose is the preferred path.

An unfinished Peewee-backed terminal work log defines entry creation, filtering, result paging and deletion. Database binding is incomplete; no HTTP routes.

## Source boundary

Execution is not qualified: Entry remains bound to None, editing is a stub, and title/notes matches can duplicate results. tests.py is development-only and omitted from the mapping input because mock.patch decorators are falsely interpreted as HTTP PATCH routes by the generic scanner; no application code was omitted.

Pinned original source: `0f4f14fd4acaa252ed4ca6a5e87a64ca2bafcd25`. Original project licensing is unchanged. See [notices](NOTICE.md), [omissions](source-census.json), [authoring](architecture.json) and [integrity pins](source-manifest.json). This is source documentation, not application execution, secure deployment approval or automatic refresh.

## Check without running the application

```sh
python3 docs/floorplan/check_freshness.py
python3 -B -m unittest discover -s docs/floorplan/tests -v
python3 -B -O -m unittest discover -s docs/floorplan/tests -v
```

The checker compares original source/config/static/input-file hashes and file membership, and all reviewed map artifacts. It does not regenerate on drift. Tests create disposable copies, never import the application, and require only Python standard library and Git. Regeneration requires a separately qualified renderer and reviewed authoring; its runtime is not bundled here.
