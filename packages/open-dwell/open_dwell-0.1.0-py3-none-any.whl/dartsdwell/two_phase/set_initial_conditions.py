import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

from dartsdwell.two_phase.define_pipe_geometry import PipeGeometry
from dartsdwell.two_phase.define_fluid_model import FluidModel

from dartsdwell.utilities.units import *

g = 9.80665 * meter() / second()**2  # Gravitational acceleration

class SingleAmbientTemperature:
    """
    This class is used when the ambient temperature along the pipe is a single value, and so the temperature of
    the fluid in the pipe does not change along the pipe.
    """
    def __init__(self, pipe_name: str, pipe_geom: PipeGeometry, fluid_model: FluidModel, ambient_temperature: float,
                 pipe_head_pressure: float, pipe_head_segment_index: int, initial_fluid_conditions: dict, verbose: bool = False):
        """
        :param pipe_name: Name of the pipe for which the initial conditions are going to be set
        :type pipe_name: str
        :param pipe_geom: Pipe geometry object
        :type pipe_geom: PipeGeometry
        :param fluid_model: Fluid model is used for density calculations
        :param ambient_temperature: The temperature of the fluid surrounding the pipe
        :type ambient_temperature: float
        :param pipe_head_pressure: Pressure at one of the heads of the pipe the index of which is specified in pip_head_segment_index
        :type pipe_head_pressure: float
        :param pipe_head_segment_index: The index of the segment of the pipe at which the pipe head pressure is specified. The index starts from 0.
        :type pipe_head_segment_index: int
        :param initial_fluid_conditions: Initial fluid conditions in the pipe including the names of the phases present
        in the pipe, the composition of the phases [mole fractions], and the depth intervals of the pipe  in which those
        phases are present [meter].
        :type initial_fluid_conditions: dict consisting three key-value pairs: list of strings, list of lists, list of lists
        :param verbose: Whether to display extra info about SingleAmbientTemperature
        :type verbose: boolean
        :return: Initial pressure and temperature profile along the pipe
        """
        assert pipe_name == pipe_geom.pipe_name, \
            "Pipe names for PipeGeometry and SingleAmbientTemperature are not identical!"
        self.pipe_name = pipe_name
        self.pipe_geom = pipe_geom
        self.fluid_model = fluid_model
        self.ambient_temperature = ambient_temperature
        self.pipe_head_pressure = pipe_head_pressure
        self.pipe_head_segment_index = pipe_head_segment_index

        for phase_composition in initial_fluid_conditions['phases_compositions']:
            assert sum(phase_composition) == 1, "Summation of initial fluid mole fractions must be equal to 1!"
            assert len(phase_composition) == fluid_model.num_components, "Number of specified initial fluid mole fractions must be equal to the number of components in the fluid!"
        self.initial_fluid_conditions = initial_fluid_conditions

        self.measured_depths_segments = sum(self.pipe_geom.segments_lengths) - self.pipe_geom.z
        self.measured_depths_interfaces = sum(self.pipe_geom.segments_lengths) - np.cumsum(self.pipe_geom.segments_lengths[:-1])
        self.true_vertical_depths_segments = self.measured_depths_segments * np.cos(pipe_geom.inclination_angle_radian)
        self.true_vertical_depths_interfaces = self.measured_depths_interfaces * np.cos(pipe_geom.inclination_angle_radian)

        # Get initial conditions
        self.get_initial_temperature_profile()
        self.get_initial_pressure_profile()

        if verbose:
            print("** Initial conditions (SingleAmbientTemperature) of the pipe \"%s\" are set!" % pipe_name)

    def get_initial_temperature_profile(self):
        num_segments = self.pipe_geom.num_segments
        self.temp_init_segments = self.ambient_temperature * np.ones(num_segments)

    def get_initial_pressure_profile(self):
        def dpdz(TVE, p):
            for i, interval in enumerate(self.initial_fluid_conditions['pipe_intervals']):
                if interval[0] <= TVE <= interval[1]:
                    phase_name = self.initial_fluid_conditions['phases_names'][i]
                    initial_phase_composition = self.initial_fluid_conditions['phases_compositions'][i]

            density = self.fluid_model.density_eval[phase_name].evaluate(p, temp, initial_phase_composition)

            return - g * density

        p_head2 = self.pipe_head_pressure   # Initial solution for the ODE
        if self.pipe_head_segment_index == self.pipe_geom.num_segments - 1:
            TVE_head1 = self.pipe_geom.z[0] * np.cos(self.pipe_geom.inclination_angle_radian)   # TVE stands for true vertical elevation
            TVE_head2 = sum(self.pipe_geom.segments_lengths) * np.cos(self.pipe_geom.inclination_angle_radian)   # TVE of the initial solution p_head2
            TVE_seg_interfaces = self.pipe_geom.z_seg_interfaces * np.cos(self.pipe_geom.inclination_angle_radian)
            TVE_seg_face = np.append(TVE_seg_interfaces, TVE_head2)

            TVE_seg_face = TVE_seg_face[::-1]

            temp = self.ambient_temperature
            # Seg and face together
            sol_seg_face = solve_ivp(dpdz, [TVE_head2, TVE_head1], [p_head2], t_eval=TVE_seg_face)
            p_seg_interfaces = sol_seg_face.y[0]

            p_seg_interfaces = p_seg_interfaces[::-1]

        elif self.pipe_head_segment_index == 0:
            TVE_head1 = sum(self.pipe_geom.segments_lengths) * np.cos(self.pipe_geom.inclination_angle_radian)
            TVE_head2 = self.pipe_geom.z[0] * np.cos(self.pipe_geom.inclination_angle_radian)   # TVE of the initial solution (p_head2)
            TVE_seg_interfaces = self.pipe_geom.z_seg_interfaces * np.cos(self.pipe_geom.inclination_angle_radian)
            TVE_seg_face = np.append(TVE_seg_interfaces, TVE_head1)

            temp = self.ambient_temperature
            # Seg and face together
            sol_seg_face = solve_ivp(dpdz, [TVE_head2, TVE_head1], [p_head2], t_eval=TVE_seg_face)
            p_seg_interfaces = sol_seg_face.y[0]

        self.p_init_segments = p_seg_interfaces[0::2]
        p_init_interfaces = p_seg_interfaces[1::2]   # Pressures at interfaces are calculated. Maybe, they'll be used later.


class LinearAmbientTemperature:
    """
    This class is used when the ambient temperature along the pipe changes linearly, and so the temperature of
    the fluid in the pipe changes linearly.
    """
    def __init__(self, pipe_name: str, pipe_geom: PipeGeometry, fluid_model: FluidModel, pipe_head_pressure: float,
                 pipe_head_temperature: float, temp_grad: float, pipe_head_segment_index: int, initial_fluid_conditions: dict,
                 verbose: bool = False):
        """
        :param pipe_name: Name of the pipe for which the initial conditions are going to be set
        :type pipe_name: str
        :param pipe_geom: Pipe geometry object
        :type pipe_geom: PipeGeometry
        :param fluid_model: Fluid model is used for density calculations
        :param pipe_head_pressure: Pressure at one of the heads of the pipe the index of which is specified in pip_head_segment_index [Pa]
        :type pipe_head_pressure: float
        :param pipe_head_temperature: Temperature at one of the heads of the pipe the index of which is specified in pip_head_segment_index [Kelvin]
        :type pipe_head_temperature: float
        :param temp_grad: Temperature gradient [Kelvin/meter]
        :type temp_grad: float
        :param pipe_head_segment_index: The index of the segment of the pipe at which the pipe head pressure is specified. The index starts from 0.
        :type pipe_head_segment_index: int
        :param initial_fluid_conditions: Initial fluid conditions in the pipe including the names of the phases present
        in the pipe, the composition of the phases [mole fractions], and the depth intervals of the pipe  in which those
        phases are present [meter].
        :type initial_fluid_conditions: dict consisting three key-value pairs: list of strings, list of lists, list of lists
        :param verbose: Whether to display extra info about LinearAmbientTemperature
        :type verbose: boolean
        :return: Initial pressure and temperature profile along the pipe
        """
        assert pipe_name == pipe_geom.pipe_name, \
            "Pipe names for PipeGeometry and LinearAmbientTemperature are not identical!"
        self.pipe_name = pipe_name
        self.pipe_geom = pipe_geom
        self.fluid_model = fluid_model
        self.pipe_head_pressure = pipe_head_pressure
        self.pipe_head_temperature = pipe_head_temperature
        self.temp_grad = temp_grad
        self.pipe_head_segment_index = pipe_head_segment_index

        for phase_composition in initial_fluid_conditions['phases_compositions']:
            assert sum(phase_composition) == 1, "Summation of initial fluid mole fractions must be equal to 1!"
            assert len(phase_composition) == fluid_model.num_components, "Number of specified initial fluid mole fractions must be equal to the number of components in the fluid!"
        self.initial_fluid_conditions = initial_fluid_conditions

        self.measured_depths_segments = sum(self.pipe_geom.segments_lengths) - self.pipe_geom.z
        self.measured_depths_interfaces = sum(self.pipe_geom.segments_lengths) - np.cumsum(self.pipe_geom.segments_lengths[:-1])
        self.true_vertical_depths_segments = self.measured_depths_segments * np.cos(pipe_geom.inclination_angle_radian)
        self.true_vertical_depths_interfaces = self.measured_depths_interfaces * np.cos(pipe_geom.inclination_angle_radian)

        # Get initial conditions
        self.get_initial_temperature_profile()
        self.get_initial_pressure_profile()

        if verbose:
            print("** Initial conditions (LinearAmbientTemperature) of the pipe \"%s\" are set!" % pipe_name)

    def get_initial_temperature_profile(self):
        print("Pipe head temperature is assumed to be the lowest temperature for the initial temperature calculation. "
              "If it's the opposite, change the sign of the temperature gradient.")
        self.temp_init_segments = np.array(self.pipe_head_temperature + self.temp_grad * self.true_vertical_depths_segments)
        self.temp_init_interfaces = np.array(self.pipe_head_temperature + self.temp_grad * self.true_vertical_depths_interfaces)  # Temperatures at interfaces are calculated even though they're not used in any part of the code.

        temp_init_seg_interfaces = np.zeros(self.pipe_geom.num_segments + self.pipe_geom.num_interfaces)
        temp_init_seg_interfaces[0::2] = self.temp_init_segments
        temp_init_seg_interfaces[1::2] = self.temp_init_interfaces
        self.temp_init_seg_interfaces = temp_init_seg_interfaces  # This is used to calculate pressures at segments and interfaces together even though the pressure values at interfaces are not used in any part of the code, but this variable is used for calculating initial pressure profile along the wellbore more easily.

    def get_initial_pressure_profile(self):
        def dpdz(TVE, p):
            for i, interval in enumerate(self.initial_fluid_conditions['pipe_intervals']):
                if interval[0] <= TVE <= interval[1]:
                    temp = temp_func(TVE)
                    phase_name = self.initial_fluid_conditions['phases_names'][i]
                    initial_phase_composition = self.initial_fluid_conditions['phases_compositions'][i]

            density = self.fluid_model.density_eval[phase_name].evaluate(p, temp, initial_phase_composition)

            return - g * density

        p_head2 = self.pipe_head_pressure   # Initial solution for the ODE
        if self.pipe_head_segment_index == self.pipe_geom.num_segments - 1:
            TVE_head1 = self.pipe_geom.z[0] * np.cos(self.pipe_geom.inclination_angle_radian)   # TVE stands for true vertical elevation
            TVE_head2 = sum(self.pipe_geom.segments_lengths) * np.cos(self.pipe_geom.inclination_angle_radian)   # TVE of the initial solution p_head2
            TVE_seg_interfaces = self.pipe_geom.z_seg_interfaces * np.cos(self.pipe_geom.inclination_angle_radian)
            TVE_seg_face = np.append(TVE_seg_interfaces, TVE_head2)

            TVE_seg_face = TVE_seg_face[::-1]

            temp_init_seg_interfaces = np.append(self.temp_init_seg_interfaces, self.pipe_head_temperature)
            temp_init_seg_interfaces = temp_init_seg_interfaces[::-1]
            temp_func = interp1d(TVE_seg_face, temp_init_seg_interfaces, fill_value='extrapolate')

            # Seg and face together
            sol_seg_face = solve_ivp(dpdz, [TVE_head2, TVE_head1], [p_head2], t_eval=TVE_seg_face)
            p_seg_interfaces = sol_seg_face.y[0]

            p_seg_interfaces = p_seg_interfaces[::-1]

        elif self.pipe_head_segment_index == 0:
            TVE_head1 = sum(self.pipe_geom.segments_lengths) * np.cos(self.pipe_geom.inclination_angle_radian)
            TVE_head2 = self.pipe_geom.z[0] * np.cos(self.pipe_geom.inclination_angle_radian)   # TVE of the initial solution (p_head2)
            TVE_seg_interfaces = self.pipe_geom.z_seg_interfaces * np.cos(self.pipe_geom.inclination_angle_radian)
            TVE_seg_face = np.append(TVE_seg_interfaces, TVE_head1)

            temp_init_seg_interfaces = np.append(self.temp_init_seg_interfaces, self.pipe_head_temperature)
            temp_func = interp1d(TVE_seg_face, temp_init_seg_interfaces, fill_value='extrapolate')

            # Seg and face together
            sol_seg_face = solve_ivp(dpdz, [TVE_head2, TVE_head1], [p_head2], t_eval=TVE_seg_face)
            p_seg_interfaces = sol_seg_face.y[0]

        self.p_init_segments = p_seg_interfaces[0::2]
        p_init_interfaces = p_seg_interfaces[1::2]   # Pressures at interfaces are calculated. Maybe, they'll be used later.
