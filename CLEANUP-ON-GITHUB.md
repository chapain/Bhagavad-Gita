# Deleting the old files on GitHub

The last update **removed 7 files**. Uploading the new files does not delete
them — GitHub's *Add file → Upload files* only adds and overwrites. Anything you
uploaded before that is no longer in the zip stays in the repo forever until you
delete it by hand.

Delete these 7, one at a time:

    source/gita_conv.py
    source/pada_overrides.py
    source/freeze_padas.py
    source/sandhi.py
    source/bg.itx
    source/gita_shankarabhashya.itx
    source/shankara_verses.json

## How to delete one file

1. Open the file on GitHub (click into `source/`, then the filename).
2. Click the **⋯** button at the top right of the file view.
3. Choose **Delete file**.
4. Scroll down, click **Commit changes**.

Repeat for each. It takes about two minutes.

## Does it matter if I forget?

**Your app is not affected.** These are build-time Python files; the published
site is only `index.html`. A stale `.py` file sitting in the repo cannot change
what your friends see — this was verified by putting all four back and
rebuilding, which produced a byte-identical `index.html`.

What it *does* affect is you, later:

* `python3 build.py` will fail with `gita_conv.py is deleted — nothing generates
  content`, because the test suite deliberately checks these files are gone.
* You would have two files that look like they matter but are dead code, which
  is exactly the confusion the cleanup removed.

So it is worth doing, but nothing is broken while you have not.

## Checking you got them all

After deleting, your `source/` folder on GitHub should contain **84 files**, and
none of the seven names above. The whole repo should be **108 files**.

## The alternative: delete the folder first

If you would rather not hunt for individual files, delete the whole `source/`
folder on GitHub, commit, then upload the fresh `source/` from the zip. Do not
delete `index.html` this way — leave the site file in place so it is never
briefly missing.
