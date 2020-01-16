import streamlit as st
import numpy as np
import pandas as pd
import time

st.title('ICS Module 3 Testing Simulator')
st.markdown('Please choose your vehicle configuration below, and click the button to commence testing.')
st.markdown('Each test takes 1.67 seconds to complete. 1000 tests will take 10 minutes.')

# creating the multi-level row indices per the Dragonfly Component Tradeoff Matrix
# active power data not currently included
engine_index = pd.MultiIndex.from_tuples([('engine_size', 'weight'), ('engine_size', 'speed'), ('engine_size', 'cost')])
frame_index = pd.MultiIndex.from_tuples([('frame', 'weight'), ('frame', 'survivability'), ('frame', 'cost')])
armor_index = pd.MultiIndex.from_tuples([('armor', 'weight'), ('armor', 'survivability'), ('armor', 'cost')])

# creating the multi-level column indices per the Dragonfly Component Tradeoff Matrix
wheeled_engine_columns = pd.MultiIndex.from_product([['wheeled_small_frame', 'wheeled_medium_frame', 'wheeled_large_frame'],
                            ['small', 'medium', 'large']])
wheeled_frame_columns = pd.MultiIndex.from_product([['wheeled_small_frame', 'wheeled_medium_frame', 'wheeled_large_frame'],
                            ['aluminum', 'composite', 'titanium']])
wheeled_armor_columns = pd.MultiIndex.from_product([['wheeled_small_frame', 'wheeled_medium_frame', 'wheeled_large_frame'],
                            ['none', 'steel', 'tungsten']])

tracked_engine_columns = pd.MultiIndex.from_product([['tracked_small_frame', 'tracked_medium_frame', 'tracked_large_frame'],
                            ['small', 'medium', 'large']])
tracked_frame_columns = pd.MultiIndex.from_product([['tracked_small_frame', 'tracked_medium_frame', 'tracked_large_frame'],
                            ['aluminum', 'composite', 'titanium']])
tracked_armor_columns = pd.MultiIndex.from_product([['tracked_small_frame', 'tracked_medium_frame', 'tracked_large_frame'],
                            ['none', 'steel', 'tungsten']])

hover_engine_columns = pd.MultiIndex.from_product([['hover_small_frame', 'hover_medium_frame', 'hover_large_frame'],
                            ['small', 'medium', 'large']])
hover_frame_columns = pd.MultiIndex.from_product([['hover_small_frame', 'hover_medium_frame', 'hover_large_frame'],
                            ['aluminum', 'composite', 'titanium']])
hover_armor_columns = pd.MultiIndex.from_product([['hover_small_frame', 'hover_medium_frame', 'hover_large_frame'],
                            ['none', 'steel', 'tungsten']])

# data from the Dragonfly matrix, except for active power for the engines
wheeled_engine_data = [[695, 756, 895, 705, 756, 895, 715, 756, 895],
                       [30, 35, 40, 25, 30, 35, 20, 25, 30],
                       [278, 347.5, 417, 347.5, 417, 486.5, 417, 486.5, 556]]
wheeled_frame_data = [[224, 317, 405, 220, 320, 420, 240, 340, 440],
                      [80, 110, 140, 100, 110, 120, 110, 120, 130],
                      [417, 486.5, 556, 486.5, 556, 625.5, 556, 625.5, 695]]
wheeled_armor_data = [[0, 135, 380, 0, 140, 380, 0, 145, 380],
                      [0, 85, 250, 0, 90, 250, 0, 95, 250],
                      [0, 417, 486.5, 0, 486.5, 556, 0, 556, 625.5]]

tracked_engine_data = [[705, 775, 910, 715, 785, 920, 725, 795, 930],
                       [14, 16, 18, 12, 14, 16, 10, 12, 14],
                       [417, 486.5, 556, 486.5, 556, 625.5, 556, 625.5, 695]]
tracked_frame_data = [[200, 300, 400, 210, 310, 410, 220, 320, 420],
                      [70, 100, 130, 75, 105, 135, 80, 110, 140],
                      [556, 625.5, 695, 625.5, 695, 764.5, 556, 625.5, 695]]
tracked_armor_data = [[0, 130, 370, 0, 135, 380, 0, 140, 390],
                      [0, 80, 240, 0, 85, 250, 0, 90, 260],
                      [0, 556, 625.5, 0, 625.5, 695, 0, 695, 764.5]]

hover_engine_data = [[670, 735, 885, 675, 750, 895, 680, 765, 905],
                       [25, 30, 35, 20, 25, 30, 15, 20, 25],
                       [347.5, 417, 486.5, 417, 486.5, 556, 486.5, 556, 625.5]]
hover_frame_data = [[220, 310, 400, 225, 315, 405, 230, 320, 410],
                      [75, 105, 135, 80, 110, 140, 85, 115, 145],
                      [486.5, 556, 625.5, 556, 625.5, 695, 625.5, 695, 764.5]]
hover_armor_data = [[0, 125, 175, 0, 130, 180, 0, 135, 185],
                      [0, 75, 200, 0, 80, 225, 0, 85, 250],
                      [0, 486.5, 556, 0, 556, 625.5, 0, 625.5, 695]]

rocket_data = [[0, 42, 43, 44, 45, 46],
               [0, 80, 90, 100, 110, 120],
               [0, 156, 173.5, 191, 208.5, 226]]

minigun_data = [[0, 40, 41, 42, 43, 44],
                [0, 10, 20, 30, 40, 50],
                [0, 138.5, 156, 173.5, 191, 208.5]]

laser_missile_data = [[0, 44, 45, 46, 47, 48],
                      [0, 80, 90, 100, 110, 120],
                      [0, 173.5, 191, 208.5, 226, 243.5]]

grenade_data = [[0, 37, 38, 39, 40, 41],
                [0, 50, 55, 60, 65, 70],
                [0, 103.5, 121, 138.5, 156, 173.5]]

targeting_comp_data = [[0, 41, 43, 45, 47, 49],
                       [0, 1.1, 1.12, 1.15, 1.175, 1.2],
                       [0, 173.5, 191, 208.5, 226, 243.5]]

# creating the dataframes, three per variant
wheeled_engine_df = pd.DataFrame(data=wheeled_engine_data,
             index=engine_index,
             columns=wheeled_engine_columns)

wheeled_frame_df = pd.DataFrame(data=wheeled_frame_data,
             index=frame_index,
             columns=wheeled_frame_columns)

wheeled_armor_df = pd.DataFrame(data=wheeled_armor_data,
             index=armor_index,
             columns=wheeled_armor_columns)

tracked_engine_df = pd.DataFrame(data=tracked_engine_data,
             index=engine_index,
             columns=tracked_engine_columns)

tracked_frame_df = pd.DataFrame(data=tracked_frame_data,
             index=frame_index,
             columns=tracked_frame_columns)

tracked_armor_df = pd.DataFrame(data=tracked_armor_data,
             index=armor_index,
             columns=tracked_armor_columns)

hover_engine_df = pd.DataFrame(data=hover_engine_data,
             index=engine_index,
             columns=hover_engine_columns)

hover_frame_df = pd.DataFrame(data=hover_frame_data,
             index=frame_index,
             columns=hover_frame_columns)

hover_armor_df = pd.DataFrame(data=hover_armor_data,
             index=armor_index,
             columns=hover_armor_columns)

# Create the drop-down menus for user input
chassis = st.selectbox(
	'Select a chassis variant',
	('Tracked', 'Wheeled', 'Hover'))
st.write('You selected ', chassis.lower())

frame_size = st.selectbox(
	'Select a vehicle frame size',
	('Small', 'Medium', 'Large'))
st.write('You selected ', frame_size.lower())

engine_size = st.selectbox(
	'Select an engine size',
	('Small', 'Medium', 'Large'))
st.write('You selected ', engine_size.lower())

frame = st.selectbox(
	'Select a frame material',
	('Aluminum', 'Composite', 'Titanium'))
st.write('You selected ', frame.lower())

armor = st.selectbox(
	'Select armor',
	('None', 'Steel', 'Tungsten'))
st.write('You selected ', armor.lower())

st.markdown('Please select the weapon configuration below.')
st.markdown('MK1 variants provide the lowest performance, while MK5 provides the highest.')
st.markdown('The laser-guided missile requires a targeting computer to be installed in order to obtain higher lethanlity than a free rocket')

rocket = st.selectbox(
	'Rocket variant',
	('None', 'MK1', 'MK2', 'MK3', 'MK4', 'MK5'))
st.write('You selected ', rocket)

minigun = st.selectbox(
	'Minigun variant',
	('None', 'MK1', 'MK2', 'MK3', 'MK4', 'MK5'))
st.write('You selected ', minigun)

laser_guided_missile = st.selectbox(
	'Laser-guided missile variant',
	('None', 'MK1', 'MK2', 'MK3', 'MK4', 'MK5'))
st.write('You selected ', laser_guided_missile)

grenade = st.selectbox(
	'Grenade-launcher variant',
	('None', 'MK1', 'MK2', 'MK3', 'MK4', 'MK5'))
st.write('You selected ', grenade)

targeting_computer = st.selectbox(
	'Targeting computer variant',
	('None', 'MK1', 'MK2', 'MK3', 'MK4', 'MK5'))
st.write('You selected ', targeting_computer)

n_runs = int(st.text_input('Enter the number of tests to perform: ', value='1', key='runs'))

start = st.button('Begin Testing')