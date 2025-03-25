from assistr.models import Configuration, Server, get_from_list
from assistr.models import  Metadata, Instance, Database, Schema, Table, Column

from sqlalchemy import create_engine, MetaData as AlchemyMetaData
from assistr.utils import logger

# CONNECTION FUNCTIONS
########################################################################
def create_connection_url(server: Server):
     # Create a connection url from the server properties in this form dialect+driver://username:password@host:port/database
     # Only adding sections if they have a value in the server instance
     
     # sqlite requires 3 slashes for reference to file db
     seperator = ":///" if server.dialect == "sqlite" else "://"
     driver_dialect = f"{server.dialect}{seperator}" #if not server.driver else f"{server.dialect}+{server.driver}{seperator}"
     user_pass = f"{server.user}:{server.password}@" if server.user and server.password else ""
     host_port = f"{server.host}:{server.port}/" if server.host and server.port else ""
     database = f"{server.database}"
     
     return driver_dialect+user_pass+host_port+database

def get_alchemy_engine(config: Configuration, server: Server = None):  
    
    if not server:
        server = get_from_list(config.servers, config.src_server)
    
    connection_url = create_connection_url(server)
    print(connection_url)
    engine = create_engine(connection_url)
 
    return engine

# METADATA FUNCTIONS
########################################################################
def get_metadata(config: Configuration = None, server: Server = None):
    """_summary_
    Uses the src_server from the config to determine datasource and load metadata for all schemas specified.
    Args:
        config: Configuration 

    """
    if not server:
        server = get_from_list(config.servers, config.src_server)

    alchemy_metadata = get_metadata_alchemy(server=server)
    metadata = load_metadata_to_models(alchemy_metadata, server)

    return metadata, alchemy_metadata

def get_metadata_alchemy(config: Configuration = None, server: Server = None):
     
    if not server:
        server = get_from_list(config.servers, config.src_server)

    if not server:
        raise Exception("Context, Config or Server nust be provided to get active db server")
    
    connection_url = create_connection_url(server)
    engine = create_engine(connection_url)
    #logger.debug(f"{engine.connect()}")
    metadata_obj = AlchemyMetaData()
    if server.schemas:
        for schema in server.schemas:
            metadata_obj.reflect(engine, schema)
            print(f"Getting Metadata for {schema} - {len(metadata_obj.tables)} tables in metadata")
        else:
            metadata_obj.reflect(engine)
        
    return metadata_obj

def load_metadata_to_models(alchemy_metadata: AlchemyMetaData, server: Server):
    
    metadata = Metadata()
    instance = Instance(name=server.name, host=server.host)
    metadata.instances.append(instance)
    
    database = Database(name=server.database)
    instance.databases.append(database)
    
    if server.schemas:
        for schema_name in server.schemas:
            schema = Schema(name=schema_name)
            database.schemas.append(schema)
    else:
        schema = Schema(name="default")
        database.schemas.append(schema)
    
    for src_table_name, src_table in alchemy_metadata.tables.items():
        # Add the table to the schema
        #logger.debug(f"loading table {src_table.fullname}")
        table_schema = src_table.schema if src_table.schema else "default"
        table = Table(name=src_table_name, full_name=src_table.fullname)
        schema = get_from_list(database.schemas, table_schema)
        
        # Only schemas listed in config will exist already
        if schema:
            schema.tables.append(table)
            
            table_field_count = 0
            # Add the columns to the table
            for col_name, col in src_table.columns.items():
                logger.trace(f"{col_name}, {col.type}, {type(col.type)}, {str(col.type)}, {col.index}, {col.unique}, {col.primary_key}, {col.nullable}")
                
                column = Column(name=col_name, instance_name=instance.name, database_name=database.name, 
                                schema_name=table_schema, table_name=src_table_name, data_type=str(col.type),
                                is_nullable=col.nullable, primary_key=col.primary_key, unique_column=col.unique)
                
                table.columns.append(column)
                table_field_count += 1
                
            setattr(table, "field_count", table_field_count)
        
    return metadata
