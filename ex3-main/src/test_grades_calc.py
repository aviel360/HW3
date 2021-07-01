import io
import string
import random
from unittest import mock

import pytest
from hypothesis import given, example, strategies as st


from gradesCalc import final_grade, check_strings


"""
Stand-alone insructions:
0. Open a shell in the directory where `gradesCalc.py` is located (in this repository, it means `/src`)
1. Download this file
    - On Windows (PowerShell): `(New-Object System.Net.WebClient).DownloadFile("https://gitlab.com/intro-to-inline-and-void-pointers-public/ex3/-/raw/main/src/test_grades_calc.py", "test_grades_calc.py")
    - On Linux, macOS, WSL or any other Unix-like shell: `wget https://gitlab.com/intro-to-inline-and-void-pointers-public/ex3/-/raw/main/src/test_grades_calc.py`
2. Install `pytest` and `hypothesis`: `pip3.4 install --user pytest hypothesis`
3. Run the tests: `pytest`

Extra:
* Install `pdbpp` and `ipython`: `pip3.4 install --user ipython pdbpp`

Documentation links are in the readme: https://gitlab.com/intro-to-inline-and-void-pointers-public/ex3/-/blob/main/README.md
"""


@pytest.mark.parametrize(
    ("expected", "s1", "s2"),
    (
            (True, "aabbcc", "abcabc"),
            (True, "caba", "abcabc"),
            (False, "aaa", "abcabc"),
            (True, "naanb", "baNaNa"),
            (False, "ananas", "baNaNa"),
            (False, "bannn", "baNaNa"),

            # Meron and Shira's
            (True, "aabbcc", "abcabc"),
            (True, "caba", "abcabc"),
            (False, "aaa", "abcabc"),
            (False, "ananas", "baNaNa"),
            (False, "bannn", "baNaNa"),
            (True, "", ""),
            (False, "a", ""),
            (True, "", "a"),
            (True, "Sarah", "Haras"),
            (True, "St", "sttt"),
            (False, "sttt", "st"),
            (True, "\na", "/\//asd\n"),
    )
)
def test_check_strings(expected, s1, s2):
    assert check_strings(s1, s2) is expected


@given(st.text(alphabet=string.ascii_letters))
@example("")
def test_check_strings_same_value(text):
    assert check_strings(text, text)


@given(st.integers(min_value=0, max_value=100), st.text(alphabet=string.ascii_letters))
def test_check_strings_some_removed_letters_reversed(count, text):
    substring = "".join(random.sample(text, count * len(text) // 100))
    assert check_strings(substring, text)


@given(st.integers(min_value=0, max_value=100), st.text(alphabet=string.ascii_letters))
def test_check_strings_some_removed_letters(count, text):
    substring = "".join(random.sample(text, count * len(text) // 100))
    assert not check_strings(text, substring) or len(substring) == len(text)


class UnclosableStringIO(io.StringIO):
    def close(self) -> None:
        # do not close the fake file to allow inspection after close
        pass


@pytest.mark.parametrize(
    ("expected_result", "raw_input", "expected_output"),
    (
            (60, "39401830,  Zeev Jabotinsky, 2 ,     78\n29441133 ,Joseph Trumpeldor,     1 , 99", "29441133, 99, 66\n39401830, 78, 54\n"),
            (0, "", ""),
    )
)
def test_final_grade(expected_result, raw_input, expected_output):
    input_file = UnclosableStringIO(raw_input)
    output_file = UnclosableStringIO()

    def patched_open(path: str, mode: str):
        return {"input": input_file, "output": output_file}[path]

    with mock.patch("builtins.open", patched_open):
        result = final_grade("input", "output")
    assert output_file.getvalue() == expected_output
    assert result == expected_result


def ms_path(name: str) -> str:
    """
    Returns a path to a resource from Meron and Shira's tests.
    """
    return "src/tests/Meron_and_Shira/" + name


@pytest.mark.parametrize(
    ("expected_result", "input_path", "expected_output_path"),
    (
            (70, "src/tests/input", "src/tests/out"),

            # Meron and Shira's
            (0, ms_path("input0"), ms_path("expected_out0")),
            (64, ms_path("input1"), ms_path("expected_out1")),
            (61, ms_path("input2"), ms_path("expected_out2")),
            (88, ms_path("input3"), ms_path("expected_out3")),
            (65, ms_path("input4"), ms_path("expected_out4")),
            (68, ms_path("input5"), ms_path("expected_out5")),
    )
)
def test_final_grade(expected_result, input_path, expected_output_path):
    output_file = UnclosableStringIO()

    # avoid infinite patching recursion
    original_open = open

    def patched_open(path: str, mode: str):
        return {"input": original_open(input_path), "output": output_file}[path]

    with mock.patch("builtins.open", patched_open):
        result =  final_grade("input", "output")
    with open(expected_output_path, "r") as expected_output:
        assert output_file.getvalue() == expected_output.read()
    assert result == expected_result
