import pytest


@pytest.fixture(scope="session")
def example_docs():
    return [
        "I'm not a Financial expert but Australian super are one of the bigger better options I guess",
        "Mate you get 15% tax on concessional contributions in super.\n\nSo no surprise it adds up to over 15%.",
        "Is the 'income' figure for this before or after tax?",
        "Message from Covid 19: \"don't touch your face, don't touch your super\"",
        "It would be better than having an imaginary jetski that I can't use after the lockdown",
        "Not really unless you will retire fairly soon",
        "That's some other government's problem.",
        "Sun Super all the way",
        "Message from Covid 19: \"don't touch your face, don't touch your super\"",
        "And before Asic politely reminded them they cannot provide financial advice",
        "Personal insurance and health insurance cover different things too.",
        "If you need a house, you need a house. I would suggest trying to top it back up when you can.",
        "Taxes are not fees. They are a federal government tax.",
        "No but considering moving I'm with unisuper at the moment their a closed fund",
    ]


@pytest.fixture(scope="session")
def example_doc():
    return "I'm not a Financial expert but Australian super are one of the bigger better options I guess"


@pytest.fixture(scope="session")
def super_dictionary():
    return {
        "regulation": sorted(["asic", "government", "federal", "tax"]),
        "contribution": sorted(
            [
                "contribution",
                "concession",
                "personal",
                "after tax",
                "10%",
                "10.5%",
            ]
        ),
        "covid": sorted(["covid", "lockdown", "downturn", "effect"]),
        "retirement": sorted(["retire", "house", "annuity", "age"]),
        "fund": sorted(
            [
                "unisuper",
                "aus super",
                "australian super",
                "sun super",
                "qsuper",
                "rest",
                "cbus",
            ]
        ),
    }


@pytest.fixture(scope="session")
def not_super_dictionary():
    return {
        "topically_irrelevant": sorted(["kitchen", "bathroom"]),
        "not_in_the_dataset": sorted(["ocean", "moon", "weeeeeeee"]),
    }
