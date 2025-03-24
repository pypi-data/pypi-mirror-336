#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2023-2025 Alexis Pietak.
# See "LICENSE" for further details.

'''
This module defines a parameters object for variables used in models of adaptation to osmotic and bioelectric stress.
'''

from beartype import beartype
from dataclasses import dataclass
import numpy as np

@dataclass
class ModelParams(object):
    '''
    Default parameter initialization and storage class for use in
    osmoelectric and bioelectrical system modeling.

    '''

    def __init__(self):

        self.R: float = 8.314  # Ideal gas constant [J/(K*mol)]
        self.F: float = 96485.0  # Faraday's Constant [C/mol]S
        self.e_o: float = 8.3145e-12  # Electric permittivity free space [F/m]
        self.T_C: float = 37.0 # Temp in degrees C

        # Osmoelectric model variables----------------------------------------------------------------------------------
        self.mu: float = 1.0e-3 # Dynamic viscosity of water Pa*s

        self.plant_model: bool = False # Use model of plant cell wall or of a cell with plasma membrane only?

        # Dimensions and geometrical aspects of cell
        self.r_cell_o: float = 10e-6 # undeformed cell radius
        self.L_cell_o: float = 10e-6 # undeformed cell length

        self.d_mem: float = 5.0e-9 # Cell membrane thickness
        self.d_wall: float = 100.0e-9 # Cell wall thickness (yeast)
        self.d_plant: float = 1.0e-6 # Cell wall thickness (plants)

        self.breaking_strain = 0.8 # Breaking strain for yeast cell wall

        # Stress-strain moduli
        self.Y_mem: float = 50e3  # Cell membrane Young's modulus (Pa)
        self.nu_f: float = 0.5 # General Poisson Ratio for simplified expressions
        self.nu_mem: float = 0.45  # Cell membrane Poisson ratio
        self.Y_wall: float = 110e6  # Cell wall Young's modulus of yeast (Pa)
        self.Y_plant: float = 350e6  # Cell wall Young's modulus of a plant (Pa)
        self.nu_wall: float = 0.2  # Cell wall Poisson ratio

        # Initialization of osmolytes
        self.m_i_base: float = 230.0 # Base concentration of non-glycerol osmolytes
        self.m_i_gly: float = 50.0 # Initial concentration of glycerol in the cell
        self.m_o_base: float = 175.0 # Base concentration of osmoyltes in the env

        # Features of glycerol/water channels
        self.N_chan_o = 0.12e6 # approximate number of water/glycerol channels expressed in membrane
        # self.chan_cover_o: float = 0.002  # fraction of cell covered by water/glycerol Fsp1 channels; response time of H2O flux

        # Production and export of intracellular glycerol
        # self.chan_rate_gly: float = 5.0e-11  # Transport coefficient for glycerol/water channels (Fsp1) m^2 s
        self.r_gly_max: float = 0.5 # Maximum rate of glycerol production by cell (mol/(m^3 s))
        self.d_gly_max: float = 0.003

        # Adaptive control parameters
        self.K_1: float = 15.0 # Slope constant of the Sln1 strain-sensor
        self.epsilon_o_1: float = -0.05 # midpoint strain of the Sln1 strain-sensor; chosen so strain in isotonic is zero
        self.b_1: float = 0.0 # minimum level of activation

        self.K_2: float = 15.0 # Slope constant of the Sln1 strain-sensor
        self.epsilon_o_2: float = -0.05 # midpoint strain of the Sln1 strain-sensor; chosen so strain in isotonic is zero
        self.b_2: float = 0.0 # minimum level of inhibition

        # self.ka_sln1 = 0.5  # value of sln1 activation response that is 1/2 max activation
        # self.ki_sln1 = 0.5  # value of sln1 inhibition response that is 1/2 max inhibition
        # self.na_sln1 = 5.0  # exponent dictating the slope/shape of activation by sln1
        # self.ni_sln1 = 5.0  # exponent dictating the slope/shape of inhibition by sln1


        # Bioelectric model variables-----------------------------------------------------------------------------------

        # constant to convert to normalized concentrations in units mol/L for consistency with thermodynamic params:
        self.c_norm = 1e3

        # Initialize to human blood plasma:
        self.cNa_i: float = 12.0
        self.cNa_o: float = 140.0

        self.cK_i: float = 135.0
        self.cK_o: float = 4.0

        self.cCl_i: float = 4.0
        self.cCl_o: float = 116.0

        self.cATP: float = 4.0
        self.cADP: float = 0.1
        self.cPi: float = 0.1
        self.PATP = 1.0 # Rate constant for ATP hydrolysis reaction

        self.delG_ATP = -32e3  # Gibbs free energy for ATP hydrolysis in J

        # Membrane permittivities and reaction rate constants:
        self.base_pmem: float = 1.0e-9

        self.base_PNa: float = 1.0
        self.base_PK: float = 5.0
        self.base_PCl: float = 1.0

        self.base_NaKpump: float = 4.0e5
        self.base_NaKCl: float = 2.0e4
        self.base_KCl: float = 1.0e4

        self.r_cell_um: float = 7.5
        self.d_mem: float = 5.0e-9
        self.d_ecm: float = 25e-9
        self.e_mem: float = 10.0

        self.vmemo = 0.0  # initial Vmem in mV

        # Network plotting options:--------------------------------------
        self.net_font_name = 'DejaVu Sans'
        self.node_font_size = 16
        self.tit_font_size = 24
        self.net_layout = 'TB'
        self.edge_width = 2.0

        self.conc_node_font_color = 'Black'
        self.conc_node_color = 'PaleTurquoise' #'LightCyan'
        self.anion_node_color = 'PaleTurquoise'
        self.cation_node_color = 'LightSalmon'
        self.neutral_node_color = 'Silver'
        self.conc_node_shape = 'ellipse'

        self.react_node_font_color = 'White'
        self.react_node_color = 'Gunmetal' # 'DarkSeaGreen'
        self.react_node_shape = 'rect'

        self.transp_node_font_color = 'White'
        self.transp_node_color = 'DarkSeaGreen'
        self.transp_node_shape = 'diamond'

        self.chan_node_font_color = 'White'
        self.chan_node_color = 'DarkSeaGreen'
        self.chan_node_shape = 'pentagon'

        self.update_parameters() # Calculate all computed properties

    def update_parameters(self):
        '''
        Recalculate calculated params after updating some settings.
        '''

        self.T = self.T_C + 273.15 # Temp in Kelvin
        self.cmem = (self.e_o * self.e_mem) / self.d_mem  # membrane capacitance
        self.r_cell = self.r_cell_um*1.0e-6

        self.vol_cell_o = self.r_cell_o * np.pi * 2 * self.L_cell_o # undeformed cell volume (assumes cylinder shape)
        self.A_cell_o = 2 * np.pi * self.r_cell_o * self.L_cell_o # Undeformed cell surface area
        self.m_i_o = self.m_i_base + self.m_i_gly # Initial concentration of osmoyltes in the cell
        self.n_i_o = self.m_i_o * self.vol_cell_o  # Initial osmolyte moles in the cell
        self.n_i_base = self.m_i_base*self.vol_cell_o # Initial moles of other osmolytes in the cell
        self.n_i_gly = self.m_i_gly*self.vol_cell_o # Initial glycerol moles in the cell

        # Water channel calculated properties
        self.A_chan_o = np.pi * (1.0e-9) ** 2 # Maximum area of glyceroaquaporin Fsp1 water/glycerol channel


        # Maximum decay rate of glycerol via Fsp1 channel function (1/s):
        # self.decay_gly_max = (self.A_chan_o * self.N_chan_o) / self.chan_rate_gly

        # Electrodiffusion permittivity constants:
        self.PNa = self.base_pmem * self.base_PNa
        self.PK = self.base_pmem * self.base_PK
        self.PCl = self.base_pmem * self.base_PCl

        # Ion pump rate constants:
        self.PNaK_ATPase = self.base_pmem * self.base_NaKpump

        # Transporter rate constants:
        self.PNaKCl = self.base_pmem * self.base_NaKCl
        self.PKCl = self.base_pmem * self.base_KCl


