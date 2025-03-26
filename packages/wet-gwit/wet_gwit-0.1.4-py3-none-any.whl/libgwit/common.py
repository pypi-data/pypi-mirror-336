"""
Et une femme qui portait un enfant dans les bras dit,
Parlez-nous des Enfants.
Et il dit : Vos enfants ne sont pas vos enfants.
Ils sont les fils et les filles de l’appel de la Vie à elle-même,
Ils viennent à travers vous mais non de vous.
Et bien qu’ils soient avec vous, ils ne vous appartiennent pas.

Vous pouvez leur donner votre amour mais non point vos pensées,
Car ils ont leurs propres pensées.
Vous pouvez accueillir leurs corps mais pas leurs âmes,
Car leurs âmes habitent la maison de demain, que vous ne pouvez visiter, 
pas même dans vos rêves.
Vous pouvez vous efforcer d’être comme eux, 
mais ne tentez pas de les faire comme vous.
Car la vie ne va pas en arrière, ni ne s’attarde avec hier.
Vous êtes les arcs par qui vos enfants, comme des flèches vivantes, sont projetés.
L’Archer voit le but sur le chemin de l’infini, et Il vous tend de Sa puissance 
pour que Ses flèches puissent voler vite et loin.
Que votre tension par la main de l’Archer soit pour la joie;
Car de même qu’Il aime la flèche qui vole, Il aime l’arc qui est stable. 

K.Gibran - le Prophète
"""
import re
import logging

ID_REGEX = re.compile('^0x[0-f]{40}$')
INI_INTRODUCTION_FILE_REGEX = re.compile('^0x[0-f]{40}.ini')
GWIT_BRANCH_REGEX = re.compile('^gwit-0x[0-f]{8}$')

def define_logger(log_level = 'ERROR'):
    if len(logging.getLogger().handlers) == 0:
        # Initialize the root logger only if it hasn't been done yet by a
        # parent module.
        logging.basicConfig(level=log_level, format=self.__LOG_FORMAT)
    logger = logging.getLogger(__name__)
    # logger.setLevel(log_level)
    return logger