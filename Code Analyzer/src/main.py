from antlr4 import FileStream
from gen.JavaLexer import JavaLexer, CommonTokenStream, ParseTreeWalker
from gen.JavaParserLabeled import JavaParserLabeled
from utils.code_analyzer_listener import code_analyzer_listener
from utils.get_java_files import get_files


def main():
    java_files = get_files("../test_project")
    classes_fields = {}
    classes_methods = {}
    java_file_names = []
    for file in java_files:
        file_name = (file.split('\\')[-1]).split('java')[0][0:-1]
        java_file_names.append(file_name)
        try:
            stream = FileStream(file)
        except UnicodeDecodeError:
            print("This file can not be decoded:\n" + file + "\n")
            return
        lexer = JavaLexer(stream)
        tokens = CommonTokenStream(lexer)
        Parser = JavaParserLabeled(tokens)
        tree = Parser.compilationUnit()
        listener = code_analyzer_listener(lexer)
        walker = ParseTreeWalker()
        walker.walk(listener=listener, t=tree)
        for cl in listener.class_names:
            classes_fields[cl] = []
            classes_methods[cl] = []
            for var in listener.classes_fields[cl]:
                classes_fields[cl].append(var)
            for method in listener.classes_methods[cl]:
                classes_methods[cl].append(method)

    private_field_count = 0
    public_field_count = 0
    private_method_count = 0
    public_method_count = 0

    for cl in classes_fields:
        for name, mod in classes_fields[cl]:
            if mod == "public":
                public_field_count += 1
            elif mod == "private":
                private_field_count += 1

    for cl in classes_methods:
        for name, mod in classes_fields[cl]:
            if mod == "public":
                public_method_count += 1
            elif mod == "private":
                private_method_count += 1

    output = open("../output/Analysis.txt", "w+")

    output.write("Analysis completed successfully!\n\n")
    output.write("Number of Java files: " + str(len(java_file_names)) + "\n")
    output.write("Number of java classes: " + str(len(classes_fields)) + "\n")
    output.write("Total number of fields: " + str(private_field_count + public_field_count) + "\n")
    output.write("Total number of private fields: " + str(private_field_count) + "\n")
    output.write("Total number of public fields: " + str(public_field_count) + "\n")
    output.write("Total number of methods: " + str(public_method_count + private_method_count) + "\n")
    output.write("Total number of private methods: " + str(private_method_count) + "\n")
    output.write("Total number of public methods: " + str(public_method_count) + "\n\n")

    output.write("Java files names:\n\t")
    i = 0
    for java_file_name in java_file_names:
        output.write(java_file_name + "\n")
        i += 1
        if i != len(java_file_names):
            output.write("\t")

    output.write("\nJava classes Fields:\n\t")
    for cl in classes_fields:
        output.write("Class name: " + cl + "\n\t\t")
        output.write("Number of fields: " + str(len(classes_fields[cl])) + "\n\t\t")
        output.write("Class fields:\n\t\t")
        i = 0
        for name, mod in classes_fields[cl]:
            if mod is not None:
                output.write(name + " (Modifier = " + mod + ")\n\t")
            else:
                output.write(name + "\n\t")
            i += 1
            if i != len(classes_fields[cl]):
                output.write("\t")

    output.write("\n\nJava classes Methods:\n\t")
    for cl in classes_fields:
        output.write("Class name: " + cl + "\n\t\t")
        output.write("Number of methods: " + str(len(classes_methods[cl])) + "\n\t\t")
        output.write("Class methods:\n\t\t")
        i = 0
        for name, mod in classes_methods[cl]:
            if mod is not None:
                output.write(name + " (Modifier = " + mod + ")\n\t")
            else:
                output.write(name + "\n\t")
            i += 1
            if i != len(classes_methods[cl]):
                output.write("\t")


if __name__ == '__main__':
    main()
