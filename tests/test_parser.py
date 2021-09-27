from chemical_formula_parser.parser import parse_molecule
import pytest
from lark.exceptions import UnexpectedToken

  
@pytest.mark.parametrize(
    "formula,expected_result,is_valid",[
        # Empty cases
        ('', {}, True),
        ('()', {}, True),
        ('(())', {}, True),
        ('[]', {}, True),
        ('[[]]', {}, True),
        # Invalid cases
        ('[', {}, False),
        (']', {}, False),
        ('(', {}, False),
        (')', {}, False),
        ('(O', {}, False),
        ('(O2)[', {}, False),
        # Valid cases
        ## One element
        ('H', {'H': 1}, True),
        ('Mg', {'Mg': 1}, True),
        # One element several atoms
        ('H2', {'H': 2}, True),
        ('Mg2', {'Mg': 2}, True),
        ## Several elements and several atoms
        ('MgH2', {'Mg': 1,'H': 2}, True),
        ('Mg2H2', {'Mg': 2,'H': 2}, True),
        ('OMgOMg', {'O': 2,'Mg': 2}, True),
        ('O2MgMg', {'O': 2,'Mg': 2}, True),
        ## Subgroups without coefficient
        ('(Mg)', {'Mg': 1}, True),
        ('[Mg]', {'Mg': 1}, True),
        ('(Mg)H2', {'Mg': 1,'H': 2}, True),
        ('(H2(Mg))', {'H': 2,'Mg': 1}, True),
        ('[(H2)[Mg]]', {'H': 2,'Mg': 1}, True),
        ## Subgroups with coefficient
        ('(Mg)2H2', {'Mg': 2,'H': 2}, True),
        ('(Mg)2(H)2', {'Mg': 2,'H': 2}, True),
        ('((Mg())2(H)2)3', {'Mg': 6,'H': 6}, True),
        ('(MgH)2', {'Mg': 2,'H': 2}, True),
        ('(((MgH))2)', {'Mg': 2,'H': 2}, True),
        ('[[[MgH]]2]', {'Mg': 2,'H': 2}, True),
        ('[[[MgH]]2]2', {'Mg': 4,'H': 4}, True),
        ## Formulas from test 
        ('H2O', {'H': 2, 'O': 1}, True),
        ('Mg(OH)2',{'Mg': 1, 'O': 2,'H': 2}, True),
        ('K4[ON(SO3)2]2',{'K': 4, 'O': 14, 'N': 2, 'S': 4},True),
        ]
)
def test_formula(formula,expected_result,is_valid):
    if not is_valid:
        with pytest.raises(UnexpectedToken):
            parse_molecule(formula)
    else:
        result = parse_molecule(formula)
        assert result == expected_result
    
    

    