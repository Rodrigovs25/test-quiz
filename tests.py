import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_add_choice_with_invalid_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)

def test_add_choice_generates_incremental_ids():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    assert choice1.id == 1
    assert choice2.id == 2

def test_remove_choice_by_id_successfully_removes_item():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_choice_by_id(1)
    
    assert len(question.choices) == 1
    assert question.choices[0].text == 'b'
    assert question.choices[0].id == 2

def test_remove_choice_by_nonexistent_id_raises_exception():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.remove_choice_by_id(99)

def test_remove_all_choices_clears_the_choices_list():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    
    assert len(question.choices) == 0

def test_set_correct_choices_updates_is_correct_attribute():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', False)
    
    question.set_correct_choices([2])
    assert not question.choices[0].is_correct
    assert question.choices[1].is_correct

def test_set_correct_choices_with_nonexistent_id_raises_exception():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.set_correct_choices([99])

def test_correct_selected_choices_returns_only_correct_ids():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', True)
    question.add_choice('b', True)
    question.add_choice('c', False)
    
    correct_ids = question.correct_selected_choices([1, 3])
    
    assert correct_ids == [1]

def test_correct_selected_choices_exceeding_max_selections_raises_exception():
    question = Question(title='q1', max_selections=1)
    question.add_choice('a', True)
    question.add_choice('b', True)
    
    with pytest.raises(Exception):
        question.correct_selected_choices([1, 2])