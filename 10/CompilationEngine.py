
statementsList = ["let", "if", "while", "do", "return"]
operationList=["+","-","*","/","&","|","<",">","="]

keywordConstList=["true","false","null","this"]

class CompilationEngine:


    def _openTag(self, string):
        self.f.write("<"+string +">")

    def _closeTag(self, string):
        self.f.write("</"+string +">\n")

    def compileExpressionList(self):
        self._openTag("expressionList")
        self.f.write("\n")
        if (not self.tkn.getToken()== ")" ):
            self.CompileExpression()
            while (self.tkn.getToken() == ","):
                self.nextToken()  # ,
                self.CompileExpression()
        self._closeTag("expressionList")

    def _compileSubroutineCall(self): # todo check if need open and close
        self.nextToken()  # varName / subroutineName /className
        if (self.tkn.getToken() == "("):
            self.nextToken()  # (
            self.compileExpressionList()
            self.nextToken()  # )
        else:
            self.nextToken()  # .
            self.nextToken()  # subroutineName
            self.nextToken()  # (
            self.compileExpressionList()
            self.nextToken()  # )



    def compileTerm(self):
        self._openTag("term")
        self.f.write("\n")

        # if term is integer const or keyword const
        if (self.tkn.curTokenType == "integerConstant" or
            self.tkn.getToken() in keywordConstList):
            self.nextToken()  # int or keyword

        # if term is string const
        elif (self.tkn.curTokenType == "stringConstant"):
                self.tkn.curToken = self.tkn.curToken[1:-1]
                self.tkn.curTokenType = "stringConstant"
                self.nextToken()  # string

        # if term is unary operation
        elif (self.tkn.getToken() == "-" or self.tkn.getToken() == "~"):
            self.nextToken() # - or ~
            self.compileTerm()



        # (expression)
        elif (self.tkn.getToken() == "("):
            self.nextToken() # (
            self.CompileExpression()
            self.nextToken() #)

        #
        elif (self.tkn.tokenType() == "identifier"):
            nextToken = self.tkn.tokenList[self.tkn.curIndex]
            if (nextToken == "." or nextToken == "("):
                self._compileSubroutineCall()
            elif (nextToken == "["):
                self.nextToken()  # varName
                self.nextToken()  # [
                self.CompileExpression()
                self.nextToken()  # ]
            else:
                self.nextToken()  # varName
        else:
            self._compileSubroutineCall()

        self._closeTag("term")



    def CompileExpression(self):
        self._openTag("expression")
        self.f.write("\n")
        self.compileTerm()
        while (self.tkn.getToken() in operationList):
            self.nextToken()  # operation
            self.compileTerm()
        self._closeTag("expression")



    def compileLet(self):
        self._openTag("letStatement")
        self.f.write("\n")
        self.nextToken() # let
        self.nextToken()  # varName
        if (self.tkn.getToken() =="["):
            self.nextToken() # [
            self.CompileExpression()
            self.nextToken() # ]
        self.nextToken()  # =
        self.CompileExpression()
        self.nextToken()  # ;
        self._closeTag("letStatement")

    def compileDo(self):
        self._openTag("doStatement")
        self.f.write("\n")
        self.nextToken()  # do
        self._compileSubroutineCall()
        self.nextToken()  # ;
        self._closeTag("doStatement")

    def compileIf(self):
        self._openTag("ifStatement")
        self.f.write("\n")
        self.nextToken()  # if
        self.nextToken()  # (
        self.CompileExpression()
        self.nextToken()  # )
        self.nextToken()  # {
        self.compileStatements()
        self.nextToken()  # }
        if (self.tkn.getToken() == "else"):
            self.nextToken()  # else
            self.nextToken()  # {
            self.compileStatements()
            self.nextToken()  # }
        self._closeTag("ifStatement")

    def compileWhile(self):
        self._openTag("whileStatement")
        self.f.write("\n")
        self.nextToken()  # while
        self.nextToken()  # (
        self.CompileExpression()
        self.nextToken()  # )
        self.nextToken()  # {
        self.compileStatements()
        self.nextToken()  # }
        self._closeTag("whileStatement")

    def compileReturn(self):
        self._openTag("returnStatement")
        self.f.write("\n")
        self.nextToken()  # return
        if (not self.tkn.getToken() == ";"):
            self.CompileExpression()
        self.nextToken()  # ;
        self._closeTag("returnStatement")

    def compileStatements(self):
        self._openTag("statements") # todo check if always has statements
        self.f.write("\n")
        while(self.tkn.getToken() in statementsList):
            if (self.tkn.getToken() =="let"):
                self.compileLet()
            if (self.tkn.getToken() =="do"):
                self.compileDo()
            if (self.tkn.getToken() =="if"):
                self.compileIf()
            if (self.tkn.getToken() =="return"):
                self.compileReturn()
            if (self.tkn.getToken() =="while"):
                self.compileWhile()
        self._closeTag("statements")



    def CompileParameterList(self):
        self._openTag("parameterList")
        self.f.write("\n")
        if (not self.tkn.getToken() ==")"): # check if there are parameters
            self.nextToken()  # type (int/boolean etc)
            self.nextToken()  # varName
            while (self.tkn.getToken() == ","):
                self.nextToken()  # ,
                self.nextToken()  # type
                self.nextToken()  # varName

        self._closeTag("parameterList")


    def  _CompileSubroutineBody(self):
        self._openTag("subroutineBody")
        self.f.write("\n")
        self.nextToken()  # {
        while (self.tkn.getToken() == "var"):
            self.compileVarDec()
        self.compileStatements()
        self.nextToken()  # }
        self._closeTag("subroutineBody")

    def compileVarDec(self):
        self._openTag("varDec")
        self.f.write("\n")
        self.nextToken()  # var
        self.nextToken()  # type
        self.nextToken()  # varName
        while (self.tkn.getToken() == ","):
            self.nextToken()  # ,
            self.nextToken()  # varName
        self.nextToken()  # ;
        self._closeTag("varDec")


    def CompileClassVarDec(self):
        self._openTag("classVarDec")
        self.f.write("\n")
        self.nextToken() # field or static
        self.nextToken() # type (int/boolean etc)
        self.nextToken() #varName
        while (self.tkn.getToken() == ","):
            self.nextToken() # ,
            self.nextToken() # varName
        self.nextToken() # ;
        self._closeTag("classVarDec")

    def CompileSubroutine(self):
        self._openTag("subroutineDec")
        self.f.write("\n")
        self.nextToken() #constructor, function or method
        self.nextToken() #void or type
        self.nextToken() #subroutine name
        self.nextToken() #(
        self.CompileParameterList()
        self.nextToken()  # )
        self._CompileSubroutineBody()
        self._closeTag("subroutineDec")



    def CompileClass(self):
        self._openTag("class") # <class>
        self.f.write("\n")
        self.nextToken() # class
        self.nextToken() # className
        self.nextToken() # {

        while (self.tkn.getToken() == "static" or self.tkn.getToken() == "field"):
            self.CompileClassVarDec()

        while (self.tkn.getToken() == "constructor" or
               self.tkn.getToken() == "function" or
                self.tkn.getToken() == "method"):
            self.CompileSubroutine()
        self.nextToken()  # }
        self._closeTag("class")  # <class>





    def nextToken(self):
        self._openTag(self.tkn.curTokenType)
        toWrite = self.tkn.getToken()
        if (self.tkn.getToken() == "&"):
            toWrite = "&amp;"
        elif (self.tkn.getToken() == "<"):
            toWrite = "&lt;"
        elif (self.tkn.getToken() == ">"):
            toWrite = "&gt;"
        elif (self.tkn.getToken() == '\\"'):
            toWrite = "&quot;"
        self.f.write(toWrite)
        self._closeTag(self.tkn.curTokenType)
        self.tkn.advance()

    def __init__(self, outputFileName, tokenizer):
        self.f = open(outputFileName, "a")
        self.tkn = tokenizer