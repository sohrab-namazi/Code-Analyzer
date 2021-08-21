from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from gen.JavaParserLabeled import JavaParserLabeled
from gen.JavaParserLabeledListener import JavaParserLabeledListener
from gen.JavaLexer import JavaLexer


class code_analyzer_listener(JavaParserLabeledListener):
    def __init__(self, common_token_stream: CommonTokenStream = None):
        self.class_names = []
        self.class_texts = []
        self.current_class_name = None
        self.classes_fields = {}
        self.classes_methods = {}
        self.token_stream = common_token_stream
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        class_name = ctx.IDENTIFIER().getText()
        self.class_names.append(class_name)
        self.classes_fields[class_name] = []
        self.classes_methods[class_name] = []
        self.current_class_name = class_name

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        access_mod = None
        if ctx.parentCtx.parentCtx.getText().startswith("public"):
            access_mod = "public"
        elif ctx.parentCtx.parentCtx.getText().startswith("private"):
            access_mod = "private"

        field_name = ctx.variableDeclarators().getText().split('=')[0]
        self.classes_fields[self.current_class_name].append((field_name, access_mod))

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        access_mod = None
        if ctx.parentCtx.parentCtx.getText().startswith("public"):
            access_mod = "public"
        elif ctx.parentCtx.parentCtx.getText().startswith("private"):
            access_mod = "private"
        method_name = ctx.IDENTIFIER().getText()
        self.classes_methods[self.current_class_name].append((method_name, access_mod))

    # def exitClassBodyDeclaration2(self, ctx:JavaParserLabeled.ClassBodyDeclaration2Context):
    # if (ctx.modifier(1) != None):
    #   print(ctx.modifier(1))

    # def exitVariableDeclaratorId(self, ctx:JavaParserLabeled.VariableDeclaratorIdContext):
    #     variable_name = ctx.IDENTIFIER().getText()
    #     self.classes_fields[self.current_class_name].append(variable_name)
