import mesa

from .model import PdGrid
from .portrayal import portrayPDAgent

# Make a world that is 50x50, on a 500x500 display.
canvas_element = mesa.visualization.CanvasGrid(portrayPDAgent, 50, 50, 500, 500)

model_params = {
    "height": 50,
    "width": 50,
    "schedule_type": mesa.visualization.Choice(
        "Scheduler type",
        value="Random",
        choices=list(PdGrid.schedule_types.keys()),
    ),
    "radius": mesa.visualization.Slider(
        name="Search Radius", value=1, min_value=1, max_value=25, step=1
    ),
}

server = mesa.visualization.ModularServer(
    PdGrid, [canvas_element], "Prisoner's Dilemma", model_params
)
