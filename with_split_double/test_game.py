from game import *
from q_learner import QLearner
from deck import Deck
from card import Card
from player import Player
from unittest.mock import Mock, patch
import pytest

def test_perform_hit():
    hand = QLearner()
    deck = Deck()

    assert len(hand._hand) == 0
    assert hand._can_double 
    perform_hit(hand, deck)
    assert len(hand._hand) == 1
    assert not hand._can_double 
    perform_hit(hand, deck)
    assert len(hand._hand) == 2
    assert not hand._can_double 
    perform_hit(hand, deck)
    assert len(hand._hand) == 3

def test_perform_hit():
    hand = QLearner()
    deck = Deck()

    assert len(hand._hand) == 0
    assert hand._can_double 
    perform_hit(hand, deck)
    assert len(hand._hand) == 1
    assert not hand._can_double 
    perform_hit(hand, deck)
    assert len(hand._hand) == 2
    assert not hand._can_double 
    perform_hit(hand, deck)
    assert len(hand._hand) == 3
    
def test_perform_stay():
    hand = QLearner()
    staying_hands = []

    perform_stay(hand, staying_hands)
    assert len(hand._hand) == 0
    assert staying_hands == [hand]
    assert not hand._can_double

def test_perform_split(): 
    with patch.object(QLearner, 'update') as mock_update:
        hand = QLearner()
        hand._hand.append(Card()) 
        hand._hand.append(Card())
        staying_hands = []
        hands = []
        deck = Deck()
        game = Game(1)
        get_state = game.get_state
        good_orig = [Card(), Card()]
        dealer = Dealer()
        dealer.hit(deck)
        dealer.hit(deck)
        hand._last_state = (4, 4)

        perform_split(hand, staying_hands, hands, deck, get_state, good_orig, dealer)

        #check both hands added to hands
        assert len(staying_hands) == 2

        #check both hands contain split original hand
        assert(staying_hands[0]._hand[0].get_value() == 1)
        assert(staying_hands[1]._hand[0].get_value() == 1)
        
        # check both hands have been hit
        assert(len(staying_hands[1].get_hand())) == 2
        assert(len(staying_hands[0].get_hand())) == 2

        #check both hands can double after splitting
        assert staying_hands[0]._can_double
        assert staying_hands[1]._can_double

        #assert error occurs when hand is not a pair

def test_fail_perform_split():
    hand = QLearner()
    hand._hand.append(Card()) 
    hand._hand.append(Card())
    
    hands = []
    staying_hands = []
    deck = Deck()
    game = Game(1)
    get_state = game.get_state
    bad_orig = [Card(), Card(2, "2", "Spades")]
    dealer = Dealer()
    dealer.hit(deck)
    dealer.hit(deck)
    hand._last_state = (4, 4)

    with pytest.raises(AssertionError):
        perform_split(hand, staying_hands, hands, deck, get_state, bad_orig, dealer)

def test_perform_double():
    hand = QLearner()
    deck = Deck()

    perform_double(hand, deck)
    assert len(hand._hand) == 1
    assert not hand._can_double
    assert hand._has_doubled

def test_get_state():
    hand = QLearner()
    hand._hand.append(Card(2, "2", "Spades")) 
    hand._hand.append(Card(2, "2", "Spades"))

    dealer = Dealer()
    dealer._hand.append(Card()) 
    game = Game(1)

    # check for pairs
    state = game.get_state(hand, dealer)
    assert state == ('2,2', 1)
    
    # check for non-pair
    hand._hand = [Card(2, "2", "Spades"), Card(3, "3", "Spades")]
    hand._total_hand_val = 5
    state = game.get_state(hand, dealer)
    assert state == (5, 1)

def test_determine_winner():
    game = Game(1)
    player = QLearner()
    player._total_hand_val = 21
    dealer = Dealer()
    dealer._total_hand_val = 20
    assert game.determine_winner(player, dealer) == Constants.player1
    
    player._total_hand_val = 19
    assert game.determine_winner(player, dealer) == Constants.player2

    player._total_hand_val = 20
    assert game.determine_winner(player, dealer) == None

def test_is_bust():
    player = QLearner()
    player._total_hand_val = 22
    game = Game(1)

    assert game.is_bust(player) 
    
    player._total_hand_val = 21
    assert not game.is_bust(player)