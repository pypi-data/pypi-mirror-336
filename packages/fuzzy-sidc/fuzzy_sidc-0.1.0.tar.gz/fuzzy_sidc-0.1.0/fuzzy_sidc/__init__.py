import json
import pathlib
import rapidfuzz
import importlib.resources
from py_mini_racer import MiniRacer


class SIDCFuzzySearcher:
    def __init__(self, path_to_set_a: pathlib.Path, path_to_set_b: pathlib.Path, path_to_milsymbolsjs: pathlib.Path):
        self.score_cutoff = 70  # threshold for rapidfuzz
        # you may change it for your needs
        #    version 1.0, reality, unknown, unknown, present, unknown, unknown
        self.defaults_set_a = {'1': '1', '2': '0', '3': '0', '4': '1', '56': '00', '7': '0', '8': '0', '910': '00'}
        self._data_a = self._load_json(path_to_set_a)
        self._data_b = self._load_json(path_to_set_b)
        self._ctx = self._load_js(path_to_milsymbolsjs)

    def _load_json(self, path: pathlib.Path) -> dict:
        with open(path, 'r') as fp:
            return json.load(fp)

    def _load_js(self, path: pathlib.Path) -> MiniRacer:
        # get script from <https://github.com/spatialillusions/milsymbol/releases/tag/v2.2.0>
        with open(path, 'r') as fp:
            txt = fp.read()
        ctx = MiniRacer()
        ctx.eval(txt)
        return ctx

    def _search_a(self, query: str, n=1, show_results=False) -> str:
        """ query in set A treated like few separate words
        """
        choices_a = self._data_a.keys()
        # try to find each word separately, get uniq results
        findings = set([self._fuzzy_search(q, choices_a, n, show_results) for q in query.split()])
        # update default values
        answer_a = self.defaults_set_a.copy()
        # '3.Reality' is a key to self._data_a where '3' is a idx of set_a
        #   self._data_a['3.Reality'] -> '0'
        answer_a.update({f.split('.')[0]: self._data_a[f] for f in findings if f})
        # format an answer string
        a = f"{answer_a['1']}{answer_a['2']}{answer_a['3']}{answer_a['4']}{answer_a['56']}{answer_a['7']}{answer_a['8']}{answer_a['910']}"
        return a

    def _search_b(self, query: str, mod1: str = '', mod2: str = '', n=1, show_results=False) -> str:
        """ query in set B treated like a single sentence
            each modifier is a separate single word/sentence
        """
        choices = self._data_b.keys()
        # try to find entity
        #   'Land unit.Fires.Mortar.Armored/Mechanized/Tracked'
        selected_key = self._fuzzy_search(query, choices, n, show_results)
        #   '130801'
        answer_b = self._data_b[selected_key] if selected_key else '000000'
        #   'Land unit' -- prefix of selected_key
        selected_b = selected_key.split('.')[0] if selected_key else selected_key
        # try to find modifiers
        answer_mod1 = self._search_b_mode(mod1, selected_b, suffix='.modifier_1', show_results=show_results)
        answer_mod2 = self._search_b_mode(mod2, selected_b, suffix='.modifier_2', show_results=show_results)
        # format an answer string
        b = answer_b + answer_mod1 + answer_mod2
        return b

    def _search_b_mode(self, query: str | None, selected_b: str | None, suffix='.modifier_1', n=1, show_results=False) -> str:
        if query and selected_b:
            # ['Land unit.modifier_1.Attack', ..]
            choices = [k for k in self._data_b.keys() if selected_b + suffix in k]
            # 'Land unit.modifier_1.Attack'
            x = self._fuzzy_search(query, choices, n, show_results)
            # '03'
            answer_mod = self._data_b[x] if x else '00'
        else:
            answer_mod = '00'
        return answer_mod

    def _fuzzy_search(self, query: str, choices: list[str], n: int, show_results: bool) -> str:
        # TODO score_cutoff as a parameter
        x = rapidfuzz.process.extract(query, choices, limit=n, score_cutoff=self.score_cutoff, scorer=rapidfuzz.fuzz.partial_ratio)
        if show_results:
            print(f"{query}:")
            if x:
                for i in x:
                    print(f'\t{i}')
            else:
                print('\tNOTHING')
        x = x[0][0] if x else ''
        return x

    def get_sidc(self, query_a='', query_b='', mod1='', mod2='', show_results=False) -> str:
        """ query in set A treated like few separate words
            query in set B treated like a single sentence
            each modifier is a separate single word/sentence
        """
        a = self._search_a(query_a, show_results=show_results)
        b = self._search_b(query_b, mod1, mod2, show_results=show_results)
        return a + b

    def get_svg(self, sidc: str, size=35) -> str:
        svg_text = self._ctx.eval(f'new ms.Symbol({sidc}, {{"size": {size}}}).asSVG()')
        return svg_text

    def show_top_n(self, query, n=10) -> None:
        print('IN SET A -- ', end='')
        choices_a = self._data_a.keys()
        _ = self._fuzzy_search(query, choices_a, n, True)
        print('\n', end='')
        print('IN SET B -- ', end='')
        choices_b = self._data_b.keys()
        _ = self._fuzzy_search(query, choices_b, n, True)


def get_preloaded_SIDCFuzzySearcher(std: str = '2525d') -> SIDCFuzzySearcher:
    # load data for sets, and js lib
    #   https://importlib-resources.readthedocs.io/en/latest/using.html#migrating-from-legacy
    path_to_set_a = importlib.resources.files('fuzzy_sidc').joinpath("set_a.json")
    if std == '2525d':
        path_to_set_b = importlib.resources.files('fuzzy_sidc').joinpath("set_b_2525d.json")
    elif std == 'app6d':
        path_to_set_b = importlib.resources.files('fuzzy_sidc').joinpath("set_b_app6d.json")
    else:
        raise Exception('Wrong datatset')
    path_to_milsymbolsjs = importlib.resources.files('fuzzy_sidc').joinpath("milsymbol.js")
    # load searcher
    x = SIDCFuzzySearcher(path_to_set_a, path_to_set_b, path_to_milsymbolsjs)
    return x
