import pytest
from player import Player
from dealer import Dealer
from deck import Deck
from card import Card
from constants import *

def test_hit_with_actual_deck():
    deck = Deck()
    player = Player()

    player.hit(deck)
    assert len(player.get_hand()) == 1
    assert len(deck._cards) == 51
    assert player.get_hand_value() > 0

def test_hit_with_multiple_cards_from_deck():
    deck = Deck()
    player = Player()

    player.hit(deck)
    player.hit(deck)

    assert len(player.get_hand()) == 2
    assert len(deck._cards) == 50
    assert player.get_hand_value() > 0

def test_hand_value_with_aces_from_deck():
    deck = Deck()
    player = Player()

    deck._cards = [Card(1, "Ace", "Spades"), Card(1, "Ace", "Hearts")] 
    player.hit(deck)
    player.hit(deck)

    assert len(player.get_hand()) == 2
    assert player.get_hand_value() == 12

def test_reset_hand_with_actual_deck():
    deck = Deck()
    player = Player()

    player.hit(deck)
    player.hit(deck)
    assert len(player.get_hand()) == 2

    player.reset_hand()
    assert len(player.get_hand()) == 0
    assert player.get_hand_value() == 0

def test_dealer_initial_state():
    dealer = Dealer()
    assert dealer.get_hand() == ()
    assert dealer.get_hand_value() == 0

def test_dealer_get_original_showing_value():
    dealer = Dealer()
    deck = Deck()
    
    dealer.hit(deck)
    dealer.hit(deck)
    
    assert len(dealer.get_hand()) == 2
    assert dealer.get_original_showing_value() == dealer.get_hand()[0].get_value()

def test_dealer_get_action_hit():
    dealer = Dealer()
    deck = Deck()
    
    dealer.hit(deck)
    dealer.hit(deck)
    dealer._total_hand_val = 16  

    assert dealer.get_action() == Constants.hit

def test_dealer_get_action_stay():
    dealer = Dealer()
    deck = Deck()
    
    dealer.hit(deck)
    dealer.hit(deck)
    dealer._total_hand_val = 17  

    assert dealer.get_action() == Constants.stay

def test_dealer_integration_with_deck():
    dealer = Dealer()
    deck = Deck()
    
    dealer.hit(deck)
    dealer.hit(deck)
    assert len(dealer.get_hand()) == 2
    assert len(deck._cards) == 50
    assert dealer.get_hand_value() > 0
    