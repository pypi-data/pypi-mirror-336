How to use wet ?
================

First use
---------

You must begin by visiting a site, using `get <url> -r <remote>` or `get <url>#??<remote>`.
Let's do it with the Oldest gwit site:

```bash
$ ./wet.py get gwit://0x408198c2c363076c6b1eabe797ea3168a78cd65a -r https://git.sr.ht/~ivilata/oldest-gwit-site
```

You will see the index of the site. If you kept the default behavior, everything is set in `~/.local/share/gwit`. It will have created here:
- petnames.yaml, the storage for each site information.
- context.txt, the last Gwit URL visited.
- sites/0x408198c2c363076c6b1eabe797ea3168a78cd65a, the repo for Oldest Gwit Site.

Manage petnames
-------------

Now that we loaded the petnames from a site, we can list them:
```bash
$ ./wet.py list

Locals :
--------
- Oldest gwit Site =>  0x408198c2c363076c6b1eabe797ea3168a78cd65a

Introductions :
---------------
> Oldest gwit Site - 0x408198c2c363076c6b1eabe797ea3168a78cd65a
  - Matograine => 0x16c8a566bb88303c2513cf6328996d46e0440e85
  - Ploum non officiel (Gemini) => 0x24860d48d3abbb5ceffbc5126483fd2f7b9eaddf
  - Ploum non officiel (Web) => 0xb1f5a34aac62bfda746a3188aab4500edeaf682a
```

Hmm, what has 'Matograine' to say ? Let's see ! Note the search is case-insensitive:

```bash
$ ./wet.py show matograine

Matograine - 0x16c8a566bb88303c2513cf6328996d46e0440e85
-------------------------------------------------------
- desc:   Matograine's site with a log, gwit tutorials, lyrics and recipes.
- root:   /
- remotes:
  - https://framagit.org/matograine/gwitsite.git
```

But if I want to see one of Ploum's introductions, I have to be precise:

```bash
$ ./wet.py show ploum

Error: There are many introductions for same search ploum. Please use site IDs.
```

I can use the full petname :

```bash
$ ./wet.py show "Ploum non officiel (Gemini)"

Ploum non officiel (Gemini) - 0x24860d48d3abbb5ceffbc5126483fd2f7b9eaddf
------------------------------------------------------------------------
- root:   /
- remotes:
  - https://git.sr.ht/~ivilata/ploum-gwit-unoff
```

Or the site ID:

```bash
> $ ./wet.py show 0xb1f5a34aac62bfda746a3188aab4500edeaf682a
Ploum non officiel (Web) - 0xb1f5a34aac62bfda746a3188aab4500edeaf682a
---------------------------------------------------------------------
- root:   /
- remotes:
  - https://git.sr.ht/~ivilata/ploum-gwit-unoff

```

Browsing other sites
--------------------

Now that the site Matograine has been introduced, I can browse to it without entering a remote.
I can load the site by its petname:

```bash
$ ./wet.py get -p matograine
```

Or directly through its URL:

```bash
$ ./wet.py get gwit://0x16c8a566bb88303c2513cf6328996d46e0440e85
```

I can directly go to a specific resource, at a specific git ref, even if it is the first time I visit a site. 

```bash
# Here we load Ploum's Gemtext website, sadly the repo is ~200Mo heavy, I am positive we could divide it by 10. Please be patient while the repo is cloned.
./wet.py get gwit://0x24860d48d3abbb5ceffbc5126483fd2f7b9eaddf/118-vocabulaire-romantisme-d-ascenceur/ 
```

I can now browse using relative paths, because the last visited URL is already :
```bash
./wet.py get ../../121-la-proclamation/
```

Or go to the root of the site, at the latest commit :
```bash
./wet.py get gwit://self
```

I can also use links relatively to another context, here visiting the blog of Matograine:
```bash
./wet.py get blog -c gwit://0x16c8a566bb88303c2513cf6328996d46e0440e85
```

Browsing the history
--------------------

While wet does not provide a log of the history for a site, we can navigate to refs:
```bash
./wet.py get gwit://f74db9476@0x16c8a566bb88303c2513cf6328996d46e0440e85/blog
```