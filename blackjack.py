from random import shuffle
import time


class Table:

    def __init__(self, table_number, num_decks=1):
        self.table_num = table_number
        self.num_of_decks = num_decks
        self.list_of_suits = ['S','H','C','D']
        self.list_of_pips = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        self.deck = [(i, j, k) for i in range(0,self.num_of_decks) for j in self.list_of_suits for k in self.list_of_pips]
        self.next_card_index = 0
        self.players = []
        self.num_of_players = len(self.players)
        self.dealer_cards = []
        self.dealer_cards_sp = []
        self.num_of_dealer_cards = 0
        self.sum_of_dealer_cards = 0
        self.num_of_dealer_aces = 0
        self.dealer_has_to_play = False
        self.dealer_turn_decision = ''
    
    def __str__(self):
        return f'Table: {self.table_num}; {self.num_of_players} players\nPlayers: {self.players}\nDeck:{self.deck}\n{self.num_of_dealer_cards} dealer cards; sum: {self.sum_of_dealer_cards}; includes {self.num_of_dealer_aces} Aces\nDealer cards: {self.dealer_cards}\nDealer decision: {self.dealer_turn_decision};  dealer has to play: {str(self.dealer_has_to_play)}\n'
    
    def shuffle_deck(self):
        shuffle(self.deck)
    
    def add_player(self,player,index=0):
        self.players.insert(index,player)
        self.num_of_players = len(self.players)
        player.table_id = self.table_num
        
    def remove_player(self,player):
        self.players.remove(player)
        self.num_of_players = len(self.players)
    
    
class Player:
    def __init__(self,player_id):
        self.player_id = player_id
        self.friendly_name = ''
        self.funds = 0
        self.game_bet = 0
        self.game_winnings = 0
        # status must be one of 'watching', 'at_table', 'waiting_to_play', 'in_play', 'stand' or 'bust'
        self.status = 'watching'
        self.table_id = 0
        self.cards = []
        self.num_of_cards = 0
        self.sum_of_cards = 0
        self.num_of_aces = 0
        # turn_decision must be one of 'stand', 'hit' or ''
        self.turn_decision = ''
    
    def __str__(self):
        return f"\nPlayer: {self.player_id} ({self.friendly_name}) Table: {self.table_id}\nAvailable funds: {self.funds}\nCurrent bet: {self.game_bet}\nNumber of cards: {self.num_of_cards}\nSum of cards: {self.sum_of_cards}\nNumber of Aces: {self.num_of_aces}\nCards held: {self.cards}\nPlayer\'s Turn Decision: {self.turn_decision}\n\n"
    
    def set_friendly_name(self,nickname):
        self.friendly_name = nickname
        
    def set_funds(self,value):
        self.funds = value
    
    def add_funds(self,value):
        self.funds += value
        
    def withdraw_funds(self,value):
        self.funds -= value
        
    def set_status(self,status):
        self.status = status
        
    def remove_cards(self):
        self.cards = []
        self.num_of_cards = 0
        self.sum_of_cards = 0
        self.num_of_aces = 0
    
    def add_card(self,card):
        self.cards.append(card)
        self.num_of_cards += 1
        deck,suit,value = card
        if value=='J' or value=='Q' or value=='K':
            self.sum_of_cards += 10
        elif value=='A':
            self.sum_of_cards += 11
            self.num_of_aces += 1
        else:
            self.sum_of_cards += int(value)
    
    
 
if __name__ == '__main__':
    table1 = Table(1,1)
    (_,_,_,_,_,tm_sec,_,_,_)=time.localtime()
    for _ in range(0,(tm_sec%10)+10):
        table1.shuffle_deck()
    
    player1=Player(1)
    player1.set_friendly_name('Player1')
    player1.set_funds(100)
    #print(player1)

    table1.add_player(player1,table1.num_of_players)
    #print(table1)

    #'''
    player2=Player(2)
    player2.set_friendly_name('Player2')
    player2.set_funds(100)
    #print(player2)

    table1.add_player(player2,table1.num_of_players)
    #print(table1)
    #'''
    player3=Player(3)
    player3.set_friendly_name('Player3')
    player3.set_funds(100)
    #print(player1)

    table1.add_player(player3,table1.num_of_players)
    #print(table1)
    #'''
    while True:
    
        # Place bets
        print('\n\nPlace your bets!')
        for player in table1.players:
            player.game_bet=0
            announce = player.friendly_name+', you have '+str(player.funds)+' available; what is your bet? :'
            while player.game_bet <= 0 or player.game_bet>player.funds:
                player.game_bet=int(input(announce))
            player.funds -= player.game_bet
        print ('\n\n')  
        
        # Deal to all players and then the dealer
        for dealer_round in [1,2]:
            for player in table1.players:
                (pack,suit,pips)=table1.deck[table1.next_card_index]
                player.cards += [(pack,suit,pips)]
                player.num_of_cards += 1
                try:
                    int_pips=int(pips)
                except:
                    if pips=='A':
                        int_pips=11
                        player.num_of_aces += 1
                    else:
                        int_pips=10
                finally:
                    player.sum_of_cards += int_pips
                table1.next_card_index += 1
                #print(player)
            (pack,suit,pips)=table1.deck[table1.next_card_index]
            table1.dealer_cards += [(pack,suit,pips)]
            table1.num_of_dealer_cards += 1
            try:
                int_pips=int(pips)
            except:
                if pips=='A':
                    int_pips=11
                    table1.num_of_dealer_aces += 1
                else:
                    int_pips=10
            finally:
                table1.sum_of_dealer_cards += int_pips
            table1.next_card_index += 1
        #print(table1)
        
        # Game On !!
        # For loop, from 1 to n for each player
        dealer_cards_sp = table1.dealer_cards[0][1]+table1.dealer_cards[0][2]+' and '
        if table1.num_of_dealer_cards == 2 and table1.sum_of_dealer_cards == 21:
            # Dealer has Blackjack
            dealer_cards_sp += table1.dealer_cards[1][1]+table1.dealer_cards[1][2]+' - BLACKJACK !'
            table1.dealer_turn_decision = 'Blackjack'
        else:
            dealer_cards_sp += '?'
        #print (f'Dealer\'s cards: {dealer_cards_sp}')
            
        if table1.dealer_turn_decision != 'Blackjack':
            #print('Dealer doesn\'t have blackjack - game continues\n')
            pass
        

        for player in table1.players:
            player_cards_sp = player.cards[0][1]+player.cards[0][2]+', '+player.cards[1][1]+player.cards[1][2]
            # does player have blackjack?
            if player.num_of_cards == 2 and player.sum_of_cards == 21:
                player.turn_decision = 'Blackjack'

            # if dealer has blackjack and player has blackjack -> draw; bet returned; break
            if table1.dealer_turn_decision == 'Blackjack' and player.turn_decision == 'Blackjack':
                print (f'Dealer\'s cards: {dealer_cards_sp}')
                print (f'{player.friendly_name}\'s cards: {player_cards_sp}')
                player.funds += player.game_bet
                print ('You both had Blackjack - your bet has been returned.  Your fund is: {player.funds}\n\n')
                break

            # if dealer has blackjack and player doesn't have blackjack -> show dealer's cards / blackjack; player lost; break
            if table1.dealer_turn_decision == 'Blackjack' and player.turn_decision != 'Blackjack':
                print (f'Dealer had Blackjack: {dealer_cards_sp}')
                print (f'{player.friendly_name}\'s cards: {player_cards_sp}')
                print ('You lost your bet.  Your fund is: {player.funds}\n\n')
                break

            # if dealer doesn't have blackjack
            print (f'Dealer\'s cards: {dealer_cards_sp}')
            if player.turn_decision == 'Blackjack':
                player.game_winnings = 1.5*player.game_bet
                player.funds += player.game_bet + player.game_winnings
                print(f'Congratulations, you had Blackjack! Collect your bet of '+str(player.game_bet)+' and winnings of '+str(player.game_winnings)+'\n'+'Your Fund is now '+str(player.funds)+'\n\n')
                break

            player_decision = 'H'
            while player_decision=='H' or player_decision=='':
                print (f'{player.friendly_name}\'s cards: {player_cards_sp}')
                if player.num_of_cards > 2 and player.sum_of_cards > (21+(player.num_of_aces*10)):
                    # Bust
                    print (f'Bust !  You lost your bet.  Your fund is: {player.funds}\n\n')
                    player.turn_decision = 'Bust'
                    break
                if player.num_of_cards == 2:
                    input_prompt = '[H]it, [S]tand or S[u]rrender?'
                    input_allowed = ['H','S','U','']
                else:
                    input_prompt = '[H]it or [S]tand?'
                    input_allowed = ['H','S','']
                player_decision = input(input_prompt).upper()
                while player_decision not in input_allowed:
                    player_decision = input(input_prompt).upper()
                if player_decision == 'U':
                    player.funds += (player.game_bet*0.5)
                    print (f'You\'ve surrendered. You lost half your bet.  Your fund is: {player.funds}\n\n')
                    player.turn_decision = 'Surrender'
                    break
                elif player_decision=='S':
                    player.turn_decision = 'Stand'
                    print ('You\'re standing. We\'ll see if you\'ve won after the dealer\'s turn\n\n')                    
                    table1.dealer_has_to_play = True
                else:
                    # Hit
                    (pack,suit,pips)=table1.deck[table1.next_card_index]
                    player.cards += [(pack,suit,pips)]
                    player.num_of_cards += 1
                    try:
                        int_pips=int(pips)
                    except:
                        if pips=='A':
                            int_pips=11
                            player.num_of_aces += 1
                        else:
                            int_pips=10
                    finally:
                        player.sum_of_cards += int_pips
                    player_cards_sp += ', '+suit+pips
                    table1.next_card_index += 1
            #print(player)
            
        # When no more players, it's dealer's turn
        # While not stand, keep hitting and updating dealer's hand details
        #print(table1)
        while table1.dealer_has_to_play and table1.dealer_turn_decision != 'Stand' and table1.dealer_turn_decision != 'Bust':
            if 17 <= table1.sum_of_dealer_cards <= 21:
                table1.dealer_turn_decision = 'Stand'
                print(f'Dealer is standing - {table1.dealer_cards_sp}')
            else:
                # draw another card
                print('Dealer taking another card')
                (pack,suit,pips)=table1.deck[table1.next_card_index]
                table1.dealer_cards += [(pack,suit,pips)]
                table1.num_of_dealer_cards += 1
                try:
                    int_pips=int(pips)
                except:
                    if pips=='A':
                        int_pips=11
                        table1.num_of_dealer_aces += 1
                    else:
                        int_pips=10
                finally:
                    table1.sum_of_dealer_cards += int_pips
                table1.next_card_index += 1
                # check for bust
                if table1.sum_of_dealer_cards > 21:
                    # Bust
                    table1.dealer_turn_decision = 'Bust'
                    print('Dealer has bust\n')
        #print(table1)

        # Assess hands of those who Stand, determine who wins and how much
        print(f'\n\nPaying out bets... Dealer has {table1.dealer_cards}')
        for player in table1.players:
            if player.turn_decision == 'Stand':
                announce=player.friendly_name+': You\'re cards: '+str(player.cards)+'\n'
                if table1.dealer_turn_decision == 'Bust':
                    player.game_winnings = player.game_bet
                    player.funds += player.game_bet + player.game_winnings
                    announce+='The dealer bust so you Win! . Collect your bet of '+str(player.game_bet)+' and winnings of '+str(player.game_winnings)+'\n'+'Your Fund is now '+str(player.funds)+'\n\n'
                elif table1.dealer_turn_decision == 'Stand':
                    number_of_aces = player.num_of_aces
                    sum_of_players_cards = player.sum_of_cards
                    while number_of_aces > 0 and sum_of_players_cards > 21:
                        number_of_aces -= 1
                        sum_of_players_cards -= 10
                    if table1.sum_of_dealer_cards == sum_of_players_cards:
                        player.funds += player.game_bet
                        announce+='Congratulations, you had the same as the dealer so your bet is returned.\n'+'Your Fund is now '+str(player.funds)+'\n\n'
                    elif table1.sum_of_dealer_cards > sum_of_players_cards:
                        announce+='Unlucky, you had less than the dealer so your lost your bet.\n'+'Your Fund is now '+str(player.funds)+'\n\n'
                    elif table1.sum_of_dealer_cards < sum_of_players_cards:
                        player.game_winnings = player.game_bet
                        player.funds += player.game_bet + player.game_winnings
                        announce+='Congratulations, you beat the dealer so you Win! Collect your bet of '+str(player.game_bet)+' and winnings of '+str(player.game_winnings)+'\n'+'Your Fund is now '+str(player.funds)+'\n\n'
                print(announce)                        
                #print(player)
                #print('\n\n')
        
        # Play another game or leave table?
        print('Anyone for another game?')
        players_to_be_removed = []
        for player in table1.players:
            player_input = ''
            while player_input not in ['y','n']:
                player_input = input(f'{player.friendly_name}, would you like to play again (y/n)').lower()
            if player_input == 'n':
                print(f'Thanks for playing. Collect your {player.funds} and enjoy!')
                players_to_be_removed.append(player)
            else:
                player.game_bet = 0
                player.game_winnings = 0
                player.cards = []
                player.num_of_cards = 0
                player.sum_of_cards = 0
                player.num_of_aces = 0
                player.turn_decision = ''
            #print(player)
        table1.dealer_cards = []
        table1.dealer_cards_sp = []
        table1.num_of_dealer_cards = 0
        table1.sum_of_dealer_cards = 0
        table1.num_of_dealer_aces = 0
        table1.dealer_has_to_play = False
        table1.dealer_turn_decision = ''
        #print(table1)
        #print(f'Players to be removed: {players_to_be_removed}')
        for player in players_to_be_removed:
            table1.remove_player(player)
        #print(table1)

        if table1.num_of_players == 0:
            break

