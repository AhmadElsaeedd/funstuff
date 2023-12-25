from graphviz import Digraph

# Create a Finite State Machine diagram
fsm = Digraph('finite_state_machine', filename='fsm.gv')
fsm.attr(rankdir='LR', size='24', dpi='600')
fsm.attr('node', shape='circle', fontsize='40')  # Font size for nodes
fsm.attr('edge', fontsize='30')

# States
fsm.attr('node', shape='circle')
fsm.node('S', 'Start')
fsm.node('IU', 'Image Upload')
fsm.node('CI', 'Crop Identification')
fsm.node('DD', 'Disease Diagnosis')
fsm.node('RS', 'Recommendation \n(Disease Specific)')
fsm.node('MA', 'Maintenance Advice')
fsm.node('FR', 'Fertilization Recommendation')
fsm.node('FB', 'Feedback')
fsm.node('E', 'End')

# Transitions
fsm.edge('S', 'IU', label='Upload Image')
fsm.edge('IU', 'CI', label='Image Validated')
fsm.edge('CI', 'DD', label='Crop Identified')
fsm.edge('DD', 'RS', label='Disease Detected')
fsm.edge('DD', 'MA', label='No Disease')
fsm.edge('RS', 'MA', label='Advice Given')
fsm.edge('MA', 'FR', label='Maintenance Tips Provided')
fsm.edge('FR', 'FB', label='Fertilization Suggested')
fsm.edge('FB', 'E', label='Feedback Collected')
fsm.edge('E', 'S', label='Restart/End Session')

fsm.render(directory='capstone', view=False, format='png')