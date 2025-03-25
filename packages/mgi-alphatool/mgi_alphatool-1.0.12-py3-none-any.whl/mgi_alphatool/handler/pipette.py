from . import Handler

from typing import List, Literal, Union
from ..utils.exception import LocationErr
from ..utils.common import flatten_wells
from ..labware import Labware, Well, Column
from ..labware.tiprack import TipRack
from ..labware.trashbin import TrashBin
from ..commands.pipette import (MoveToCommand, MoveToParams,
                               MoveToAreaCommand, MoveToAreaParams,
                               PickUpTipCommand, PickUpTipParams,
                               AspirateCommand, AspirateParams,
                               DispenseCommand, DispenseParams,
                               DispenseInplaceCommand, DispenseInplaceParams,
                               DropTipCommand, DropTipInPlaceCommand, DropTipParams,
                               BlowOutCommand, BlowOutParams,
                               TouchTipCommand, TouchTipParams,
                               MoveToAreaForDropTipCommand, MoveToAreaForDropTipParams)

from ..app.commands.command import TransferCommand, MixCommand

class Pipette(Handler):
    def __init__(self, id: str, name: str, mount: str, context: 'Context'):
        super().__init__(id, name, mount, context)
        self.__has_tip = False
        self.__current_tip_location = None

        self.n_channel = 1 if self.__is_single_channel() else 8
    
    def __validate_transfer_params(self, 
                                   source_wells: Union[List[Well], List[Column]], 
                                   dest_wells: Union[List[Well], List[Column]]) -> None:
        """validate the parameter of transfer

        Args:
            source_wells (Union[List[Well], List[Column]]): source wells
            dest_wells (Union[List[Well], List[Column]]): destination wells
        """

        def get_n_wells(wells):
            return sum(len(w) if isinstance(w, Column) else 1 for w in wells)

        def is_only_first_row(wells):
            return all(next(filter(str.isalpha, w.id())) == 'A' for w in wells if isinstance(w, Well))

        # get the length of the wells
        n_src_wells = get_n_wells(source_wells)
        n_dest_wells = get_n_wells(dest_wells)

        if self.__is_single_channel():
            if not (n_src_wells == n_dest_wells or 
                    n_src_wells == 1 or 
                    n_dest_wells == 1):
                raise ValueError("Transfer must be 1 to many, many to 1, or N to N.")
            
        else:
            if not (n_src_wells % 8 == 0 or 
                    is_only_first_row(source_wells)):
                raise ValueError("For multi-channel pipette, the number of source wells must each be divisible by 8.")
            
            if not (n_dest_wells % 8 == 0 or 
                    is_only_first_row(dest_wells)):
                raise ValueError("For multi-channel pipette, the number of destination wells must each be divisible by 8.")
            
            if not (n_src_wells == n_dest_wells or 
                    (n_src_wells / 8 == 1 or (len(source_wells) == 1 and is_only_first_row(source_wells))) or 
                    (n_dest_wells / 8 == 1 or (len(dest_wells) == 1 and is_only_first_row(dest_wells)))):
                raise ValueError("Transfer must be 1 to many, many to 1, or N to N (where N is divisible by 8).")

    def __validate_mix_params(self, wells: Union[List[Well], List[Column]]) -> None:
        """vlidate the parameters of mix

        Args:
            wells (Union[List[Well], List[Column]]): wells for mixing
        """

        def get_n_wells(wells):
            return sum(1 if isinstance(w, Well) else len(w) for w in wells)
        
        def is_only_first_row(wells):
            return all(next(filter(str.isalpha, w.id())) == 'A' for w in wells if isinstance(w, Well))

        n_wells = get_n_wells(wells)

        if not self.__is_single_channel():
            if not (n_wells % 8 == 0 or is_only_first_row(wells)):
                raise ValueError("For multi-channel pipette, the number of wells must be divisible by 8")
           
    def __validate_wells(self, wells: List[Well]):
        """check is the wells in the list come from the same location(labware)

        Args:
            wells (List[Well]): wells in the list
        """
        if len(set(well._get_parent() for well in wells)) != 1:
            raise ValueError("All wells must in the same labware")

    def __validate_tiprack(self, tiprack: Union[TipRack, None]):
        """check is the tiprack provided.

        Args:
            tiprack (TipRack): tiprack instance
        """
        if tiprack is None:
            raise ValueError("Tiprack should be provided useless there is only one tiprack type loaded.")
    
        if not tiprack._is_tiprack():
            raise ValueError("Please provide the valid tiprack instance.")
    
    def __validate_mix_in_transfer_params(self, mix_param: Union[tuple, None], param_name: str) -> None:
        """Validate the mix_before and mix_after parameters.

        Args:
            mix_param (Union[tuple, None]): The mix parameter to validate.
            param_name (str): The name of the parameter ('mix_before' or 'mix_after').

        Raises:
            ValueError: If the mix parameter is invalid.
        """
        if mix_param is not None:
            if not isinstance(mix_param, (tuple, list)) or len(mix_param) != 2:
                raise ValueError(f"{param_name} must be a tuple or list of two elements")
            if not isinstance(mix_param[0], int) or mix_param[0] <= 0:
                raise ValueError(f"First element of {param_name} must be a positive integer (number of repetitions)")
            if not isinstance(mix_param[1], (int, float)) or mix_param[1] <= 0:
                raise ValueError(f"Second element of {param_name} must be a positive number (volume)")

    def __validate_delay(self, delay: int, param_name: str) -> None:
        """Validate the delay parameters.

        Args:
            delay (int): The delay value to validate.
            param_name (str): The name of the parameter.

        Raises:
            ValueError: If the delay parameter is invalid.
        """
        if not isinstance(delay, int) or delay < 0:
            raise ValueError(f"{param_name} must be a non-negative integer")

    def __validate_air_gap(self, air_gap: float,
                           max_volume: int, 
                           param_name: str):
        """Validate the air gap parameters.

        Args:
            air_gap (float): The air gap volume to validate.
            max_volume (int): The maximum volume capacity of the tip.
            param_name (str): The name of the parameter.

        Raises:
            ValueError: If the air gap parameter is invalid or exceeds the maximum tip volume.
        """
        if not isinstance(air_gap, (int, float)) or air_gap < 0:
            raise ValueError(f"Invalid value for {param_name}. Must be a non-negative number.")
        
        if air_gap >= max_volume:
            raise ValueError(f"The volume of air gap should not be larger then the maximum volume of tip.")

    def __process_wells(
            self,
            wells: Union[List[Well],List[Column]]
        ) -> List[Well]:
        """convert the column into well.

        Args:
            wells (Union[List[Well],List[Column]]): input wells or columns

        Returns:
            List[Well]: output wells
        """
        
        # Process wells or columns based on pipette type
        processed = []
        for w in wells:
            if isinstance(w, Column):
                # For multi-channel pipettes, keep columns intact
                # For single-channel pipettes, expand columns to individual wells
                processed.extend([w] if not self.__is_single_channel() else w.wells())
            else:
                processed.append(w)
        return processed
 
    def __execute_transfer(
            self,
            volume: int,
            source_wells: List[Well],
            dest_wells: List[Well],
            tiprack: Union[TipRack, Column, Well],
            use_new_tip: str,
            return_tip: bool,
            aspirate_position: Literal['top', 'bottom'],
            aspirate_offset: tuple,
            dispense_position: Literal['top', 'bottom'],
            dispense_offset: tuple,
            aspirate_flow_rate: float,
            dispense_flow_rate: float,
            pre_wet: bool,
            aspirate_touch_tip: bool,
            aspirate_touch_tip_position: Literal['top', 'bottom'],
            aspirate_touch_tip_offset: tuple,
            dispense_touch_tip: bool,
            dispense_touch_tip_position: Literal['top', 'bottom'],
            dispense_touch_tip_offset: tuple,
            blow_out: bool,
            blow_out_location: str,
            mix_before_aspirate: Union[tuple, None],
            mix_after_dispense: Union[tuple, None],
            air_gap_after_aspirate: float, 
            air_gap_before_drop_tip: float,
            delay_after_aspirate: int,
            delay_after_aspirate_position: Literal['top', 'bottom'],
            delay_after_aspirate_offset: tuple,
            delay_after_dispense: int,
            delay_after_dispense_position: Literal['top', 'bottom'],
            delay_after_dispense_offset: tuple,
            drop_tip: bool
        ) -> None:

        """Executes the liquid transfer process based on the provided parameters."""
        n_src_wells = len(source_wells)
        n_dest_wells = len(dest_wells)

        if isinstance(tiprack, TipRack):
            _tiprack = tiprack
        elif isinstance(tiprack, (Well, Column)):
            _tiprack = tiprack._get_parent()
        
        max_volume = (_tiprack or self.__current_tip_location._get_parent())._get_max_volume()

        def _transfer_chunk(vol, max_vol, src, dest):
            volume_remaining = volume

            if pre_wet:
                self.aspirate(volume=min(vol, max_volume), 
                              location=src, 
                              position=aspirate_position,
                              offset=aspirate_offset, 
                              flow_rate=aspirate_flow_rate)
                
                self.dispense(volume=min(vol, max_volume), 
                              location=src, 
                              position=aspirate_position,
                              offset=aspirate_offset, 
                              flow_rate=dispense_flow_rate)
            
            if mix_before_aspirate:
                self.mix(repetitions=mix_before_aspirate[0], 
                          volume=mix_before_aspirate[1], 
                          location=src, 
                          use_new_tip='never', 
                          aspirate_position=aspirate_position,
                          aspirate_offset=aspirate_offset,
                          dispense_position=aspirate_position,
                          dispense_offset=aspirate_offset)
                
            while volume_remaining > 0:
                volume_chunk = min(volume_remaining, max_vol)

                if air_gap_after_aspirate:
                    volume_chunk = min(max_vol-air_gap_after_aspirate, volume_remaining)

                self.aspirate(volume=volume_chunk, 
                              location=src, 
                              position=aspirate_position,
                              offset=aspirate_offset, 
                              flow_rate=aspirate_flow_rate)

                if delay_after_aspirate:
                    self.move_to(src, delay_after_aspirate_position, delay_after_aspirate_offset)
                    self._get_context().pause(delay_after_aspirate)

                if aspirate_touch_tip:
                    self.touch_tip(position=aspirate_touch_tip_position, offset=aspirate_touch_tip_offset)

                if air_gap_after_aspirate:
                    # call the internal function to grant more parameter control (position)
                    # dispense the air gap before dispense the liquid
                    self.air_gap(air_gap_after_aspirate)
                    self.dispense(volume=air_gap_after_aspirate,
                                  location=dest,
                                  position='top',
                                  offset=(0,0,5),
                                  flow_rate=dispense_flow_rate)

                if isinstance(dest._get_parent(), TrashBin):
                    self.dispense(volume_chunk, dest._get_parent(), flow_rate=dispense_flow_rate)
                else:
                    self.dispense(volume_chunk, dest, position=dispense_position, offset=dispense_offset, flow_rate=dispense_flow_rate)
                
                if delay_after_dispense:
                    self.move_to(dest, delay_after_dispense_position, delay_after_dispense_offset)
                    self._get_context().pause(delay_after_dispense)
                
                if dispense_touch_tip:
                    self.touch_tip(position=dispense_touch_tip_position, offset=dispense_touch_tip_offset)

                if blow_out:
                    if blow_out_location == 'source':
                        loc = src
                    elif blow_out_location == 'destination':
                        loc = dest
                    elif blow_out_location == 'trash_bin':
                        loc = self._get_context().trash_bin
                    self.blow_out(loc)

                volume_remaining -= volume_chunk
            
            if mix_after_dispense:
                self.mix(repetitions=mix_after_dispense[0], volume=mix_after_dispense[1], 
                          location=dest, 
                          use_new_tip='never', 
                          aspirate_position=dispense_position,
                          aspirate_offset=dispense_offset,
                          dispense_position=dispense_position,
                          dispense_offset=dispense_offset)

        tip_loc = self.__current_tip_location if return_tip else None

        if n_src_wells == n_dest_wells:
            for src, dest in zip(source_wells, dest_wells):
                if use_new_tip == 'always' and self.__has_tip:
                    
                    if air_gap_before_drop_tip:
                        self.air_gap(air_gap_after_aspirate)
                    
                    self.drop_tip(tip_loc)
                    self.pick_up_tip(tiprack)
                
                if not self.__has_tip:
                    self.pick_up_tip(tiprack)    

                _transfer_chunk(volume, max_volume, src, dest)

        elif n_src_wells == 1 or (n_src_wells // 8 == 1 and not self.__is_single_channel()):
            for dest in dest_wells:
                if use_new_tip == 'always' and self.__has_tip:
                    
                    if air_gap_before_drop_tip:
                        self.air_gap(air_gap_after_aspirate)
                    
                    self.drop_tip(tip_loc)
                    self.pick_up_tip(tiprack)
                
                if not self.__has_tip:
                    self.pick_up_tip(tiprack)
                
                _transfer_chunk(volume, max_volume, source_wells[0], dest)
  
        elif n_dest_wells == 1 or (n_dest_wells // 8 == 1 and not self.__is_single_channel()):
            for src in source_wells:
                if use_new_tip == 'always' and self.__has_tip:

                    if air_gap_before_drop_tip:
                        self.air_gap(air_gap_after_aspirate)
                        
                    self.drop_tip(tip_loc)
                    self.pick_up_tip(tiprack)
                
                if not self.__has_tip:
                    self.pick_up_tip(tiprack)

                _transfer_chunk(volume, max_volume, src, dest_wells[0])
        
        if drop_tip:
            self.drop_tip()
                
    def transfer(self, 
                 volume: float, 
                 source_wells: Union[List[Well], Well, List[Column], Column, Labware], 
                 dest_wells: Union[List[Well], Well, List[Column], Column, Labware, TrashBin], 
                 tiprack: Union[TipRack, Well, Column, None] = None, 
                 use_new_tip: Literal['once', 'always', 'never'] = 'once',
                 return_tip: bool = False,
                 aspirate_position: Literal['top', 'bottom'] = 'bottom',
                 aspirate_offset: tuple = (0,0,1),
                 dispense_position: Literal['top', 'bottom'] = 'bottom',
                 dispense_offset: tuple = (0,0,1),
                 aspirate_flow_rate: float = 150,
                 dispense_flow_rate: float = 300,
                 pre_wet: bool = False,
                 aspirate_touch_tip: bool = False,
                 aspirate_touch_tip_position: Literal['top', 'bottom'] = 'bottom',
                 aspirate_touch_tip_offset: tuple = (0,0,1),
                 dispense_touch_tip: bool = False,
                 dispense_touch_tip_position: Literal['top', 'bottom'] = 'bottom',
                 dispense_touch_tip_offset: tuple = (0,0,1),
                 blow_out: bool = False,
                 blow_out_location: Literal['source', 'destination', 'trash_bin'] = 'trash_bin',
                 mix_before_aspirate: Union[tuple, None] = None,
                 mix_after_dispense: Union[tuple, None] = None,
                 air_gap_after_aspirate: float = 0,
                 air_gap_before_drop_tip: float = 0,
                 delay_after_aspirate: int = 0,
                 delay_after_aspirate_position: Literal['top', 'bottom'] = 'bottom',
                 delay_after_aspirate_offset: tuple = (0,0,1),
                 delay_after_dispense: int = 0,
                 delay_after_dispense_position: Literal['top', 'bottom'] = 'bottom',
                 delay_after_dispense_offset: tuple = (0,0,1),
                 drop_tip: bool = True,
                 ) -> 'Pipette':
        """Transfer liquid from source to destination wells.

        This method facilitates the transfer of a specified volume of liquid from source wells to destination wells using a pipette.
        It supports various options for tip usage, liquid handling, and transfer customization.

        Args:
            volume (float): The volume of liquid to transfer.
            source_wells (Union[List[Well], Well, List[Column], Column, Labware]): Source wells/columns to transfer from. If Labware is passed, all wells in the labware will be used.
            dest_wells (Union[List[Well], Well, List[Column], Column, Labware, TrashBin]): Destination wells/columns or trash bin to transfer to.
            tiprack (Union[TipRack, Well, Column, None], optional): Tip rack (Supports TipRack, Well, Column) for picking up tips. If None, attempts automatic selection. Defaults to None.
            use_new_tip (str, optional): When to use new tips - 'once' (first transfer), 'always' (each transfer), 'never' (reuse tip). Defaults to 'once'.
            return_tip (bool, optional): Return tips to tiprack instead of trash when dropping. Defaults to False.
            aspirate_offset (tuple, optional): (x,y,z) offset in mm from bottom of source well. Defaults to (0,0,1).
            dispense_offset (tuple, optional): (x,y,z) offset in mm from bottom of destination well. Defaults to (0,0,1).
            aspirate_flow_rate (float, optional): Aspirate flow rate in uL/s. Defaults to 150.
            dispense_flow_rate (float, optional): Dispense flow rate in uL/s. Defaults to 300.
            pre_wet (bool, optional): Pre-wet tip by aspirating and dispensing before transfer. Defaults to False.
            aspirate_touch_tip (bool, optional): Touch tip to well side after aspiration. Defaults to False.
            aspirate_touch_tip_position (str, optional): Position for aspirate touch tip - 'top' or 'bottom'. Defaults to 'bottom'.
            aspirate_touch_tip_offset (tuple, optional): (x,y,z) offset in mm for aspirate touch tip. Defaults to (0,0,1).
            dispense_touch_tip (bool, optional): Touch tip to well side after dispensing. Defaults to False.
            dispense_touch_tip_position (str, optional): Position for dispense touch tip - 'top' or 'bottom'. Defaults to 'bottom'.
            dispense_touch_tip_offset (tuple, optional): (x,y,z) offset in mm for dispense touch tip. Defaults to (0,0,1).
            blow_out (bool, optional): Blow out tip after dispensing. Defaults to False.
            blow_out_location (str, optional): Where to blow out - 'source', 'destination', or 'trash_bin'. Defaults to 'trash_bin'.
            mix_before_aspirate (tuple, optional): (repetitions, volume) for mixing before aspirating. Defaults to None.
            mix_after_dispense (tuple, optional): (repetitions, volume) for mixing after dispensing. Defaults to None.
            air_gap_after_aspirate (float, optional): Air volume to aspirate after liquid to prevent drips. Defaults to 0.
            air_gap_before_drop_tip (float, optional): Air volume to aspirate before dropping tip. Defaults to 0.
            delay_after_aspirate (int, optional): Seconds to wait after aspirating. Defaults to 0.
            delay_after_aspirate_position (str, optional): Position for delay after aspirating - 'top' or 'bottom'. Defaults to 'bottom'.
            delay_after_aspirate_offset (tuple, optional): (x,y,z) offset in mm for delay after aspirating. Defaults to (0,0,1).
            delay_after_dispense (int, optional): Seconds to wait after dispensing. Defaults to 0.
            delay_after_dispense_position (str, optional): Position for delay after dispensing - 'top' or 'bottom'. Defaults to 'bottom'.
            delay_after_dispense_offset (tuple, optional): (x,y,z) offset in mm for delay after dispensing. Defaults to (0,0,1).
            drop_tip (bool, optional): Drop tip at the end of transfer. Defaults to True.

        Returns:
            Pipette: The pipette instance for method chaining.

        Note:
            - For mix parameters, provide a tuple of (repetitions, volume)
            - Offsets are measured in millimeters relative to well positions
            - Air gaps help prevent cross-contamination and dripping
        """

        if isinstance(source_wells, Well) or isinstance(source_wells, Column):
            source_wells = [source_wells]
        if isinstance(dest_wells, Well) or isinstance(dest_wells, Column):
            dest_wells = [dest_wells]
        if isinstance(source_wells, Labware):
            # by default return column, not well since single channel pipette can access column but 8 channel pipette cannot access well
            # source_wells = source_wells.wells()
            source_wells = source_wells.columns()
        if isinstance(dest_wells, Labware):
            # dest_wells = dest_wells.wells()
            dest_wells = dest_wells.columns()

        source_wells = flatten_wells(source_wells)
        dest_wells = flatten_wells(dest_wells)

        # validation parameters
        self.__validate_transfer_params(source_wells, dest_wells)
        self.__validate_wells(source_wells)
        self.__validate_wells(dest_wells)

        # Validate mix_before and mix_after
        self.__validate_mix_in_transfer_params(mix_before_aspirate, "mix_before")
        self.__validate_mix_in_transfer_params(mix_after_dispense, "mix_after")

        # Validate delay_after_aspirate and delay_after_dispense
        self.__validate_delay(delay_after_aspirate, "delay_after_aspirate")
        self.__validate_delay(delay_after_dispense, "delay_after_dispense")

        # Validate option
        if use_new_tip not in ['once', 'always', 'never']:
            raise ValueError("Invalid value for use_new_tip. Expected 'once', 'always', or 'never'.")
        if blow_out_location not in ['source', 'destination', 'trash_bin']:
            raise ValueError("Invalid value for blow_out_location. Expected 'source', 'destination', or 'trash_bin'.")

        # try to get the tiprack from deck
        # if no need to change tip and there is a tip on the pipette, skip the tip check
        if use_new_tip == 'never' and self.__has_tip:
            pass
        else:
            if isinstance(tiprack, TipRack):
                _tiprack = tiprack
            elif isinstance(tiprack, Well) or isinstance(tiprack, Column):
                _tiprack = tiprack._get_parent()
            elif tiprack is None:
                tiprack = self._get_context()._auto_get_tiprack(volume=volume, n_tip=self.n_channel)
                _tiprack = tiprack
            else:
                raise ValueError("Invalid tiprack type. Expected TipRack, Well, or Column.")

        max_volume = (_tiprack and _tiprack._get_max_volume()) or (self.__current_tip_location and self.__current_tip_location._get_parent()._get_max_volume())
        if not max_volume:
            raise ValueError("Tiprack must be provided when using new tips and no tiprack is loaded on the deck.")

        # Validate air gap volumes
        self.__validate_air_gap(air_gap_after_aspirate, max_volume, "air_gap_after_aspirate")
        self.__validate_air_gap(air_gap_before_drop_tip, max_volume, "air_gap_before_drop_tip")

        # preprocessing the well list
        source_wells = self.__process_wells(source_wells)
        dest_wells = self.__process_wells(dest_wells)

        # once: need to replace tip only at the beginning (if possible)
        # always: replace the tip for each transfer
        if (use_new_tip == 'once' or use_new_tip == 'always') and self.__has_tip:
            self.drop_tip()

        # run the command
        self.__execute_transfer(volume, source_wells, dest_wells, 
                                tiprack, 
                                use_new_tip, return_tip,
                                aspirate_position,
                                aspirate_offset,
                                dispense_position,
                                dispense_offset,
                                aspirate_flow_rate,
                                dispense_flow_rate,
                                pre_wet, 
                                aspirate_touch_tip, aspirate_touch_tip_position, aspirate_touch_tip_offset, 
                                dispense_touch_tip, dispense_touch_tip_position, dispense_touch_tip_offset, 
                                blow_out, blow_out_location,
                                mix_before_aspirate, mix_after_dispense,
                                air_gap_after_aspirate, air_gap_before_drop_tip,
                                delay_after_aspirate, delay_after_aspirate_position, delay_after_aspirate_offset,
                                delay_after_dispense, delay_after_dispense_position, delay_after_dispense_offset,
                                drop_tip)

        # TODO: check if this is correct

        self._get_context()._append_saved_step_form(
            TransferCommand(
                volume=volume,
                pipette=self.id(),
                tipRack=_tiprack._get_name() if _tiprack is not None else self.__current_tip_location._get_parent()._get_name(),
                preWetTip=pre_wet,
                aspirate_wells=[self.__get_well_name(well) for well in source_wells],
                dispense_wells=[self.__get_well_name(well) for well in dest_wells],
                aspirate_labware=source_wells[0]._get_parent().id(),
                dispense_labware=dest_wells[0]._get_parent().id(),
                dropTip_location=self._get_context()._get_trash_bin().id(),
                blowout_checkbox=blow_out,
                aspirate_mix_checkbox=False if mix_before_aspirate is None else True,
                dispense_mix_checkbox=False if mix_after_dispense is None else True,
                
                path='single', # pending to check
                changeTip=use_new_tip, # pending to check
                disposalVolume_volume=30,# pending to check
                disposalVolume_checkbox=False,# pending to check
                
                aspirate_airGap_volume=air_gap_after_aspirate,
                aspirate_airGap_checkbox=air_gap_after_aspirate > 0,
                dispense_airGap_volume=air_gap_before_drop_tip,
                dispense_airGap_checkbox=air_gap_before_drop_tip > 0,
                aspirate_delay_seconds=delay_after_aspirate,
                aspirate_delay_checkbox=delay_after_aspirate > 1,
                dispense_delay_seconds=delay_after_dispense,
                dispense_delay_checkbox=delay_after_dispense > 1,
                aspirate_touchTip_checkbox=aspirate_touch_tip,
                dispense_touchTip_checkbox=dispense_touch_tip,

                # not supported yet
                # aspirate_wells_grouped=False, # not sure what is this
                # aspirate_detect_checkbox=False,
                # aspirate_wellOrder_first="t2b",
                # aspirate_wellOrder_second="l2r", 
                # dispense_wellOrder_first="t2b",
                # dispense_wellOrder_second="l2r",
                
            )
        )

        return self

    def __get_well_name(self, location: Union[Well, Column]) -> str:
        """Extract well name from location, handling both Well and Column types."""
        if isinstance(location, Column):
            return location.wells()[0].id()
        return location.id()

    def mix(self,
            repetitions: int,
            volume: float,
            wells: Union[List[Well], List[Column], Well, Column, None] = None,
            tiprack: Union[TipRack, None] = None,
            use_new_tip: Literal['once', 'always', 'never'] = 'once',
            aspirate_position: Literal['top', 'bottom'] = 'bottom',
            aspirate_offset: tuple = (0,0,1),
            dispense_position: Literal['top', 'bottom'] = 'bottom',
            dispense_offset: tuple = (0,0,1),
            delay_after_aspirate: int = 0,
            delay_after_dispense: int = 0,
            touch_tip: bool = False,
            touch_tip_position: Literal['top', 'bottom'] = 'top',
            touch_tip_offset: tuple = (0,0,0),
            blow_out: bool = False,
            aspirate_flow_rate: float = 150,
            dispense_flow_rate: float = 300,
            drop_tip: bool = True,
            ) -> 'Pipette':
        """Mix liquid in specified wells. Performs a mixing operation by repeatedly aspirating and dispensing liquid in the given wells.

        Args:
            repetitions (int): Number of times to repeat the mix operation.
            volume (float): Volume in microliters (µL) to aspirate and dispense.
            wells (Union[List[Well], List[Column], Well, Column], optional): Target wells for mixing.
                Can be a single Well/Column or a list. Defaults to current location.
            tiprack (Union[TipRack, None], optional): Tip rack to use. If None, auto-selected.
            use_new_tip (str, optional): When to use new tips - 'once', 'always', or 'never'.
                'once': New tip at start only
                'always': New tip for each well
                'never': Reuse existing tip
                Defaults to 'once'.
            aspirate_position (str, optional): Position for aspirate - 'top' or 'bottom'. Defaults to 'bottom'.
            aspirate_offset (tuple, optional): (x,y,z) offset in mm for aspirate. Defaults to (0,0,1).
            dispense_position (str, optional): Position for dispense - 'top' or 'bottom'. Defaults to 'bottom'.
            dispense_offset (tuple, optional): (x,y,z) offset in mm for dispense. Defaults to (0,0,1).
            delay_after_aspirate (int, optional): Seconds to wait after aspirating. Defaults to 0.
            delay_after_dispense (int, optional): Seconds to wait after dispensing. Defaults to 0.
            touch_tip (bool, optional): Touch tip to well side after mixing. Defaults to False.
            touch_tip_position (str, optional): Position for touch tip - 'top' or 'bottom'. Defaults to 'top'.
            touch_tip_offset (tuple, optional): (x,y,z) offset in mm for touch tip. Defaults to (0,0,0).
            blow_out (bool, optional): Blow out tip after mixing. Defaults to False. 
            aspirate_flow_rate (float, optional): Aspirate flow rate in uL/s. Defaults to 150.
            dispense_flow_rate (float, optional): Dispense flow rate in uL/s. Defaults to 300.
            drop_tip (bool, optional): Drop tip at the end of mixing. Defaults to True.

        Returns:
            Pipette: The pipette instance.
        """
        # Get current location if no wells specified
        if wells is None:
            wells = self._get_context()._get_arm_location()

        # Convert single well/column to list
        if isinstance(wells, (Well, Column)):
            wells = [wells]
        
        # Convert labware to well list
        if isinstance(wells, Labware):
            # wells = wells.wells()
            wells = wells.columns()

        # Flatten and validate wells
        wells = flatten_wells(wells)

        self.__validate_mix_params(wells)
        self.__validate_wells(wells)

        self.__validate_delay(delay_after_aspirate, "delay_after_aspirate")
        self.__validate_delay(delay_after_dispense, "delay_after_dispense")

        wells = self.__process_wells(wells)
        
        # try to get the tiprack from deck
        # if no need to change tip and there is a tip on the pipette, skip the tip check
        if use_new_tip == 'never' and self.__has_tip:
            pass
        else:
            if tiprack is None:
                tiprack = self._get_context()._auto_get_tiprack(n_tip=self.n_channel)
            self.__validate_tiprack(tiprack)

        # once: need to replace tip only at the beginning (if possible)
        # always: replace the tip for each transfer
        if (use_new_tip == 'once' or use_new_tip == 'always') and self.__has_tip:
            self.drop_tip()
        
        for well in wells:
            # Handle tip management
            # Ensure we have a fresh tip if needed
            if not self.__has_tip or (use_new_tip == 'always' and self.__has_tip):
                if self.__has_tip:
                    self.drop_tip()
                self.pick_up_tip(tiprack)

            # Perform mixing
            for _ in range(repetitions):
                self.aspirate(volume=volume, location=well, 
                              position=aspirate_position,
                              offset=aspirate_offset, 
                              flow_rate=aspirate_flow_rate)
                
                if delay_after_aspirate:
                    self._get_context().pause(delay_after_aspirate)

                self.dispense(volume=volume, location=well, 
                              position=dispense_position,
                              offset=dispense_offset, 
                              flow_rate=dispense_flow_rate)
                
                if delay_after_dispense:
                    self._get_context().pause(delay_after_dispense)

            # Optional post-mix steps
            if touch_tip:
                self.touch_tip(position=touch_tip_position, offset=touch_tip_offset)
            
            if blow_out:
                self.blow_out()
        
        if drop_tip:
            self.drop_tip()
        
        # TODO: check if this is correct
        self._get_context()._append_saved_step_form(
            MixCommand(
                times=repetitions,
                wells=[self.__get_well_name(w) for w in wells],
                volume=volume,
                labware=wells[0]._get_parent().id(),
                pipette=self.id(),
                tipRack=tiprack._get_name() if tiprack is not None else self.__current_tip_location._get_parent()._get_name(),
                changeTip=use_new_tip, # need to check
                blowout_checkbox=blow_out,
                dropTip_location=self._get_context()._get_trash_bin().id(),
                mix_touchTip_checkbox=touch_tip
            )
        )

        return self
    
    def aspirate(self, volume: float, 
                 location: Union[Well, Column]=None,
                 flow_rate: float = 5,
                 position: Literal['top','bottom'] = 'bottom',
                 offset: tuple = (0,0,1),
                 **kwargs) -> 'Pipette':
        """Aspirate liquid from a specified location. This method performs an aspiration of a specified volume from a given well or column.

        Args:
            volume (float): The volume in microliters (µL) to aspirate.
            location (Union[Well, Column], optional): The well or column from which to aspirate. Defaults to current location if not specified.
            float_rate (float, optional): The aspirate speed. Defaults to 5 ul/s
            offset (tuple, optional): A tuple of (x,y,z) offsets in millimeters from the reference position. Defaults to (0,0,1).
            **kwargs: Additional keyword arguments to pass to the internal aspirate function.

        Returns:
            Pipette: The pipette instance.
        """
        return self.__aspirate(volume=volume,
                        location=location,
                        flow_rate=flow_rate,
                        position=position,
                        offset=offset,
                        **kwargs
                        )
    
    def __aspirate(self, volume: float, 
                 location: Union[Well, Column, None]=None,
                 flow_rate: float = 5,
                 position: Literal['top','bottom'] = 'bottom',
                 offset: tuple = (0,0,1),
                 **kwargs) -> 'Pipette':
        """internal function of aspirate."""
        location = self.__get_validated_location(location)
        
        if not self.__has_tip:
            raise ValueError("Need to pick up tips first before aspiration.")

        self.__validate_location(location)
            
        self._get_context()._append_command(AspirateCommand(
            params=AspirateParams(
                pipetteId=self.id(), 
                volume=volume, 
                labwareId=location._get_parent().id(), 
                wellName=self.__get_well_name(location),
                flowRate=flow_rate,
                wellLocation=self.__create_well_location(position, offset),
                **kwargs
                )))
        
        self._get_context()._set_arm_location(location)
        return self
        
    def dispense(self, volume: float, 
                 location: Union[Well, Column, TrashBin]= None,
                 flow_rate: float = 10,
                 position: Literal['top','bottom'] = 'bottom',
                 offset: tuple = (0,0,1),
                 **kwargs) -> 'Pipette':
        """Dispense liquid into a specified location. This method performs a dispensation of a specified volume into a given well or column.

        Args:
            volume (float): The volume in microliters (µL) to dispense.
            location (Union[Well, Column, TrashBin], optional): The well or column to dispense into. If TrashBin is passed, it will dispense the liquid to the trash bin. Defaults to the current location if not specified.
            float_rate (float): The dispense speed. Defaults to 10 ul/s
            position (Literal['top', 'bottom'], optional): The position within the well. Wether the 'top' of the well or 'bottom' of the well. Defaults to 'bottom'.
            offset (tuple, optional): A tuple of (x,y,z) offsets in millimeters from the reference position. Defaults to (0,0,1).

        Returns:
            Pipette: The pipette instance.
        """
        return self.__dispense(volume=volume,
                           location=location, 
                           flow_rate=flow_rate,
                           position=position,
                           offset=offset,
                           **kwargs)
    
    def __dispense(self, volume: float, 
                 location: Union[Well, Column, TrashBin, None]= None,
                 flow_rate: float = 10,
                 position: Literal['top','bottom'] = 'bottom',
                 offset: tuple = (0,0,1),
                 **kwargs) -> 'Pipette':
        """internal function of dispense.
        """
        location = self.__get_validated_location(location)
        
        if not self.__has_tip:
            raise ValueError("Need to pick up tips first before dispensation.")
        
        self.__validate_location(location)
        
        if isinstance(location, TrashBin):
            self.move_to(location, 'top', (0,0,5))
            self._get_context()._append_command(DispenseInplaceCommand(
                params=DispenseInplaceParams(
                    pipetteId=self.id(), 
                    volume=volume
                )
            ))

        else:
            self._get_context()._append_command(DispenseCommand(
                params=DispenseParams(pipetteId=self.id(), 
                    volume=volume, 
                    labwareId=location._get_parent().id(), 
                    wellName=self.__get_well_name(location),
                    flowRate=flow_rate,
                    wellLocation=self.__create_well_location(position, offset),
                    **kwargs
                    )))
        
            self._get_context()._set_arm_location(location)
        return self
    
    def pick_up_tip(self, location: Union[TipRack, Well, Column, None] = None) -> 'Pipette':
        """Pick up a tip from the specified location. This method picks up a tip from a given TipRack, Well, or Column. If no location is provided, it attempts to automatically select a TipRack.

        Args:
            location (Union[TipRack, Well, Column], optional): The location to pick up a tip from. Can be a TipRack, Well, or Column. Defaults to None for automatic selection.

        Returns:
            Pipette: The pipette instance.
        """
        if self.__has_tip:
            raise RuntimeError("Pipette already has a tip on it. Please drop the tip before picking up a new one.")
        
        # check if another pipette already has a tip (since it is not allow to having tip on two pipettes at the same time)
        # TODO
        
        if isinstance(location, (Well,Column)):
            self.__validate_location(location)
            tiprack = location._get_parent()
        elif isinstance(location, TipRack):
            tiprack = location
        else:
            tiprack = self._get_context()._auto_get_tiprack(n_tip=self.n_channel)

        # validate if tiprack provided or found
        self.__validate_tiprack(tiprack)

        # Get tip location and well name
        if isinstance(location, (Well, Column)):
            tiprack._set_used_tip(location)
            self.__current_tip_location = location
        else:
            self.__current_tip_location = tiprack._get_new_tip(self.n_channel)

        well_name = self.__get_well_name(self.__current_tip_location)

        self._get_context()._append_command(PickUpTipCommand(
            params=PickUpTipParams(
                pipetteId=self.id(), 
                labwareId=self.__current_tip_location._get_parent().id(), 
                wellName=well_name)
        ))
        
        self.__has_tip = True
        self._get_context()._set_arm_location(location)
        return self

    def drop_tip(self, location: Union[Well, Column, None] = None) -> 'Pipette':
        """Drop the tip from the pipette. This method drops the current tip. If a location is specified, the tip is dropped there; otherwise, it is dropped into the trash.

        Args:
            location (Union[Well, Column], optional): The location to drop the tip. Defaults to None, which drops the tip into the trash.
        
        Returns:
            Pipette: The pipette instance.

        Raises:
            ValueError: If the specified location is not part of a tip rack.
        """
        if not self.__has_tip:
            print("Warning: No tip is attached to the pipette. Will ignore this command.")
            return 

        if location is not None:
            # Validate that location is part of a tip rack
            parent = location._get_parent()
            if not isinstance(parent, TipRack):
                raise ValueError("Tips can only be dropped into tip racks or trash. The specified location is not part of a tip rack.")
            
            self.move_to(location,'bottom',(0,0,10))
            self._get_context()._append_command(DropTipInPlaceCommand(params=DropTipParams(pipetteId=self.id())))
        else:
            # drop tip to trash bin
            self._get_context()._append_command(MoveToAreaForDropTipCommand(params=MoveToAreaForDropTipParams(pipetteId=self.id())))
            self._get_context()._append_command(DropTipInPlaceCommand(params=DropTipParams(pipetteId=self.id())))
            self._get_context()._set_arm_location(self._get_context().trash_bin)

        self.__has_tip = False
        self.__current_tip_location = None
        return self
    
    def return_tip(self) -> 'Pipette':
        """Return the current tip to its original location in the tiprack. This is an alias function of pipette.drop_tip(tip_location).

        Returns:
            Pipette: The pipette instance.
        """
        self.drop_tip(self.__current_tip_location)

    def touch_tip(self, 
                  location: Union[Well, Column] = None,
                  position: Literal['top', 'bottom'] = 'top',
                  offset: tuple = (0,0,0)) -> 'Pipette':
        """Touch the pipette tip to the side of a well or column. This method performs a touch tip action, which can help remove droplets from the tip. If no location is specified, the action is performed at the current location.

        Args:
            location (Union[Well, Column], optional): The well or column to touch the tip. Defaults to None for performing the action in place.
            position (str, optional): The position within the well. Wether the 'top' of the well or 'bottom' of the well. Defaults to 'top'.
            offset (int, optional): The x, y, z offset in millimeters for the touch tip operation. Defaults to (0,0,0).

        Returns:
            Pipette: pipette instance
        """
        if location is not None:
            self.move_to(location, position, offset)
        
        if not self.__has_tip:
            raise RuntimeError("No tip is attached to the pipette. Please pick up the tip first.")

        loc = self._get_context()._get_arm_location()
        if isinstance(loc, Column):
            loc = loc.wells()[0]

        self._get_context()._append_command(TouchTipCommand(
            params=TouchTipParams(
                pipetteId=self.id(),
                labwareId=loc._get_parent().id(),
                wellName=loc.id(),
                wellLocation=self.__create_well_location(position, offset)
                )))
        
        return self

    def blow_out(self, location: Union[Well, Column, TrashBin, None] = None,
                 position: Literal['top', 'bottom'] = 'top',
                 offset: tuple = (0,0,0)) -> 'Pipette':
        """Perform a blow out action to expel remaining liquid. This method expels any remaining liquid in the pipette tip. If a location is specified, the action is performed there; otherwise, it's done at the current location.

        Args:
            location (Union[Well, Column, TrashBin], optional): The well or column where the blow out should occur. If TrashBin is passed, it will perform the blow out to the trash bin. Defaults to None for performing the action in place.
            position (str, optional): The position within the well. Wether the 'top' of the well or 'bottom' of the well. Defaults to 'top'.
            offset (int, optional): The x, y, z offset in millimeters from the specified position. Defaults to (0,0,0).
            
        Returns:
            Pipette: The pipette instance after the blow out action.
        """
        if location is None:
            location = self._get_context()._get_arm_location()

            if location is None:
                raise RuntimeError("Cannot locate the current location. Please provide the location params or use move_to command to tell the robot the current location.")
        
        self.move_to(location, position, offset)
        
        if not self.__has_tip:
            raise RuntimeError("No tip is attached to the pipette. Please pick up the tip first.")
        
        self._get_context()._append_command(BlowOutCommand(
            params=BlowOutParams(pipetteId=self.id())))
        
        return self
    
    def air_gap(self, volume):
        """Aspirates air into the pipette tip in place to create an air gap.

        Args:
            volume (float): The volume of air to aspirate, typically in microliters (µL).
        
        Returns:
            Pipette: The pipette instance after the air gap action.
        """
        if not self.__has_tip:
            raise RuntimeError("No tip is attached to the pipette. Please pick up the tip first.")

        if not self._get_context()._get_arm_location():
            raise RuntimeError("Cannot locate the current location. Please provide the location params or use move_to command to tell the robot the current location.")

        tiprack = self.__current_tip_location._get_parent()
        self.__validate_air_gap(volume, tiprack._get_max_volume(), "volume")

        loc = self._get_context()._get_arm_location()
        if isinstance(loc, Column):
            well_name = loc.wells()[0].id()
        elif isinstance(loc, Well):
            well_name = loc.id()

        self._get_context()._append_command(AspirateCommand(
            params=AspirateParams(
                pipetteId=self.id(), 
                volume=volume, 
                labwareId=loc._get_parent().id(), 
                wellName=well_name,
                wellLocation=self.__create_well_location("top", {'x':0, 'y':0, 'z':5})
                )))
    
    def home(self) -> 'Pipette':
        """Home the pipette. This method moves the pipette to the trash bin.

        Returns:
            Pipette: The pipette instance after homing.
        """
        # drop tip include move to trash bin
        # call move to function to gurantee the pipette will go to trash bin if drop tip command is ignored
        self.move_to(self._get_context().trash_bin)
        self.drop_tip()
        return self

    def move_to(self, location: Union[Well, Column, TrashBin],
                position: Literal['top', 'bottom'] = 'top',
                offset: tuple = (0,0,5)) -> 'Pipette':
        """Move the pipette to a specified location. This method moves the pipette to the given well or column or trash bin location.

        Args:
            location (Union[Well, Column, TrashBin]): The target well or column to move to. Also support the moving to the trash bin.
            position (str, optional): The position within the well. Wether the 'top' of the well or 'bottom' of the well. Defaults to 'top'.
            offset (int, optional): The x, y, z offset in millimeters from the specified position. Defaults to (0,0,5).
        
        Returns:
            Pipette: The pipette instance after moving.
        """
        self.__validate_location(location)

        if isinstance(location, TrashBin):
            self._get_context()._append_command(MoveToAreaCommand(
                params=MoveToAreaParams(pipetteId=self.id(),
                                        addressableAreaName='fixedTrash',
                                        offset={'x':offset[0],'y':offset[1],'z':offset[2]})))
        else:
            self._get_context()._append_command(MoveToCommand(
                params=MoveToParams(pipetteId=self.id(),
                                    labwareId=location._get_parent().id(),
                                    wellName=self.__get_well_name(location),
                                    wellLocation=self.__create_well_location(position, offset)))
            )
        
        self._get_context()._set_arm_location(location)
        return self

    def rise(self, 
             position: Literal['top', 'bottom'] = 'top', 
             offset: tuple = (0,0,10)):
        """Rise the pipette to a specified height inplace.

        Args:
            position (str, optional): The position within the well. Wether the 'top' of the well or 'bottom' of the well. Defaults to 'top'.
            offset (tuple, optional): The z, y, x offset in millimeters from the specified position. Defaults to (0,0,10).
        """
        self.move_to(self._get_context()._get_arm_location(), position, offset)

    def __is_single_channel(self):
        """Return true if the pipette is single-channel, false otherwise (multi-channel)

        Returns:
            bool: is single-channel pipette
        """
        return True if self._get_name().endswith('_single') else False
    
    def __validate_location(self, location: Union[Well, Column, Labware, TrashBin]):
        """Validate is the location type match the pipette type.

        Args:
            location (Union[Well, Column, Labware, TrashBin]): location (well or column instance)

        Raises:
            LocationErr: mismatched location and pipette.
        """
        if isinstance(location, TrashBin):
            return  True
        
        if not isinstance(location, (Column, Well, Labware)):
            raise ValueError("Location must be a well, column, labware or trash bin instance.")

        if self.__is_single_channel() and isinstance(location, Column):
            raise LocationErr("Unable to locate column for a single-channel pipette.")
        
        if not self.__is_single_channel() and isinstance(location, Well):
            raise LocationErr("Unable to locate well for a multi-channel pipette.")
        
        # check if anything on top of the labware
        target = location if isinstance(location, Labware) else location._get_parent()
        labware_on_top = self._get_context()._get_labware_on_location(target)
        if labware_on_top is not None:
            raise ValueError("There are labware on top of the location. Please remove the labware first.")
        
        # TOOD: find a better way to check if the irregular labware is compatible with the pipette
        # p200 multi channel pipette cannot be used with irregular labware
        # if self._get_name() == 'p200_multi' and location._get_parent()._is_irregular():
        #     raise ValueError("P200 multi channel pipette cannot be used with irregular labware.")
        
        # check collosion when using p200 single channel pipette (8ch in single channel mode)
        if self._get_name() == 'p200_single':
            if not isinstance(location, TrashBin):
                self._get_context()._check_collision(location)
    
    def _has_tip(self) -> bool:
        """Check if the pipette has a tip.
        
        Returns:
            bool: True if the pipette has a tip, False otherwise.
        """
        return self.__has_tip

    def __create_well_location(self, position: str, offset: tuple) -> dict:
        """Create a well location dictionary with position and offset."""
        return {
            "origin": position,
            "offset": {
                "x": offset[0],
                "y": offset[1],
                "z": offset[2]
            }
        }

    def __get_validated_location(self, location: Union[Well, Column, TrashBin, None]) -> Union[Well, Column, TrashBin]:
        """Get and validate location, using current location if None provided."""
        if location is None:
            location = self._get_context()._get_arm_location()
            if location is None:
                raise RuntimeError("Cannot locate current location. Please provide location or use move_to command.")
        self.__validate_location(location)
        return location