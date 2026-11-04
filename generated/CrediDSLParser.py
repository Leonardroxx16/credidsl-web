# Generated from CrediDSL.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,22,84,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,1,0,1,0,1,0,1,0,1,
        0,1,1,1,1,1,1,1,1,3,1,34,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
        1,3,1,3,1,3,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,3,5,56,8,5,1,6,1,6,1,
        6,1,7,1,7,1,7,1,7,1,7,3,7,66,8,7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,
        3,8,76,8,8,1,9,1,9,1,10,1,10,1,11,1,11,1,11,0,0,12,0,2,4,6,8,10,
        12,14,16,18,20,22,0,3,1,0,11,16,1,0,19,20,1,0,8,10,75,0,24,1,0,0,
        0,2,33,1,0,0,0,4,35,1,0,0,0,6,44,1,0,0,0,8,47,1,0,0,0,10,55,1,0,
        0,0,12,57,1,0,0,0,14,65,1,0,0,0,16,75,1,0,0,0,18,77,1,0,0,0,20,79,
        1,0,0,0,22,81,1,0,0,0,24,25,3,4,2,0,25,26,3,2,1,0,26,27,3,6,3,0,
        27,28,5,0,0,1,28,1,1,0,0,0,29,30,3,4,2,0,30,31,3,2,1,0,31,34,1,0,
        0,0,32,34,1,0,0,0,33,29,1,0,0,0,33,32,1,0,0,0,34,3,1,0,0,0,35,36,
        5,1,0,0,36,37,5,21,0,0,37,38,5,2,0,0,38,39,5,20,0,0,39,40,5,3,0,
        0,40,41,3,8,4,0,41,42,5,4,0,0,42,43,3,22,11,0,43,5,1,0,0,0,44,45,
        5,5,0,0,45,46,3,22,11,0,46,7,1,0,0,0,47,48,3,12,6,0,48,49,3,10,5,
        0,49,9,1,0,0,0,50,51,5,7,0,0,51,52,3,12,6,0,52,53,3,10,5,0,53,56,
        1,0,0,0,54,56,1,0,0,0,55,50,1,0,0,0,55,54,1,0,0,0,56,11,1,0,0,0,
        57,58,3,16,8,0,58,59,3,14,7,0,59,13,1,0,0,0,60,61,5,6,0,0,61,62,
        3,16,8,0,62,63,3,14,7,0,63,66,1,0,0,0,64,66,1,0,0,0,65,60,1,0,0,
        0,65,64,1,0,0,0,66,15,1,0,0,0,67,68,5,21,0,0,68,69,3,18,9,0,69,70,
        3,20,10,0,70,76,1,0,0,0,71,72,5,17,0,0,72,73,3,8,4,0,73,74,5,18,
        0,0,74,76,1,0,0,0,75,67,1,0,0,0,75,71,1,0,0,0,76,17,1,0,0,0,77,78,
        7,0,0,0,78,19,1,0,0,0,79,80,7,1,0,0,80,21,1,0,0,0,81,82,7,2,0,0,
        82,23,1,0,0,0,4,33,55,65,75
    ]

class CrediDSLParser ( Parser ):

    grammarFileName = "CrediDSL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'REGLA'", "'PRIORIDAD'", "'SI'", "'ENTONCES'", 
                     "'POR_DEFECTO'", "'Y'", "'O'", "'APROBAR'", "'RECHAZAR'", 
                     "'REVISION_MANUAL'", "'>='", "'<='", "'>'", "'<'", 
                     "'=='", "'!='", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "REGLA", "PRIORIDAD", "SI", "ENTONCES", 
                      "POR_DEFECTO", "Y", "O", "APROBAR", "RECHAZAR", "REVISION_MANUAL", 
                      "GE", "LE", "GT", "LT", "EQ", "NE", "PA", "PC", "DECIMAL", 
                      "ENTERO", "ID", "BLANCO" ]

    RULE_pol = 0
    RULE_rest = 1
    RULE_reg = 2
    RULE_defecto = 3
    RULE_exp = 4
    RULE_eo = 5
    RULE_con = 6
    RULE_cy = 7
    RULE_atom = 8
    RULE_op = 9
    RULE_num = 10
    RULE_acc = 11

    ruleNames =  [ "pol", "rest", "reg", "defecto", "exp", "eo", "con", 
                   "cy", "atom", "op", "num", "acc" ]

    EOF = Token.EOF
    REGLA=1
    PRIORIDAD=2
    SI=3
    ENTONCES=4
    POR_DEFECTO=5
    Y=6
    O=7
    APROBAR=8
    RECHAZAR=9
    REVISION_MANUAL=10
    GE=11
    LE=12
    GT=13
    LT=14
    EQ=15
    NE=16
    PA=17
    PC=18
    DECIMAL=19
    ENTERO=20
    ID=21
    BLANCO=22

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class PolContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def reg(self):
            return self.getTypedRuleContext(CrediDSLParser.RegContext,0)


        def rest(self):
            return self.getTypedRuleContext(CrediDSLParser.RestContext,0)


        def defecto(self):
            return self.getTypedRuleContext(CrediDSLParser.DefectoContext,0)


        def EOF(self):
            return self.getToken(CrediDSLParser.EOF, 0)

        def getRuleIndex(self):
            return CrediDSLParser.RULE_pol




    def pol(self):

        localctx = CrediDSLParser.PolContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_pol)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.reg()
            self.state = 25
            self.rest()
            self.state = 26
            self.defecto()
            self.state = 27
            self.match(CrediDSLParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def reg(self):
            return self.getTypedRuleContext(CrediDSLParser.RegContext,0)


        def rest(self):
            return self.getTypedRuleContext(CrediDSLParser.RestContext,0)


        def getRuleIndex(self):
            return CrediDSLParser.RULE_rest




    def rest(self):

        localctx = CrediDSLParser.RestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_rest)
        try:
            self.state = 33
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 29
                self.reg()
                self.state = 30
                self.rest()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RegContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REGLA(self):
            return self.getToken(CrediDSLParser.REGLA, 0)

        def ID(self):
            return self.getToken(CrediDSLParser.ID, 0)

        def PRIORIDAD(self):
            return self.getToken(CrediDSLParser.PRIORIDAD, 0)

        def ENTERO(self):
            return self.getToken(CrediDSLParser.ENTERO, 0)

        def SI(self):
            return self.getToken(CrediDSLParser.SI, 0)

        def exp(self):
            return self.getTypedRuleContext(CrediDSLParser.ExpContext,0)


        def ENTONCES(self):
            return self.getToken(CrediDSLParser.ENTONCES, 0)

        def acc(self):
            return self.getTypedRuleContext(CrediDSLParser.AccContext,0)


        def getRuleIndex(self):
            return CrediDSLParser.RULE_reg




    def reg(self):

        localctx = CrediDSLParser.RegContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_reg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.match(CrediDSLParser.REGLA)
            self.state = 36
            self.match(CrediDSLParser.ID)
            self.state = 37
            self.match(CrediDSLParser.PRIORIDAD)
            self.state = 38
            self.match(CrediDSLParser.ENTERO)
            self.state = 39
            self.match(CrediDSLParser.SI)
            self.state = 40
            self.exp()
            self.state = 41
            self.match(CrediDSLParser.ENTONCES)
            self.state = 42
            self.acc()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefectoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def POR_DEFECTO(self):
            return self.getToken(CrediDSLParser.POR_DEFECTO, 0)

        def acc(self):
            return self.getTypedRuleContext(CrediDSLParser.AccContext,0)


        def getRuleIndex(self):
            return CrediDSLParser.RULE_defecto




    def defecto(self):

        localctx = CrediDSLParser.DefectoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_defecto)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.match(CrediDSLParser.POR_DEFECTO)
            self.state = 45
            self.acc()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def con(self):
            return self.getTypedRuleContext(CrediDSLParser.ConContext,0)


        def eo(self):
            return self.getTypedRuleContext(CrediDSLParser.EoContext,0)


        def getRuleIndex(self):
            return CrediDSLParser.RULE_exp




    def exp(self):

        localctx = CrediDSLParser.ExpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_exp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self.con()
            self.state = 48
            self.eo()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def O(self):
            return self.getToken(CrediDSLParser.O, 0)

        def con(self):
            return self.getTypedRuleContext(CrediDSLParser.ConContext,0)


        def eo(self):
            return self.getTypedRuleContext(CrediDSLParser.EoContext,0)


        def getRuleIndex(self):
            return CrediDSLParser.RULE_eo




    def eo(self):

        localctx = CrediDSLParser.EoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_eo)
        try:
            self.state = 55
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7]:
                self.enterOuterAlt(localctx, 1)
                self.state = 50
                self.match(CrediDSLParser.O)
                self.state = 51
                self.con()
                self.state = 52
                self.eo()
                pass
            elif token in [4, 18]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def atom(self):
            return self.getTypedRuleContext(CrediDSLParser.AtomContext,0)


        def cy(self):
            return self.getTypedRuleContext(CrediDSLParser.CyContext,0)


        def getRuleIndex(self):
            return CrediDSLParser.RULE_con




    def con(self):

        localctx = CrediDSLParser.ConContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_con)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self.atom()
            self.state = 58
            self.cy()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Y(self):
            return self.getToken(CrediDSLParser.Y, 0)

        def atom(self):
            return self.getTypedRuleContext(CrediDSLParser.AtomContext,0)


        def cy(self):
            return self.getTypedRuleContext(CrediDSLParser.CyContext,0)


        def getRuleIndex(self):
            return CrediDSLParser.RULE_cy




    def cy(self):

        localctx = CrediDSLParser.CyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_cy)
        try:
            self.state = 65
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6]:
                self.enterOuterAlt(localctx, 1)
                self.state = 60
                self.match(CrediDSLParser.Y)
                self.state = 61
                self.atom()
                self.state = 62
                self.cy()
                pass
            elif token in [4, 7, 18]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(CrediDSLParser.ID, 0)

        def op(self):
            return self.getTypedRuleContext(CrediDSLParser.OpContext,0)


        def num(self):
            return self.getTypedRuleContext(CrediDSLParser.NumContext,0)


        def PA(self):
            return self.getToken(CrediDSLParser.PA, 0)

        def exp(self):
            return self.getTypedRuleContext(CrediDSLParser.ExpContext,0)


        def PC(self):
            return self.getToken(CrediDSLParser.PC, 0)

        def getRuleIndex(self):
            return CrediDSLParser.RULE_atom




    def atom(self):

        localctx = CrediDSLParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_atom)
        try:
            self.state = 75
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [21]:
                self.enterOuterAlt(localctx, 1)
                self.state = 67
                self.match(CrediDSLParser.ID)
                self.state = 68
                self.op()
                self.state = 69
                self.num()
                pass
            elif token in [17]:
                self.enterOuterAlt(localctx, 2)
                self.state = 71
                self.match(CrediDSLParser.PA)
                self.state = 72
                self.exp()
                self.state = 73
                self.match(CrediDSLParser.PC)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GE(self):
            return self.getToken(CrediDSLParser.GE, 0)

        def LE(self):
            return self.getToken(CrediDSLParser.LE, 0)

        def GT(self):
            return self.getToken(CrediDSLParser.GT, 0)

        def LT(self):
            return self.getToken(CrediDSLParser.LT, 0)

        def EQ(self):
            return self.getToken(CrediDSLParser.EQ, 0)

        def NE(self):
            return self.getToken(CrediDSLParser.NE, 0)

        def getRuleIndex(self):
            return CrediDSLParser.RULE_op




    def op(self):

        localctx = CrediDSLParser.OpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_op)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 77
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 129024) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENTERO(self):
            return self.getToken(CrediDSLParser.ENTERO, 0)

        def DECIMAL(self):
            return self.getToken(CrediDSLParser.DECIMAL, 0)

        def getRuleIndex(self):
            return CrediDSLParser.RULE_num




    def num(self):

        localctx = CrediDSLParser.NumContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_num)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            _la = self._input.LA(1)
            if not(_la==19 or _la==20):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AccContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def APROBAR(self):
            return self.getToken(CrediDSLParser.APROBAR, 0)

        def RECHAZAR(self):
            return self.getToken(CrediDSLParser.RECHAZAR, 0)

        def REVISION_MANUAL(self):
            return self.getToken(CrediDSLParser.REVISION_MANUAL, 0)

        def getRuleIndex(self):
            return CrediDSLParser.RULE_acc




    def acc(self):

        localctx = CrediDSLParser.AccContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_acc)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1792) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





