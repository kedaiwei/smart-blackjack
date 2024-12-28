from deck import Deck
from card import Card

# test deck


def test_deck():
    deck = Deck()
    assert len(deck._cards) == 52
    card1 = deck.draw()
    assert len(deck._cards) == 51
    card2 = deck.draw()
    assert len(deck._cards) == 50
    assert card1 != card2

# test card


def test_card():
    QH = Card(10, "Queen", "Hearts")
    assert QH.get_rank() == "Queen"
    assert QH.get_value() == 10

    QH.set_value(5)
    assert QH.get_value() == 5
