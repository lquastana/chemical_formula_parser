"""
Chemical formula parser
================
A Chemical formula parser using Lark 
"""
from lark import Lark, Transformer, v_args,Tree


chemical_grammar = """
start: element*
element: ELEMENT
 | ELEMENT nb_atoms
 | "[" element+ "]" [coeff] -> group
 | "(" element+ ")" [coeff] -> group

coeff : NUMBER
nb_atoms : NUMBER
ELEMENT: UCASE_LETTER LCASE_LETTER
 | UCASE_LETTER

%import common.NUMBER  
%import common.UCASE_LETTER
%import common.LCASE_LETTER

%ignore " "
%ignore "()"
%ignore "[]"
"""


@v_args(inline=True)
class ChemicalFormulaTree(Transformer):
    """
    A class to transform the Tree to a dictionary
    The Methods start,group and element are called according to chemical_grammar. 
    Transformers work bottom-up (or depth-first)
    """

    def __init__(self):
        """
        Initialize the result
        """
        self.result = {}
        
    def start(self, *args):
        """ This method is called at the end 
        where `args` could be groups or elements
        Return: A `dict` with the result of the chemical formula
        """
        self.result = {}  
        self._fuse_and_dictify(args)
      
        return self.result 
           
    def _fuse_and_dictify(self,element_or_groups):
        """ 
            This method fuse and dictify all the elements and group of elements
            Elements are list [element:number of atoms] and groups are list a of elements
        """ 
        for element in element_or_groups:
            if isinstance(element[0], list):
                self._fuse_and_dictify(element)
            else:  
                self.result[element[0]] = self.result[element[0]] + element[1] if element[0] in self.result else int(element[1])
  

    
    def group(self,*args):
        """ 
            This method process groups of elements by multiply each atoms by the coefficient outside the brackets
            where `args` could be groups or elements , the last argument is the coefficient
            return a list of elements multiplied by the coefficent
        """ 
        result_elements = []
        
        # The last argument is the coefficient, if the coefficient is not provided we set it to one
        if isinstance(args[-1],Tree):
            coeff = int(args[-1].children[0].value)
            self.__multiply(args[0:-1],result_elements,coeff)
        else :
            coeff = 1
            self.__multiply(args,result_elements,coeff)
 
        

        return result_elements
    
    def __multiply(self,groups_or_elements,processed_elements,coeff):
        """ 
            This method multiply each atoms by the coefficient outside the brackets
            where `groups_or_elements` could be groups or elements,
            `processed_elements` processed elements and `coeff` the coefficient to multiply
            Return a list of elements multiplied by the coefficient
        """ 
        for arg in groups_or_elements:
            if isinstance(arg[0], list):
                arg,processed_elements = self.__multiply(arg,processed_elements,coeff)
            else : 
                arg[1]= arg[1] * coeff
                processed_elements.append(arg)
        return groups_or_elements,processed_elements
        
    def element(self, *args):
        """ 
            This method process elements
            where `args` are the element for the first argument, the second one are the number of atoms
            return a list [element:number of atoms]
        """ 
        element = args[0].value

        if len(args) > 1 and len(args[1].children) > 0:
            nb_atoms = int(args[1].children[0].value)
        else :
            nb_atoms = 1
            
        return [element,nb_atoms]

# Initialize the Lark Parser
chemical_formula_parser = Lark(chemical_grammar, parser='lalr', transformer=ChemicalFormulaTree())
chemical_formula_calc = chemical_formula_parser.parse


def parse_molecule(formula):
    """ 
        This method parse chemical formula
        where `formula` a given chemical formula represented by a string
        return a dict which count the number of atoms of each element 
    """ 
    return chemical_formula_calc(formula)
