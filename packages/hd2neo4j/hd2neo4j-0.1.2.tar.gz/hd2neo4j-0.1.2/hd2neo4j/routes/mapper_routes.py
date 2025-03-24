from fastapi import APIRouter, File
from typing import Annotated
from hd2neo4j.services import MapperService, RepositoryService

rt = APIRouter(
    prefix="/mapper",
    tags=["mapper"],
)


@rt.get("/graph")
def get_graph():
    response = RepositoryService().get_graph()
    return response.records


@rt.get("/query")
def execute_query(query: str):
    return RepositoryService().execute_external_query(query)


@rt.post("/start")
def start_mapping(
    configFile: Annotated[bytes, File()],
    dataFile: Annotated[bytes, File()],
):
    controller = MapperService(configFile, dataFile)
    controller.start_mapping()


@rt.post("/drop")
def drop_db():
    RepositoryService().clean_graph_db()
