"""
Imports data from an Excel file into Neo4j using Cypher queries.

"""

# Access environment variables
import os

# Use Pandas to read Excel
import pandas as pd

# Load .env settings
from dotenv import load_dotenv
load_dotenv(".env")

# Connection to neo4j
from neo4j import GraphDatabase


EXCEL_FILE = "data/data.xlsx"

# ---------------------------------------------------------------------------
# Queries to import data from the different tables in the Excel
# ---------------------------------------------------------------------------


CHANNEL_QUERY = """
MERGE (channel:Channel {item_number: $item_number})
SET channel.designation = $designation,
    channel.length = $length,
    channel.t = $t,
    channel.weight = $weight,
    channel.fy = $fy,
    channel.area = $area,
    channel.ix = $ix,
    channel.iy = $iy,
    channel.sx = $sx,
    channel.sy = $sy,
    channel.rx = $rx,
    channel.ry = $ry,
    channel.ix_eff = $ix_eff,
    channel.iy_eff = $iy_eff,
    channel.sx_eff = $sx_eff,
    channel.sy_eff = $sy_eff,
    channel.mal_x = $mal_x,
    channel.phi_ml_x = $phi_ml_x,
    channel.mal_y = $mal_y,
    channel.phi_ml_y = $phi_ml_y,
    channel.mad_x = $mad_x,
    channel.phi_md_x = $phi_md_x,
    channel.mad_y = $mad_y,
    channel.phi_md_y = $phi_md_y,
    channel.va_x = $va_x,
    channel.phi_v_x = $phi_v_x,
    channel.va_y = $va_y,
    channel.phi_v_y = $phi_v_y,
    channel.lu = $lu,
    channel.j = $j,
    channel.cw = $cw,
    channel.x0 = $x0,
    channel.y0 = $y0,
    channel.r0 = $r0

MERGE (material:Material {name: $material})
MERGE (coating_material:CoatingMaterial {name: $coating_material})
MERGE (coating_standard:CoatingStandard {name: $coating_standard})

MERGE (channel)-[:HAS_MATERIAL]->(material)
MERGE (channel)-[:HAS_COATING_MATERIAL]->(coating_material)
MERGE (channel)-[:HAS_COATING_STANDARD]->(coating_standard)
"""


CONNECTOR_QUERY = """
MERGE (connector:Connector {item_number: $item_number})
SET connector.designation = $designation

MERGE (material:Material {name: $material})
MERGE (material_standard:MaterialStandard {name: $material_standard})
MERGE (coating_method:CoatingMethod {name: $coating_method})

MERGE (connector)-[:HAS_MATERIAL]->(material)
MERGE (connector)-[:HAS_MATERIAL_STANDARD]->(material_standard)
MERGE (connector)-[:HAS_COATING_METHOD]->(coating_method)
"""


TORQUE_QUERY = """
MATCH (connector:Connector {item_number: $item_number})

MERGE (configuration:TorqueConfiguration {torque_id: $torque_id})
SET configuration.torque = $torque

MERGE (connector)-[:HAS_TORQUE_CONFIGURATION]->(configuration)

FOREACH (
    bolt_name IN CASE
        WHEN $bolt_designation IS NULL OR trim($bolt_designation) = ""
        THEN []
        ELSE [$bolt_designation]
    END |
    MERGE (bolt:Bolt {designation: bolt_name})
    MERGE (configuration)-[:HAS_BOLT]->(bolt)
)
"""


RESISTANCE_QUERY = """
MATCH (connector:Connector {item_number: $item_number})

MERGE (configuration:ResistanceConfiguration {
    resistance_id: $resistance_id
})
SET configuration.angle_connector_quantity = $angle_connector_quantity,
    configuration.fx_positive = $fx_positive,
    configuration.fx_negative = $fx_negative,
    configuration.fy_positive = $fy_positive,
    configuration.fy_negative = $fy_negative,
    configuration.fz_positive = $fz_positive,
    configuration.fz_negative = $fz_negative

MERGE (connector)-[:HAS_RESISTANCE_CONFIGURATION]->(configuration)

MERGE (channel:Channel {
    designation: $installation_channel_designation
})
MERGE (configuration)-[:USES_CHANNEL]->(channel)

FOREACH (
    connector_name IN CASE
        WHEN $channel_connector_1_designation IS NULL
             OR trim($channel_connector_1_designation) = ""
        THEN []
        ELSE [$channel_connector_1_designation]
    END |
    MERGE (channel_connector:Connector {designation: connector_name})
    MERGE (configuration)-[usage:USES_CHANNEL_CONNECTOR]->(channel_connector)
    SET usage.quantity = $channel_connector_1_quantity
)

FOREACH (
    connector_name IN CASE
        WHEN $channel_connector_2_designation IS NULL
             OR trim($channel_connector_2_designation) = ""
        THEN []
        ELSE [$channel_connector_2_designation]
    END |
    MERGE (channel_connector:Connector {designation: connector_name})
    MERGE (configuration)-[usage:USES_CHANNEL_CONNECTOR]->(channel_connector)
    SET usage.quantity = $channel_connector_2_quantity
)
"""


# ---------------------------------------------------------------------------
# Functions that map table rows to query parameters
# ---------------------------------------------------------------------------

def import_channels(driver, table):
    for _, row in table.iterrows():
        driver.execute_query(
            CHANNEL_QUERY,
            parameters_={
                "item_number": int(row["item_number"]),
                "designation": str(row["designation"]),
                "length": float(row["length"]),
                "material": str(row["material"]),
                "coating_material": str(row["coating_material"]),
                "coating_standard": str(row["coating_standard"]),
                "t": float(row["t"]),
                "weight": float(row["weight"]),
                "fy": float(row["fy"]),
                "area": float(row["area"]),
                "ix": float(row["ix"]),
                "iy": float(row["iy"]),
                "sx": float(row["sx"]),
                "sy": float(row["sy"]),
                "rx": float(row["rx"]),
                "ry": float(row["ry"]),
                "ix_eff": float(row["ix_eff"]),
                "iy_eff": float(row["iy_eff"]),
                "sx_eff": float(row["sx_eff"]),
                "sy_eff": float(row["sy_eff"]),
                "mal_x": float(row["mal_x"]),
                "phi_ml_x": float(row["phi_ml_x"]),
                "mal_y": float(row["mal_y"]),
                "phi_ml_y": float(row["phi_ml_y"]),
                "mad_x": float(row["mad_x"]),
                "phi_md_x": float(row["phi_md_x"]),
                "mad_y": float(row["mad_y"]),
                "phi_md_y": float(row["phi_md_y"]),
                "va_x": float(row["va_x"]),
                "phi_v_x": float(row["phi_v_x"]),
                "va_y": float(row["va_y"]),
                "phi_v_y": float(row["phi_v_y"]),
                "lu": float(row["lu"]),
                "j": float(row["j"]),
                "cw": float(row["cw"]),
                "x0": float(row["x0"]),
                "y0": float(row["y0"]),
                "r0": float(row["r0"]),
            },
            database_=os.environ["NEO4J_DATABASE"],
        ) 
        
        
        
        
def import_connectors(driver, table):
    for _, row in table.iterrows():
        driver.execute_query(
            CONNECTOR_QUERY,
            parameters_={
                "item_number": int(row["item_number"]),
                "designation": str(row["designation"]),
                "material": str(row["material"]),
                "material_standard": str(row["material_standard"]),
                "coating_method": str(row["coating_method"]),
            },
            database_=os.environ["NEO4J_DATABASE"],
        )
        



def import_torque(driver, table):
    for _, row in table.iterrows():
        driver.execute_query(
            TORQUE_QUERY,
            parameters_={
                "torque_id": str(row["torque_id"]),
                "item_number": int(row["item_number"]),
                "torque": float(row["torque"]),
                "bolt_designation": (
                    None
                    if pd.isna(row["bolt_designation"])
                    else str(row["bolt_designation"]).strip()
                ),
            },
            database_=os.environ["NEO4J_DATABASE"],
        )



def import_resistances(driver, table):
    for _, row in table.iterrows():
        driver.execute_query(
            RESISTANCE_QUERY,
            parameters_={
                "resistance_id": str(row["resistance_id"]),
                "item_number": int(row["item_number"]),
                "angle_connector_quantity": int(row["angle_connector_quantity"]),
                "installation_channel_designation": str(
                    row["installation_channel_designation"]
                ).strip(),
                "channel_connector_1_designation": (
                    None
                    if pd.isna(row["channel_connector_1_designation"])
                    else str(row["channel_connector_1_designation"]).strip()
                ),
                "channel_connector_1_quantity": (
                    None
                    if pd.isna(row["channel_connector_1_quantity"])
                    else int(row["channel_connector_1_quantity"])
                ),
                "channel_connector_2_designation": (
                    None
                    if pd.isna(row["channel_connector_2_designation"])
                    else str(row["channel_connector_2_designation"]).strip()
                ),
                "channel_connector_2_quantity": (
                    None
                    if pd.isna(row["channel_connector_2_quantity"])
                    else int(row["channel_connector_2_quantity"])
                ),
                "fx_positive": (
                    None if pd.isna(row["fx_positive"])
                    else float(row["fx_positive"])
                ),
                "fx_negative": (
                    None if pd.isna(row["fx_negative"])
                    else float(row["fx_negative"])
                ),
                "fy_positive": (
                    None if pd.isna(row["fy_positive"])
                    else float(row["fy_positive"])
                ),
                "fy_negative": (
                    None if pd.isna(row["fy_negative"])
                    else float(row["fy_negative"])
                ),
                "fz_positive": (
                    None if pd.isna(row["fz_positive"])
                    else float(row["fz_positive"])
                ),
                "fz_negative": (
                    None if pd.isna(row["fz_negative"])
                    else float(row["fz_negative"])
                ),
            },
            database_=os.environ["NEO4J_DATABASE"],
        )
    
    
# ---------------------------------------------------------------------------
# Function that imports tables using one shared driver
# ---------------------------------------------------------------------------

def import_data():

    tables = pd.read_excel(EXCEL_FILE, sheet_name=None)

    with GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(
            os.environ["NEO4J_USERNAME"],
            os.environ["NEO4J_PASSWORD"],
        ),
    ) as driver:
        driver.verify_connectivity()

        import_channels(driver, tables["channel"])
        import_connectors(driver, tables["connector"])
        import_torque(driver, tables["connector_torque"])
        import_resistances(driver, tables["connector_resistance"])

    print("Data imported into Neo4j!")



if __name__ == "__main__":
    import_data()