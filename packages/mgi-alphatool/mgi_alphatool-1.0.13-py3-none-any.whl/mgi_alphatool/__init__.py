from typing import Literal
from .context import Context
from .handler.gripper import Gripper
from .handler.pipette import Pipette
from .liquid import Liquid
from .labware import Labware
from .module import Module

def init(robot_type: str = 'alphatool', 
         deck_type: Literal['standard', 'ext1'] = 'standard', 
         home_slot: int = 12,
         auto_revise: bool = True) -> Context:
    """Initialize the protocol context. This function sets up the protocol context based on the alphatool.

    Args:
        robot_type (str): Type of robot to use (e.g. 'alphatool')
        deck_type (Literal['standard', 'ext1']): Type of deck to use (e.g. 'standard' or 'ext1')
        home_slot (int): The slot to home the robot
        auto_revise (bool): If True, automatically corrects name errors for pipette, module, and labware if possible. Defaults to True.

    Returns:
        Context: The initialized protocol context.
    """
    if robot_type != 'alphatool':
        raise ValueError(f"Unsupported robot type: {robot_type}. Must be 'alphatool'.")
    if deck_type not in ['standard', 'ext1']:
        raise ValueError(f"Unsupported deck type: {deck_type}. Must be 'standard' or 'ext1'.")
    if not isinstance(home_slot, int):
        raise ValueError(f"home_slot must be an integer, got {type(home_slot)}")
    if not isinstance(auto_revise, bool):
        raise TypeError(f"auto_revise must be a boolean, got {type(auto_revise)}")

    return Context(robot_type=robot_type, deck_type=deck_type, home_slot=home_slot, auto_revise=auto_revise)