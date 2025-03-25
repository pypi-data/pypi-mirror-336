# Notes

## Objects

new Petnames(conf_file)

Petnames
.all -> all loaded petnames
.local -> local petnames
.all_remotes -> remotes petnames (array)
.remotes_by_local

.search -> search string
.results -> search result
.results.all
.results.local
.results.all_remotes -> remotes petnames (array)
.results.remotes_by_local

.search()

Repository

.fetch(git_remote)
.verify()
.go(path)

## Tests

Commands to test :

```
./wet.py get gwit://0x408198c2c363076c6b1eabe797ea3168a78cd65a -r https://git.sr.ht/~ivilata/oldest-gwit-site
./wet.py news gwit://0x408198c2c363076c6b1eabe797ea3168a78cd65a 
```