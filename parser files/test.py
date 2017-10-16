import grammar
import morph_parser
import time
import json
import codecs


def load_test_data(fname):
    testData = {}
    fTest = open(fname, 'r', encoding='utf-8-sig')
    lines = [line.strip() for line in fTest.readlines() if '\t' in line]
    for line in lines:
        wf, analyses = line.split('\t')
        analyses = json.loads(analyses)
        testData[wf] = analyses
    fTest.close()
    print('Test data loaded.')
    return testData


def test_wf(parser, wf, analyses):
    """
    Test whether a single wordform is analyzed by the parser
    in the way described by the list of analyses. Each element of the
    analyses list is a dictionary where keys represent properties
    of the Wordform objects. If an actual analysis has more non-empty
    fields than specified in the dictionary, these are not taken
    into account.
    Return a report string.
    """
    if type(analyses) != list:
        return 'Wrong test data: list of analyses expected.'
    realAnalyses = parser.parse(wf)
    if len(realAnalyses) != len(analyses):
        return 'FAILED: ' + str(len(analyses)) + ' expected, ' +\
               str(len(realAnalyses)) + ' given.'
    correctAna = [False] * len(realAnalyses)
    for ana in analyses:
        for iRealAna in range(len(realAnalyses)):
            bAnalysisConforms = True
            for k, v in ana.items():
                try:
                    realValue = realAnalyses[iRealAna].__dict__[k]
                    if realValue != v:
                        bAnalysisConforms = False
                        break
                except KeyError:
                    if any(d[0] == k and d[1] == v
                           for d in realAnalyses[iRealAna].otherData):
                        continue
                    bAnalysisConforms = False
                    break
            if bAnalysisConforms:
                correctAna[iRealAna] = True
    if all(correctAna):
        return 'OK'
    return 'FAILED'


def perform_tests(parser, testData):
    """
    Check if the wordforms in the testData dictionary
    are analyzed correctly by the parser.
    Return a report string.
    """
    if parser is None:
        return 'The parser is not initialized, exiting tests.'
    t1 = time.clock()
    report = ''
    for wf in sorted(testData, key=lambda w: (len(w), w)):
        report += wf + ': ' + test_wf(parser, wf, testData[wf]) + '\n'
    print(time.clock() - t1, ' seconds for performing the tests.')
    return report


def parse_file_words(path, namefile):
    serg = codecs.open(path, 'r', 'utf-8')
    serg_p = codecs.open(namefile, 'w', 'utf-8')
    for line in serg:
        token = line.rstrip()
        serg_p.write(m.ana2xml(token, m.parse(token)) + '\r\n')
    serg_p.close()


def analyse_text(test_text, results_name):
    t = codecs.open(test_text, 'r', 'utf-8')
    text = t.read().replace('.', ' .').replace('\r\n', ' ').replace('\n', ' ')
    text_words = text.split(' ')
    r = codecs.open(results_name, 'w', 'utf-8')
    for token in text_words:
        r.write(m.ana2xml(token, m.parse(token)) + '\r\n')
    r.close()

t1 = time.clock()
g = grammar.Grammar(verbose=True)
print(g.load_paradigms('./словари/conjoined_paradigms.txt', compileParadigms=True), 'simple paradigms loaded.')
print(g.load_lexemes(u'./словари//themain_d_for_parser3.txt'), 'lexemes loaded.')
print(g.load_bad_analyses('test/bad_analyses.txt'), 'wrong analyses loaded.')

g.compile_all()
print(time.clock() - t1, ' seconds for loading and compiling paradigms.')

print('\n\n**** Starting parser... ****\n')
m = morph_parser.Parser(verbose=0)
m.fill_stems()
m.fill_affixes()




print(m.ana2xml('бысть', m.parse('бысть')))


test_text = './test/test_text.txt'
results_name = './test/test_results.txt'
analyse_text(test_text, results_name)
