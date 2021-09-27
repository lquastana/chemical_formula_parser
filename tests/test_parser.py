from chemical_formula_parser.parser import parse_molecule
import pytest
from lark.exceptions import UnexpectedToken

  
@pytest.mark.parametrize(
    "formula,expected_result,is_valid",[
        # Empty cases
        ('', {}, True),
        ('()', {}, True),
        ('[]', {}, True),
        # Invalid cases
        ('[', {}, False),
        (']', {}, False),
        ('(', {}, False),
        (')', {}, False),
        ('(O', {}, False),
        # Valid cases
        ('H2O', {'H': 2, 'O': 1}, True),
        ('Mg(OH)2',{'Mg': 1, 'O': 2,'H': 2}, True),
        ('K4[ON(SO3)2]2',{'K': 4, 'O': 14, 'N': 2, 'S': 4},True),
        ('K4[ON()(SO3)2]2',{'K': 4, 'O': 14, 'N': 2, 'S': 4},True),
        ('(K4)',{'K': 4},True)
        ]
)
def test_formula(formula,expected_result,is_valid):
    if not is_valid:
        with pytest.raises(UnexpectedToken):
            parse_molecule(formula)
    else:
        result = parse_molecule(formula)
        assert result == expected_result
    
    

    