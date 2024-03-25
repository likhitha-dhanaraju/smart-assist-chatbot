
# https://colab.research.google.com/drive/1aFk8-7nq3oAp402jjLGLpEb2Nzq210Eo

import jamspell

corrector = jamspell.TSpellCorrector()
corrector.LoadLangModel('en.bin')

corrector.FixFragment('I am the begt spell cherken!')
# u'I am the best spell checker!'

corrector.GetCandidates(['i', 'am', 'the', 'begt', 'spell', 'cherken'], 3)
# (u'best', u'beat', u'belt', u'bet', u'bent', ... )

corrector.GetCandidates(['i', 'am', 'the', 'begt', 'spell', 'cherken'], 5)
# (u'checker', u'chicken', u'checked', u'wherein', u'coherent', ...)