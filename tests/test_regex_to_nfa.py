__author__ = 'aortegag'

# Append parent directory when running from command line
import sys

sys.path.append("..")

import unittest
from re_notation import infix_to_prefix
from regex_to_nfa import build_dfa
from regex_to_nfa import compare_dfas


class TestRegexToNfa(unittest.TestCase):
    def test_valid_tests(self):
        f = lambda reg: build_dfa(infix_to_prefix(reg))
        compare = lambda r1, r2: compare_dfas(f(r1), f(r2))
        tup = (True, "dfa1 and dfa2 accept the same language")

        self.assertEqual(tup, compare("", ""))
        self.assertEqual(tup, compare("a", "a"))
        self.assertEqual(tup, compare("a(a+b)*bb", "a(b+a)*bb"))
        self.assertEqual(tup, compare("(a+b)* b (a+b)* b (a+b)*", "a* b a* b (a+b)*"))
        self.assertEqual(tup, compare("(0+11*0)*", "(0+11*0)*+(11*0)*00*"))
        self.assertEqual(tup, compare("(0+11*0)*", "0*1(1+00*1)*00* + 0*"))

        # ###############
        # Begin Alfonso's test cases
        # ###############
        self.assertEqual(tup, compare("((000*1+01)(0+11*0)+10+111*0)((1+00*1)(0+11*0))*",
                                      "(000*10+010+000*111*0+0111*0+10+111*0)((1+00*1)(0+11*0))*"))
        self.assertEqual(tup, compare("((000*1+01)(0+11*0)+10+111*0)((1+00*1)(0+11*0))*",
                                      "((000*1+01)(0+11*0)+10+111*0)(10+00*10+111*0+00*111*0)*"))
        self.assertEqual(tup, compare("((000*1+01)(0+11*0)+10+111*0)((1+00*1)(0+11*0))*",
                                      "(000*10+010+000*111*0+0111*0+10+111*0)(10+00*10+111*0+00*111*0)*"))
        self.assertEqual(tup, compare("((000*1+01)(0+11*0)+10+111*0)((1+00*1)(0+11*0))*", "0*11*0((11*0)*+00*11*0)*"))
        self.assertEqual(tup, compare("((000*1+01)(0+11*0)+10+111*0)((1+00*1)(0+11*0))*", "0*11*0((1+00*1)1*0)*"))
        self.assertEqual(tup, compare("((000*1+01)(0+11*0)+10+111*0)((1+00*1)(0+11*0))*", "0*11*0(11*0+00*11*0)*"))

        ################
        self.assertEqual(tup, compare("(000*10+010+000*111*0+0111*0+10+111*0)((1+00*1)(0+11*0))*",
                                      "((000*1+01)(0+11*0)+10+111*0)(10+00*10+111*0+00*111*0)*"))
        self.assertEqual(tup, compare("(000*10+010+000*111*0+0111*0+10+111*0)((1+00*1)(0+11*0))*",
                                      "(000*10+010+000*111*0+0111*0+10+111*0)(10+00*10+111*0+00*111*0)*"))
        self.assertEqual(tup, compare("(000*10+010+000*111*0+0111*0+10+111*0)((1+00*1)(0+11*0))*",
                                      "0*11*0((11*0)*+00*11*0)*"))
        self.assertEqual(tup,
                         compare("(000*10+010+000*111*0+0111*0+10+111*0)((1+00*1)(0+11*0))*", "0*11*0((1+00*1)1*0)*"))
        self.assertEqual(tup,
                         compare("(000*10+010+000*111*0+0111*0+10+111*0)((1+00*1)(0+11*0))*", "0*11*0(11*0+00*11*0)*"))

        ################
        self.assertEqual(tup, compare("((000*1+01)(0+11*0)+10+111*0)(10+00*10+111*0+00*111*0)*",
                                      "(000*10+010+000*111*0+0111*0+10+111*0)(10+00*10+111*0+00*111*0)*"))
        self.assertEqual(tup,
                         compare("((000*1+01)(0+11*0)+10+111*0)(10+00*10+111*0+00*111*0)*", "0*11*0((11*0)*+00*11*0)*"))
        self.assertEqual(tup,
                         compare("((000*1+01)(0+11*0)+10+111*0)(10+00*10+111*0+00*111*0)*", "0*11*0((1+00*1)1*0)*"))
        self.assertEqual(tup,
                         compare("((000*1+01)(0+11*0)+10+111*0)(10+00*10+111*0+00*111*0)*", "0*11*0(11*0+00*11*0)*"))

        ################
        self.assertEqual(tup, compare("(000*10+010+000*111*0+0111*0+10+111*0)(10+00*10+111*0+00*111*0)*",
                                      "0*11*0((11*0)*+00*11*0)*"))
        self.assertEqual(tup, compare("(000*10+010+000*111*0+0111*0+10+111*0)(10+00*10+111*0+00*111*0)*",
                                      "0*11*0((1+00*1)1*0)*"))
        self.assertEqual(tup, compare("(000*10+010+000*111*0+0111*0+10+111*0)(10+00*10+111*0+00*111*0)*",
                                      "0*11*0(11*0+00*11*0)*"))

        ################
        self.assertEqual(tup, compare("0*11*0((11*0)*+00*11*0)*", "0*11*0((1+00*1)1*0)*"))
        self.assertEqual(tup, compare("0*11*0((11*0)*+00*11*0)*", "0*11*0(11*0+00*11*0)*"))

        ################
        self.assertEqual(tup, compare("0*11*0((1+00*1)1*0)*", "0*11*0(11*0+00*11*0)*"))

        ################
        self.assertEqual(tup, compare("(((aa+b)(b((bbb*a+ab)b*a)*ba))*b((bbb*a+ab)b*a)*aa)*(aa+b)(b((bbb*a+ab)b*a)*ba)*b((bbb*a+ab)b*a)*(bbb*a+ab)b*",
                                      "(((aa+b)(b(bbb*ab*a+abb*a)*ba))*b((bbb*a+ab)b*a)*aa)*(aa+b)(b(bbb*ab*a+abb*a)*ba)*b(bbb*ab*a+abb*a)*(bbb*a+ab)b*"))
        self.assertEqual(tup, compare("(((aa+b)(b((bbb*a+ab)b*a)*ba))*b((bbb*a+ab)b*a)*aa)*(aa+b)(b((bbb*a+ab)b*a)*ba)*b((bbb*a+ab)b*a)*(bbb*a+ab)b*",
                                      "(((aa+b)(b(bbb*ab*a+abb*a+#)*ba))*b((bbb*a+ab)b*a)*aa)*(aa+b)(b(bbb*ab*a+abb*a+#)*ba)*b(bbb*ab*a+abb*a+#)*(bbb*ab*+abb*)"))
        self.assertEqual(tup, compare("(((aa+b)(b((bbb*a+ab)b*a)*ba))*b((bbb*a+ab)b*a)*aa)*(aa+b)(b((bbb*a+ab)b*a)*ba)*b((bbb*a+ab)b*a)*(bbb*a+ab)b*",
                                      "((aa(b(bbb*ab*a+abb*a+#)*ba)+b(b(bbb*ab*a+abb*a+#)*ba))*b((bbb*a+ab)b*a)*aa)*(aa+b)(b(bbb*ab*a+abb*a+#)*ba)*b(bbb*ab*a+abb*a+#)*(bbb*ab*+abb*)"))

        ################
        self.assertEqual(tup, compare("(((aa+b)(b(bbb*ab*a+abb*a)*ba))*b((bbb*a+ab)b*a)*aa)*(aa+b)(b(bbb*ab*a+abb*a)*ba)*b(bbb*ab*a+abb*a)*(bbb*a+ab)b*",
                                      "(((aa+b)(b(bbb*ab*a+abb*a+#)*ba))*b((bbb*a+ab)b*a)*aa)*(aa+b)(b(bbb*ab*a+abb*a+#)*ba)*b(bbb*ab*a+abb*a+#)*(bbb*ab*+abb*)"))
        self.assertEqual(tup, compare("(((aa+b)(b(bbb*ab*a+abb*a)*ba))*b((bbb*a+ab)b*a)*aa)*(aa+b)(b(bbb*ab*a+abb*a)*ba)*b(bbb*ab*a+abb*a)*(bbb*a+ab)b*",
                                      "((aa(b(bbb*ab*a+abb*a+#)*ba)+b(b(bbb*ab*a+abb*a+#)*ba))*b((bbb*a+ab)b*a)*aa)*(aa+b)(b(bbb*ab*a+abb*a+#)*ba)*b(bbb*ab*a+abb*a+#)*(bbb*ab*+abb*)"))

        ################
        self.assertEqual(tup, compare("(((aa+b)(b(bbb*ab*a+abb*a+#)*ba))*b((bbb*a+ab)b*a)*aa)*(aa+b)(b(bbb*ab*a+abb*a+#)*ba)*b(bbb*ab*a+abb*a+#)*(bbb*ab*+abb*)",
                                      "((aa(b(bbb*ab*a+abb*a+#)*ba)+b(b(bbb*ab*a+abb*a+#)*ba))*b((bbb*a+ab)b*a)*aa)*(aa+b)(b(bbb*ab*a+abb*a+#)*ba)*b(bbb*ab*a+abb*a+#)*(bbb*ab*+abb*)"))

        ################
        self.assertEqual(tup, compare("((abb*a(b+a(ab+bbb*a))*aaa)+(aa+b+abb*a(b+a(ab+bbb*a))*aba)(b+aba+a(ab+bbb*a)(b+a(ab+bbb*a))*aba)*(aaa+a(ab+bbb*a)(b+a(ab+bbb*a))*aaa))*(((aa+b+abb*a(b+a(ab+bbb*a))*aba)(b+aba+a(ab+bbb*a)(b+a(ab+bbb*a))*aba)*(a(ab+bbb*a)(b+a(ab+bbb*a))*+#))+abb*a(b+a(ab+bbb*a))*)",
                                      "(ab*a+b)(aaa(ab*a+b)+abb*a+b+aab)*"))
        self.assertEqual(tup, compare("((abb*a(b+a(ab+bbb*a))*aaa)+(aa+b+abb*a(b+a(ab+bbb*a))*aba)(b+aba+a(ab+bbb*a)(b+a(ab+bbb*a))*aba)*(aaa+a(ab+bbb*a)(b+a(ab+bbb*a))*aaa))*(((aa+b+abb*a(b+a(ab+bbb*a))*aba)(b+aba+a(ab+bbb*a)(b+a(ab+bbb*a))*aba)*(a(ab+bbb*a)(b+a(ab+bbb*a))*+#))+abb*a(b+a(ab+bbb*a))*)",
                                      "(ab*a+b)(aaa(ab*a+b)+abb*a+b+aab+#)*"))
        self.assertEqual(tup, compare("((abb*a(b+a(ab+bbb*a))*aaa)+(aa+b+abb*a(b+a(ab+bbb*a))*aba)(b+aba+a(ab+bbb*a)(b+a(ab+bbb*a))*aba)*(aaa+a(ab+bbb*a)(b+a(ab+bbb*a))*aaa))*(((aa+b+abb*a(b+a(ab+bbb*a))*aba)(b+aba+a(ab+bbb*a)(b+a(ab+bbb*a))*aba)*(a(ab+bbb*a)(b+a(ab+bbb*a))*+#))+abb*a(b+a(ab+bbb*a))*)",
                                      "(ab*a+b)(aaa(ab*a+b)+abb*a+b+aab+#)*"))
        self.assertEqual(tup, compare("((abb*a(b+a(ab+bbb*a))*aaa)+(aa+b+abb*a(b+a(ab+bbb*a))*aba)(b+aba+a(ab+bbb*a)(b+a(ab+bbb*a))*aba)*(aaa+a(ab+bbb*a)(b+a(ab+bbb*a))*aaa))*(((aa+b+abb*a(b+a(ab+bbb*a))*aba)(b+aba+a(ab+bbb*a)(b+a(ab+bbb*a))*aba)*(a(ab+bbb*a)(b+a(ab+bbb*a))*+#))+abb*a(b+a(ab+bbb*a))*)",
                                      "(ab*a+b)(aaaab*a+aaab+abb*a+b+aab+#)*"))

        ################
        self.assertEqual(tup, compare("(ab*a+b)(aaa(ab*a+b)+abb*a+b+aab)*", "(ab*a+b)(aaa(ab*a+b)+abb*a+b+aab+#)*"))
        self.assertEqual(tup, compare("(ab*a+b)(aaa(ab*a+b)+abb*a+b+aab)*", "(ab*a+b)(aaa(ab*a+b)+abb*a+b+aab+#)*"))
        self.assertEqual(tup, compare("(ab*a+b)(aaa(ab*a+b)+abb*a+b+aab)*", "(ab*a+b)(aaaab*a+aaab+abb*a+b+aab+#)*"))

        ################
        self.assertEqual(tup, compare("(ab*a+b)(aaa(ab*a+b)+abb*a+b+aab+#)*", "(ab*a+b)(aaa(ab*a+b)+abb*a+b+aab+#)*"))
        self.assertEqual(tup, compare("(ab*a+b)(aaa(ab*a+b)+abb*a+b+aab+#)*", "(ab*a+b)(aaaab*a+aaab+abb*a+b+aab+#)*"))

        ################
        self.assertEqual(tup, compare("(ab*a+b)(aaa(ab*a+b)+abb*a+b+aab+#)*", "(ab*a+b)(aaaab*a+aaab+abb*a+b+aab+#)*"))

        ################
        # End of Alfonso's test cases
        ################

        self.assertEqual(tup, compare("a", "#a"))
        self.assertEqual(tup, compare("a", "a#"))
        self.assertEqual(tup, compare("a", "#a#"))
        self.assertEqual(tup, compare("a*", "a*#"))
        self.assertEqual(tup, compare("a*", "#a*"))
        self.assertEqual(tup, compare("a*", "#a*#"))
        self.assertEqual(tup, compare("#", "##"))
        self.assertEqual(tup, compare("a+ab", "a(#+b)"))
        self.assertEqual(tup, compare("(11*0+00*11*0)*(00*)", "((1+00*1)1*0)*(00*)"))

        self.assertEqual(tup, compare("(1+0)#(1+0)#####(1+0)", "000+001+010+011+100+101+110+111"))
        self.assertEqual(tup, compare("#", "#"))
        self.assertEqual(tup, compare("abcdefghijklmnopqrstuvwxyz", "a#bc#de#fghi#jklm#nopq#rst#uvw#xyz#"))
        self.assertEqual(tup, compare("hello+world", "world+hello"))
        self.assertEqual(tup, compare("#a*(b(a+b)*)#", "a*b(a+b)*"))

        # empty set
        self.assertEqual(tup, compare("%*", "#"))


    def test_invalid_tests(self):
        f = lambda reg: build_dfa(infix_to_prefix(reg))
        compare = lambda r1, r2: compare_dfas(f(r1), f(r2))
        tup = (True, "dfa1 and dfa2 accept the same language")

        self.assertNotEqual(tup, compare("a", "a*"))
        self.assertNotEqual(tup, compare("a+#", "a"))
        self.assertNotEqual(tup, compare("a(a+b)*bb", "a(b+a)*bbb"))
        self.assertNotEqual(tup, compare("(a+b)* b (a+b)* b (a+b)*", "a* b a* b (a+b)*aa"))
        self.assertNotEqual(tup, compare("(0+11*0)*", "(11*0)*+(11*0)0*"))
        self.assertNotEqual(tup, compare("(0+11*0)*", "0*1(1+00*1)*00* + 0"))

        self.assertNotEqual(tup, compare("00+11+22+33", "00*+11*+22*+33*"))
        self.assertNotEqual(tup, compare("1(0+1)*1", "101+111+#"))
        self.assertNotEqual(tup, compare("0*1*0*", "#"))
        self.assertNotEqual(tup, compare("a(aa+b)* + a(aa+b)*ab+b(ba+a)((aa+b)*ab+bb)*(ba+a)(aa+b)*#",
                                         "(a(aa+b)*ab+b)((ba+a)(aa+b)*ab+bb)*((ba+a)(aa+b)*#)+a(aa+b)*"))

        self.assertNotEqual(tup, compare("(a)*b(a+b)*", "#+a*b(a+b)*#"))


if __name__ == "__main__":
    unittest.main()
