import random
import cards_players
import tkinter as tk


class Deck:
    #constructor
    #initializes 52 cards in the deck in use and player Dealer
    def __init__(self, master):
        self.cards_in_deck = []
        self.players = []
        self.CPU_dealer = cards_players.Players('Dealer')
        self.master = master
        self.num_players = 0

        self.master.minsize(width=1000, height=760)
        self.master.maxsize(width=1000, height=760)

        rank_count = 2
        suit_count = 1
        for i in range(52):
            if rank_count > 14:
                rank_count = 2
                suit_count += 1

            x = cards_players.Cards(suit_count, rank_count)
            self.cards_in_deck.append(x)

            rank_count += 1

    #greets players and gets information about player number
    #calls start_set_player() when player selects an option
    def setup_game(self):

        greet_screen = tk.Frame(self.master)
        greet_screen.pack()

        greetings = tk.Label(greet_screen, text = "Welcome to Blackjack!")
        greetings.pack(anchor="center", pady=(50,0))

        tk.Label(greet_screen, text = "How many players?").pack(pady=(253,0), anchor="center")

        player_count = tk.IntVar()
        tk.Radiobutton(greet_screen, text="1", variable=player_count, value=1).pack(anchor="w")
        tk.Radiobutton(greet_screen, text="2", variable=player_count, value=2).pack(anchor="w")
        
        tk.Button(greet_screen, text="OK!", command=lambda: self.start_set_player(greet_screen, player_count)).pack()
        

    #gets player names from user(s)
    #call end_set_player() when finished
    def start_set_player(self, greet_screen, player_count):
        greet_screen.destroy()
        self.num_players = player_count.get()

        set_player = tk.Frame(self.master)
        set_player.pack()
        e = []
        labels = []

        for i in range(self.num_players):
            labels.append( tk.Label(set_player, text="Player {} Name: ".format(i+1)) )
            e.append( tk.Entry(set_player) )

        labels[0].pack(pady=(253,0))
        e[0].pack()
        if self.num_players == 2:
            labels[1].pack()
            e[1].pack()

        tk.Button(set_player, text="OK!", command=lambda: self.end_set_player(set_player, e)).pack()


    #intializes vector of Player objects with user inputted names from start_set_player()
    #calls begin_game() when finished
    def end_set_player(self, set_player, e):
        for i in range(self.num_players):
            new_player = cards_players.Players(e[i].get())
            self.players.append(new_player)
        set_player.destroy()
        self.play_round(1)

    #calls play_round() to play one round, passing in 1 to indicate its player 1's turn
    #after the a round is finished it resets player hands and asks if user will keep playing
    #if player chooses to quit, end_game()
    #if player chooses to continue playing, begin_game() calls itself
    def end_game(self):
        keep_playing_frame = tk.Frame(self.master)
        keep_playing_frame.pack()
        #empty hands
        for i in range(self.num_players):
            self.CPU_dealer.hand = []
            self.players[i].hand = []
            
        keep_playing = tk.Label(keep_playing_frame,text="Play another round?")
        keep_playing.pack()
        tk.Button(keep_playing_frame, text="Play Again", command=lambda: self.play_round(1)).pack()
        tk.Button(keep_playing_frame, text="Quit", command=self.end_game2).pack()
        
    #ends game and displays scores
    def end_game2(self):
        #display score

        end_game_frame = tk.Frame(self.master)
        end_game_frame.grid()


        tk.Label(text="Thanks for playing!").pack()
        tk.Label(text="Final score: ").pack()
        tk.Label(text="Dealer:").pack()
        tk.Label(text="Wins: {}".format(self.CPU_dealer.wins) ).pack()
        tk.Label(text="Losses: {}".format(self.CPU_dealer.losses) ).pack()

        for i in range(int(player_count)):
            print("Player {}:".format(i+1) )
            print("Wins: {}".format(self.players[i].wins) )
            print("Losses: {}".format(self.players[i].losses) )
            print("")
    

    #begins to play one round
    #for a two player game, if turn == 1 it is player 1's turn
    #if turn == 2 it is player 2's turn
    def play_round(self, turn):

        self.dealer_cards_frame = tk.Frame(self.master)
        self.dealer_cards_frame.pack()

        self.player1_cards_frame = tk.Frame(self.master)
        self.player1_cards_frame.pack()

        self.buttons1_frame = tk.Frame(self.master)
        self.buttons1_frame.pack()

        canvas_height = 350

        if self.num_players == 2:
            self.player2_cards_frame = tk.Frame(self.master)
            self.player2_cards_frame.pack()
            
            self.buttons2_frame = tk.Frame(self.master)
            self.buttons2_frame.pack(side="bottom")

            canvas_height = 180
        
        
        #draw cards
        for i in range(2):
            self.CPU_dealer.hand.append(self.draw_card())

        for i in range(self.num_players):
            self.players[i].hand.append(self.draw_card())
            self.players[i].hand.append(self.draw_card())
        
        #show dealer cards
        #only one card is face up
        dealer_label = tk.Label(self.dealer_cards_frame, text="Dealer's cards:")
        dealer_label.pack(anchor="w", pady=(10,0))

        dealer_card_canvas = tk.Canvas(self.dealer_cards_frame, width="1000", height=canvas_height)
        dealer_card_canvas.pack()

        #returns rectangle that begins top left corner at (25, 25) and ends bottom right at (150,220)
        dealer_card_1 = self.CPU_dealer.hand[0].PrintCard(dealer_card_canvas,25,25)

        #30 pixels in between dealer_card_1 and hidden card
        #begins top left corner at (190, 25) and ends bottom right at (315, 220)
        dealer_card_hidden = dealer_card_canvas.create_rectangle(180, 25, 180+100, 25+150, fill="blue")

        #show player 1 cards
        player1_label = tk.Label(self.player1_cards_frame, text="{}'s cards: ".format(self.players[0].name))
        player1_label.pack(side="top",anchor="w")
            
        self.player1_card_canvas = tk.Canvas(self.player1_cards_frame, width="1000", height=canvas_height)
        self.player1_card_canvas.pack(side="top")

        player1_card_recs = []
        xoffset = 0
        for i, j in enumerate(self.players[0].hand):
            player1_card_recs.append( j.PrintCard(self.player1_card_canvas,25+xoffset, 25) )
                # width of a card (125) + number of pixels between cards (20)
            xoffset += 155

        if self.num_players == 2:

            player2_label = tk.Label(self.player2_cards_frame, text="{}'s cards: ".format(self.players[1].name))
            player2_label.pack(anchor="w")
            
            self.player2_card_canvas = tk.Canvas(self.player2_cards_frame, width="1000", height=canvas_height)
            self.player2_card_canvas.pack()

            player2_card_recs = []
            xoffset = 0
            for i, j in enumerate(self.players[1].hand):
                player2_card_recs.append( j.PrintCard(self.player2_card_canvas,25+xoffset, 25) )
                # width of a card (125) + number of pixels between cards (20)
                xoffset += 155
        
            self.take_turn(1)
        else:
            self.take_turn()

    #if one player
    def take_turn(self):
        #ask player for hit or stand
        tk.Label(self.buttons1_frame, text="{}'s turn.".format(self.players[0].name)).pack()
        stand_button = tk.Button(self.buttons1_frame, text="Stand", command=lambda: play_round2(1))
        stand_button.pack()
        hit_button = tk.Button(self.buttons1_frame, text="Hit", command=lambda: self.hit(1))
        hit_button.pack()


    #if 2 players
    def take_turn(self, turn):
        #check if dealer has blackjack
        total = self.total_cards(self.CPU_dealer.hand)
        if total == 21:
            self.dealer_blackjack()
            return

        if turn == 1:

            #ask player for hit or stand
            tk.Label(self.buttons1_frame, text="{}'s turn:".format(self.players[turn].name)).pack(anchor = "w")
            stand_button = tk.Button(self.buttons1_frame, text="Stand", command=lambda: self.take_turn(turn+1))
            stand_button.pack(side="right")
            hit_button = tk.Button(self.buttons1_frame, text="Hit", command=lambda: self.hit(turn))
            hit_button.pack(side="left")

            waitlabel = tk.Label(self.buttons2_frame, text="[WAITING]")
            waitlabel.pack(pady=(0,50))


        if turn == 2:

            waitlabel = tk.Label(self.buttons1_frame, text="[WAITING]")
            waitlabel.pack()

            tk.Label(self.buttons2_frame, text="{}'s turn.".format(self.players[turn-1].name)).pack()
            stand_button = tk.Button(self.buttons2_frame, text="Stand", command=self.end_turn)
            stand_button.pack(side="right")
            hit_button = tk.Button(self.buttons2_frame, text="Hit", command=lambda: self.hit(buttons2_frame, turn) )
            hit_button.pack(side="left")



    def play_round2(turn):


        print("")
        #stand
        total = self.total_cards(self.players[i-1].hand)

        if total > 21:
            print("Bust!")
            self.players[i].losses += 1
                
        elif total == 21:
            #blackjack
            print("Player {} has Blackjack!".format(i+1) )
            self.players[i].wins += 1

        else:
            total = self.total_cards(self.players[i].hand)
            dealer_total = self.total_cards(self.CPU_dealer.hand)
            print("Player {}'s hand adds up to {}.".format(i+1, total) )
            print("The dealer's hand adds up to {}.".format(dealer_total) )
            if dealer_total < total:
                print("Player {} wins!".format(i+1) )
                self.players[i].wins += 1
            elif dealer_total > total:
                print("The dealer wins!")
                self.CPU_dealer.wins += 1
            else:
                print("It's a tie!")
                self.players[i].wins += 1
                self.CPU_dealer.wins += 1
            print("")
            

    # def end_round(self):
    #     dealer_cards_frame.destroy()
    #     player1_cards_frame.destroy()
    #     buttons1_frame.destroy()
    #     if self.num_players == 2:
    #         player2_cards_frame.destroy()
    #         buttons2_frame.destroy()
        
    
    def dealer_blackjack(self):
        print("The dealer has Blackjack!")

        print("Dealer's cards: ")
        #for j in self.CPU_dealer.hand:
            #j.PrintCard()
        player_win = 0
        winning_player = []
        #check if any players also have blackjack. if not, end the round
        for i in range(self.num_players):
            total = self.total_cards(self.players[i].hand)
            if total == 21:
                print("Player {} also has Blackjack!".format(i+1) )
                player_win += 1
                winning_player.append(i)
            else:
                print("Player {} loses their bet.".format(i+1) )

            if player_win == 0:
                self.CPU_dealer.wins += 1

            elif player_win == 1:
                print("Player {} and the dealer have tied.".format(player[winning_player]) )
            else:
                print("All players and the dealer have tied.")

            print("")


#####
# utility functions 
#####

    #total the values of a player's hand
    def total_cards(self, hand):
        total = 0
        ace_count = 0
        for i in hand:
            #if ace, do not increment total but increment count of aces in hand
            if i.rank == 11:
                ace_count += 1
            #kings, queens, and jacks are all valued at 10
            elif i.rank > 11:
                total += 10
            else:
                total += i.rank

        if ace_count > 0:
            for j in range(ace_count):
                if (total + 11) <= 21:
                    total += 11
                else:
                    total += 1
        return total

    #returns a random card out of the cards_in_deck
    #if card is not marked as in the deck in play, another index is generated
    def draw_card(self):
        random.seed(a=None, version=2)
        condition = False
        while (not condition):
            i = random.randrange(52)
            condition = self.cards_in_deck[i].in_deck
        self.cards_in_deck[i].in_deck = False
        return self.cards_in_deck[i]

    #print suit and rank of entire deck
    def print_deck(self):
        for i in range(52):
            self.cards_in_deck[i].PrintCard()


    #logic for if a player chooses a hit
    #draw a card and add it to player's hand
    #allow player to continue choosing to hit until player busts
    def hit(self,turn):
        xoffset = 155*len(self.players[turn-1].hand)
        self.players[turn-1].hand.append(self.draw_card())
        total = self.total_cards(self.players[turn-1].hand)
            
        #print new card
        if turn == 1:
            self.players[0].hand[-1].PrintCard(self.player1_card_canvas,25+xoffset, 25)
        else:
            self.players[1].hand[-1].PrintCard(self.player2_card_canvas,25+xoffset, 25)

        #stop player from choosing to take another hit if player busts or has blackjack
        if total > 21:
            return
        elif total == 21:
            return

        else:
            stand_button.forget_pack()
            hit_button.forget_pack()
            if turn == 1:
                stand_button = tk.Button(self.buttons1_frame, text="Stand", command=lambda: self.take_turn(turn+1))
                stand_button.pack(side="right")
                hit_button = tk.Button(self.buttons1_frame, text="Hit", command=lambda: self.hit(turn))
                hit_button.pack(side="left")
            else:
                stand_button = tk.Button(self.buttons2_frame, text="Stand", command=lambda: self.end_turn)
                stand_button.pack(side="right")
                hit_button = tk.Button(self.buttons2_frame, text="Hit", command=lambda: self.hit(turn))
                hit_button.pack(side="left")

def main():
    root = tk.Tk()

    obj = Deck(root)
    #obj.print_deck()
    obj.setup_game()


    root.mainloop() 

if __name__ == "__main__":
    main()