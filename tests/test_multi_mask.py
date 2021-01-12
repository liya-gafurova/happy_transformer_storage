from happytransformer import HappyBERT
from tests.error import get_error

happy = HappyBERT()

def test_multi_mask():
    # should give something like
    # "I have a great dog and I love him so much"
    all_predictions = happy.predict_masks(
        "[MASK] have a [MASK] dog and I love [MASK] so much",
        num_results=2
    )
    assert len(all_predictions) == 3
    assert all(
        len(specific_predictions) == 2
        for specific_predictions in all_predictions
    )
    assert all_predictions[0][0]["word"] == 'i'
    assert all_predictions[0][0]["softmax"] > 0.5

    assert all_predictions[2][0]["word"] == 'him'

def test_multi_mask_options():
    MASKS_OPTIONS = [
        ['I', 'You'],
        ['big', 'small'],
        ['him', 'her']
    ]
    options_set = set(
        option
        for mask in MASKS_OPTIONS
        for option in mask
    )
    all_predictions = happy.predict_masks(
        "[MASK] have a [MASK] dog and I love [MASK] so much",
        options=MASKS_OPTIONS
    )
    assert len(all_predictions) == 3
    assert all(
        prediction["word"] in options_set
        for mask_predictions in all_predictions
        for prediction in mask_predictions
    )

def test_predict_no_mask_tokens_errors():
    error = get_error(
        lambda: happy.predict_masks('There is no mask token in here')
    )
    assert type(error) is ValueError

def test_predict_with_cls_errors():
    error = get_error(
        lambda: happy.predict_masks('There is a [CLS] token in here')
    )
    assert type(error) is ValueError

def test_predict_with_sep_errors():
    error = get_error(
        lambda: happy.predict_masks('There is a [SEP] token in here')
    )
    assert type(error) is ValueError