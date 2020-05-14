
import os


class Seg(object):
    """docstring for Seg"""

    def __init__(self, mode='seg'):
        super(Seg, self).__init__()
        self.mode = mode
        self.cutter = self.impl_func

    def cut(self, sentence):
        return self.cutter(sentence)

    def impl_func(self, sentence):
        return None


class lac_impl(Seg):
    def __init__(self, mode='seg'):
        super().__init__(mode)
        from LAC import LAC
        if mode == 'seg':
            self.lac = LAC(mode='seg')
            self.cutter = self.lac.run
        else:
            self.lac = LAC()
            self.cutter = self.impl_func

    def impl_func(self, sentence):
        words, tags = self.lac.run(sentence)
        return [(word, tag) for word, tag in zip(words, tags)]


class jieba_impl(Seg):
    def __init__(self, mode='seg'):
        super().__init__(mode)

        if mode == 'seg':
            import jieba
            self.cutter = jieba.lcut

        else:
            import jieba.posseg as posseg
            self.cutter = posseg.lcut
        self.cutter("")


class pkuseg_impl(Seg):
    def __init__(self, mode='seg'):
        super().__init__(mode)

        import pkuseg
        if mode == 'seg':
            self.pkuseg = pkuseg.pkuseg()

        else:
            self.pkuseg = pkuseg.pkuseg(postag=True)
        self.cutter = self.pkuseg.cut


class thulac_impl(Seg):
    def __init__(self, mode='seg'):
        super().__init__(mode)

        import thulac

        if mode == 'seg':
            self.thulac = thulac.thulac(seg_only=True)
        else:
            self.thulac = thulac.thulac()
        # self.cutter = self.impl_func

    def impl_func(self, sentence):
        if self.mode == 'seg':
            return [word[0] for word in self.thulac.cut(sentence)]
        else:
            return self.thulac.cut(sentence)


class pynlpir_impl(Seg):
    def __init__(self, mode='seg'):
        super().__init__(mode)

        import pynlpir
        self.pynlpir = pynlpir
        self.pynlpir.open()

    def impl_func(self, sentence):
        if self.mode == 'seg':
            return self.pynlpir.segment(sentence, pos_tagging=False)
        elif self.mode == 'postag':
            return self.pynlpir.segment(sentence)
        else:
            return self.pynlpir.segment(sentence, pos_names='all')

    # def __del__(self):
        # self.pynlpir.close()


class pyhanlp_impl(Seg):
    def __init__(self, mode='seg'):
        super().__init__(mode)

        from pyhanlp import HanLP
        self.hanlp = HanLP
        # self.cut = self.impl_func

    def impl_func(self, sentence):
        res = self.hanlp.segment(sentence)
        if self.mode == 'seg':
            return [str(term.word) for term in res]
        else:
            return [(str(term.word), str(term.nature)) for term in res]


class foolnltk_impl(Seg):
    def __init__(self, mode='seg'):
        super().__init__(mode)

        import fool
        self.fool = fool
        # self.cut = self.impl_func

    def impl_func(self, sentence):
        if self.mode == 'seg':
            return self.fool.cut([sentence])
        elif self.mode == 'postag':
            return self.fool.pos_cut([sentence])[0]
        else:
            return self.fool.analysis([sentence])[0]


class snownlp_impl(Seg):
    def __init__(self, mode='seg'):
        super().__init__(mode)

        from snownlp import SnowNLP
        self.snownlp = SnowNLP
        # self.cut = self.impl_func

    def impl_func(self, sentence):
        snow_res = self.snownlp(sentence)

        if self.mode == 'seg':
            return list(snow_res.words)
        else:
            return list(snow_res.tags)


class standfordnlp_impl(Seg):
    def __init__(self, dictpath, mode='seg'):
        super().__init__(mode)
        from stanfordcorenlp import StanfordCoreNLP

        self.standfornlp = StanfordCoreNLP(dictpath, lang='zh')

        if mode == 'seg':
            self.cut = self.standfornlp.word_tokenize
        elif mode == 'postag':
            self.cut = self.standfornlp.pos_tag
        else:
            self.cut = self.standfornlp.ner


class pyltp_impl(Seg):
    def __init__(self, dictpath, mode='seg'):
        super().__init__(mode)

        from pyltp import Segmentor
        from pyltp import Postagger
        from pyltp import NamedEntityRecognizer
        self.ltp_seg = Segmentor()
        self.ltp_pos = Postagger()
        self.ltp_ner = NamedEntityRecognizer()

        self.ltp_seg.load(os.path.join(dictpath, 'cws.model'))

        if mode != 'seg':
            self.ltp_pos.load(os.path.join(dictpath, 'pos.model'))

        if mode == 'ner':
            self.ltp_ner.load(os.path.join(dictpath, 'ner.model'))

    def impl_func(self, sentence):
        seg_res = self.ltp_seg.segment(sentence)
        if self.mode == 'seg':
            return seg_res

        pos_res = self.ltp_pos.postag(seg_res)
        if self.mode == 'postag':
            return [(word, tag) for (word, tag) in zip(seg_res, pos_res)]

        ner_res = self.ltp_ner.recognize(seg_res, pos_res)
        return [(word, tag) for (word, tag) in zip(seg_res, ner_res)]


if __name__ == '__main__':
    names = ['pynlpir', 'thulac', 'pyhanlp']
    for name in names:
        # cutter = globals()[name + "_impl"]()
        cutter = eval(name + "_impl")()
        print(name, 'cutter', cutter.cut("我来自中山大学"))
        print(name, 'cutter', cutter.cut("百度是家高科技公司"))
        # tagger = globals()[name + "_impl"]("postag")
        tagger = eval(name + "_impl")("postag")
        print(name, 'tagger', tagger.cut("我来自中山大学"))
        print(name, 'tagger', tagger.cut("百度是家高科技公司"))
