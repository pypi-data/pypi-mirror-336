Features of Wet
===============

Here are the features I plan to implement :

## Configuration

- [ ] configuration file

## Subcommand `get`: display a resource

- [X] `wet get <url> -r <remote>`: display the resource pointed by the URL. Clones the site. Saves the sites introductions.
- [X] `wet get <url>#??<remote>`: display the resource pointed by the URL. Clones the site. Saves the sites introductions.
- [X] `wet get <url>`: display the resource pointed by the URL, if it is available in known sites.
  - [X] `wet get <url_to_dir>`: display the resource pointed by the URL. If it is a dir without an index page, list the dir content.
  - [X] `wet get gwit://self/<path>`: URL using 'self' keyword.
  - [X] `wet get gwit://<git_ref>@self/<path>`: got to a resource on a specific git ref, using 'self' keyword.
  - [X] `wet get gwit://<git_ref>@<site_id>`: got to a resource on a specific git ref.
  - [X] `wet get <relative_path>`: go to a resource with a link relative to the last resource successfuly fetched.
  - [X] `wet get <relative_path> -c <context>`: go to a resource with a link relative to the given context.
  - [X] If the resource is not a text file, try to open it with xdg-open.
  - [X] Manage context by console session.
- [X] `wet get -p <petname>`: if the petname is unique in known sites, go to its index. This feature does not accept paths.
- [x] `wet get <url> --rewrite <always|never|archive>`: indicates how to handle a rewrite
- [X] `wet get <url> --fresh <yes|no|unknown>`: indicates when we should try to pull from remotes
- [x] `wet get <url> --save-local`: don't display the document, only pull from remote. Implies `--fresh yes`
- [X] `wet get --import <directory_to_import>`
- [X] `wet get --import <directory_to_import> <searches...>`
- [X] `wet get --export <directory_to_import>`
- [X] `wet get --export <directory_to_import> <searches...>`

## Subcommand `list`: list and search sites

- [X] `wet list`: displays the known sites, both locally cloned and introductions
- [ ] `wet list --details <short|name|title|description>`: only displays the site IDs | plus the name | plus title | plus description
- [X] `wet list <search>`: filters the list with the search.
- [ ] `wet list --known-petnames`: displays the known sites, only locally cloned sites
- [ ] `wet list --introductions`: displays the known sites, only introductions
- [ ] `wet list --format <json|yaml|gmi|md|html>`: formats the output

## Subcommand `show`: show site information

- [X] `wet show <site|petname>`: shows information about the searched site, if the result is unique
- [X] `wet show <site|petname> --format <json|yaml|ini>`: formats the output. INI can be directly used as a site introduction.
- [ ] `wet show <site|petname> --format <gmi|md|html>`: formats the output.

## Subcommand `news`: show latest news (commits)

- [ ] `wet news`: shows latest commit message for each site. 
- [ ] `wet news <site|petname>`: show latest commits for the given site
- [ ] `wet news -n 10`: number of commits to show (default 4)
- [ ] `wet news --since <date>`: news since this date
- [ ] `wet news --fresh <yes|no>`: indicates if we should try to pull from remotes.

## Subcommande `remove`: remove a site / disable a remote

- [ ] `wet remove <site|petname>`: delete this locally cloned site. Also deletes its introductions.
- [ ] `wet remove <site|petname> <remote>`: mark this remote as disabled, to avoid pulling from it.

## Security

- [ ] protection against heavy repos / timeout of the pulls
- [ ] protection against large number of introductions
- [ ] setting files permissions to 440