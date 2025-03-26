"""
Une nuit, je fis un rêve :
Je marchais sur la plage avec mon Seigneur,
Sur le ciel noir, des épisodes de ma vie furent projetés,
Comme sur un immense écran.
Et sur le sable je voyais à chaque fois, deux traces de pas :
Les miens et ceux de mon Seigneur.

Après la dernière scène de ma vie, je me retournai.
Je fus surpris de voir par endroits
Les traces d'une seule personne.
Je me rendis compte
Que je traversais alors les moments les plus difficiles de ma vie.

Inquiète, je demandai au Seigneur :
"Le jour où j'ai décidé de te suivre
Tu m'as dit que tu marcherais toujours avec moi.
Mais je découvre maintenant
Qu'aux pires moments de ma vie
Il n'y a les empreintes que d'une seule personne.
Pourquoi m'as tu abandonnée
Lorsque j'avais le plus besoin de toi ?"

Il me répondit :
"Mon enfant chérie, je t'aime
Et je ne t'abandonnerai jamais, jamais, jamais.
Surtout pas lorsque tu passes par l'épreuve.
Les jours où  il n'y a qu'une seule empreinte dans le sable
Sont exactement ceux où je t'ai porté dans mes bras"

Margaret Fishback Powers

J'ai découvert cette histoire dans le film C.R.A.Z.Y.
"""

import configparser
import sys

# copied from https://stackoverflow.com/questions/13921323/handling-duplicate-keys-with-configparser

class GwitIniParser(configparser.RawConfigParser):
  """ConfigParser allowing duplicate keys. Values are stored in a list"""

  def __init__(self):
    configparser.RawConfigParser.__init__(self, empty_lines_in_values=False, strict=False)

  def _read(self, fp, fpname):
    """Parse a sectioned configuration file.

    Each section in a configuration file contains a header, indicated by
    a name in square brackets (`[]'), plus key/value options, indicated by
    `name' and `value' delimited with a specific substring (`=' or `:' by
    default).

    Values can span multiple lines, as long as they are indented deeper
    than the first line of the value. Depending on the parser's mode, blank
    lines may be treated as parts of multiline values or ignored.

    Configuration files may include comments, prefixed by specific
    characters (`#' and `;' by default). Comments may appear on their own
    in an otherwise empty line or may be entered in lines holding values or
    section names.
    """
    elements_added = set()
    cursect = None                        # None, or a dictionary
    sectname = None
    optname = None
    lineno = 0
    indent_level = 0
    e = None                              # None, or an exception
    for lineno, line in enumerate(fp, start=1):
      comment_start = None
      # strip inline comments
      for prefix in self._inline_comment_prefixes:
        index = line.find(prefix)
        if index == 0 or (index > 0 and line[index-1].isspace()):
          comment_start = index
          break
      # strip full line comments
      for prefix in self._comment_prefixes:
        if line.strip().startswith(prefix):
          comment_start = 0
          break
      value = line[:comment_start].strip()
      if not value:
        if self._empty_lines_in_values:
          # add empty line to the value, but only if there was no
          # comment on the line
          if (comment_start is None and
              cursect is not None and
              optname and
              cursect[optname] is not None):
              cursect[optname].append('') # newlines added at join
        else:
          # empty line marks end of value
          indent_level = sys.maxsize
        continue
      # continuation line?
      first_nonspace = self.NONSPACECRE.search(line)
      cur_indent_level = first_nonspace.start() if first_nonspace else 0
      if (cursect is not None and optname and
          cur_indent_level > indent_level):
          cursect[optname].append(value)
      # a section header or option header?
      else:
        indent_level = cur_indent_level
        # is it a section header?
        mo = self.SECTCRE.match(value)
        if mo:
          sectname = mo.group('header')
          if sectname in self._sections:
            if self._strict and sectname in elements_added:
              raise DuplicateSectionError(sectname, fpname,
                                          lineno)
            cursect = self._sections[sectname]
            elements_added.add(sectname)
          elif sectname == self.default_section:
            cursect = self._defaults
          else:
            cursect = self._dict()
            self._sections[sectname] = cursect
            self._proxies[sectname] = configparser.SectionProxy(self, sectname)
            elements_added.add(sectname)
          # So sections can't start with a continuation line
          optname = None
        # no section header in the file?
        elif cursect is None:
          raise MissingSectionHeaderError(fpname, lineno, line)
        # an option line?
        else:
          mo = self._optcre.match(value)
          if mo:
            optname, vi, optval = mo.group('option', 'vi', 'value')
            if not optname:
              e = self._handle_error(e, fpname, lineno, line)
            optname = self.optionxform(optname.rstrip())
            if (self._strict and
              (sectname, optname) in elements_added):
              raise configparser.DuplicateOptionError(sectname, optname, fpname, lineno)
            elements_added.add((sectname, optname))
            # This check is fine because the OPTCRE cannot
            # match if it would set optval to None
            if optval is not None:
              optval = optval.strip()
              # Check if this optname already exists
              if (optname in cursect) and (cursect[optname] is not None):
                # If it does, convert it to a tuple if it isn't already one
                if not isinstance(cursect[optname], tuple):
                  cursect[optname] = tuple(cursect[optname])
                cursect[optname] = cursect[optname] + tuple([optval])
              else:
                cursect[optname] = [optval]
            else:
                # valueless option handling
                cursect[optname] = None
          else:
            # a non-fatal parsing error occurred. set up the
            # exception but keep going. the exception will be
            # raised at the end of the file and will contain a
            # list of all bogus lines
            e = self._handle_error(e, fpname, lineno, line)
    # if any parsing errors occurred, raise an exception
    if e:
        raise e
    self._join_multiline_values()