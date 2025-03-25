from abc import ABC, abstractmethod
from copy import deepcopy
import random

class State(ABC):
    """
    Abstract base class representing the state.
    """

    def clone(self):
        """
        Returns:
            A deep copy of the state.
        """
        return deepcopy(self)
    
class Action(ABC):
    """
    Abstract base class representing an action.
    """

    def clone(self):
        """
        Returns:
            A deep copy of the action.
        """
        return deepcopy(self)    


class Observation(ABC):
    """
    Abstract base class representing an observation of a state.
    """

    def clone(self):
        """
        Returns:
            A deep copy of the observation of the state.
        """
        return deepcopy(self)

class Player(ABC):
    """
    Abstract base class for a player.

    Attributes:
        rng (random.Random): Random number generator for the player.
        name (str): The player's name.
    """

    def __init__(self, seed: int, name: str):
        """
        Initialize the player with a seed for RNG and a name.

        Args:
            seed (int): Random seed.
            name (str): The player's name.
        """
        self._rng = random.Random(seed)
        self._name = name

    @property
    def rng(self):
        return self._rng

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def get_all_actions(self, game_state) -> list[Action]:
        """
        Return all valid actions the player can take given the game state.

        Args:
            game_state: An observation or snapshot of the current game state.

        Returns:
            list: All possible actions.
        """
        pass

    @abstractmethod
    def select_action(self, state: State) -> Action:
        """
        Select one action to take from all possible actions.

        Args:
            game_state: An observation or snapshot of the current game state.

        Returns:
            An action chosen by the player.
        """
        pass

    def clone(self):
        """
        Returns:
            A deep copy of the observation of the game state.
        """
        return deepcopy(self)

class Game:
    """
    Represents a game.

    Attributes:
        players (list[Player]): A list of the players involved in the game.
        current_player (Player): THe current player.
        current_state (State): The current state.
    """
    
    def __init__(self,
                 players: list[Player],
                 initial_state: State):
        """
        Initializes the game with the given traders and market.

        Args:
            players (list[Player]): The list of players involved in the game.
            initial_state (State): The initial state of the game.
        """
        
        self.players = players
        self.current_player_idx = 0

        self.current_player = self.players[self.current_player_idx]

        self.current_state = initial_state.clone()
        self.state_sequence = [initial_state.clone()]
    
    def play(self):
        """
        Runs the game loop.

        The function plays the game.

        Returns:
            state_sequence (list[State]): A list of all states traversed in the game.
            action_sequence (list): A list of all actions taken in the game.
        """
        
        while not self.is_terminal():
            # determine the current player's legal actions from the current state
            legal_actions = self.legal_actions(self.current_player, self.current_state)

            # have the current player observe the state
            observation = self.observe(self.current_player, self.current_state)

            # have the current player choose an action based on the observation of the state
            chosen_action = self.current_player.select_action(legal_actions, observation)
            self.action_sequence.append(chosen_action)
            
            # apply the chosen action onto the current state (resutling in a new state)
            self.apply_action(chosen_action)

            old_state = self.state_sequence[-1]
            new_state =  self.current_state

            self.state_sequence.append(new_state.clone())

            # reward the players
            for player in self.players:
                has_acted = (player == self.current_player) 
                reward_value = self.calculate_reward(
                    player.clone(),
                    old_state.clone(),
                    chosen_action.clone(),
                    new_state.clone())
                self.reward_sequences[player].append(reward_value)
                # reward each player (allows learning within an episode)
                player.reward(reward_value, has_acted)

            # output useful information
            self.output()

        # let each player retro (allows learning between episodes)  
        for player in self.players:
            player.retro()
    
    @abstractmethod
    def output(self) -> str:
        """
        Specifies what to output after each turn.
        """
        pass

    @abstractmethod
    def terminal(self) -> bool:
        """
        Determines whether the game should terminate or not.
        """
        pass


    @abstractmethod
    def observe(self,
                player: Player,
                state: State) -> Observation:
        """
        Returns an observation of the current state for the current player.
        """
        pass

    @abstractmethod
    def legal_actions(self,
                      player: Player,
                      state: State) -> list[Action]:
        """
        Returns a list of legal actions for the specified player from the specified state.
        """
        pass

    @abstractmethod
    def apply_action(self,
                     player: Player,
                     state: State,
                     action: Action) -> State:
        """
        Applies the specified action by the current player onto the current state,
        and returns the new state.
        """
        pass

    @abstractmethod
    def calculate_reward(self,
                         player: Player,
                         old_state: State,
                         action: Action,
                         new_state: State) -> float:
        """
        Returns the reward for the specified player.
        """