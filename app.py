import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html
import numpy as np

# not sure what this css contains

external_scripts = [
    {"src": "https://cdn.tailwindcss.com"},
]

app = Dash(
    __name__,
    external_scripts=external_scripts,
)

rcem_data = pd.read_csv("rcem_data.csv")
bound_data = pd.read_csv("data.csv")
Ad_bound = pd.read_csv("adeq_data.csv")

to_plot = rcem_data[rcem_data["RCEM data point?"] == "Y"]


def apply_warning(warning):
    if warning == "no warning":
        return "Little or No Warning"
    elif warning == "adequate warning":
        return "Adequate Warning"
    else:
        return "Partial Warning"



ft2s_to_m2s = 0.092903

# transform ft2/s to m2/s
to_plot["DV(m2/s)"] = to_plot["DV(ft2/s)"] * ft2s_to_m2s

to_plot["Warning Category"] = to_plot["Warning"].apply(apply_warning)
pltPartial = to_plot
AdeqWar_plot = to_plot
to_plot = to_plot[to_plot["Warning Category"] == "Little or No Warning"]
# print(to_plot)
pltPartial = pltPartial[pltPartial["Warning Category"] == "Partial Warning"]
TexasHillCT = pltPartial # CREATE TO INCLUDE TEXAS HILL FLOOD ON ADEQUATE OR PARTIAL WARNING GROUPS
# print(pltPartial)
warnings = rcem_data["Warning"].unique()
to_plot = to_plot[to_plot["DV(ft2/s)"] >= 10]

# Delete NAN Values in the FATALITY RATE COLUMN
to_plot = to_plot[~to_plot["Fatality Rate"].isnull()]
# REPLACE ZERO TO ALMOST ZERO (0.00001) BECAUSE OF THE LOG FUNCTION THAT WE USE IN OUR AXES
to_plot["Fatality Rate"] = to_plot["Fatality Rate"].replace(0, 0.00001)
LtlWar_plot = to_plot # STOCK FOR TOGGLING
pltPartial["Fatality Rate"] = pltPartial["Fatality Rate"].replace(0, 0.00001)
# Adequate Warning Plot
AdeqWar_plot = AdeqWar_plot[AdeqWar_plot["Warning Category"] == "Adequate Warning"]
# Delete NAN Values in the FATALITY RATE COLUMN
AdeqWar_plot = AdeqWar_plot[~AdeqWar_plot["Fatality Rate"].isnull()]
AdeqWar_plot ["Fatality Rate"] = AdeqWar_plot ["Fatality Rate"].replace(0, 0.00001)

# wrg_toplt = to_plot["Warning"].unique()

# print(wrg_toplt)
# if "no warning" in wrg_toplt:
#   clr='#8B0000'
#  sym="triangle-up"
# elif "adequate warning" in wrg_toplt:
#   clr='#008000'
#  sym="triangle-up"
# else:
#    clr='#00008B'
# sym="square"
c = ""

app.layout = html.Div(
    className="container mx-auto pt-2 ",
    children=[
        html.Div(
            [
                html.H1(
                    children="RCEM Case Comparison",
                    className="text-2xl text-center",
                ),
                html.Div(
                    children="An application to filter and compare historical RCEM cases",
                    className="text-center",
                ),
            ]
        ),
        html.Div(
            className="flex flex-col gap-4",
            children=[
                html.Div(
                    className="flex flex-row gap-4 mx-auto",
                    children=[
                        # Column 1
                        html.Div(
                            className="bg-gray-50 rounded-md p-2",
                            children=[
                                html.Div(
                                    [
                                        html.P(
                                            children="General",
                                            className="text-2xl text-center",
                                        ),
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    className="group relative w-max font-bold",
                                                    children=[
                                                        "Dam Failure?",
                                                        html.Span(
                                                            className="pointer-events-none absolute bg-white -top-7 left-6 w-max opacity-0 px-2 drop-shadow transition-opacity group-hover:opacity-100",
                                                            #children="Is the case a dam failure or other (like a rainfall flood)?",
                                                        ),
                                                    ],
                                                ),
                                                dcc.Checklist(
                                                    [' Yes ', ' No'],
                                                    [' Yes ', ' No'],
                                                    id="DmFl-toggle",
                                                    className="list-none px-2",
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            children=[
                                                html.Label(
                                                    className="group relative w-max font-bold",
                                                    children="Warning Category",
                                                ),
                                                dcc.RadioItems(
                                                    value=False,
                                                    options=[
                                                        {
                                                            "label": "No or Little Warning    ",
                                                            "value": False,
                                                        },
                                                        {
                                                            "label": "Adequate Warning",
                                                            "value": True,
                                                        },
                                                    ],
                                                    id="label-toggle",
                                                    #inputClassName="mr-1",
                                                    className="px-2",
                                                    inputClassName="mr-1 pl-2 rounded-full border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-offset-0 focus:ring-indigo-200 focus:ring-opacity-50",
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        # Column 2
                        html.Div(
                            className="bg-gray-50 rounded-md p-2 flex flex-col",
                            children=[
                                html.P(
                                    className="text-2xl text-center",
                                    children="Dam",
                                ),
                                html.Label(
                                    className="font-bold",
                                    children="Dam Type",
                                ),
                                dcc.Checklist(
                                    ['Concrete', ' Earthfill or Composite'],
                                    ['Concrete', ' Earthfill or Composite'],
                                    id="type-toggle",
                                    inputClassName="mr-1",
                                    className="px-2",
                                ),
                                # dcc.Dropdown(
                                #     ["Concrete", "Earthfill or Composite"],
                                #     ["Concrete", "Earthfill or Composite"],
                                #     multi=True,
                                #     id="type-toggle",
                                # ),
                                html.Label(
                                    className="font-bold",
                                    children="Height of Dam (ft)",
                                ),
                                dcc.Input(
                                    id="input-Min",
                                    type="number",
                                    placeholder="Enter Min",
                                    min=1,
                                    className="mt-1 block w-full p-1 pl-2  rounded-md border-gray-950 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                                ),
                                dcc.Input(
                                    id="input-Max",
                                    type="number",
                                    placeholder="Enter Max",
                                    max=2000,
                                    className="mt-1 block w-full p-1 pl-2  rounded-md border-gray-950 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                                ),
                                html.Label(
                                    className="font-bold",
                                    children="Reservoir Storage (ac-ft)",
                                ),
                                dcc.Input(
                                    id="VRS-Min",
                                    type="number",
                                    placeholder="Enter Min",
                                    min=1,
                                    className="mt-1 block w-full p-1 pl-2  rounded-md border-gray-950 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                                ),
                                dcc.Input(
                                    id="VRS-Max",
                                    type="number",
                                    placeholder="Enter Max",
                                    max=9000000,
                                    className="mt-1 block w-full p-1 pl-2  rounded-md border-gray-950 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                                ),
                                html.Label(
                                    className="font-bold",
                                    children="Mode of failure",
                                ),
                                dcc.Checklist(
                                    ['Hydrologic', ' Static'],
                                    ['Hydrologic', ' Static'],
                                    id="Mode-checked",
                                    inputClassName="mr-1",
                                    className="px-2",
                                ),
                            ],
                        ),
                        html.Div(
                            className="bg-gray-50 rounded-md p-2 flex flex-col",
                            children=[
                                html.P(
                                    className="text-2xl text-center",
                                    children="Population",
                                ),
                                html.Label(
                                    className="font-bold",
                                    children="Population at Risk (PAR)",
                                ),
                                dcc.Input(
                                    id="inputPAR-Min", 
                                    type="number", 
                                    placeholder="Enter Min PAR", 
                                    min=0,
                                    className="mt-1 block w-full p-1 pl-2  rounded-md border-gray-950 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                                    ),
                                dcc.Input(
                                    id="inputPAR-Max",
                                    type="number", 
                                    placeholder="Enter Max PAR",
                                    min=1,
                                    className="mt-1 block w-full p-1 pl-2  rounded-md border-gray-950 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                                    ),
                                html.Label(
                                    className="font-bold",
                                    children="Distance to Downstream PAR (miles)",
                                ),
                                dcc.Input(
                                    id="inputDDis-Min",
                                    type="number", 
                                    placeholder="Enter Min",
                                    min=0,
                                    className="mt-1 block w-full p-1 pl-2  rounded-md border-gray-950 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                                ),
                                dcc.Input(
                                    id="inputDDis-Max", 
                                    type="number", 
                                    placeholder="Enter Max",
                                    min=1,
                                    className="mt-1 block w-full p-1 pl-2  rounded-md border-gray-950 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                                ),
                                html.Label(
                                    className="font-bold",
                                    children="Time of the Catastrophe",
                                ),
                                dcc.Checklist(
                                    ['Day', ' Night'],
                                    ['Day', ' Night'],
                                    id="Time-checked",
                                    inputClassName="mr-1",
                                    className="px-2",
                                ),
                            ],
                        ),
                        html.Div(
                            className="bg-gray-50 rounded-md p-2",
                            children=[
                                html.P(
                                    className="text-2xl text-center",
                                    children="Floodplain",
                                ),
                                html.Label(
                                    className="font-bold",
                                    children="Floodplain Type",
                                ),
                                dcc.Checklist(
                                    ['Narrow', ' Wide'],
                                    ['Narrow', ' Wide'],
                                    id="FLP-toggle",
                                    className="px-2",
                                    inputClassName="mr-1",
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="bg-white rounded-md p-2",
                    children=[
                        html.P(
                            id="graph-title",
                            className="text-2xl text-center",
                            children=" ",
                        ),
                        html.Br(
                            # 
                        ),
                        dcc.Graph(
                            className="flex aspect-[345/217] max-h-[75vh] mx-auto",
                            id="graph-output",
                            config={
                                "displaylogo": False,
                                #"toImageButtonOptions": {
                                   # "format": "svg",  # one of png, svg, jpeg, webp
                                   # "filename": "custom_image",
                                    #"height": 500,
                                    #"width": 200,
                                   # "scale": 0.01,
                                     # Multiply title/legend/axis/canvas sizes by this factor
                               # },
                            },
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            id="table-container",
            className="h-[800px] min-h-[800px] pt-2 ",
        ),
    ],
)


@callback(
    #Output("my-output", "src"), 
    Output("table-container", "children"),Input("graph-output", "clickData"),prevent_initial_call=False
)

def update_output_div(clickData):
    if clickData is None:
        return html.Iframe(id="1", src="assets/RCEM-CaseHistories20140304.pdf#page=1", style={"display":"inherit","width":"100%","height":"800px"}) 
    try:
        clicked_case_name = clickData["points"][0]["customdata"][0]
        case_data = rcem_data.loc[rcem_data["Case Name"] == clicked_case_name].to_dict("records")[0] 
        pge = case_data["Page Number"]
    except:
        clicked_case_dv = clickData["points"][0]["x"]
        clicked_case_ft = clickData["points"][0]["y"]
        filterPart = pltPartial[pltPartial["DV(ft2/s)"] == clicked_case_dv]
        clicked_case_name  = filterPart.loc[filterPart["Fatality Rate"] == clicked_case_ft].to_dict("records")[0] 
        pge = clicked_case_name["Page Number"]
    
    print(pge)
    NewId = str(pge)
    pge = "RCEM-CaseHistories20140304.pdf#page="+str(pge)
    #print(f"assets/{pge}")
    #print(f"{NewId}")
    return html.Iframe(id=f"{NewId}", src=f"assets/{pge}", style={"display":"inherit","width":"100%","height":"800px"})

# CALLBACKS FOR SETTING NEW MIN AND MAX VALUES FOR THE DAM HEIGHT INPUTS BOXES
@callback(
    #Output("my-output", "src"), 
    Output("input-Min", "max"),
    Input("input-Max", "value"),prevent_initial_call=False
)
def Update_inpMin(inputMax):
    if inputMax==None:
        return inputMax

@callback(
    #Output("my-output", "src"), 
    Output("input-Max", "min"),
    Input("input-Min", "value"),prevent_initial_call=False
)
def Update_inpMax(inputMin):
    if inputMin==None:
        return 1
    else:
        return inputMin
# CALLBACKS FOR SETTING NEW MIN AND MAX VALUES FOR THE DAM RESERVOIR STORAGE (AC-FEET) INPUTS BOXES
@callback(
    #Output("my-output", "src"), 
    Output("VRS-Min", "max"),
    Input("VRS-Max", "value"),prevent_initial_call=False
)
def Update_inpMin(VRSMax):
    if VRSMax==None:
        return VRSMax

@callback(
    #Output("my-output", "src"), 
    Output("VRS-Max", "min"),
    Input("VRS-Min", "value"),prevent_initial_call=False
)
def Update_inpMax(VRSMin):
    if VRSMin==None:
        return 1
    else:
        return VRSMin

# CALLBACKS FOR SETTING NEW MIN AND MAX VALUES FOR THE POPULATION AT RISK INPUTS BOXES
@callback(
    #Output("my-output", "src"), 
    Output("inputPAR-Min", "max"),
    Input("inputPAR-Max", "value"),prevent_initial_call=False
)
def Update_inpPARMin(inputMax):
    return inputMax

@callback(
    #Output("my-output", "src"), 
    Output("inputPAR-Max", "min"),
    Input("inputPAR-Min", "value"),prevent_initial_call=False
)
def Update_inpPARMax(inputMin):
    if inputMin==None:
        return 1
    else:
        return inputMin

# CALLBACKS FOR SETTING NEW MIN AND MAX VALUES FOR THE DOWNSTREAM DISTANCE TO THE PAR INPUTS BOXES
@callback(
    #Output("my-output", "src"), 
    Output("inputDDis-Min", "max"),
    Input("inputDDis-Max", "value"),prevent_initial_call=False
)
def Update_inpDDISMin(inputMax):
    return inputMax

@callback(
    #Output("my-output", "src"), 
    Output("inputDDis-Max", "min"),
    Input("inputDDis-Min", "value"),prevent_initial_call=False
)
def Update_inpDDISMax(inputMin):
    if inputMin==None:
        return 1
    else:
        return inputMin
@callback(
    Output("graph-title", "children"),
    
    # Input("warning-filter", "value"),
    Input("label-toggle", "value"),
)
def update_graph(label_toggle):
    if label_toggle:
        return f"Case History Data Identified for Cases with Adequate Warning and Cases with Partial Warning",
    else:
        return f"Case History Data Identified for Cases with Little or No Warning  and Cases with Partial Warning",

@callback(
    Output("graph-output", "figure"),
    # Input("warning-filter", "value"),
    Input("label-toggle", "value"),
    Input("DmFl-toggle", "value"),
    # Input to display concrete or earthfill dams (Check list)
    Input("type-toggle", "value"),
    # Inputs to filter dams according to height range
    Input("input-Min", "value"),
    Input("input-Max", "value"),
    # Inputs to filter dams according to the number of population at risk downstream
    Input("inputPAR-Min", "value"),
    Input("inputPAR-Max", "value"),
    # Inputs to filter dams according to the downstream distance to the PAR
    Input("inputDDis-Min", "value"),
    Input("inputDDis-Max", "value"),
    # Inputs to filter dams according to the reservoir storage
    Input("VRS-Min", "value"),
    Input("VRS-Max", "value"),
    # Inputs to filter dams according to the mode of failure
    Input("Mode-checked", "value"),
    # Inputs to filter dams according to the time of failure
    Input("Time-checked", "value"),
    # Inputs to filter dams according to the time of failure
    Input("FLP-toggle", "value"),
    
)
def update_graph(label_toggle,DmFl_toggle,type_toggle,input_Min,input_Max,MinPAR,MaxPAR,DDMIN,DDMAX,VRSMin, VRSMax,MChecked,TIMECH,FLPCHK):
    if label_toggle:
        Choose_plot = AdeqWar_plot
        COULR = "#00C000",
        NO_W_LWDTH = [0,0],
        AD_W_LWDTH = [5,3],
        LGD_No = False,
        LGD_Ad = True,
        NAMEIT = "<b> Cases with Adequate Warning </b> ",
        TxHFL = "Texas Hill Country Flood",
        BRUSHFL = " ",
    else:
        Choose_plot  = LtlWar_plot
        COULR  = "#8B0000",
        NO_W_LWDTH = [5,3],
        AD_W_LWDTH = [0,0],
        LGD_No = True,
        LGD_Ad = False,
        NAMEIT = "<b> Cases with Little or No Warning </b> ",
        TxHFL = " ",
        BRUSHFL = "Brush Creek Flash Flood",
    
       # print(to_plot)
     #print(to_plot.columns),
    # CHECKED WARNING CATEGORIES 
    Readyto_plot = Choose_plot
    if DmFl_toggle==[]:
        Choose_plot  = Readyto_plot
        VSBLE = False
        DM = "OUI-NON",
    elif DmFl_toggle==[' No']:
        VSBLE = True
        Choose_plot  = Readyto_plot[Readyto_plot["Dam Failure?"]=="no"]
        DM = "yes",
    elif DmFl_toggle==[' Yes ']:
        VSBLE = True
        Choose_plot  = Readyto_plot[Readyto_plot["Dam Failure?"]=="yes"]
        DM = "no", # SET TO FILTER WIT "!="
    else:
        VSBLE = True
        Choose_plot  = Readyto_plot
        DM = "OUI-NON",
    # TYPES OF DAMS
   
    Readyto_plot = Choose_plot   # UPDATE CHOOSE TO PLOT FOR THIS TEST
    if DmFl_toggle == [' Yes ']:
        Readyto_plot = Choose_plot
        Ready_VSBLE = VSBLE
        if type_toggle==[]:
            TYDM = "OUI-NON"
            Ready_VSBLE = False
        elif type_toggle==[' Earthfill or Composite']:
            Choose_plot  = Readyto_plot[Readyto_plot["Types of Dams"]=="earth"]
            TYDM = "concrete"
            Ready_VSBLE = True
        elif type_toggle==['Concrete']:
            Choose_plot  = Readyto_plot[Readyto_plot["Types of Dams"]=="concrete"]
            TYDM = "earth" # SET TO FILTER WIT "!="
            Ready_VSBLE = True
        else:
            Choose_plot  = Readyto_plot
            TYDM = "OUI-NON"
            Ready_VSBLE = True
    else:
        TYDM = "OUI-NON"
        Choose_plot  = Readyto_plot
        Ready_VSBLE = VSBLE
    
    # CHOOSE RANGE OF THE HEIGHT OF DAMS (FEET )
    Readyto_plot = Choose_plot   # UPDATE CHOOSE TO PLOT FOR THIS TEST
    HGTDM = [] # USE FOR INITIALIZE (TO AVOID BAD FILTERING IN THE PARTIAL WARNING DATA)
    LHF_CODE = "MIN-MAX" # USE FOR INITIALIZE (TO AVOID BAD FILTERING IN THE PARTIAL WARNING DATA)
    if DmFl_toggle == [' Yes '] and type_toggle!=[]:
        Readyto_plot = Choose_plot
        Readyto_plot["Dam Height (ft)"] = Readyto_plot["Dam Height (ft)"].astype(float)  # IS SET TO CONVERT CELLS VALUES INTO DOUBLE NUMBERS. IT SERVES IN THE USE OF >= AND <= CHECK
        if input_Min==None and input_Max==None:
            Choose_plot  = Readyto_plot
            HGTDM = []
        elif input_Min==None and input_Max!=None:
            Choose_plot  = Readyto_plot[Readyto_plot["Dam Height (ft)"]<=input_Max]
            HGTDM = [input_Max] 
            LHF_CODE = "VAL_MAX"  
        elif input_Min!=None and input_Max==None:
            Choose_plot  = Readyto_plot[Readyto_plot["Dam Height (ft)"]>=input_Min]
            HGTDM = [input_Min]
            LHF_CODE = "VAL_MIN"
        else: 
            HGTDM = [input_Min,input_Max]
            Readyto_plot  = Readyto_plot[Readyto_plot["Dam Height (ft)"]>=input_Min]
            Choose_plot  = Readyto_plot[Readyto_plot["Dam Height (ft)"]<=input_Max]
    else:
        Choose_plot  = Readyto_plot

    # CHOOSE RANGE OF RESERVOIR STORAGE (AC-FEET )
    Readyto_plot = Choose_plot   # UPDATE CHOOSE TO PLOT FOR THIS TEST
    VRSDM = [] # USE FOR INITIALIZE (TO AVOID BAD FILTERING IN THE PARTIAL WARNING DATA)
    LRS_CODE = "MIN-MAX" # USE FOR INITIALIZE (TO AVOID BAD FILTERING IN THE PARTIAL WARNING DATA)

    if DmFl_toggle == [' Yes '] and type_toggle!=[]:
        Readyto_plot = Choose_plot
        Readyto_plot["Reservoir Storage (af)"] = Readyto_plot["Reservoir Storage (af)"].astype(float)  # IS SET TO CONVERT CELLS VALUES INTO DOUBLE NUMBERS. IT SERVES IN THE USE OF >= AND <= CHECK
        if VRSMin==None and VRSMax==None:
            Choose_plot  = Readyto_plot
            VRSDM = []
        elif VRSMin==None and VRSMax!=None:
            Choose_plot  = Readyto_plot[Readyto_plot["Reservoir Storage (af)"]<=VRSMax]
            VRSDM = [VRSMax] 
            LRS_CODE = "VAL_MAX"  
        elif VRSMin!=None and VRSMax==None:
            Choose_plot  = Readyto_plot[Readyto_plot["Reservoir Storage (af)"]>=VRSMin]
            VRSDM = [VRSMin]
            LRS_CODE = "VAL_MIN"
        else: 
            VRSDM = [VRSMin,VRSMax]
            Readyto_plot  = Readyto_plot[Readyto_plot["Reservoir Storage (af)"]>=VRSMin]
            Choose_plot  = Readyto_plot[Readyto_plot["Reservoir Storage (af)"]<=VRSMax]
    else:
        Choose_plot  = Readyto_plot

    # CHOOSE THE MODE OF FAILURE (HYDROLOGIC OR STATIC)
    if DmFl_toggle == [' Yes '] and type_toggle!=[]:
        Readyto_plot = Choose_plot
        Ready_VSBLE = VSBLE
        if MChecked==[]:
            RSDM = "OUI-NON"
            Ready_VSBLE = False
        elif MChecked==['Hydrologic']:
            Choose_plot  = Readyto_plot[Readyto_plot["Scenario"]=="hydrologic"]
            RSDM = "static"
            Ready_VSBLE = True
        elif MChecked==[' Static']:
            Choose_plot  = Readyto_plot[Readyto_plot["Scenario"]=="static"]
            RSDM = "hydrologic" # SET TO FILTER WIT "!="
            Ready_VSBLE = True
        else:
            Choose_plot  = Readyto_plot
            RSDM = "OUI-NON"
            Ready_VSBLE = True
    else:
        RSDM = "OUI-NON"
        Choose_plot  = Readyto_plot
        Ready_VSBLE = VSBLE
    
    # CHOOSE THE TIME WHEN THE CATASTROPHE OCCURED (DAY OR NIGHT)
    Readyto_plot = Choose_plot
    #[Choose_plot["Day or Night"]!="varied"]
    if TIMECH==[]:
        TIMECAS = "OUI-NON"
        Ready_VSBLE = False
    elif TIMECH==['Day']:
        Choose_plot  = Readyto_plot[Readyto_plot["Day or Night"]=="day"]
        TIMECAS = "night"
        Ready_VSBLE = True
    elif TIMECH==[' Night']:
        Choose_plot  = Readyto_plot[Readyto_plot["Day or Night"]=="night"]
        TIMECAS = "day" # SET TO FILTER WIT "!="
        Ready_VSBLE = True
    else:
        Choose_plot  = Readyto_plot
        TIMECAS = "OUI-NON"
        Ready_VSBLE = True


# CHOOSE THE FLOOD AREA CHARACTERISTIC  (WIDE OR NARROW)
    Readyto_plot = Choose_plot
    #[Choose_plot["Day or Night"]!="varied"]
    if FLPCHK==[]:
        FLTY = "OUI-NON"
        Ready_VSBLE = False
    elif FLPCHK==['Narrow']:
        Choose_plot  = Readyto_plot[Readyto_plot["Floodplain"]=="Narrow"]
        FLTY = "Wide"
        Ready_VSBLE = True
    elif FLPCHK==[' Wide']:
        Choose_plot  = Readyto_plot[Readyto_plot["Floodplain"]=="Wide"]
        FLTY = "Narrow" # SET TO FILTER WIT "!="
        Ready_VSBLE = True
    else:
        Choose_plot  = Readyto_plot
        FLTY = "OUI-NON"
        Ready_VSBLE = True

    print(Choose_plot["Floodplain"])
    
    # CHOOSE RANGE OF THE NUMBER OF POPULATION AT RISK 
    Readyto_plot = Choose_plot   # UPDATE CHOOSE TO PLOT]>=VRSMin] FOR THIS TEST
    PARD_DM = [] # USE FOR INITIALIZE (TO AVOID BAD FILTERING IN THE PARTIAL WARNING DATA)
    PAR_CODE = "MIN-MAX" # USE FOR INITIALIZE (TO AVOID BAD FILTERING IN THE PARTIAL WARNING DATA)
    if (DmFl_toggle == [' Yes '] and type_toggle!=[]) or DmFl_toggle==[' No'] or DmFl_toggle==[' Yes ', ' No']:
        Readyto_plot = Choose_plot
        Readyto_plot = Readyto_plot[Readyto_plot["Total PAR"]!="unknown"] # unknown cells of the number of PAR in the database are deleted here first before proceeding 
        Readyto_plot["Total PAR"] = Readyto_plot["Total PAR"].astype(float)  # IS SET TO CONVERT CELLS VALUES INTO DOUBLE NUMBERS. IT SERVES IN THE USE OF >= AND <= CHECK
        if MinPAR==None and MaxPAR==None:
            Choose_plot  = Readyto_plot
            PARD_DM = []
        elif MinPAR==None and MaxPAR!=None:
            Choose_plot  = Readyto_plot[Readyto_plot["Total PAR"]<=MaxPAR]
            PARD_DM = [MaxPAR] 
            PAR_CODE = "VAL_MAX"
        elif MinPAR!=None and MaxPAR==None:
            Choose_plot  = Readyto_plot[Readyto_plot["Total PAR"]>=MinPAR]
            PARD_DM = [MinPAR] 
            PAR_CODE = "VAL_MIN"
        else: 
            Readyto_plot  = Readyto_plot[Readyto_plot["Total PAR"]<=MaxPAR]
            Choose_plot  = Readyto_plot[Readyto_plot["Total PAR"]>=MinPAR]
            PARD_DM = [MinPAR, MaxPAR] 
    else:
        Choose_plot  = Readyto_plot
    
    
    # CHOOSE RANGE OF THE DOWNSTREAM DISTANCE TO THE PAR
    Readyto_plot = Choose_plot   # UPDATE CHOOSE TO PLOT FOR THIS TEST
    DDPAR_DM = [] # USE FOR INITIALIZE (TO AVOID BAD FILTERING IN THE PARTIAL WARNING DATA)
    DDPAR_CODE = "MIN-MAX" # USE FOR INITIALIZE (TO AVOID BAD FILTERING IN THE PARTIAL WARNING DATA)
    if DmFl_toggle == [' Yes '] and type_toggle!=[]:
        Readyto_plot = Readyto_plot[Readyto_plot["DD to PAR (miles)"]!="na"] 
        Readyto_plot["DD to PAR (miles)"] = Readyto_plot["DD to PAR (miles)"].astype(float)  # IS SET TO CONVERT CELLS VALUES INTO DOUBLE NUMBERS. IT SERVES IN THE USE OF >= AND <= CHECK
        if DDMIN==None and DDMAX==None:
            Choose_plot  = Readyto_plot
            DDPAR_DM  = []
        elif DDMIN==None and DDMAX!=None:
            Choose_plot  = Readyto_plot[Readyto_plot["DD to PAR (miles)"]<=DDMAX]
            DDPAR_DM  = [DDMAX] 
            DDPAR_CODE = "VAL_MAX"  
        elif DDMIN!=None and DDMAX==None:
            Choose_plot  = Readyto_plot[Readyto_plot["DD to PAR (miles)"]>=DDMIN]
            DDPAR_DM  = [DDMIN]
            DDPAR_CODE = "VAL_MIN"
        else: 
            DDPAR_DM  = [DDMIN,DDMAX]
            Readyto_plot  = Readyto_plot[Readyto_plot["DD to PAR (miles)"]>=DDMIN]
            Choose_plot  = Readyto_plot[Readyto_plot["DD to PAR (miles)"]<=DDMAX]
    else:
        Choose_plot  = Readyto_plot

    
    #print(Choose_plot["DD to PAR (miles)"] )

    #print(Choose_plot["Total PAR"])
    
    #print(Choose_plot)

    to_plot = Choose_plot
    
    VSBLE = Ready_VSBLE
    #print(to_plot)
    fig = px.scatter(
        to_plot,
        x="DV(ft2/s)",
        y="Fatality Rate",
        labels={"Cases with Little or No Warning"},
        # color='#008000',
        #width=345*4.3,
        #height=217 * 4.5,
        hover_name="Case Name",
        custom_data=to_plot.columns,
        #text="Case Name" if label_toggle else None,
    )
    # fig.update_layout(xaxis4 = {'anchor': 'y',  'overlaying': 'x', 'side': 'top'})
    fig.update_traces(
        name=NAMEIT[0],
        showlegend=True,
        visible=VSBLE,
        marker=dict(
            color= COULR[0],
            size=18,
            symbol="triangle-up",
            line=dict(
                width=1,
                color=COULR[0],  # Line colors don't apply to open markers
            ),
        ),
        selector=dict(mode="markers"),
    )
    # to create secondary y-axis
    # Partial Warning Graph
    #pltPartial = TexasHillCT
    TexasHillCT = pltPartial[pltPartial["Case Name"]!=TxHFL[0]]
    #TexasHillCT = pltPartial[pltPartial["Case Name"]!=TxHFL[0]]
    TexasHillCT = TexasHillCT[TexasHillCT["Case Name"]!=BRUSHFL[0]]
    # filtering partial warning cases according to " DAM FAILURE ?"
    TexasHillCT = TexasHillCT[TexasHillCT["Dam Failure?"]!=DM[0]]
    # to filter types of dams (concrete or earthfill) for partial data
    TexasHillCT = TexasHillCT[TexasHillCT["Types of Dams"]!=TYDM]

    # filter partial date according to the range of height chosen
    LENGTH = len(HGTDM)
    CHO_HEIGHT = TexasHillCT
    if LENGTH>=2:
        CHO_HEIGHT["Dam Height (ft)"] = CHO_HEIGHT["Dam Height (ft)"].astype(float)
        RDY_HEIGHT  = CHO_HEIGHT[CHO_HEIGHT["Dam Height (ft)"]>=HGTDM[0]]
        CHO_HEIGHT  = RDY_HEIGHT[RDY_HEIGHT["Dam Height (ft)"]<=HGTDM[1]]
    elif LENGTH==1:
        CHO_HEIGHT["Dam Height (ft)"] = CHO_HEIGHT["Dam Height (ft)"].astype(float)
        if LHF_CODE == "VAL_MAX":
            CHO_HEIGHT  = CHO_HEIGHT[CHO_HEIGHT["Dam Height (ft)"]<=HGTDM[0]] 
        else:
            CHO_HEIGHT  = CHO_HEIGHT[CHO_HEIGHT["Dam Height (ft)"]>=HGTDM[0]]
    else:
        CHO_HEIGHT = TexasHillCT
    
    TexasHillCT = CHO_HEIGHT 
    
    # filter partial date according to the range of reservoir storage chosen
    LENGTH = len(VRSDM)
    CHO_VRS = TexasHillCT
    print(VRSDM)
    if LENGTH>=2:
        CHO_VRS["Reservoir Storage (af)"] = CHO_VRS["Reservoir Storage (af)"].astype(float)
        RDY_VRS  = CHO_VRS[CHO_VRS["Reservoir Storage (af)"]>=VRSDM[0]]
        CHO_VRS  = RDY_VRS[RDY_VRS["Reservoir Storage (af)"]<=VRSDM[1]]
    elif LENGTH==1:
        CHO_VRS["Reservoir Storage (af)"] = CHO_VRS["Reservoir Storage (af)"].astype(float)
        if LRS_CODE == "VAL_MAX":
            CHO_VRS  = CHO_VRS[CHO_VRS["Reservoir Storage (af)"]<=VRSDM[0]] 
        else:
            CHO_VRS = CHO_VRS[CHO_VRS["Reservoir Storage (af)"]>=VRSDM[0]]
    else:
        CHO_VRS = TexasHillCT
    
    TexasHillCT = CHO_VRS 
    
    # to filter mode of failure of the dams (Hydrologic or static) for partial data
    TexasHillCT = TexasHillCT[TexasHillCT["Scenario"]!=RSDM]

# to filter according to the time when the catastrophe occured for partial data
    TexasHillCT = TexasHillCT[TexasHillCT["Day or Night"]!=TIMECAS]

# to filter according to the time when the catastrophe occured for partial data
    TexasHillCT = TexasHillCT[TexasHillCT["Floodplain"]!=FLTY]

    # filter partial date according to the range of the population at risk downstream
    LENGTH = len(PARD_DM)
    CHO_PAR = TexasHillCT
    CHO_PAR = CHO_PAR[CHO_PAR["Total PAR"]!="unknown"] # unknown cells of the number of PAR in the database are deleted here first before proceeding 
    if LENGTH>=2:
        CHO_PAR["Total PAR"] = CHO_PAR["Total PAR"].astype(float)
        RDY_PAR  = CHO_PAR[CHO_PAR["Total PAR"]>=PARD_DM[0]]
        CHO_PAR  = RDY_PAR[RDY_PAR["Total PAR"]<=PARD_DM[1]]
    elif LENGTH==1:
        CHO_PAR["Total PAR"] = CHO_PAR["Total PAR"].astype(float)
        if PAR_CODE == "VAL_MAX":
            CHO_PAR  = CHO_PAR[CHO_PAR["Total PAR"]<=PARD_DM[0]] 
        else:
            CHO_PAR  = CHO_PAR[CHO_PAR["Total PAR"]>=PARD_DM[0]]
    else:
        CHO_PAR = TexasHillCT
    
    TexasHillCT = CHO_PAR  # RETURN

# filter partial date according to the range of the downstream distance to the PAR
    LENGTH = len(DDPAR_DM)
    DDIS_PAR = TexasHillCT
    DDIS_PAR = DDIS_PAR[DDIS_PAR["DD to PAR (miles)"]!="na"] # unknown cells of the number of PAR in the database are deleted here first before proceeding 
    if LENGTH>=2:
        DDIS_PAR["DD to PAR (miles)"] = DDIS_PAR["DD to PAR (miles)"].astype(float)
        RDY_DD  = DDIS_PAR[DDIS_PAR["DD to PAR (miles)"]>=DDPAR_DM[0]]
        DDIS_PAR = RDY_DD[RDY_DD["DD to PAR (miles)"]<=DDPAR_DM[1]]
    elif LENGTH==1:
        DDIS_PAR["DD to PAR (miles)"] = DDIS_PAR["DD to PAR (miles)"].astype(float)
        if DDPAR_CODE == "VAL_MAX":
            DDIS_PAR  = DDIS_PAR[DDIS_PAR["DD to PAR (miles)"]<=DDPAR_DM[0]] 
        else:
            DDIS_PAR = DDIS_PAR[DDIS_PAR["DD to PAR (miles)"]>=DDPAR_DM[0]]
    else:
        DDIS_PAR = TexasHillCT
    
    TexasHillCT = DDIS_PAR
    hvPrtial = TexasHillCT["Case Name"]
    #ctdat1 = pltPartial["DV(ft2/s)"]
    #print(TexasHillCT["Total PAR"])
    #print(TexasHillCT)


    fig.add_scatter(
        x=[10],
        y=[0.1],
        xaxis="x2",
        showlegend=False,
        mode=None,
        visible=False,
    )

    fig.add_scatter(
        x=TexasHillCT["DV(ft2/s)"],
        y=TexasHillCT["Fatality Rate"],
        name="<b> Cases with Partial Warning </b> ",
        showlegend=True,
        visible=VSBLE,
        mode="markers",
        marker={"size":18,"symbol": "square", "color": "#00008B"},
        hovertemplate=hvPrtial
        + "<br>"
        + "<br> DV (ft2/s): %{x}"
        + "<br>Fatality Rate: %{y}",
        xaxis="x1",
    )

    # print(to_plot["Maximum DV high (ft2/s)"], to_plot["Fatality Rate"])
    # print(pltPartial["Maximum DV high (ft2/s)"], pltPartial["Fatality Rate"])

    # SUGGESTED BOUND FOR NO OR LITTLE WARNING CASES 
    fig.add_scatter(
        x=bound_data["DvsL(sqf/s)"],
        y=bound_data["Suggested lower Limit"],
        showlegend=False,
        mode="lines",
        line={"dash": "dot", "color": "orange", "width": NO_W_LWDTH[0][0]},
        xaxis="x1",
    )
    fig.add_scatter(
        x=bound_data["DvsU(sqf/s)"],
        y=bound_data["Suggested Upper Limit"],
        showlegend=LGD_No[0],
        name="<b> Suggested Limit </b> ",
        mode="lines",
        line={"dash": "dot", "color": "orange", "width": NO_W_LWDTH[0][0]},
        xaxis="x1",
    )

    fig.add_scatter(
        x=bound_data["DvL(sqf/s)"],
        y=bound_data["Overall lower Limit"],
        showlegend=LGD_No[0],
        name="<b> Overall Limit ",
        mode="lines",
        line={"dash": "dash", "color": "orange", "width": NO_W_LWDTH[0][1]},
        xaxis="x1",
    )
    fig.add_scatter(
        x=bound_data["DvU(sqf/s)"],
        y=bound_data["Overall Upper Limit"],
        showlegend=False,
        mode="lines",
        line={"dash": "dash", "color": "orange", "width": NO_W_LWDTH[0][1]},
        xaxis="x1",
    )
# SUGGESTED BOUND FOR ADEQUATE WARNING CASES 

    fig.add_scatter(
        x=Ad_bound["DvsL(sqf/s)"],
        y=Ad_bound["Suggested lower Limit"],
        showlegend=False,
        mode="lines",
        line={"dash": "dot", "color": "cyan", "width": AD_W_LWDTH[0][0]},
        xaxis="x1",
    )
    fig.add_scatter(
        x=Ad_bound["DvsU(sqf/s)"],
        y=Ad_bound["Suggested Upper Limit"],
        showlegend=LGD_Ad[0],
        name="<b> Suggested Limit </b> ",
        mode="lines",
        line={"dash": "dot", "color": "cyan", "width": AD_W_LWDTH[0][0]},
        xaxis="x1",
    )

    fig.add_scatter(
        x=Ad_bound["DvL(sqf/s)"],
        y=Ad_bound["Overall lower Limit"],
        showlegend=LGD_Ad[0],
        name="<b> Overall Limit ",
        mode="lines",
        line={"dash": "dash", "color": "cyan", "width": AD_W_LWDTH[0][1]},
        xaxis="x1",
    )
    fig.add_scatter(
        x=Ad_bound["DvU(sqf/s)"],
        y=Ad_bound["Overall Upper Limit"],
        showlegend=False,
        mode="lines",
        line={"dash": "dash", "color": "cyan", "width": AD_W_LWDTH[0][1]},
        xaxis="x1",
    )

    fig.update_yaxes(
        title_text="Fatality Rate",
        title_font=dict(size=20),
        type="log",
        range=[np.log10(0.00001), np.log10(1)],
        showline=True,
        linewidth=1,
        linecolor="#000000",
        tickformat=".5~g",
        ticks="outside",
        mirror=True,
        ticklen=10,
        tickwidth=2,
        showgrid=True,
        gridcolor="#7a7a7a",
        griddash="solid",
        gridwidth=0.5,
        tickvals=[0.00001, 0.0001, 0.001, 0.01, 0.1, 1],
        ticktext=["Zero", 0.0001, "0.001", "0.01", "0.1", "1.0"],
        minor=dict(
            tickvals=[
                0.00002,
                0.00003,
                0.00004,
                0.00005,
                0.00006,
                0.00007,
                0.00008,
                0.00009,
                0.0002,
                0.0003,
                0.0004,
                0.0005,
                0.0006,
                0.0007,
                0.0008,
                0.0009,
                0.002,
                0.003,
                0.004,
                0.005,
                0.006,
                0.007,
                0.008,
                0.009,
                0.02,
                0.03,
                0.04,
                0.05,
                0.06,
                0.07,
                0.08,
                0.09,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
            ],
            ticklen=5,
            tickwidth=2,
            showgrid=True,
            ticks="outside",
            gridcolor="#7a7a7a",
            griddash="dot",
            gridwidth=0.5,
        ),
    )

    # Create axis objects
    # fig.update_traces(marker_size=12, textposition="top center")
    fig.update_layout(
        newshape_line_color="cyan",
        modebar={
            'orientation': 'v',
            'bgcolor':'#000000',
            'color':'white',
        },
        modebar_add=[
            "drawline",
            "drawopenpath",
            "drawclosedpath",
            "drawcircle",
            "drawrect",
            "eraseshape",
        ],

        modebar_remove=[
            "lasso",
        ],
        # margin=dict(l=20, r=20, t=250, b=20),
        #title =f"Case History Data Identified for Cases with {GRAPHTITLE[0]}",
        legend=dict(
            yanchor="bottom",
            xanchor="right",
            y=0.01,
            x=0.99,
            bgcolor="white",
            bordercolor="black",
            borderwidth=1,
        ),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        xaxis=dict(
            title_text="DV (depth x velocity, ft²/sec)",
            title_font=dict(size=20),
            type="log",
            range=[np.log10(10), np.log10(10000)],
            ticks="outside",
            showline=True,
            linewidth=1,
            linecolor="#000000",
            ticklen=10,
            tickwidth=2,
            showgrid=True,
            gridcolor="#7a7a7a",
            griddash="solid",
            gridwidth=0.5,
            tickvals=[10, 100, 1000, 10000],
            tickformat=",.0f",
            minor=dict(
                tickvals=[
                    20,
                    30,
                    40,
                    50,
                    60,
                    70,
                    80,
                    90,
                    200,
                    300,
                    400,
                    500,
                    600,
                    700,
                    800,
                    900,
                    2000,
                    3000,
                    4000,
                    5000,
                    6000,
                    7000,
                    8000,
                    9000,
                ],
                ticklen=5,
                showgrid=True,
                ticks="outside",
                gridcolor="#7a7a7a",
                griddash="dot",
                gridwidth=0.5,
            ),
        ),
        xaxis2=dict(
            title_text="DV (depth x velocity, m²/sec)",
            title_font=dict(size=20),
            type="log",
            range=[np.log10(10), np.log10(10000)],
            ticks="outside",
            side="top",
            linewidth=1,
            linecolor="#000000",
            ticklen=10,
            tickwidth=2,
            gridcolor="#7a7a7a",
            griddash="solid",
            gridwidth=0.5,
            tickmode="array",
            tickvals=[10, 100, 1000, 10000],
            ticktext=[round(x * ft2s_to_m2s, 2) for x in [10, 100, 1000, 10000]],
            tickformat=",.0f",
            automargin=True,
            overlaying="x1",
            minor=dict(
                tickvals=[
                    20,
                    30,
                    40,
                    50,
                    60,
                    70,
                    80,
                    90,
                    200,
                    300,
                    400,
                    500,
                    600,
                    700,
                    800,
                    900,
                    2000,
                    3000,
                    4000,
                    5000,
                    6000,
                    7000,
                    8000,
                    9000,
                ],
                ticklen=5,
                showgrid=True,
                ticks="outside",
                gridcolor="#7a7a7a",
                griddash="dot",
                gridwidth=0.5,
            ),
        ),
        # showlegend=False,
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True, host="localhost")