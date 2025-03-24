import json
from abc import abstractmethod
from pathlib import Path
from typing import Any, Dict, Literal, Self

import torch
from safetensors.torch import load_file, save_file

from velora.buffer.experience import BatchExperience

MetaDataKeys = Literal[
    "capacity",
    "state_dim",
    "action_dim",
    "position",
    "size",
    "device",
]
BufferKeys = Literal["states", "actions", "rewards", "next_states", "dones"]


class BufferBase:
    """
    A base class for all buffers.

    Stores experiences `(states, actions, rewards, next_states, dones)` as
    individual items in tensors.
    """

    def __init__(
        self,
        capacity: int,
        state_dim: int,
        action_dim: int,
        *,
        device: torch.device | None = None,
    ) -> None:
        """
        Parameters:
            capacity (int): the total capacity of the buffer
            state_dim (int): dimension of state observations
            action_dim (int): dimension of actions
            device (torch.device, optional): the device to perform computations on
        """
        self.capacity = capacity
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.device = device

        # Position indicators
        self.position = 0
        self.size = 0

        # Pre-allocate storage
        self.states = torch.zeros((capacity, state_dim), device=device)
        self.actions = torch.zeros((capacity, action_dim), device=device)
        self.rewards = torch.zeros((capacity, 1), device=device)
        self.next_states = torch.zeros((capacity, state_dim), device=device)
        self.dones = torch.zeros((capacity, 1), device=device)

    def add(
        self,
        state: torch.Tensor,
        action: torch.Tensor,
        reward: float,
        next_state: torch.Tensor,
        done: bool,
    ) -> None:
        """
        Adds a single experience to the buffer.

        Parameters:
            state (torch.Tensor): current state observation
            action (torch.Tensor): action taken
            reward (float): reward received
            next_state (torch.Tensor): next state observation
            done (bool): whether the episode ended
        """
        self.states[self.position] = state.to(torch.float32)
        self.actions[self.position] = action
        self.rewards[self.position] = reward
        self.next_states[self.position] = next_state.to(torch.float32)
        self.dones[self.position] = done

        # Update position - deque style
        self.position = (self.position + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)

    @abstractmethod
    def sample(self) -> BatchExperience:
        """
        Samples experience from the buffer.

        Returns:
            batch (BatchExperience): an object of samples with the attributes (`states`, `actions`, `rewards`, `next_states`, `dones`).

                All items have the same shape `(batch_size, features)`.
        """
        pass  # pragma: no cover

    def __len__(self) -> int:
        """
        Gets the current size of the buffer.

        Returns:
            size (int): the current size of the buffer.
        """
        return self.size

    def metadata(self) -> Dict[MetaDataKeys, Any]:
        """
        Gets the metadata of the buffer.

        Includes:
        - `capacity` - the maximum capacity of the buffer.
        - `state_dim` - state dimension.
        - `action_dim` - action dimension.
        - `position` - current buffer position.
        - `size` - current size of buffer.
        - `device` - the device used for computations.

        Returns:
            metadata (Dict[str, Any]): the buffers metadata
        """
        return {
            "capacity": self.capacity,
            "state_dim": self.state_dim,
            "action_dim": self.action_dim,
            "position": self.position,
            "size": self.size,
            "device": str(self.device) if self.device else None,
        }

    def state_dict(self) -> Dict[BufferKeys, torch.Tensor]:
        """
        Return a dictionary containing the buffers state.

        Includes:
        - `states` - tensor of states.
        - `actions` - tensor of actions.
        - `rewards` - tensor of rewards.
        - `next_states` - tensor of next states.
        - `dones` - tensor of dones.

        Returns:
            state_dict (Dict[str, torch.Tensor]): the current state of the buffer
        """
        return {
            "states": self.states,
            "actions": self.actions,
            "rewards": self.rewards,
            "next_states": self.next_states,
            "dones": self.dones,
        }

    def save(self, dirpath: str | Path, prefix: str = "buffer_") -> None:
        """
        Saves a buffers `state_dict()` to a `safetensors` file.

        Includes:
        - `<prefix>metadata.json` - the buffers metadata
        - `<prefix>state.safetensors` - the buffer state

        Parameters:
            dirpath (str | Path): the folder path to save the buffer state
            prefix (str, optional): a name prefix for the files
        """
        save_path = Path(dirpath)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        metadata_path = Path(save_path, f"{prefix}metadata").with_suffix(".json")
        buffer_path = Path(save_path, f"{prefix}state").with_suffix(".safetensors")

        save_file(self.state_dict(), buffer_path)

        with metadata_path.open("w") as f:
            f.write(json.dumps(self.metadata(), indent=2))

    @classmethod
    def load(cls, state_path: str | Path, metadata: Dict[MetaDataKeys, Any]) -> Self:
        """
        Restores the buffer from a saved state.

        Parameters:
            state_path (str | Path): the filepath to the buffer state
            metadata (Dict[str, Any]): a dictionary of metadata already
                loaded from a `metadata.json` file

        Returns:
            buffer (Self): a new buffer instance with the saved state restored
        """
        buffer_path = Path(state_path).with_suffix(".safetensors")
        device = metadata["device"] or "cpu"

        # Create new buffer instance
        buffer = cls(
            capacity=metadata["capacity"],
            state_dim=metadata["state_dim"],
            action_dim=metadata["action_dim"],
            device=torch.device(device) if device else None,
        )
        buffer.position = metadata["position"]
        buffer.size = metadata["size"]

        # Load buffer state
        data: Dict[BufferKeys, torch.Tensor] = load_file(buffer_path, device)

        buffer.states = data["states"]
        buffer.actions = data["actions"]
        buffer.rewards = data["rewards"]
        buffer.next_states = data["next_states"]
        buffer.dones = data["dones"]

        return buffer
