Libgwit
=======

Libgwit is a set of tools to build a [gwit](https://git.sr.ht/~ivilata/gwit-spec) client.

It is in early stages of development.

Vision
======

libgwit is for now only used as a submodule in [wet](https://framagit.org/matograine/wet).

In order to make a robust library, I intend to add :

- [ ] using `uv` to ease development for other developpers
- [ ] unit testing
- [ ] `make` scripts to ease the publication on Pipy (I am not familiar with setting up CI/CD)
- [ ] some missing features (adding features is always more fun than testing)
  
Install
=======

For now, the directory containing libgwit should be installed as a submodule of your project.

```bash
pip install -r requirements.txt
```